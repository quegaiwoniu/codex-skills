#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
SHANGHAI = ZoneInfo("Asia/Shanghai")


def load_token() -> str:
    auth_path = Path.home() / ".codex" / "auth.json"
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    token = data.get("tokens", {}).get("access_token")
    if not token:
        raise SystemExit("access_token not found in ~/.codex/auth.json")
    return token


def log_path() -> Path:
    path = Path.home() / ".codex" / "codex-pace" / "logs" / "anchor.log"
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def write_log(event: dict) -> None:
    event["ts_shanghai"] = datetime.now(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S CST")
    with log_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a sanitized Codex Pace authenticated ping.")
    parser.add_argument("--url", default=DEFAULT_URL, help="Authenticated endpoint to call")
    args = parser.parse_args()

    req = urllib.request.Request(args.url, headers={
        "Authorization": f"Bearer {load_token()}",
        "Accept": "application/json",
        "User-Agent": "codex-pace/1.0",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            write_log({"ok": True, "status": resp.status, "url_host": urllib.parse.urlparse(args.url).netloc})
            print(json.dumps({"ok": True, "status": resp.status, "log": str(log_path())}, ensure_ascii=False))
            return 0
    except urllib.error.HTTPError as exc:
        message = "401 Unauthorized: Codex credential expired or Authorization header was not accepted." if exc.code == 401 else f"HTTP {exc.code}"
        write_log({"ok": False, "status": exc.code, "message": message})
        print(json.dumps({"ok": False, "error": message, "log": str(log_path())}, ensure_ascii=False))
        return 1
    except Exception as exc:
        write_log({"ok": False, "message": type(exc).__name__})
        print(json.dumps({"ok": False, "error": type(exc).__name__, "log": str(log_path())}, ensure_ascii=False))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())


