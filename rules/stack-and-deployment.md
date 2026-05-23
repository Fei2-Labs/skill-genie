# Stack and deployment

## Platform split
- For macOS and iOS apps, follow Apple-native conventions and the recommended Apple stack.
- For other projects, use the Nuxt 3 + Appwrite + Dokploy defaults below.

## Default structure
- `apps/web` for the frontend.
- `apps/api` for the backend.
- `packages` for shared code.

## Nuxt and UI
- Define page metadata with title, description, and OG metadata.
- Use semantic layout tags.
- Prefer server components by default and keep client-side JavaScript small.
- Put form logic behind server routes when possible.
- Use `NuxtImg` with configured image domains.
- Generate OG images through a Nitro endpoint.
- Use Tailwind CSS with dark mode support and accessible interactions.
- Include proper SEO basics: title, meta description, one H1, OG tags, canonical links, and image alt text.

## Appwrite
- Use the Appwrite client/server wrappers instead of ad hoc client creation.
- Keep auth logic in `services/appwrite/auth.ts`.
- Use `databases.listDocuments(...)` for queries and `storage.createFile(bucketId, "unique()", file)` for uploads.
- Keep collection ownership fields and timestamps in place.
- Use Appwrite RBAC and explicit permissions.
- If realtime is used, put it behind a dedicated composable.

## Data and state
- Keep sensitive server-side operations in server routes.
- Use `useAsyncData` or TanStack Query for client fetching.
- Prefer Pinia or composables for shared state.
- Use Zod-based validation.
- Keep forms progressively enhanced.

## Deployment
- Build Nuxt apps with the Node 20 + pnpm + Nitro flow.
- Keep Dokploy env vars in the UI, and match client/server Appwrite endpoints.
- If the Dokploy API is unavailable, fall back to SSH only when the host is already configured.
- Rebuild desktop app installers whenever bundled app code changes, and do not commit build artifacts unless asked.