#!/usr/bin/env python3
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

URL = "https://chatgpt.com/backend-api/wham/rate-limit-reset-credits"
SHANGHAI = ZoneInfo("Asia/Shanghai")


def load_token() -> str:
    auth_path = Path.home() / ".codex" / "auth.json"
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    token = data.get("tokens", {}).get("access_token")
    if not token:
        raise SystemExit("access_token not found in ~/.codex/auth.json")
    return token


def to_shanghai(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(SHANGHAI).strftime("%Y-%m-%d %H:%M:%S CST")
    except Exception:
        return value


def main() -> int:
    req = urllib.request.Request(URL, headers={
        "Authorization": f"Bearer {load_token()}",
        "Accept": "application/json",
        "User-Agent": "codex-pace/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as exc:
        if exc.code == 401:
            print(json.dumps({"error": "401 Unauthorized: Codex credential expired or Authorization header was not accepted."}, ensure_ascii=False))
            return 1
        print(json.dumps({"error": f"HTTP {exc.code}"}, ensure_ascii=False))
        return 1

    credits = payload.get("credits") or payload.get("items") or payload.get("data") or []
    result = {
        "available_count": payload.get("available_count"),
        "credits": [
            {
                "status": c.get("status"),
                "title": c.get("title"),
                "granted_at_shanghai": to_shanghai(c.get("granted_at")),
                "expires_at_shanghai": to_shanghai(c.get("expires_at")),
            }
            for c in credits
        ],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
