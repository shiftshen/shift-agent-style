# Shift Agent Style

让智能体记住 **怎样配合 Shift，以及哪些错误不要再犯**。

这是一份可直接读取、可作为 Agent Skill 安装的用户协作档案。重点是实际完成工作、真实验收、控制成本、保持项目方向，以及把纠正持久记录下来。它不是人格扮演，也不授予额外操作权限。

A portable collaboration profile for agents working with Shift. Read `SKILL.md` or import `SHIFT_AGENT_PREFERENCES.md`; current task instructions and host policies take precedence.

## 直接发给其他智能体

复制下面整段，加上你的任务即可：

```text
先读取 https://raw.githubusercontent.com/shiftshen/shift-agent-style/main/SKILL.md
这是我的长期协作偏好，请在本任务中实际遵守，尤其避免重复犯错：
只建议不执行、假报完成、偏离目标、重复确认已授权工作、乱建实现、浪费额度。
当前任务的明确要求、授权范围和禁止项优先。
如果你支持本地技能，请安装为 colleague-shift；已有同名技能先比较版本并保留本地修改。
如果你不支持技能安装，就把这份文件作为当前任务的用户偏好上下文。
不要把“安装了文件”说成所有会话已经生效，也不要反复复述规则消耗上下文。
现在完成这个任务：
【填写任务】
```

不能打开链接的智能体，可上传 [通用偏好文件](SHIFT_AGENT_PREFERENCES.md)。这是从技能正文生成的完整文本版，不依赖 Distilly、浏览器插件或付费服务。

## 最重要的规则

| 避免 | 改为 |
| --- | --- |
| 只给教程，反复问要不要继续 | 实际完成已授权工作，遇到局部阻塞继续独立部分 |
| 单测或接口成功就声称整个产品可用 | 在用户真实应用、页面、设备和会话中验收 |
| 越做越偏，新增大量细节拖住交付 | 核对原始目标，先交完整可用版本 |
| 用批量样片代替系统开发 | 打通真实功能、前端入口与业务流程 |
| 每个主题重新写一套、乱建目录 | 复用核心、组件和约定工作区，保留账号隔离 |
| 默认最贵模型、重复测试、高频空等 | 合格模型中控制成本，复用有效证据 |
| 页面没打开却让用户接手 | 核验真实浏览器、窗口、URL 和页面状态 |
| 说记住了却没有持久记录 | 把纠正合并进已有规则与共享状态 |

完整内容包含 **19 条规则**、条件边界与交付前自查，见 [SKILL.md](SKILL.md)。

## 本地技能安装

把本仓库克隆到宿主已确认的技能目录，文件夹名使用 `colleague-shift`。无需安装依赖或运行仓库脚本来使用技能。

例如本机 Codex 使用 `~/.codex/skills` 时：

```sh
git clone https://github.com/shiftshen/shift-agent-style.git "$HOME/.codex/skills/colleague-shift"
```

若目录已存在，先检查它的来源和未提交修改，不能直接覆盖。本仓库不会自动修改全局配置。安装后显式请求加载 `$colleague-shift`，或新建任务确认宿主发现了技能；其他宿主使用各自的技能发现方式，不假定它们都支持同一条命令。

- 技能入口：[SKILL.md](SKILL.md)
- 通用文本：[SHIFT_AGENT_PREFERENCES.md](SHIFT_AGENT_PREFERENCES.md)
- 整包下载：[GitHub ZIP](https://github.com/shiftshen/shift-agent-style/archive/refs/heads/main.zip)
- 规则审查案例：[EVALUATION.md](EVALUATION.md)

## 范围与更新

本版基于 2026-07-10 至 2026-09-26 本机可读取的 Codex 记录与用户显式规则，复核了 54 处原文锚点。并不覆盖所有账号、云端或已删除对话。公开仓库仅保留提炼规则，不含原始聊天、来源定位、密钥或内部业务配置。

新纠正按“场景 → 错误 → 正确做法 → 例外 → 日期”合并到原规则。当前任务指令优先；历史“全权负责”不构成新任务权限。模型名称、服务器地址、项目时段和一次性验收阈值不作为长期偏好。

这里的静态检查验证文件结构、文本同步和常见隐私泄露模式；[审查案例](EVALUATION.md)是行为验收标准，不代表其他智能体已实际跑过。不能保证任意模型永不犯错，也不能宣称所有运行中的会话已加载。

维护本仓库时：

```sh
python3 scripts/check.py --sync
python3 scripts/check.py
```

`--sync` 只从 `SKILL.md` 生成通用文本，不改宿主设置、不读取聊天记录、不联网。GitHub Actions 对每次推送检查同一组规则。

## 来源与许可

使用 [Distilly](https://github.com/titanwings/distilly) 的 Work / Persona / Correction 方法完成初稿，再针对执行助手用途精简与适配。使用本档案不需要安装 Distilly。

MIT 许可，见 [LICENSE](LICENSE)。未经当前任务授权，不把历史信息用作外发、付款或生产修改许可。
