# codex-skills

<p align="center">
  <strong>English</strong>
  &nbsp;|&nbsp;
  <a href="README.zh-CN.md"><strong>中文</strong></a>
</p>

Reusable Codex skills for global users. This repository stores skills under `skills/<skill-name>/` so they can be installed individually and shared with others.

## Skills

### Codex Pace (`codex-pace`)

Align Codex usage windows with your high-focus work periods. It can calculate suggested trigger times from one or more peak work windows and use Codex built-in automations to run a lightweight authenticated ping.

Good for:

- Users with morning and afternoon Codex work peaks
- Users who want 5-hour usage windows to better match their daily rhythm
- Users who want to inspect reset credit counts and expiration times
- Users who prefer Codex built-in automations instead of OS schedulers

## Install

Install a single skill from GitHub with `npx skills`:

```powershell
npx skills add https://github.com/quegaiwoniu/codex-skills --skill codex-pace --yes --global
```

Manual install on Windows:

```powershell
Copy-Item -Recurse .\skills\codex-pace $HOME\.codex\skills\codex-pace -Force
```

Manual install on macOS/Linux:

```bash
cp -R skills/codex-pace ~/.codex/skills/codex-pace
```

Restart Codex or open a new session after installation.

## Usage

Example prompt:

```text
Use codex-pace to plan my Codex rhythm for 09:00-12:00 and 14:00-18:00.
```

You can also run the planner directly:

```powershell
python $HOME\.codex\skills\codex-pace\scripts\plan_schedule.py --work-window 09:00-12:00 --work-window 14:00-18:00
```

The output includes:

- Suggested trigger time
- Target reset times
- Covered work windows
- Example 5-hour cadence

## Safety

Skills in this repository should never print or log `access_token`, `refresh_token`, cookies, Authorization headers, or full unique IDs.

`codex-pace` is for aligning usage windows, not increasing limits or bypassing restrictions. OpenAI behavior may change, so verify the actual effect with `show_credits.py` or the Codex UI.

## Add New Skills

Put each new skill here:

```text
skills/<skill-name>/
```

Each skill should include at least:

```text
SKILL.md
agents/openai.yaml
```

Put deterministic helper code under `scripts/`. Do not commit caches, tokens, logs, local config, or credentials.
