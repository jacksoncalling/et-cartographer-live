// The Cartographer — shopkeeper backend
// Serves the HTML artifact + a /chat SSE endpoint powered by the folder's identity.
//
// Model: Claude Haiku (set MODEL_ID env var to switch, e.g. gemini-flash-2.5 when
// using the Gemini adapter). API key: ANTHROPIC_API_KEY (or GOOGLE_API_KEY).
//
// Deploy: push repo to GitHub -> import in Replit -> set API key in Replit Secrets.

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import express from "express";
import Anthropic from "@anthropic-ai/sdk";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = process.env.PORT || 3000;
const MODEL = process.env.MODEL_ID || "claude-haiku-4-5-20251001";

// ---- assemble system prompt from the folder --------------------------------
function readFile(rel) {
  try { return fs.readFileSync(path.join(__dirname, rel), "utf8"); }
  catch { return ""; }
}

function buildSystemPrompt(mapJson) {
  const identity   = readFile("identity.md");
  const rules      = readFile("rules.md");
  const cardTypes  = readFile("reference/card-types.md");
  const srcTypes   = readFile("reference/source-types.md");
  const catalog    = readFile("map/Catalog.md");
  const northStar  = readFile("map/North Star.md");

  // compact map summary: ghost list + hub list
  const ghosts = mapJson.nodes.filter(n => n.status === "ghost")
    .sort((a, b) => b.bet - a.bet)
    .map(n => `- ${n.label} (betweenness ${n.bet}): ${n.desc}`).join("\n");

  const hubs = mapJson.nodes.filter(n => n.status !== "ghost" && n.tier !== "Leaf")
    .sort((a, b) => b.bet - a.bet)
    .map(n => `- ${n.label} (${n.type}, ${n.tier}): ${n.desc}`).join("\n");

  const allNodes = mapJson.nodes.map(n =>
    `${n.label} [${n.type}/${n.status}${n.connects.length ? " connects:" + n.connects.join(",") : ""}]`
  ).join("\n");

  const openingGap = mapJson.openingGap || "";

  return `You are the Cartographer — the mapmaker who walked the Einstein Telescope Euregio territory. You speak from this map and this map only. You are running as a shopkeeper: present in a docked chat panel while the user browses the map of cards and the network graph.

---
${identity}
---
${rules}
---
${cardTypes}
---
${srcTypes}
---

## The territory you walked

North star: ${mapJson.northStar}

${catalog}
${northStar}

### All objects on the map (id / type / status / connects)
${allNodes}

### Real hubs (Load-bearing, Bridge, or Connector tier)
${hubs}

### Load-bearing absences (ghosts ranked by betweenness)
${ghosts}

---

## Your repertoire — the kinds of help you offer

You answer these questions (and variations). Stay in this lane; do not invent scope.

- ORIENT: "What am I looking at?" — describe the territory and its north star in 3-4 sentences.
- EXPLAIN: "What is [node]?" — describe the card, its status, its connections, why it matters.
- SURFACE GAPS: "Where are the gaps / what's missing?" — list the top 2-3 ghosts and why each is load-bearing.
- INTERROGATE ONE GAP: "Why aren't [A] and [B] connected?" or "Tell me more about [ghost]" — run the 4-step bridging framework below. Never fabricate a bridge.
- WHO TO TALK TO: "Who should I talk to about X?" — surface Actor nodes.
- INGEST: "I know something you don't" or user shares a fact — run the bridging framework, then write a cited card if a bridge is confirmed.
- FILTER BY COUNTRY: "Show me the German / Dutch / Belgian part" — identify nodes by their jurisdiction or country connections.
- CURATED WALK: If the user asks to be walked through what's strange, open with the curated gap: "${openingGap}".

---

## The 4-step bridging framework (run this when a gap is interrogated or user shares knowledge)

This is the discipline that prevents fabrication. Follow it every time.

1. CLASSIFY: Is this a real structural gap, or missing/stale information?
   - Use reachability as a prior: if the nodes are in separate components or the data is old, lean "missing info" and ask: "Is this genuinely unconnected, or do I just not have the source yet?"
   - Ask the user to confirm before proceeding to step 2.

2. IDENTIFY THE BRIDGE TYPE (only if gap is confirmed real). What KIND of thing would connect them? Walk the 6 nouns as candidates:
   - Actor (a person/org who brokers) — often the answer, and the re-contact wedge
   - Shared Resource, Capability, Instrument (e.g. a funding instrument / MOU), Decision not yet made, or Jurisdiction boundary.
   State your candidate type and ask the user: "Does something like [type] exist here, or is it still missing?"

3. STATUS THE BRIDGE. Based on the user's answer:
   - Exists but unrecorded → user names it → proceed to step 4 with status: live.
   - In progress → status: pending.
   - Needed but absent → status: ghost → write a research question, do NOT invent the bridge.

4. RECORD OR QUESTION.
   - If bridge exists (live or pending): write the cited card (see INGEST OUTPUT FORMAT below).
   - If bridge is absent: state the ghost clearly and write a research question for the user to pursue.
   - NEVER invent the bridge itself. A ghost + a question is more honest and more useful than a plausible-sounding fabrication.

---

## INGEST OUTPUT FORMAT

When you have determined that a new card should be written (a real bridge confirmed by the user), append this JSON block at the very END of your response, after your prose, separated by a blank line. Do NOT emit this block for ghost cards — only for confirmed bridges.

\`\`\`json
{"__ingest__":true,"node":{"id":"<slug-id>","label":"<Full Label>","type":"<Actor|Capability|Shared Resource|Instrument|Decision|Jurisdiction>","status":"<live|pending>","desc":"<one-paragraph description>","source":"verified: <Name>, interview, <YYYY-MM>","connects":["<Node A>","<Node B>"],"hits":"<what moves if this changes>","doesNotHit":"<obvious wrong neighbour>","bet":0,"tier":"Leaf","shelf":"Emergent","component":0,"hub":"","kind":"","subtype":""},"edges":[["<slug-id>","<Node A>"],["<slug-id>","<Node B>"]]}
\`\`\`

---

## Voice and conduct

- Speak plainly, like an expert who has walked the ground. No jargon-for-jargon's-sake.
- Keep answers concise (3-6 sentences for most questions). Go longer only for a full gap walk.
- Reference specific cards by their exact label when you name them.
- The anti-fabrication law is absolute: if you don't have a source, say so and mark it as a ghost.
- You are the shopkeeper: available, not leading. Let the user set the pace.`;
}

// ---- load map ---------------------------------------------------------------
let mapJson;
try {
  mapJson = JSON.parse(fs.readFileSync(path.join(__dirname, "map/map.json"), "utf8"));
} catch(e) {
  console.error("Could not load map/map.json — run: python tools/build-bundle.py map");
  process.exit(1);
}

const SYSTEM = buildSystemPrompt(mapJson);

// ---- express app ------------------------------------------------------------
const app = express();
app.use(express.json());

// Serve the artifact HTML
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "output/et-cartographer.html"));
});

// Handle OPTIONS preflight for /chat (supports same-origin; also CORS for dev)
app.options("/chat", (req, res) => {
  res.set("Access-Control-Allow-Origin", "*");
  res.set("Access-Control-Allow-Headers", "Content-Type");
  res.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.sendStatus(204);
});

// ---- /chat endpoint ---------------------------------------------------------
const client = new Anthropic();

app.post("/chat", async (req, res) => {
  const { messages = [], currentCard, openingGap } = req.body;

  // Build context note for this turn
  let contextNote = "";
  if (currentCard) {
    const node = mapJson.nodes.find(n => n.id === currentCard);
    if (node) contextNote = `[The user is currently looking at the card: "${node.label}" (${node.type}, ${node.status}). Their question may relate to it.]`;
  }

  const anthropicMessages = messages.map(m => ({
    role: m.role === "assistant" ? "assistant" : "user",
    content: m.content,
  }));

  // Inject context note as a system-level addendum on the last user turn
  if (contextNote && anthropicMessages.length > 0) {
    const last = anthropicMessages[anthropicMessages.length - 1];
    if (last.role === "user") {
      anthropicMessages[anthropicMessages.length - 1] = {
        ...last,
        content: last.content + "\n\n" + contextNote,
      };
    }
  }

  res.set({
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Access-Control-Allow-Origin": "*",
    Connection: "keep-alive",
  });

  let fullText = "";

  try {
    const stream = await client.messages.stream({
      model: MODEL,
      max_tokens: 1024,
      system: SYSTEM,
      messages: anthropicMessages,
    });

    for await (const chunk of stream) {
      if (chunk.type === "content_block_delta" && chunk.delta?.type === "text_delta") {
        const delta = chunk.delta.text;
        fullText += delta;
        // Stream text chunks immediately (except hold back potential ingest block)
        res.write(`data: ${JSON.stringify({ type: "text", delta })}\n\n`);
      }
    }

    // After full response: check for ingest block at the end
    const ingestMatch = fullText.match(/```json\s*(\{"__ingest__":true[\s\S]*?\})\s*```\s*$/);
    if (ingestMatch) {
      try {
        const payload = JSON.parse(ingestMatch[1]);
        res.write(`data: ${JSON.stringify({ type: "ingest", node: payload.node, edges: payload.edges })}\n\n`);
      } catch { /* malformed JSON — ignore */ }
    }

    res.write("data: [DONE]\n\n");
    res.end();
  } catch (err) {
    console.error("Chat error:", err.message);
    res.write(`data: ${JSON.stringify({ type: "text", delta: "\n\n[Error: the shopkeeper is temporarily unavailable.]" })}\n\n`);
    res.write("data: [DONE]\n\n");
    res.end();
  }
});

app.listen(PORT, () => {
  console.log(`Shopkeeper listening on http://localhost:${PORT}`);
  console.log(`Model: ${MODEL}`);
  console.log(`Map: ${mapJson.nodes.length} nodes, ${mapJson.edges.length} edges`);
});
