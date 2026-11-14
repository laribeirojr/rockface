# Mio's connectors: Google, Microsoft 365, references, geological data and tasks

## What it is for

**Connectors** take RockFace's work to the services the team already uses and bring back what helps the
description. With them Mio can:

* send the table of the samples of a query to a Google Sheets or Excel **spreadsheet**;
* write a **document** (Google Docs, Word) or build a **presentation** with the result;
* prepare an **email** (Gmail, Outlook) to the address you give, or put an **event** in the calendar;
* create a **task** or a card (Trello, Jira, Google Tasks, Planner);
* find a **reference** and its DOI in Crossref or in your Zotero library;
* bring the data of a **mineral** from Mindat and of a **stratigraphic unit** from Macrostrat;
* open a problem report (**issue**) on GitHub.

The Google, Microsoft 365, Trello and Jira connectors use the **Model Context Protocol (MCP)**, the open standard by
which AI assistants talk to outside services. Crossref, Zotero, Mindat, Macrostrat and GitHub are called by RockFace
directly.

## Before you start

* A project open.
* For Google, Microsoft 365 and Jira: the matching MCP server installed on the computer. These servers are not part
  of RockFace; the catalogue only knows how to start them. Google's needs `uv` (the `uvx` command) and an OAuth
  "Desktop app" credential made in Google Cloud; Microsoft 365's needs `Node.js` (the `npx` command) and signs the
  account in the first time.
* For Mindat, Zotero and GitHub: the API key or token of your account. Crossref and Macrostrat are open.
* For the remote servers (Google's own Drive server, GitHub's, Trello): the account's token.

## Step by step

### Switch a connector on for the project

1. In Mio's panel click **Connectors** (or, in Petro, on the Help tab, **Connectors…**).
2. The table shows each connector: group, kind (built-in or MCP, with how it starts), what it does and, in brackets,
   the keys still missing on this computer.
3. Tick **On for this project** in the connector's row. All start off; switching on is for this project only.
4. Select the row and click **Keys and tokens…** to give the keys (kept only on this computer) and the connector's
   settings (the Zotero user id, the GitHub repository, the Crossref contact email).
5. Click **Test**: RockFace starts the server and lists its tools, sending no project data.

### Ask Mio

Write in Mio's panel, as in a conversation. Examples:

* `@mio find the reference Folk 1980 petrology on crossref`
* `@mio mineral data of dolomite on mindat`
* `@mio stratigraphic unit Barreirinhas on macrostrat`
* `@mio send the samples with calcite to a Google sheet`
* `@mio create a Word document with the samples of well ILLUSTRATIVE-1`
* `@mio schedule in the calendar the review of the sections of well ILLUSTRATIVE-2`
* `@mio create a task in Trello: recount section TS-002`
* `@mio open an issue on github: the LAS export skips samples without depth`

Mio does the RockFace part (the samples asked for, the table, the text), picks the connector switched on and the
service's tool that fits, and **prepares** the call. A window shows the connector, the tool, the arguments and
whether project data leave the computer. Only **Confirm and run** sends; **Cancel** sends nothing. The result shows in
the panel (for Crossref, already as a reference list).

### Confidential project

Tick **Confidential project** in the connectors dialog. In that project every call that takes project data out asks
a second time, with a warning; look-ups that carry only the words typed (a reference, a mineral) follow the normal
rule.

### An MCP server of your choice

**Add an MCP server…** asks for a short name and a command (`uvx my-server`, `python server.py`) or an address
(`https://…`). The server enters the table switched off and works as the catalogue's do.

## Options

| Connector | Group | How it works | Needs |
|---|---|---|---|
| Google Workspace | google | community MCP server on the computer (`uvx workspace-mcp --tool-tier core`): Sheets, Docs, Slides, Drive, Calendar, Gmail, Tasks | `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET` and your account `USER_GOOGLE_EMAIL` |
| Google Drive (Google's server) | google | Google's own remote server (Developer Preview) | `TOKEN` |
| Microsoft 365 | microsoft | community server (`npx -y @softeria/ms-365-mcp-server`): Outlook, Calendar, OneDrive, Excel, Word, To Do, OneNote, Teams, SharePoint | the Microsoft sign-in the first time |
| Microsoft 365 (CLI) | microsoft | the PnP community's CLI for Microsoft 365: SharePoint, Teams, Planner, OneDrive | the account sign-in |
| Crossref | references | direct, open | optional: `mailto` |
| Zotero | references | direct | `API_KEY` and the setting `user_id` |
| Mindat | geodata | direct | `API_KEY` (free) |
| Macrostrat | geodata | direct, open | — |
| GitHub | dev | direct (issues) | `TOKEN` and, if wished, the setting `repo` |
| GitHub (GitHub's server) | dev | GitHub's remote server | `TOKEN` |
| Trello | dev | Atlassian's remote server | `TOKEN` |
| Jira and Confluence | dev | community server (`uvx mcp-atlassian`) | `JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN` |

Keys may also come from environment variables `ROCKFACE_<CONNECTOR>_<NAME>` (e.g. `ROCKFACE_GITHUB_TOKEN`), which win
over the file.

## How it works

* **Off by default.** The list of connectors switched on is kept in the project; the keys only on the computer, in
  `~/.rockface/connectors.json` (permissions 600), never in the project nor in the audit.
* **Shown before it runs.** Every call is prepared first; nothing leaves without your confirmation.
* **Audit.** Every call — done, refused, declined or failed — leaves a row in the project's audit (`connector`), with
  the tool and a cryptographic digest of the arguments; the dialog shows the last ones.
* **The right tool.** MCP servers say which tools they have. To send a table, Mio looks for the tool whose name and
  description speak of a spreadsheet and of creating, and puts the table in the data parameter (`values`, `rows`,
  `data`…). She never proposes a deleting tool. You see the tool chosen before confirming.
* **What the tool carries (0.31).** Among the tools that fit, Mio prefers the one that takes the content — a
  spreadsheet imported from CSV rather than an empty one, a document imported from Markdown (with a title and a
  table) rather than plain text. Tools such as `manage_event` and `manage_task` get the action `create`; the
  default task list is `@default`. The date and time of an event come from the request (*tomorrow at 3pm*,
  *amanhã às 10h*, *on 02/12 at 14h*), one hour long. An email is prepared only with the address written in the
  request.
* **Your account.** Servers that ask for the account on every call (Google's asks for `user_google_email`) get it
  from the secret `USER_GOOGLE_EMAIL` of this computer; without it, Mio says what is missing instead of guessing.
* **Safety.** Documents and emails coming back from a service may hold instructions written by other people; Mio does
  not follow them — she only shows the result.

## From a script

```python
prj.enable_connector("crossref")
r = prj.connector_call("crossref", "search_works", {"query": "Folk 1980 petrology"}, confirm=True)
for item in r.data:
    print(rf.connectors.reference_text(item))

prj.enable_connector("google")
header, rows = prj.query_table("identification", ("diagenetic", "constituent", "calcite_dia"))
call = prj.connector_plan("google", "export_table", {"title": "Samples with calcite", "rows": [header] + rows})
print(call.preview())                            # what will leave
res = prj.connector_run(call, confirm=True)      # you wrote the call: confirm=True
print(res.ok, res.text)
print(prj.connector_calls()[-1])                 # the audit row
```

On the command line: `rockface connectors list project.rockface`, `rockface connectors enable project.rockface
crossref`, `rockface connectors secret github TOKEN`, `rockface connectors test project.rockface google`,
`rockface connectors call project.rockface crossref search_works '{"query": "Folk 1980"}'`.

## Limits and common problems

* "The connector … is off": switch it on in the table, for this project.
* "missing …": give the keys in **Keys and tokens…**.
* The test does not answer: the server is not installed (`uvx`, `npx` not found) or the account has not signed in.
* Different servers name their tools differently; if Mio picks badly, use **From a script** with the right tool
  (`prj.connector_tools("google")` lists them all) or ask differently.
* Google's own remote Gmail server makes drafts, it does not send: you send. The community server at the `core`
  tier only has the **send** tool: check the recipient in the confirmation window.

## Coverage

ROADMAP stage 0.30 (owner's request of 2026-11-13: Mio's MCP connectors, first Google's tools; and, by his choice,
Microsoft 365, references and geological data, GitHub and tasks).
