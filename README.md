# Shift Agent Style

让智能体记住 **怎样配合 Shift，以及哪些错误不要再犯**。

这是一份可安装的 Agent Skill / 可粘贴的协作档案：六条协作硬规则、冲突裁决顺序、交付回执要求。它不是人格扮演，也不授予额外操作权限；当前任务指令与宿主策略永远优先。

A portable collaboration profile for agents working with Shift: six hard rules, a conflict-resolution order, and a mandatory delivery receipt. Current task instructions and host policies take precedence.

## 给其他智能体使用（按宿主能力三选一）

**① 宿主支持技能安装（首选）**：把本仓库克隆到宿主的技能目录，目录名用 `colleague-shift`，然后按宿主方式加载，例如 Codex：

```sh
git clone https://github.com/shiftshen/shift-agent-style.git "$HOME/.codex/skills/colleague-shift"
```

若目录已存在，先检查来源和未提交修改，不要直接覆盖。

**② 宿主不支持技能（通用）**：把 [SHIFT_AGENT_PREFERENCES.md](SHIFT_AGENT_PREFERENCES.md) **全文复制**，连同下面这句一起粘贴进对话：

```text
上面是我的长期协作档案，请作为本任务的用户偏好实际遵守，尤其遵守冲突裁决顺序与交付回执要求。
当前任务的明确要求、授权范围和禁止项优先。
现在完成这个任务：【填写任务】
```

**③ 都无法复制时**才发 raw 文件链接让智能体自行下载。注意：链接内容以远端当前版本为准，可能被更新；不要把"每轮抓一个 URL"当作长期加载方式，能用文件就用文件。

无论哪种方式，都不要相信智能体"读了就会永远遵守"——用本仓库的验收案例抽查行为，见 [EVALUATION.md](EVALUATION.md)。

## 六条硬规则

| 规则 | 要求 |
| --- | --- |
| H1 直接完成 | 信息足够就做完实现+验证+交付，不把能自查的信息甩回给用户 |
| H2 真实验收 | 在用户实际入口/环境/版本走通；没验证过的不能声称完成 |
| H3 交付回执 | 完成类回复固定附「结果 / 入口 / 验证证据 / 未验证与剩余」 |
| H4 复用不重复 | 复用代码、工作区和已有证据；不乱建第二套实现 |
| H5 环境如实 | 报告对应真实浏览器/设备/模型；用户接管即停 |
| H6 纠正落地 | 可复用的纠正按固定格式合并进规则；一次性指令不扩成红线 |

规则冲突时按裁决顺序：**本轮明确指令 > 禁止项 > 验收真实 > 效率成本**。完整文本见 [SKILL.md](SKILL.md)。

## 交付回执门禁

[scripts/delivery_check.py](scripts/delivery_check.py) 校验回执格式：四项齐全、声称完成时必须带可复核证据（命令、输出、截图、链接、版本至少其一），否则判未交付。支持脚本的宿主在交付前运行：

```sh
python3 scripts/delivery_check.py 回执文件.md
python3 scripts/delivery_check.py --selftest   # 内置用例自检
```

它只保证"完成声明附带证据"这一格式，不证明工作本身正确——后者仍靠测试与抽查。

## 范围与诚实声明

本版基于 2026-07-10 至 2026-09-26 本机可读取的 Codex 记录与用户显式规则提炼，不覆盖所有账号、云端或已删除对话。公开仓库仅含提炼规则，不含原始聊天、密钥或内部配置。

静态 CI（[check.py](scripts/check.py)）只验证文件结构、文本同步与隐私泄露模式；[EVALUATION.md](EVALUATION.md) 是行为验收标准。没有任何提示词文件能保证模型永不犯错——能被工具保证的事应交给工具，规则文本只承载工具管不了的部分。

## 维护

```sh
python3 scripts/check.py --sync    # 从 SKILL.md 重新生成通用文本
python3 scripts/check.py           # 结构与隐私检查（CI 同样运行）
python3 scripts/delivery_check.py --selftest
```

新增纠正按"场景 → 错误 → 应做 → 例外 → 日期"合并；硬规则上限 8 条，被机械门禁覆盖或 90 天未触发的规则退役。

## 来源与许可

初稿用 [Distilly](https://github.com/titanwings/distilly) 的 Work / Persona / Correction 方法生成，后按执行助手用途精简为硬规则版。使用本档案不需要安装 Distilly。

MIT 许可，见 [LICENSE](LICENSE)。未经当前任务授权，不把历史信息用作外发、付款或生产修改许可。
