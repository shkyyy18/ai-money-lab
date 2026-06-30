# 实验 001 · AI 简历优化器

> 贴旧简历 + 目标 JD → AI 输出 ATS 友好、量化成果、关键词匹配的重写版。
> 单文件 Flask MVP，实测中。过程/数据/结论见 [result.md](./result.md)，假说与 9 块拆解见 [Lean Canvas](./lean_canvas.md)。

## 跑起来（本地，3 步）

```bash
pip install -r requirements.txt
# 设置智谱 GLM API Key（去 open.bigmodel.cn 申请，有免费额度）
set ZHIPU_API_KEY=你的key        # Windows
# export ZHIPU_API_KEY=你的key   # macOS / Linux
python app.py
```

浏览器打开 http://localhost:5011 ，贴简历 + JD → 点「AI 优化简历」。

## 它在测什么

**一个假说**：不买量、只靠 GitHub 自然流量，能不能拿到第一笔 ¥9.9？

- `/optimize` 调 GLM-4-flash 出改写 + ATS 关键词评分 —— 交付价值
- 页面底部「¥9.9 解锁导出」是 **fake-door**：点击只记 `events.jsonl`（转化信号），**不真收费**
- 转化信号 = `fake_door` 次数 ÷ `optimize` 次数。>3% 才接真支付，否则归失败（见 methodology）

## 文件

| 文件 | 作用 |
|---|---|
| `app.py` | Flask 单文件 MVP（页面 + /optimize + /fake-door） |
| `lean_canvas.md` | 9 块商业假设（过第一性原理门后填） |
| `result.md` | 实测过程 / 真实数据 / 结论 / 坑 |
| `events.jsonl` | 事件日志（本地，已 gitignore） |
| `requirements.txt` | flask + requests |

## 代码公开 / 复刻指南付费

MVP 代码 build-in-public（本目录）。**完整复刻指南**（部署 + 导流 + 调优 + 变现细节）只在**实测净利 > 0** 后开放付费版（守 [methodology](../../methodology.md) 付费层原则）。

---
_ai-money-lab · 每周实测 1 个 AI 变现项目，失败也发。_
