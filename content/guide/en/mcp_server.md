# RockFace as an MCP server for other AI assistants

## What it is for

Besides calling outside services, RockFace can be called by them. The command `rockface mcp serve` opens a project
as an **MCP server** (Model Context Protocol): an AI assistant that speaks MCP — Claude Desktop, a code editor, a
corporate agent — can then query the samples, read tables, find guide pages and write scripts for RockFace, talking
in plain language with the user. It is the way to tasks larger than Mio's recipes: the assistant reads the reference
of the programming interface and writes the script, which you run in RockFace.

## Before you start

* RockFace installed on the computer, and a project.
* An assistant that accepts MCP servers. You are responsible for what the assistant sends out: if it runs in the
  cloud, RockFace's answers reach its service. For a confidential project use a local assistant, or do not use this.

## Step by step

### Link RockFace to the assistant

1. Make the configuration: `rockface mcp config project.rockface`. It prints an `mcpServers` JSON entry with the
   command that starts the server.
2. Paste that entry into the assistant's MCP configuration file (in Claude Desktop, the configuration file of the
   developer tools) and restart the assistant.
3. Ask the assistant, for example:
   * "In RockFace, how many samples have calcite, and in which wells?"
   * "Show the petrophysics table of the samples with porosity above 15 %."
   * "How do I count points with a motorized stage in RockFace?"
   * "Write a RockFace script that, for each well, exports the LAS and a Folk classification table."

### Let the assistant run scripts

With `rockface mcp config project.rockface --allow-scripts` the server also offers `run_script`: the assistant runs
scripts on the project and sees their output. Use it only on a working project, with a backup, and an assistant you
trust.

### Serve over HTTP

`rockface mcp serve project.rockface --http 8765` serves the same over HTTP (Streamable HTTP) at `127.0.0.1:8765`,
on this computer only.

## Options

| Server tool | What it gives the assistant |
|---|---|
| `ask` | Mio's answer to a question (counts, lists, statistics, values, gaps, a description) |
| `search` | the descriptions of a question and the conditions read |
| `describe` | one description in words |
| `table` | a concept as a table (identification, composition, petrophysics, totals, classifications…), optionally only for the descriptions of a question |
| `guide` | the pages of this guide that answer a question |
| `write_script` | a script written by Mio's recipes (returned, not run) |
| `api` | the reference of the programming interface (`rf`) |
| `run_script` | only with `--allow-scripts`: runs a script on the project |

Resources: `rockface://api` (the reference) and `rockface://guide/<page>` (the guide pages). Command options:
`--lang en|pt|es` (language of the answers), `--allow-scripts`, `--http PORT`.

## How it works

The server uses the official MCP Python SDK (MIT licence). Every call of the assistant leaves a row in the project's
audit (`mcp`) with the tool and the text asked. The tools, except `run_script`, only read the project. The answers
come from the database and from the tested recipes; the assistant may rephrase them, but the numbers are RockFace's.

## From a script

```python
cfg = rf.mcp_config("project.rockface")          # the mcpServers entry
print(cfg)
print(rf.api_reference()[:2000])                 # what the api tool returns
```

## Limits and common problems

* The assistant does not see RockFace: check the project path in the `mcpServers` entry and restart the assistant.
* Answers in the wrong language: start with `--lang`.
* `run_script` is missing: `--allow-scripts` was not given.
* The project is open in RockFace at the same time: reading works; writes of `run_script` and of the program may
  cross — close one of them to write.

## Coverage

ROADMAP stage 0.30 (Mio's tools also offered as an MCP server).
