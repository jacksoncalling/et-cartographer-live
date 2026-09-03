# The Cartographer — future path

## Option 1: GitHub-persistent writes (the full promise)

The demo (Option 2) writes new cards to an in-session copy of the map.
Option 1 makes those writes durable: the agent commits them back to GitHub.

### How it would work

1. The Replit server authenticates to GitHub via a personal access token (stored in Replit Secrets as `GITHUB_TOKEN`).
2. When `ingestNode` fires on the backend, it writes the new card as a `.md` file to `map/objects/` using the GitHub Contents API (a PUT to `/repos/{owner}/{repo}/contents/...`).
3. A post-ingest hook re-runs `build-bundle.py` and `build-artifact.py` (or the server holds the live graph in memory and only persists the raw note file).
4. Future sessions load the updated `map/map.json` and the committed card is part of the permanent record.

### Why this is the right upgrade path

The folder IS the map IS the method. A card that lives only in session memory disappears when the tab closes. A committed card attributed to Ralf-Peter Meyer, with a verified: stamp and a date, is a real contribution to the territory.

The email to Ralf promises this upgrade, not the demo. Build it after the demo lands.

### Connection to et-foerder-navigator

`~/et-foerder-navigator` catalogs EU grant money for research collaborations — the supply-side of the ET ecosystem. A future corpus integration would let the agent answer "what funding is available for this gap?" by pulling from that corpus as a second data source alongside the map. The cartographer stays the primary index; the navigator is a retrievable annex.
