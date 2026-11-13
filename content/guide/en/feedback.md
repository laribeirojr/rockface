# Sending your opinion

## What it is for

RockFace is tested by colleagues and students before it reaches every user. **Send feedback…** opens the feedback
form of RockFace in your browser, where you say what works, what does not, and what is missing — for the program in
general or for one function of this guide. The answers go to the RockFace team.

## Before you start

* A web browser and a network connection.
* The form is a Microsoft Forms form of the RockFace team (University of Brasília). Until its address is set, the
  button says so (below).

## Step by step

1. In RockFace Petro: **Help → Send feedback…**. In RockFace Atlas, Explorer, Lab and MC: the **Send feedback…**
   button of the toolbar.
2. Your browser opens the form. Say which program and which function you are writing about — the **Coverage**
   section at the end of each page of this guide gives the items of the function (for example *GT11*), which help
   the team find it.
3. Describe what you did, what you expected and what happened. Attach a screenshot if it helps; never attach
   confidential data.
4. Send the form.

When the form is not defined yet, RockFace shows "The feedback form is not defined yet." — write to your team's
support address instead (**Help → Support…** prepares the versions to send).

## Options

| Where | What it changes |
|---|---|
| Preference `feedback/url` | The address of the form (set by the team when the form changes). |
| Environment variable `ROCKFACE_FEEDBACK_URL` | The same, for one computer or one session; it wins over the preference. |

## How it works

RockFace only opens the address of the form in the browser: nothing is sent by the program, and no file, project or
personal data leaves the computer. The text of **Help → Support…** (versions only) may be pasted into the form.

## From a script

```python
print(rf.feedback_url())          # the address of the form, or "" when it is not defined yet
rf.send_feedback("lab")           # opens the form in the browser; returns the address, or "" when not defined
```

From a terminal: `rockface feedback` prints the address of the form (or that it is not defined yet) and opens it.

## Limits and common problems

* "The feedback form is not defined yet." — the team has not set its address: use **Help → Support…**.
* Nothing opens: no browser is set as the default of the system; copy the address printed by `rockface feedback`.

## Coverage

O2 (the testers' feedback form in the programs, after 1.0 and the site).
