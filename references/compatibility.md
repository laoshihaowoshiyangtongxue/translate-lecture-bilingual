# 跨平台安装与调用

核对日期：2026-10-19。这里适配的是承载模型的 Agent 客户端；模型名称本身不决定是否能加载技能。需要读取本地文件、运行 Python/Node、查看原页图片的能力。没有图片查看能力时，可以生成译文草稿，但必须明确公式尚未视觉核对；没有执行环境时只能提供翻译内容，不能声称已生成 PDF。

## 安装整套目录

解压 ZIP 后保留 `translate-lecture-bilingual/SKILL.md`、`scripts/`、`assets/` 和 `references/` 的相对位置，不能只复制 SKILL.md。安装脚本只复制技能，不修改客户端配置、不调用模型、不安装依赖，也不覆盖已有同名目录。

### ZCode

用户目录为 `~/.zcode/skills/translate-lecture-bilingual/`。Windows PowerShell 在解压后的父目录执行：

```powershell
python .\translate-lecture-bilingual\scripts\install.py --skills-root "$env:USERPROFILE/.zcode/skills"
```

随后进入“设置 → 技能”刷新并启用；输入 `$translate-lecture-bilingual 翻译这份 PDF，输出中文对照版`。也可以使用 ZCode 的外部技能导入，从现有 Codex 技能中选中它，选择复制或软链。软链会跟随原目录更新。

官方依据：https://zcode.z.ai/cn/docs/skill

### MiniMax Code

优先使用官方代码文档确认的项目技能目录：`<项目>/.minimax/skills/translate-lecture-bilingual/`。在 MiniMax Code 将要打开的项目目录执行（把脚本路径改成解压位置）：

```powershell
python "D:/Downloads/translate-lecture-bilingual/scripts/install.py" --skills-root "$pwd/.minimax/skills"
```

重新打开该项目会话，用 `/skills translate-lecture-bilingual` 检查技能清单。选择对应技能命令，或直接要求“使用 translate-lecture-bilingual 翻译这份 PDF”。命令以客户端实际显示的名称为准。同名或被停用的外部来源可能被过滤。

此路径依据公开 MiniMax Code 仓库；独立桌面发行版的全局数据目录可能不同，不将 `.minimax-code` 安装目录猜作技能数据目录。桌面版若不显示项目技能，可让该客户端读取完整技能路径并按内容执行，或使用其自身技能管理界面导入。

官方依据：https://github.com/MiniMax-AI/minimax-code/blob/main/docs/tui-capabilities.md （Skill directory links / ACP Skill commands）

### Kimi Code CLI

使用两套官方资料均支持的项目目录 `<项目>/.agents/skills/translate-lecture-bilingual/`，在该项目根目录启动 Kimi：

```powershell
python "D:/Downloads/translate-lecture-bilingual/scripts/install.py" --skills-root "$pwd/.agents/skills"
```

在新会话中输入：

```text
/skill:translate-lecture-bilingual 翻译这份 PDF，输出中文对照版
```

不同版本的 Kimi 用户目录可能为 `.kimi`、`.kimi-code` 或共享目录。不要盲目选择某个版本的默认全局目录；项目目录或当前安装版本确认的自定义 skills 路径更清楚。项目发现可能以最近的 Git 根目录为边界，应在实际项目中安装；如果没有被发现，直接让 Agent 读取 SKILL.md，或查当前版本的 `kimi --help`。

官方依据：
- https://www.kimi.com/code/docs/en/kimi-code-cli/customization/skills.html
- https://github.com/MoonshotAI/kimi-cli/blob/main/docs/en/customization/skills.md

Kimi 网页聊天不是 Kimi Code CLI；仅上传此 ZIP 不保证网页端能注册或执行技能。

## 非 Codex 环境依赖

依赖与模型无关。复用已安装工具；下列命令是缺少依赖时的可选准备步骤，遵循宿主权限和用户要求。Python 建议 3.10+，Node 使用 Playwright 支持的版本。

```text
python -m pip install pymupdf
npm install --prefix <runtime-dir> playwright
```

Pandoc 使用系统安装或 `python -m pip install pypandoc_binary` 提供的可执行文件；构建器可通过 `--pandoc` 显式指定，否则从 PATH 查找。PyMuPDF 用于 PDF 提取和检查。

运行 `print_pdf.cjs` 时通过 `--playwright <runtime-dir>/node_modules/playwright` 指定包。使用已有 Chrome/Edge/Chromium 可传 `--browser <browser-executable>`；不传时使用 Playwright 已安装的 Chromium。只有用户同意下载浏览器时才运行相应 Playwright `install chromium` 命令。其他客户端无需 Codex dependency loader，也无需安装 Codex 的 PDF 技能。

## 通用调用提示

如果客户端尚未发现技能，可以直接发送：

> 请读取 `<完整路径>/translate-lecture-bilingual/SKILL.md`，按其中流程将 `<PDF路径>` 翻译成中文。所有辅助脚本相对于该 SKILL.md 所在目录查找。没有子代理时串行执行；先检查依赖。输出 PDF、离线 HTML 和 Markdown 图片包；必须核对公式及最终分页，报告没有完成的步骤。

## 验证边界

该包的脚本在 Windows 上使用本地 Python、Pandoc、Playwright/Chrome 测试。目录与命令参考上述官方资料；没有在三种客户端分别调用真实模型完成端到端翻译。加载技能成功、依赖就绪和模型翻译质量是三个不同的检查项。
