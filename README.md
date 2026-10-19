# 讲义双语翻译 / Bilingual Lecture Translation

A portable Agent Skill for translating technical PDF lecture slides with visually checked equations and page-by-page comparison against the original slides.

面向 Codex、ZCode、MiniMax Code 和 Kimi Code CLI 的讲义翻译技能。默认翻译成简体中文，也可指定其他语言。

## 功能

- 提取 PDF 文本并渲染原始页面。
- 按页翻译，统一术语并核对公式、表格和图示标注。
- 导出双栏对照 PDF、内嵌图片的离线 HTML、Markdown 图片包。
- 支持并行子代理；没有子代理时串行处理。

翻译由加载技能的 Agent 完成，辅助脚本不调用模型 API。

## 安装

将本仓库下载或克隆到名为 `translate-lecture-bilingual` 的目录，保留所有子目录。

```bash
git clone https://github.com/laoshihaowoshiyangtongxue/translate-lecture-bilingual.git
```

安装到客户端的技能目录，例如 ZCode：

```bash
python translate-lecture-bilingual/scripts/install.py --skills-root ~/.zcode/skills
```

| 客户端 | 技能目录 | 调用 |
| --- | --- | --- |
| Codex | `~/.codex/skills/` | `$translate-lecture-bilingual` |
| ZCode | `~/.zcode/skills/` | 设置中刷新启用后输入 `$translate-lecture-bilingual` |
| MiniMax Code | 项目下 `.minimax/skills/` | `/skills` 检查并选择技能 |
| Kimi Code CLI | 项目下 `.agents/skills/` | `/skill:translate-lecture-bilingual` |

详细版本差异、依赖与调用方法见 [跨平台说明](references/compatibility.md)。安装脚本不会覆盖已有同名技能。

## 使用

附上讲义或提供可访问的 PDF 路径，告诉 Agent：

> 使用 translate-lecture-bilingual 将这份讲义翻译成中文，保留公式和图示，生成逐页对照 PDF、离线 HTML 和 Markdown 图片包。

流程入口：[SKILL.md](SKILL.md)。需要本地文件读写、命令执行及图片查看能力；普通网页聊天不一定能执行该流程。

## 依赖与验证

- Python 3.10+、PyMuPDF、Pandoc。
- PDF 导出另需 Node.js、Playwright 和可用的 Chromium/Chrome/Edge。
- Windows 本地测试覆盖 27 页提取与导出、安装覆盖保护及公式/表格页面检查。
- 未在所有客户端及操作系统分别运行真实模型进行端到端测试。

仓库仅包含通用技能与辅助代码，不包含用于测试的课程讲义或翻译成品。
