---
name: codex-pace
description: Help Chinese-speaking Codex users align Codex 5-hour usage/reset windows with one or more high-focus work periods. Use when the user asks to set up Codex 节奏助手, arrange Codex usage rhythm, schedule automatic authenticated ping tasks with Codex built-in automations, calculate trigger times from morning/afternoon/evening work windows, view rate-limit reset credits, or update/remove Codex Pace automations across macOS and Windows.
---

# Codex Pace

Codex Pace is the Chinese-friendly "Codex 节奏助手". It helps users align Codex usage windows with their real high-focus work periods by calculating one or more daily trigger times, installing a Codex built-in automation, and verifying reset credits without exposing credentials.

## Safety Rules

Never print or log `access_token`, `refresh_token`, cookies, authorization headers, or full account/user IDs.

Treat this as usage-window alignment, not quota bypassing. Do not claim it increases limits. Explain that OpenAI may change reset behavior, and that the user should verify the effect with credit data after setup.

Prefer Codex built-in automations over OS schedulers. Do not use Windows Task Scheduler, macOS launchd, cron, or other OS-specific schedulers unless Codex automation is unavailable and the user explicitly asks for an OS fallback.

Before installing, updating, pausing, or deleting an automation, summarize the automation name, trigger time or times, working directory, prompt purpose, and log path, then get user approval if the action was not explicitly requested.

## Workflow

1. Understand the user's high-focus windows.
   - Accept Chinese or English phrasing such as "上午9点到12点，下午2点到6点", "09:00-12:00 and 14:00-18:00", or "晚上8点到凌晨1点".
   - Convert each window to 24-hour local time in Asia/Shanghai unless the user says otherwise.

2. Calculate the suggested trigger rhythm.
   - For one window, run `scripts/plan_schedule.py --work-window HH:MM-HH:MM`.
   - For multiple windows, pass one `--work-window` per high-focus period, for example:
     `scripts/plan_schedule.py --work-window 09:00-12:00 --work-window 14:00-18:00`.
   - If the user gives desired reset points directly, use `--target-reset HH:MM` one or more times.
   - Prefer the script output over mental arithmetic, especially for cross-midnight windows.

3. Show the recommendation.
   - Explain whether the strategy is `single-trigger` or `multi-trigger-candidate`.
   - Mention the expected 5-hour cadence examples, but do not promise exact reset behavior.
   - If multiple triggers are suggested, explain that more than one daily ping can disturb the observed rhythm and should be confirmed deliberately.

4. Install or update the Codex built-in automation when requested.
   - Use Codex app's `automation_update` tool. If the tool is not already available, discover it with `tool_search` using a query like `automation_update`.
   - Create a `cron` automation named `Codex Pace Ping` for one trigger time, or `Codex Pace Ping HHMM` for multiple confirmed trigger times.
   - Use local execution in a stable cwd. Prefer the current workspace if the user is working in a repo; otherwise use a simple local projectless/default workspace if available.
   - The automation prompt should run `scripts/ping_codex.py` from this skill and report only sanitized success/failure. It must not print tokens, cookies, or full IDs.
   - Do not show raw RRULE strings to the user. Let the Codex automation tool store the schedule.

5. Verify credits.
   - Run `scripts/show_credits.py` to display `available_count` and each credit's `status`, `title`, `granted_at`, and `expires_at` in Shanghai time.
   - If 401 occurs, tell the user the Codex credential is expired or the Authorization header was not accepted.

## Scripts

- `scripts/plan_schedule.py`: calculate trigger time from one or more high-focus work windows or desired reset times.
- `scripts/show_credits.py`: read `~/.codex/auth.json`, call the reset-credit endpoint, and print only sanitized credit fields.
- `scripts/ping_codex.py`: read `~/.codex/auth.json`, make a lightweight authenticated request, and write sanitized logs.
- `scripts/install_windows_task.ps1`: legacy fallback only. Use it only when Codex automation is unavailable and the user explicitly asks for a Windows OS scheduler.

## Cross-Platform Notes

The Python scripts are cross-platform and use `Path.home()` for `~/.codex`. They work on macOS and Windows as long as the local Codex credentials are present.

Scheduling should be cross-platform through Codex built-in automations. OS schedulers are optional fallbacks, not the default path.

## Recommended User-Facing Language

Use "Codex 节奏助手" in Chinese explanations. Use `codex-pace` for commands, folders, and task internals.

Say: "把 Codex 的使用窗口对齐到你的高强度工作时段。"

Avoid saying: "刷额度", "绕过限制", or "无限重置".
