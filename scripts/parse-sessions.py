#!/usr/bin/env python3

import json
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: parse-sessions.py <project-dir> [--skip id1,id2,...]", file=sys.stderr)
        sys.exit(1)

    project_dir = sys.argv[1]
    skip_ids = set()
    if "--skip" in sys.argv:
        idx = sys.argv.index("--skip")
        if idx + 1 < len(sys.argv):
            skip_ids = set(sys.argv[idx + 1].split(","))

    if not os.path.isdir(project_dir):
        print(f"Directory not found: {project_dir}", file=sys.stderr)
        sys.exit(1)

    files = sorted(f for f in os.listdir(project_dir) if f.endswith(".jsonl"))

    for filename in files:
        session_id = filename.removesuffix(".jsonl")
        if session_id in skip_ids:
            continue

        filepath = os.path.join(project_dir, filename)
        first_ts = None
        last_ts = None
        exchanges = []

        with open(filepath) as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                ts = d.get("timestamp")
                if ts:
                    if not first_ts:
                        first_ts = ts
                    last_ts = ts

                role = d.get("type")
                if role not in ("user", "assistant"):
                    continue

                content = d.get("message", {}).get("content")
                if not content:
                    continue

                if isinstance(content, list):
                    text = " ".join(
                        p.get("text", "")
                        for p in content
                        if isinstance(p, dict) and "text" in p
                    )
                else:
                    text = str(content)

                text = text.strip()
                if not text:
                    continue
                if text.startswith("<local-command-caveat>"):
                    continue
                if "<command-name>/exit</command-name>" in text:
                    continue

                label = "HUMAN" if role == "user" else "ASSISTANT"
                truncated = text[:1500] + "..." if len(text) > 1500 else text
                exchanges.append((label, truncated))

        if not exchanges:
            continue

        print(f"=== SESSION: {session_id} ===")
        print(f"TIMESTAMP_FIRST: {first_ts or 'unknown'}")
        print(f"TIMESTAMP_LAST: {last_ts or 'unknown'}")
        print(f"EXCHANGE_COUNT: {len(exchanges)}")
        print()

        for i, (label, text) in enumerate(exchanges, 1):
            print(f"[{i}] {label}:")
            print(text)
            print()


if __name__ == "__main__":
    main()
