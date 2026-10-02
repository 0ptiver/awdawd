#!/usr/bin/env python3
"""Generate small-business ideas with Claude and post them to a Discord forum.

Each idea becomes its own forum thread (webhook `thread_name`).

Environment:
  ANTHROPIC_API_KEY     required unless --dry-run with --from-file
  DISCORD_WEBHOOK_URL   required unless --dry-run
  IDEAS_MODEL           optional, default claude-sonnet-5-5

Usage:
  python ideas.py --dry-run          # generate and print, don't post
  python ideas.py -n 3               # generate 3 ideas and post them
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
CRITERIA_FILE = HERE / "criteria.md"
HISTORY_FILE = HERE / "posted.json"
DEFAULT_MODEL = "claude-sonnet-5-5"

FIELDS = [
    "title",
    "pitch",
    "problem",
    "who_pays",
    "how_it_makes_money",
    "how_to_start",
    "difficulty",
    "competition",
    "first_10_customers",
    "risks",
]

SYSTEM = """You are a sharp, practical startup-idea generator for a small Discord \
community of builders. Follow the criteria document exactly. Prefer specific \
niches over generic categories, and be honest about competition and risks. \
Never repeat or lightly reword a previously posted idea."""


def load_history() -> list[str]:
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []


def save_history(titles: list[str]) -> None:
    HISTORY_FILE.write_text(json.dumps(titles, indent=2) + "\n")


def build_prompt(n: int, history: list[str]) -> str:
    criteria = CRITERIA_FILE.read_text()
    previous = "\n".join(f"- {t}" for t in history[-100:]) or "- (none yet)"
    return f"""{criteria}

## Already posted (do NOT repeat these or close variants)
{previous}

## Task
Generate {n} new business ideas that fit the criteria above.

Return ONLY a JSON array of {n} objects, no prose, no code fences. Each object \
must have exactly these string keys:
- title: short and catchy, under 80 characters
- pitch: one sentence
- problem: the annoying/big problem it solves and for whom
- who_pays: the specific customer
- how_it_makes_money: pricing model with a rough price point
- how_to_start: the concrete first 3 steps to launch a version 1
- difficulty: Easy, Medium, or Hard, with a few words why
- competition: who else exists and why a newcomer can still win
- first_10_customers: how to land the first 10 paying customers
- risks: the main reason this could fail
"""


def generate(n: int, history: list[str]) -> list[dict]:
    try:
        import anthropic
    except ImportError:
        sys.exit("Missing dependency: pip install -r requirements.txt")

    client = anthropic.Anthropic()
    resp = client.messages.create(
        model=os.environ.get("IDEAS_MODEL", DEFAULT_MODEL),
        max_tokens=4000,
        system=SYSTEM,
        messages=[{"role": "user", "content": build_prompt(n, history)}],
    )
    text = "".join(b.text for b in resp.content if b.type == "text")
    return parse_ideas(text)


def parse_ideas(text: str) -> list[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    ideas = json.loads(text)
    if not isinstance(ideas, list):
        raise ValueError("Expected a JSON array of ideas")
    return [i for i in ideas if all(k in i for k in FIELDS)]


def clip(s: str, limit: int) -> str:
    return s if len(s) <= limit else s[: limit - 1] + "…"


def to_payload(idea: dict) -> dict:
    """Discord forum webhook payload: thread_name + one embed."""
    field = lambda name, key: {  # noqa: E731
        "name": name,
        "value": clip(str(idea[key]), 1024),
        "inline": False,
    }
    return {
        "thread_name": clip(idea["title"], 100),
        "embeds": [
            {
                "title": clip(idea["title"], 256),
                "description": clip(idea["pitch"], 4096),
                "color": 0x5865F2,
                "fields": [
                    field("Problem", "problem"),
                    field("Who pays", "who_pays"),
                    field("Makes money by", "how_it_makes_money"),
                    field("How to start", "how_to_start"),
                    field("Difficulty", "difficulty"),
                    field("Competition", "competition"),
                    field("First 10 customers", "first_10_customers"),
                    field("Risks", "risks"),
                ],
            }
        ],
    }


def post(webhook: str, payload: dict) -> None:
    req = urllib.request.Request(
        webhook + ("&" if "?" in webhook else "?") + "wait=true",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "idea-bot/1.0"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=30).read()
    except urllib.error.HTTPError as e:
        sys.exit(f"Discord rejected the post ({e.code}): {e.read().decode()[:300]}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-n", type=int, default=3, help="ideas to generate (default 3)")
    ap.add_argument("--dry-run", action="store_true", help="print, don't post")
    ap.add_argument("--from-file", help="read ideas JSON from file (skips Claude)")
    args = ap.parse_args()

    history = load_history()
    if args.from_file:
        ideas = parse_ideas(Path(args.from_file).read_text())
    else:
        ideas = generate(args.n, history)

    if not ideas:
        sys.exit("No valid ideas returned.")

    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not args.dry_run and not webhook:
        sys.exit("Set DISCORD_WEBHOOK_URL (or use --dry-run).")

    for idea in ideas:
        payload = to_payload(idea)
        if args.dry_run:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
            continue
        post(webhook, payload)
        history.append(idea["title"])
        save_history(history)
        print(f"Posted: {idea['title']}")


if __name__ == "__main__":
    main()
