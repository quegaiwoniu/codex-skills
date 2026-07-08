# codex-skills

面向中文用户的 Codex skills 集合。这个仓库用于存放可复用的 Codex skills，后续新增 skill 请放在 `skills/<skill-name>/` 下。

## Skills

### Codex 节奏助手 (`codex-pace`)

把 Codex 的使用窗口对齐到你的高强度工作时段。它可以根据一个或多个工作高峰期计算建议触发时间，并通过 Codex 内置 automation 定时执行轻量 authenticated ping。

适合这些场景：

- 上午和下午都有 Codex 使用高峰
- 想让 5 小时使用窗口更贴近自己的工作节奏
- 想查看 reset credits 的可用次数和过期时间
- 想用 Codex 自带 automation，而不是系统定时任务

## 安装

推荐用 `npx skills` 从 GitHub 安装单个 skill：

```powershell
npx skills add https://github.com/quegaiwoniu/codex-skills --skill codex-pace --yes --global
```

如果你手动安装，可以复制目录：

```powershell
Copy-Item -Recurse .\skills\codex-pace $HOME\.codex\skills\codex-pace -Force
```

macOS/Linux 手动安装：

```bash
cp -R skills/codex-pace ~/.codex/skills/codex-pace
```

安装后重启 Codex 或新开会话。

## 使用示例

```text
用 codex-pace 帮我安排上午 9 点到 12 点、下午 2 点到 6 点的 Codex 使用节奏
```

也可以直接运行计算脚本：

```powershell
python $HOME\.codex\skills\codex-pace\scripts\plan_schedule.py --work-window 09:00-12:00 --work-window 14:00-18:00
```

示例输出会包含：

- 推荐触发时间
- 目标刷新时间
- 覆盖到的高峰期
- 预期 5 小时节奏示例

## 安全说明

这些 skills 不应打印或记录 `access_token`、`refresh_token`、cookie、Authorization header 或完整唯一 ID。

`codex-pace` 的定位是对齐使用窗口，不是提升额度或绕过限制。OpenAI 的内部策略可能变化，请用 `show_credits.py` 或 Codex 界面验证实际效果。

## 贡献新 skill

新增 skill 时请放在：

```text
skills/<skill-name>/
```

每个 skill 至少包含：

```text
SKILL.md
agents/openai.yaml
```

如果需要确定性脚本，请放在 `scripts/` 下。不要提交缓存、token、日志或本机配置。

