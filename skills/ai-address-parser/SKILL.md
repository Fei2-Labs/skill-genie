---
name: "ai-address-parser"
description: "Parses a free-text address blob (supplier email, Google Maps result, business card) into structured fields (street, postal code, city, state, country, contact, phone) via an LLM chat-completions call. Use when a form has separate address inputs and you want a paste-a-blob-to-autofill affordance instead of manual field-by-field entry."
license: "MIT"
metadata: {"version":"1.0.0","category":"developer-tools","tags":["address-parsing","llm","json-mode","forms","autofill","data-extraction"],"license":"MIT","hermes":{"tags":["address-parsing","llm","json-mode","forms","autofill","data-extraction"]}}
allowed-tools: Read, Write, Edit
---

# AI Address Parser

Turns messy pasted address text into structured form fields using an OpenAI-compatible chat-completions endpoint in JSON mode, applied non-destructively so it never clobbers fields the user already filled in.

---

## Step 1: Design the Output Schema

Extract exactly the fields your form needs, no more. A typical set:

```json
{
  "address": "",
  "postalCode": "",
  "city": "",
  "state": "",
  "country": "",
  "contact": "",
  "phone": "",
  "confidence": "high"
}
```

- Every address field is a **string**, including `postalCode` — never coerce it to a number. Many countries' postal codes have leading zeros or embedded spaces (e.g. Swedish `123 45`), and a numeric type silently destroys both.
- Add a `confidence` enum (`high` / `medium` / `low`) so the UI can flag results worth double-checking instead of presenting every parse as equally certain.
- Do not add fields the codebase has deliberately left unvalidated (e.g. skip an ISO country-code enum or a postal-code regex if the rest of the app treats these as free text — matching the model's output format to the app's actual validation avoids introducing a stricter contract than the rest of the system has).

## Step 2: Write the Extraction Prompt

The prompt is the actual product here — get these rules right:

- **Field-by-field extraction rules.** Spell out what belongs in each field explicitly, especially the boundary between fields that are easy to blend. Example: "address = street line(s) only — never repeat city/postal/country into it." Without this, models happily dump the whole address into one field.
- **Empty-string-not-guess rule.** State directly: "If a field cannot be confidently determined, return an empty string — never guess, never write 'N/A' or 'unknown'." Models default to filling every field with something; this rule is what makes partial/ambiguous input safe to merge.
- **Postal-code-as-string rule.** Tell the model explicitly to preserve leading zeros and the country's native format as a string.
- **Normalize country to one format.** If the app's country field is free text (no ISO enum), ask for the full English country name so results are consistent and human-readable, matching whatever format the rest of the app already uses for that field.
- **Length limits.** If the target fields have max-length constraints, state each one's limit in the prompt so the model self-truncates, then truncate again defensively server-side (see Step 5).
- End the prompt with `Return ONLY this JSON object:` followed by the exact empty-valued schema, then the raw input text.

## Step 3: Make the Request

Call the OpenAI-compatible chat-completions endpoint (`POST {base_url}/chat/completions`) with:

- `model`: the configured model name
- `messages`: a single `user` message containing the prompt from Step 2
- `response_format: { type: 'json_object' }` — forces JSON-mode output where the provider supports it
- A generous timeout (60-90s) — parsing calls are not always fast
- **Do not send a `temperature` parameter.** Some newer models reject the request outright (HTTP 400) if `temperature` is present at all, rather than ignoring it. Omit it entirely instead of setting a default.
- Auth via a bearer token from server-side config — never expose the key to the client.

## Step 4: Parse the Response Defensively

Some models wrap JSON-mode output in markdown code fences despite `response_format`. Parse with a fallback:

```
try JSON.parse(raw)
catch: extract the first `{...}` block via a greedy regex (`/\{[\s\S]*\}/`) and JSON.parse that instead
catch again: treat as unparseable
```

Validate the parsed result against the Step 1 schema (e.g. with a schema library). On validation failure, return a distinct error ("AI returned an unexpected format — try again") rather than surfacing a raw parse error. On the network/API call failing, return a separate error ("parsing failed — try again"). Log the raw content (truncated) server-side for debugging, but do not leak it to the client.

## Step 5: Enforce Limits Server-Side

Re-apply the same length limits from Step 2 by slicing each returned string server-side before returning it to the client. Prompt instructions are not guarantees — treat them as best-effort and enforce the real constraint in code.

## Step 6: Merge Non-Destructively on the Client

This is the rule that makes the feature safe to ship: only write a parsed field into the form if the form's current value for that field is empty, and skip any field the model returned as an empty string.

```js
if (!form.city && result.city) form.city = result.city
```

Never overwrite a field the user already typed, even if the parse result disagrees with it — the user's own input is always authoritative. Surface the `confidence` field when it is `low` so the admin knows to manually verify before saving, but do not block the merge on it.

## Step 7: Test These Failure Modes

Before shipping, run the parser against:

- A multi-line address block (typical postal-mail format)
- A single-line comma-separated address (typical Google Maps copy-paste)
- Non-Latin script input (e.g. an address in Chinese or Arabic) — confirm the model still extracts into the target language/format your app expects, or at minimum degrades to low confidence rather than fabricating fields
- Phone-only input with no address at all — confirm every address field comes back empty rather than guessed
- Garbage/unrelated input (e.g. a recipe, random text) — confirm the model returns empty strings and low confidence rather than hallucinating a plausible-looking address

## Step 8: Bilingual Field Variant

Some record types carry paired fields for two languages instead of one canonical value — e.g. `companyNameZh`/`companyNameEn`, `companyAddressZh`/`companyAddressEn`. Extend the base technique like this:

- **Pair every bilingual field.** For each concept, define both a source-language field and a counterpart field (e.g. `contactNameZh` / `contactNameEn`), not a single field plus a separate "language" flag.
- **Fill-from-source-then-render-counterpart rule.** Instruct the model: fill the field matching the language the source text actually used, taking the value from the source itself, then populate the counterpart *only where the rendering is mechanical* — romanizing a Chinese address or personal name into Latin script for a shipping label is safe, because the result is a transliteration rather than new information.
- **Distinguish transliterable values from registered ones.** A company's legal name in another language is a registered fact, not something derivable from its name in the first language; same for anything officially issued. Leave the counterpart empty for those fields rather than producing a plausible-looking translation that will not match any document. Getting this wrong is worse than an empty field, because the invented name looks authoritative and flows into invoices and customs paperwork.
- **Do not machine-translate into a script the source did not contain.** If the input is single-language (e.g. English-only), leave the opposite-script fields empty rather than guessing a translation. This mirrors the empty-string-not-guess rule from Step 2, applied per-language: an absent language in the source is itself information, not a gap to paper over.
- State both rules explicitly and adjacently in the prompt — models default to translating everything into both fields unless told not to for the single-language case.
- The non-destructive merge rule from Step 6 applies per bilingual field independently — merging `companyNameEn` does not depend on whether `companyNameZh` was also filled.
