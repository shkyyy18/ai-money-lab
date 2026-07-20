# AGENTS.md — ai-money-lab

## 项目定位

AI 商业实验的"证据账本"：每个实验用机器可读的 `experiment.json` 记录状态/收入/证据等级，用离线校验器（`lab.py`）强制"证据等级不可凭叙事升级"，失败与无结论的实验也公开留痕，杜绝虚假成功故事。

## 技术栈

- Python，**仅标准库**（argparse/json/unittest/pathlib）；无 pyproject.toml，不是可安装包，克隆即用
- 测试：unittest（`tests/test_lab.py`，9 个用例）；**无 lint/format 配置**
- 实验 001 的历史 MVP（`experiments/001-ai-resume-optimizer/app.py`）单独依赖 flask/requests 和 `ZHIPU_API_KEY`，但不参与账本校验

## 常用命令

```bash
python lab.py validate
python lab.py summary
python lab.py leaderboard      # 重新生成 leaderboard.md 并同步 README 徽章
python -m unittest discover -s tests -v
python -m compileall -q lab.py tests
```

## 本仓库 agent 的搜索范围与要求

- 只允许改动本仓库；本仓库的核心资产是**证据的可信度**，任何改动不得弱化校验规则的严格性。
- `leaderboard.md` 与 README 徽章由 `lab.py leaderboard` 生成，**禁止手工编辑**——测试强制其与代码渲染逐字节一致（`test_repository_leaderboard_is_current`）。
- 证据等级变更（尤其升级）必须有真实证据支撑并在 `result.md` 中写明证据形式；non-zero revenue 必须 `verified-revenue`、`succeeded` 必须 `public-metrics` 或 `verified-revenue`（lab.py:75-78 强制）。
- 不得给账本工具链引入第三方依赖（纯标准库、离线可跑是设计承诺）；实验 MVP 自身的依赖记录在该实验目录内，不污染根目录。

## 升级建议有效性 / 采纳规则（本仓定制）

1. **凡改动"机器校验规则"（`lab.py` 的 `validate()`、`REQUIRED`、枚举值）的建议：必须同步修改 `tests/test_lab.py` 与 `methodology.md`**，三者不一致即无效。
2. 凡放宽校验规则的建议（允许更低证据等级升级等）：默认**记录不做**——严格性是这个仓库存在的意义，需用户明确批准。
3. 实验记录变更：必须有对应的 `result.md` 人类报告，且 `python lab.py validate` 全绿才算完成。
4. 工具链体验改进（报错可读性、输出格式）：有效即可排期做，但报错仍需包含足够定位信息。
5.  leaderboard/徽章渲染变更：改完必须重跑 `python lab.py leaderboard` 并跑全量 unittest 确认逐字节一致。

## 升级建议 backlog

### 1. 实验 001 证据等级仅为 self-test，端到端验证依赖 ZHIPU_API_KEY

- **描述**：`experiments/001-ai-resume-optimizer/experiment.json:9` 的 `evidence_level` 为 `self-test`，状态 `inconclusive`、收入 CNY 0（leaderboard.md:11 同步）。要把该实验证据等级往 `public-metrics` 推进，需要真实跑通 MVP 的端到端流程，而 MVP（`app.py:50-52`）依赖 `ZHIPU_API_KEY`（或 `GLM_API_KEY`）调用智谱 GLM API，未配置时无法验证。注意：账本工具链本身（validate/summary/leaderboard + unittest）完全不依赖任何 API key。
- **发现日期**：2026-07-20
- **来源任务**：agent 实验状态盘点（AGENTS.md 建立任务核对）
- **预估价值/成本**：价值中（首个实验若能升级证据等级，对仓库公信力是正向示范）；成本中（需配置 API key、跑通 MVP、产出公开可验证指标）。
- **状态**：待评审（属"排期做"，且必须按规则 3 提供真实证据后才允许改 experiment.json）

### 2. `lab.py validate` 报错信息含绝对路径，可读性差

- **描述**：报错格式为 `f"{path}: <规则描述>"`（lab.py:39 起），`--root` 默认值是 `Path(__file__).resolve().parent`（lab.py:208）的绝对路径，因此直接 `python lab.py validate` 时报错行会带完整绝对路径（如 `D:\...\experiments\001-...\experiment.json: ...`），在 CI 日志和截图中冗长且泄露本机目录结构。建议：报错路径相对化（相对 `--root` 或仓库根）。
- **发现日期**：2026-07-20
- **来源任务**：agent 工具链体验排查（AGENTS.md 建立任务核对）
- **预估价值/成本**：价值低-中（纯可读性/隐私洁癖改进）；成本小（路径相对化 + 同步更新测试断言）。
- **状态**：待评审（改动时遵守定制规则 1：同步改测试）
