# ChatGPT and Gemini in RockFace

## What it is for

The AI assistant panel of RockFace talks to **Claude** (Anthropic), **ChatGPT** (OpenAI) or **Gemini** (Google), as
you choose. The three use the same RockFace tools and follow the same rules as Claude (see
[Claude in RockFace](claude.md)): they read the samples of the project, find the pages of this guide, look at the
pictures of the thin section and at the window, open a description and a tab, and propose fields of the microscopic
description and of the pore system — always **unticked**, for you to decide.

The desktop apps work in RockFace too, through RockFace's MCP server: **Claude Desktop**, the **ChatGPT desktop app**
(and Codex, which shares its configuration) and **Google Antigravity**, desktop and command line, where Gemini works.

## Before you start

* **For the panel**, the API key of the company whose assistant you use. API keys are paid by use and are not part of
  a subscription to the ChatGPT or Gemini apps:
  * ChatGPT — OpenAI Platform, platform.openai.com → API keys (or the `OPENAI_API_KEY` variable);
  * Gemini — Google AI Studio, aistudio.google.com → Get API key (or `GEMINI_API_KEY`, or `GOOGLE_API_KEY`);
  * Claude — Claude Console (or `ANTHROPIC_API_KEY`).
  Each key is kept in a file of your user folder that only you can read, never in a project.
* **For a desktop app**, the app installed and signed in: no API key is needed there.
* **Your data.** What an assistant reads — the question, the tool answers, the pictures it looks at — goes to its
  company. Public data, fine; **private data, do not use them**: use Mio, which runs on this computer. RockFace asks
  before the first conversation with each assistant, and again in each session for a project marked confidential.

## Step by step

### Choose the assistant of the panel

1. Click **AI assistant** (Home → Tools, or `Ctrl+Alt+K`).
2. In the panel, choose **Claude**, **ChatGPT** or **Gemini**, then the model:
   * ChatGPT: **GPT-6.1 Sol** (default; US$ 2 / 10 per million tokens, input / output), **GPT-6 Astra** (the most
     capable; US$ 10 / 50), **GPT-6.1 Terra** (US$ 1 / 5), **GPT-6 Luna** (the fastest and cheapest;
     US$ 0.10 / 0.50);
   * Gemini: **Gemini 4 Argon** (default; US$ 2 / 10 until 30 November 2026, then US$ 4 / 20), **Gemini 3.8 Flash**
     (faster and cheaper; US$ 0.75 / 3.75, introductory), **Gemini 3.1 Pro (preview)** (US$ 2 / 12).
   Each assistant keeps its own model; changing the assistant starts a new conversation.
3. The first time, click the **settings** button, choose the assistant under **Keys and models of**, paste its key and
   **Save**.
4. Ask, in your language, as with Claude: "Open ILL-TS-001, look at the picture and propose the sorting and the
   pores." The proposals arrive in a window, unticked; tick what you see and **Apply the ticked ones**.

### Let a desktop app work in RockFace

In the panel's settings:

* **Write in the ChatGPT desktop app** adds RockFace to `~/.codex/config.toml`, which the ChatGPT desktop app, Codex
  and its editor extension share (a dated copy of the old file is kept). In the ChatGPT app, open Settings → MCP
  servers and restart the extensions; RockFace appears there. (You may also add it by hand there: STDIO, with the
  command shown by `rockface assistant config chatgpt`.)
* **Write in Google Antigravity (Gemini)** adds RockFace to `~/.gemini/config/mcp_config.json`, which the
  Antigravity desktop app and its command line (`agy`) share. Run `/mcp` there to see RockFace's tools.
* **Install in Claude Desktop…** and **Write in Claude Desktop's configuration**: see [Claude in RockFace](claude.md).

Each of these also switches on **Let the AI assistants work in this window**, so the app works in the window you have
open (and on the project file, when no window is open, if you chose one).

## How it works

* **One set of tools, three conversations.** The tools, the rules and the audit are those of Claude in RockFace. The
  panel talks to ChatGPT through OpenAI's Responses API (`store: false`: OpenAI does not keep the conversation; the
  model's reasoning comes back encrypted between turns) and to Gemini through the Gemini API (`generateContent` with
  function declarations; each turn of the model goes back as it came, with its thought signature). Pictures go to
  ChatGPT in a message after the tool answers and to Gemini beside them; only the last two stay in a conversation.
* **The proposals' window** says which assistant made them ("Proposals from Gemini"); when a desktop app calls, it
  says "the AI assistant", because RockFace does not know which app it is.
* **Audit.** Each tool call is written in the project's audit with its origin: `panel:` for the panel, `mcp:` for a
  desktop app.
* **The web versions of ChatGPT and Gemini** cannot reach a program on your computer; RockFace does not open it to the
  internet. Use the desktop apps.

## From a script

```python
rf.assistants()                                     # the assistants, whether a key is set, the models and prices
rf.assistant_ask("Which facies has the most porosity?", prj, assistant="gemini")
rf.assistant_ask("How many samples have calcite?", prj, assistant="chatgpt", model="gpt-6-luna")
rf.assistant_config("chatgpt")                      # the [mcp_servers.rockface] table, as text
rf.assistant_config("gemini", install=True)         # written into Antigravity's configuration
```

From the command line: `rockface assistant list`, `rockface assistant ask project.rockface "question" --with
chatgpt`, `rockface assistant config chatgpt|gemini|claude`.

## Limits and common problems

* "The API key was refused": a key of one company does not work for another; check that the key in the settings is
  under the right assistant.
* "The key has no permission for this (credit or model)": the account has no credit left or no access to that model —
  ChatGPT and Gemini keys need billing set up for these models.
* The ChatGPT desktop app does not list RockFace: restart its extensions (Settings → MCP servers) or the app.
* Antigravity does not list RockFace: check `/mcp`; an older Gemini CLI reads `~/.gemini/settings.json` instead
  (add the entry printed by `rockface mcp config --live` under `mcpServers`).
* The models and prices change often; RockFace shows those of November 2026.
* Without internet, or with private data, use Mio.

## Coverage

O10 (the owner's request of 2026-11-18: ChatGPT and Gemini working in RockFace as Claude does).

References: OpenAI, Responses API and function calling, https://platform.openai.com/docs; OpenAI, Model Context
Protocol in the ChatGPT desktop app and Codex, https://learn.chatgpt.com/docs/extend/mcp; Google, Gemini API function
calling, https://ai.google.dev/gemini-api/docs; Google Antigravity, migrating from Gemini CLI,
https://antigravity.google/docs/cli/gcli-migration.
