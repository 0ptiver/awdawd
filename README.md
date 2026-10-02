# Business idea bot

Generates small-business ideas with Claude and posts each one as a thread in a
Discord forum channel via webhook.

## Setup

```sh
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
export DISCORD_WEBHOOK_URL=...   # webhook of the forum channel
```

Never commit the webhook URL — anyone with it can post to your server. Keep it
in an env var or a git-ignored `.env`.

## Run

```sh
python ideas.py --dry-run   # preview, nothing is posted
python ideas.py -n 3        # generate and post 3 ideas
```

Posted titles are saved in `posted.json` and fed back to Claude so it doesn't
repeat itself.

## Tuning

Edit `criteria.md` — it defines what a good idea is, what to avoid, and holds a
Feedback section. It is re-read on every run. Workflow: dry-run, tell Claude
what was good/bad, add that to the Feedback section, repeat until the ideas are
right, then post for real.
