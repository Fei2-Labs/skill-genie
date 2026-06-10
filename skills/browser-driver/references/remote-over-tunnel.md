# Remote agent + local browser: bridge CDP over an SSH tunnel

This skill drives the browser that holds the user's login. When the **agent runs on a remote host (VPS) but the logged-in browser is on the user's local machine**, the CDP port is on the local machine's loopback and the remote agent cannot reach it directly. Bridge it with an SSH **reverse** tunnel.

First decide which case you are in:

| Where the agent runs | Where the logged-in browser is | What to do |
|---|---|---|
| Same machine as the browser (local) | local | No tunnel. Use `references/launch-and-drive.md` directly. |
| Remote (VPS) | user's local machine | **Reverse-tunnel the CDP port** (below). |
| Remote (VPS) | also on the VPS, headless, no display | This skill does not apply — there is no existing user session to reuse. Solve login another way (imported cookies / `storageState`) or use a different approach. |

## Reverse tunnel (agent on VPS, browser on local)

The local machine usually sits behind NAT, so the VPS cannot SSH *into* it. Initiate the tunnel **from the local machine outward** to the VPS, mapping the local CDP port onto the VPS loopback:

```bash
# Run on the user's LOCAL machine (where the browser + login live):
ssh -N -R 127.0.0.1:9223:127.0.0.1:9223 user@vps
```

- `-R 127.0.0.1:9223:127.0.0.1:9223` — VPS `127.0.0.1:9223` now forwards to the local `127.0.0.1:9223` where the browser listens.
- The agent on the VPS then connects exactly as normal: `connectOverCDP('http://127.0.0.1:9223')`.
- `-N` = no remote command, just forward.

Order of operations: launch the local browser with its debug port first (`references/launch-and-drive.md`), confirm it answers locally, then open the tunnel, then drive from the VPS. The user watches on their own local screen; the agent acts from the VPS.

## Security — non-negotiable for unauthenticated CDP

CDP has **no authentication**: anyone who can reach the port can fully control the logged-in browser. So:

- **Bind to loopback only.** Use `127.0.0.1:9223:...`, never `0.0.0.0` / `*` / a bare `-R 9223:...` that listens on all VPS interfaces. (If `GatewayPorts` is on, an unqualified `-R` can expose it publicly — always qualify with `127.0.0.1`.)
- **SSH key auth**, not passwords.
- **Tear the tunnel down** the moment the task is done (kill the `ssh -N` process), and then restart the browser normally to drop the debug port (`references/selectors-and-handoffs.md` → Cleanup).
- Never port-forward CDP to a public address or a shared host.

## Host-header note

Chromium's remote debugging rejects CDP connections whose `Host` header is not `localhost`/an IP. Because the agent connects to `127.0.0.1` on the VPS (forwarded to `127.0.0.1` locally), the Host stays `localhost` end to end and the connection is accepted. Connecting to a non-loopback hostname would be refused — another reason to keep it loopback-to-loopback.
