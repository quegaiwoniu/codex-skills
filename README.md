# codex-skills

Reusable Codex skills for global users. This repository stores skills under `skills/<skill-name>/` so they can be installed individually and shared with others.

面向全球用户的 Codex skills 集合。这个仓库按 `skills/<skill-name>/` 存放可复用 skill，方便单独安装、分享和持续扩展。

## Skills

### Codex 节奏助手 / Codex Pace (`codex-pace`)

Align Codex usage windows with your high-focus work periods. It can calculate suggested trigger times from one or more peak work windows and use Codex built-in automations to run a lightweight authenticated ping.

把 Codex 的使用窗口对齐到你的高强度工作时段。它可以根据一个或多个工作高峰期计算建议触发时间，并通过 Codex 内置 automation 定时执行轻量 authenticated ping。

Good for:

- Users with morning and afternoon Codex work peaks
- Users who want 5-hour usage windows to better match their daily rhythm
- Users who want to inspect reset credit counts and expiration times
- Users who prefer Codex built-in automations instead of OS schedulers

适合这些场景：

- 上午和下午都有 Codex 使用高峰
- 想让 5 小时使用窗口更贴近自己的工作节奏
- 想查看 reset credits 的可用次数和过期时间
- 想用 Codex 自带 automation，而不是系统定时任务

## Install

Install a single skill from GitHub with `npx skills`:

```powershell
npx skills add https://github.com/quegaiwoniu/codex-skills --skill codex-pace --yes --global
```

用 `npx skills` 从 GitHub 安装单个 skill：

```powershell
npx skills add https://github.com/quegaiwoniu/codex-skills --skill codex-pace --yes --global
```

Manual install on Windows:

```powershell
Copy-Item -Recurse .\skills\codex-pace $HOME\.codex\skills\codex-pace -Force
```

Windows 手动安装：

```powershell
Copy-Item -Recurse .\skills\codex-pace $HOME\.codex\skills\codex-pace -Force
```

Manual install on macOS/Linux:

```bash
cp -R skills/codex-pace ~/.codex/skills/codex-pace
```

macOS/Linux 手动安装：

```bash
cp -R skills/codex-pace ~/.codex/skills/codex-pace
```

Restart Codex or open a new session after installation.

安装后重启 Codex 或新开会话。

## Usage

Example prompt:

```text
Use codex-pace to plan my Codex rhythm for 09:00-12:00 and 14:00-18:00.
```

中文示例：

```text
用 codex-pace 帮我安排上午 9 点到 12 点、下午 2 点到 6 点的 Codex 使用节奏
```

You can also run the planner directly:

```powershell
python $HOME\.codex\skills\codex-pace\scripts\plan_schedule.py --work-window 09:00-12:00 --work-window 14:00-18:00
```

也可以直接运行计算脚本：

```powershell
python $HOME\.codex\skills\codex-pace\scripts\plan_schedule.py --work-window 09:00-12:00 --work-window 14:00-18:00
```

The output includes:

- Suggested trigger time
- Target reset times
- Covered work windows
- Example 5-hour cadence

示例输出会包含：

- 推荐触发时间
- 目标刷新时间
- 覆盖到的高峰期
- 预期 5 小时节奏示例

## Safety

Skills in this repository should never print or log `access_token`, `refresh_token`, cookies, Authorization headers, or full unique IDs.

这个仓库里的 skills 不应打印或记录 `access_token`、`refresh_token`、cookie、Authorization header 或完整唯一 ID。

`codex-pace` is for aligning usage windows, not increasing limits or bypassing restrictions. OpenAI behavior may change, so verify the actual effect with `show_credits.py` or the Codex UI.

`codex-pace` 的定位是对齐使用窗口，不是提升额度或绕过限制。OpenAI 的内部策略可能变化，请用 `show_credits.py` 或 Codex 界面验证实际效果。

## Add New Skills

Put each new skill here:

```text
skills/<skill-name>/
```

新增 skill 时请放在：

```text
skills/<skill-name>/
```

Each skill should include at least:

```text
SKILL.md
agents/openai.yaml
```

每个 skill 至少包含：

```text
SKILL.md
agents/openai.yaml
```

Put deterministic helper code under `scripts/`. Do not commit caches, tokens, logs, local config, or credentials.

如果需要确定性脚本，请放在 `scripts/` 下。不要提交缓存、token、日志、本机配置或凭证。
