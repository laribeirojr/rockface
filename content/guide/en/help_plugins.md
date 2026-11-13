# Help, support, plug-ins and updates

## What it is for

**Help contents** (F1) opens this guide inside the program, with contents, index and search. **Support** prepares
what to send when asking for help. **Plug-ins and updates** installs extensions written in Python and says when a
newer RockFace exists.

## Before you start

Nothing for the help. For plug-ins: a plug-in `.zip` (a folder with `plugin.json` and its code) or the address of a
plug-in server.

## Step by step

1. **Help → Help contents** (F1). *Contents*: pages and sections; *Index*: every title, with a filter; *Search*:
   words, then Enter — the best sections first.
2. **Help → Support…**: the versions of RockFace, Python, the libraries and the plug-ins, to copy or save; write to
   the support address your team set (preference `support/contact`).
3. **Help → Plug-ins and updates…**: *Install from a file…* shows the plug-in's name, author and the SHA-256 of the
   file before installing; *Install from a Git repository…* clones the repository (add `@branch` or `@tag` to the
   address for a version) and shows the commit before installing; tick *On* to enable it (at the next start); *Remove*. *Server*: blank for the RockFace
   catalogue or the address of another `index.json`; *List the server's plug-ins* and double-click one to install;
   *Check for a newer RockFace*.

## Options

| `plugin.json` field | Meaning |
|---|---|
| name, version, description, author, licence | shown in the list |
| requires | the oldest RockFace version it works with |
| module | the Python file with `register(app)` |

## How it works

* The guide is the same Markdown as the website, indexed when the program is built; the search ranks sections by
  BM25 over their words, as Mio does.
* Plug-ins live in `~/.rockface/plugins`; a plug-in starts disabled and is imported only after the user enables it;
  an archive with paths outside its folder is refused; a plug-in that fails at start is reported, not fatal.
* The server index lists the latest RockFace (version, installer, SHA-256, notes) and the plug-ins; downloads are
  kept only when their SHA-256 matches. RockFace never installs an update by itself.

## From a script

```python
rf.plugins.install_zip("tool.zip"); rf.plugins.enable("tool")
rf.plugins.install_git("https://example.org/team/tool.git", "v1.0")
rf.plugins.check_update("https://example.org/rockface/index.json")
```

## Limits and common problems

* A plug-in runs with your rights: install only what you trust.
* The default catalogue is published with the installers (from 1.0); until then use a server of your team.

## Coverage

P40 (help contents, support), P41 (plug-in manager and system updater); Counterledge C6.
