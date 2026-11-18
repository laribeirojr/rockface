# Claude in RockFace

## What it is for

Claude, the AI assistant made by Anthropic, can work **with** RockFace, as it does in a word processor or a
spreadsheet: it reads the samples of the project, finds the pages of this guide, looks at the thin-section pictures
and at the window, opens a description and a tab, and proposes fields of the microscopic description and of the pore
system. It reaches RockFace in three ways, which may be used together:

1. **The Claude panel**, inside every RockFace program (beside Mio): you talk to Claude without leaving RockFace.
2. **Claude Desktop**, with the **RockFace extension** (one double click installs it): you talk to Claude in its own
   app and it works on RockFace.
3. **The live window**: whichever way you talk to it, Claude works in the RockFace window that is open — the
   description you are on, the tab you see, the pictures of its thin section.

The three share the same tools, the same rules and the same audit, so what Claude does from Claude Desktop is what
it does from the panel.

Mio stays as it is: local, free and offline. Claude is an option for those who want a stronger model and accept
that the conversation goes to Anthropic.

## Before you start

* For the **panel**: a **Claude API key**. It is made in the Claude Console (platform.claude.com → API keys) and is
  paid by use; a subscription to the Claude apps (Pro, Max, Team) does not include it. Paste it in the panel's
  settings: it is kept in a file of your user folder that only you can read, never in a project. A key in the
  `ANTHROPIC_API_KEY` variable is used first.
* For **Claude Desktop**: the Claude Desktop app, signed in. No API key is needed — Claude Desktop uses your Claude
  plan.
* **Your data.** What Claude reads — the question, the tool answers, the pictures it looks at — is sent to Anthropic.
  Public data, fine; **private data, do not use Claude**: use Mio, which runs on this computer. RockFace asks before
  the first conversation, and again in each session for a project marked confidential (*Tools → Connectors*).

## Step by step

### Talk to Claude in RockFace (the panel)

1. Click **Claude** (Home → Tools, or `Ctrl+Alt+K`). The panel opens on the right.
2. The first time, click the **settings** button of the panel, paste the API key and **Save**. Choose the model:
   * **Claude Sonnet 5.5** (default) — fast and capable; US$ 2 / 10 per million tokens (input / output);
   * **Claude Opus 5.5** — the most capable for long work; US$ 4 / 20;
   * **Claude Haiku 5.5** — the fastest and cheapest; from US$ 0.10 / 0.50;
   * **Claude Fable 5.2** — the hardest research tasks; US$ 8 / 40.
3. Ask, in your language. For example:
   * "Which samples of the project have calcite cement above 10 %? Make a table with their porosity."
   * "Open ILL-TS-001, look at the picture and propose the sorting, the roundness and the pores."
   * "How do I make a ternary diagram of the point count?"
4. The panel shows each tool Claude used (⚙ lines) and its answer. **Stop** ends a long turn; **New conversation**
   starts over. The tokens spent are shown below the model.

### Claude proposes, you decide

* **Proposals.** When Claude proposes fields of the description, a window lists them **unticked**: the field, the
  value and the words Claude used. Tick what you see yourself, click **Apply the ticked ones**, then **save** the
  description as usual. Nothing is written before that.
* **Scripts.** If you switch on **Let Claude propose scripts** (settings), Claude may write a Python script for a
  task; it is shown in a window and runs only when you click **Run**. A description with unsaved changes is not
  touched.
* **Moving.** Claude may open a description and show a tab; it will not leave a description with unsaved changes.

### Claude Desktop works on RockFace (the extension)

1. In the Claude panel's settings, click **Install in Claude Desktop…**. RockFace writes
   `RockFace-Suite.mcpb` (in your user folder, `.rockface/claude`), opens it and switches on the live window.
2. Claude Desktop shows the installation: click **Install**. (Or open Claude Desktop → Settings → Extensions and
   drag the file there.) In its options you may choose a **project** — used when no RockFace window is open — and
   **Let Claude propose scripts**.
3. In Claude Desktop, ask as in the panel: "In RockFace, what is open now?", "Look at the picture of this sample and
   propose the description."

If your Claude Desktop does not take extensions, click **Write in Claude Desktop's configuration** instead: RockFace
adds itself to `claude_desktop_config.json` (keeping a dated copy of the old file); restart Claude Desktop.

### The live window

**Let Claude work in this window** (settings) opens a channel on this computer only (127.0.0.1, a random port and a
secret in a file only you can read). With it on, Claude Desktop works in the window you have open; with it off, it
works on the project chosen in the extension, or on nothing. It stays on for the next sessions until you switch it
off; it closes with the window.

## How it works

* **One set of tools.** `search`, `table`, `ask` (Mio), `describe`, `guide`, `write_script`, `api_reference`,
  `description_fields`, and, in a window, `window_state`, `open_description`, `show_tab`, `list_pictures`,
  `look_at` (a picture, or the window itself, reduced to 1 568 pixels), `propose_description` and, when allowed,
  `run_script`. In the panel, Claude calls them through the Claude Messages API with tool use; from Claude Desktop,
  through RockFace's MCP server (`rockface mcp serve --live`), which passes each call to the open window.
* **Proposals use RockFace's words.** `propose_description` reads "Field: value" lines with the same reader as
  dictation and *Mio looks*; only the words of RockFace's vocabulary become proposals, and they start unticked —
  people follow automated advice even when it is wrong (automation bias), so you decide each field.
* **Pictures.** Only the last two pictures stay in a conversation; earlier ones are replaced by a note, which keeps
  the cost down.
* **Audit.** Every tool call is written in the project's audit, with where it came from (`panel:` or `mcp:`).
* **No new package.** The panel talks to the API with Python's own HTTP client; the extension is a ZIP made on your
  computer, pointing at your RockFace.

## From a script

```python
rf.claude_models()                                   # the models, with their prices
rf.claude_ask("How many samples have calcite?", prj) # needs ANTHROPIC_API_KEY or the panel's key
rf.claude_extension()                                # the .mcpb file for Claude Desktop
rf.claude_desktop_config(install=True)               # or write Claude Desktop's configuration
rf.live_windows()                                    # the windows that let Claude work in them
rf.mcp_config(live=True)                             # the mcpServers entry for another assistant
```

From the command line: `rockface claude extension`, `rockface claude config`, `rockface claude ask project.rockface
"question"`, `rockface claude windows`, and `rockface mcp serve --live`.

## Limits and common problems

* "No API key yet": the panel needs a key from the Claude Console; Claude Desktop does not.
* "The API key was refused" (401) or "The key has no permission for this" (403, often no credit left): check
  the key in the Claude Console. "Too many requests for now" (429) or "Claude is busy right now" (529): wait a
  little and ask again.
* Claude Desktop says no RockFace window lets Claude work in it: open RockFace and switch on **Let Claude work in
  this window**, or choose a project in the extension's options.
* The extension points at the RockFace of the computer that made it; after reinstalling RockFace in another folder,
  make it again.
* Claude is a general model, not a petrographer: check every proposal against the picture, as with *Mio looks*.
* Without internet, use Mio.

## Coverage

O9 (the owner's request of 2026-11-18: Claude operating RockFace, as in the Word, Excel and PowerPoint apps — the
panel, the live window and the Claude Desktop extension together).

References: Anthropic, Claude Messages API and tool use, https://docs.claude.com; Model Context Protocol,
https://modelcontextprotocol.io; MCP Bundles (.mcpb), https://github.com/modelcontextprotocol/mcpb; Goddard, Roudsari &
Wyatt (2012), automation bias, https://doi.org/10.1136/amiajnl-2011-000089.
