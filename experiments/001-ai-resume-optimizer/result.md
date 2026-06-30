# 实验 001: AI 简历优化器 — 上传旧简历+JD，一键输出 ATS 友好的量化重写版

> 状态：🔄 **进行中**（Lean Canvas 已填，**MVP 已建并端到端验证 2026-06-30**）。启动日：2026-06-30。

## 假说
- 来源：ideas/2026-06-25 #1（首选）+ [Lean Canvas](./lean_canvas.md)。
- 声称：单功能 AI 简历优化器可达月入（参考 ezindie weekly #89「AI 小工具 2 个月 $7.3 万」）。
- **本实验只验一件事**：在不投流/不买量前提下，能否靠自然内容流量拿到第一笔真实 ¥9.9 转化。拿到=✅；拿不到=❌（即使技术上做出来了）。

## 投入（实测中累积，不编）
- 时间：MVP 2-3 天（Claude Code 辅助）+ 导流内容若干天（待记）
- 成本：~$10 API + ~$10 域名（待记实际）
- 技能：前端基础 + prompt 工程（Claude Code 辅助）

## 过程（Day-by-Day，按实记录）
- [x] **Day 1 — MVP 骨架（2026-06-30 完成）**：Flask 单文件 `app.py`（非 Next.js，今天就能跑）— 旧简历+JD → GLM 改写+ATS 评分 + fake-door「¥9.9 解锁导出」按钮 + events.jsonl 双事件日志。**端到端验证通过**：GLM 真实产出 519 字量化重写（"支付成功率 98.5%/提升 30%"等 STAR 指标），optimize + fake_door 均入日志。服务跑在本机 `http://localhost:5011`（`python app.py` 启动）。
- [ ] **Day 2 — 增强+部署**：ATS 关键词评分独立展示 + 部署公网（Vercel/Railway，需用户账号）+ 域名绑定
- [ ] **Day 3 — 导流**：知乎/小红书发 2-3 篇「简历优化」长尾内容，带工具链接
- [ ] **Day 4-N**：观察 events.jsonl 的 optimize→fake_door 转化率；>3% 接真支付（爱发电），<3% 归失败

## 结果（待真实数据 + 截图，不编不夸）
- 收入：$0（待）
- 访问（optimize 次数）：3（Day1 自测，见 events.jsonl）
- fake-door 点击：1（Day1 自测）
- fake-door 转化率：—（真实流量后统计）
- 净利：—

## 结论
🔄 进行中。可复刻性待评（⭐ 待）。

## 坑（实测中记录）
1. （待）

## 复刻指南（净利>0 后开付费完整版；此处仅预览）
- 选品：首选低 Effort + 付费意愿已被人工市场验证的品类
- MVP：先 fake-door 测转化，再接支付
- 引流：长尾内容截流，不买量

---
_下一个动作：MVP 代码已 **build-in-public**（独立可跑：`pip install -r requirements.txt` + `ZHIPU_API_KEY` + `python app.py` → localhost:5011，3 步）。用户拿这个 MVP 去其他平台拆解做内容；Claude 这边等 star/转化信号决定 Day 2（部署公网 + 接真支付）。_
