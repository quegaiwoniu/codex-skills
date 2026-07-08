#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass

DAY = 24 * 60
WINDOW_HOURS = 5
STEP = WINDOW_HOURS * 60

@dataclass(frozen=True)
class TimeOfDay:
    minutes: int

    @classmethod
    def parse(cls, value: str) -> "TimeOfDay":
        value = value.strip()
        if ":" not in value:
            raise SystemExit(f"Invalid time '{value}'. Use HH:MM, e.g. 14:00.")
        hour_s, minute_s = value.split(":", 1)
        hour = int(hour_s)
        minute = int(minute_s)
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise SystemExit(f"Invalid time '{value}'. Use 00:00 through 23:59.")
        return cls(hour * 60 + minute)

@dataclass(frozen=True)
class Window:
    start: int
    end: int
    label: str

    @classmethod
    def parse(cls, value: str) -> "Window":
        if "-" not in value:
            raise SystemExit(f"Invalid work window '{value}'. Use HH:MM-HH:MM.")
        start_s, end_s = value.split("-", 1)
        start = TimeOfDay.parse(start_s).minutes
        end = TimeOfDay.parse(end_s).minutes
        return cls(start, end, f"{minutes_to_label(start)}-{minutes_to_label(end)}")

    def normalized_end(self) -> int:
        return self.end + (DAY if self.end <= self.start else 0)

    def midpoint(self) -> int:
        return (self.start + self.normalized_end()) // 2

    def contains_mod(self, minutes: int) -> bool:
        start = self.start
        end = self.end
        m = minutes % DAY
        if end > start:
            return start <= m <= end
        return m >= start or m <= end


def minutes_to_label(minutes: int) -> str:
    minutes %= DAY
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def parse_range(value: str) -> tuple[int, int]:
    if "-" not in value:
        raise SystemExit(f"Invalid trigger range '{value}'. Use HH:MM-HH:MM.")
    start_s, end_s = value.split("-", 1)
    return TimeOfDay.parse(start_s).minutes, TimeOfDay.parse(end_s).minutes


def in_range(minutes: int, start: int, end: int) -> bool:
    m = minutes % DAY
    if end >= start:
        return start <= m <= end
    return m >= start or m <= end


def cadence(trigger: int, count: int = 5) -> list[int]:
    return [(trigger + STEP * n) % DAY for n in range(count)]


def target_resets_from_windows(windows: list[Window]) -> list[int]:
    return [w.midpoint() % DAY for w in windows]


def score_trigger(trigger: int, targets: list[int], windows: list[Window]) -> tuple[int, int, int]:
    resets = cadence(trigger, 6)
    covered_targets = 0
    covered_windows = 0
    total_distance = 0

    for target in targets:
        distances = [min((r - target) % DAY, (target - r) % DAY) for r in resets]
        best = min(distances)
        total_distance += best
        if best <= 45:
            covered_targets += 1

    for window in windows:
        if any(window.contains_mod(r) for r in resets):
            covered_windows += 1

    return covered_targets + covered_windows, -total_distance, -trigger


def choose_single_trigger(targets: list[int], windows: list[Window], preferred_start: int, preferred_end: int) -> tuple[int, tuple[int, int, int]]:
    candidates: set[int] = set()
    for target in targets:
        for n in range(1, 7):
            c = (target - STEP * n) % DAY
            if in_range(c, preferred_start, preferred_end):
                candidates.add(c)

    if not candidates:
        for target in targets:
            candidates.add((target - STEP) % DAY)

    ranked = sorted((score_trigger(c, targets, windows), c) for c in candidates)
    best_score, best = ranked[-1]
    return best, best_score


def multi_trigger_candidates(targets: list[int], preferred_start: int, preferred_end: int) -> list[int]:
    out: list[int] = []
    for target in targets:
        candidates = [(target - STEP * n) % DAY for n in range(1, 7)]
        preferred = [c for c in candidates if in_range(c, preferred_start, preferred_end)]
        chosen = min(preferred) if preferred else candidates[0]
        if chosen not in out:
            out.append(chosen)
    return sorted(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan Codex Pace daily trigger times.")
    parser.add_argument("--work-window", action="append", default=[], help="High-focus work window, HH:MM-HH:MM. Repeat for multiple windows.")
    parser.add_argument("--work-start", help="Legacy: high-focus work start time, HH:MM")
    parser.add_argument("--work-end", help="Legacy: high-focus work end time, HH:MM")
    parser.add_argument("--target-reset", action="append", default=[], help="Desired reset time, HH:MM. Repeat for multiple reset points.")
    parser.add_argument("--preferred-trigger-range", default="05:00-12:00", help="Preferred trigger range, HH:MM-HH:MM")
    args = parser.parse_args()

    windows = [Window.parse(w) for w in args.work_window]
    if args.work_start or args.work_end:
        if not args.work_start or not args.work_end:
            raise SystemExit("Provide both --work-start and --work-end, or use --work-window.")
        windows.append(Window.parse(f"{args.work_start}-{args.work_end}"))

    targets = [TimeOfDay.parse(t).minutes for t in args.target_reset]
    source = "target-reset" if targets else "work-window-midpoint"
    if not targets:
        if not windows:
            raise SystemExit("Provide --work-window, legacy --work-start/--work-end, or --target-reset.")
        targets = target_resets_from_windows(windows)

    preferred_start, preferred_end = parse_range(args.preferred_trigger_range)
    trigger, best_score = choose_single_trigger(targets, windows, preferred_start, preferred_end)
    resets = cadence(trigger, 5)
    covered_windows = [w.label for w in windows if any(w.contains_mod(r) for r in resets)]
    all_windows_covered = len(covered_windows) == len(windows) if windows else True
    target_hits = sum(1 for t in targets if min(min((r - t) % DAY, (t - r) % DAY) for r in resets) <= 45)

    notes: list[str] = []
    strategy = "single-trigger"
    multi = []
    if windows:
        needs_multi = not all_windows_covered
    else:
        needs_multi = target_hits < len(targets)

    if needs_multi:
        strategy = "multi-trigger-candidate"
        multi = multi_trigger_candidates(targets, preferred_start, preferred_end)
        notes.append("A single trigger does not closely cover every high-focus window; confirm deliberately before installing multiple automations.")

    result = {
        "strategy": strategy,
        "source": source,
        "work_windows": [w.label for w in windows],
        "target_reset_times": [minutes_to_label(t) for t in targets],
        "daily_trigger_time": minutes_to_label(trigger),
        "daily_trigger_times": [minutes_to_label(t) for t in multi] if multi else [minutes_to_label(trigger)],
        "covered_windows": covered_windows,
        "expected_cadence_examples": [minutes_to_label(r) for r in resets],
        "timezone": "Asia/Shanghai",
        "notes": notes,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

