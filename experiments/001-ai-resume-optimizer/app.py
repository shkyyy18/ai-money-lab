# -*- coding: utf-8 -*-
"""experiment 001 · AI 简历优化器 MVP（独立可跑，无本机依赖）

假说（见 result.md / lean_canvas.md）：
  不买量、只靠 GitHub 自然流量，能不能拿到第一笔 ¥9.9？
- /optimize : 旧简历 + JD → GLM 改写 + ATS 关键词评分（交付价值）
- /fake-door: "导出 PDF/Word" 按钮 → 记点击（转化信号，暂不收费）
- events.jsonl: 记每次 optimize(需求) 与 fake_door(转化)，供指标统计

运行：
  pip install flask requests
  set ZHIPU_API_KEY=你的智谱key      (Windows) /  export ZHIPU_API_KEY=...  (Unix)
  python app.py                       →  http://localhost:5011
"""
import os
import sys
import json
import datetime
import subprocess
from pathlib import Path

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
EVENTS = Path(__file__).parent / "events.jsonl"
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"


def _refresh_key() -> None:
    """Windows: 启动时从用户级环境变量读 ZHIPU_API_KEY 校准本进程 env
    （bash/IDE 子进程 env 在启动时固化，之后改的 User 环境变量不会反映进来）。非 Windows 跳过。"""
    if sys.platform != "win32":
        return
    try:
        r = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "[Environment]::GetEnvironmentVariable('ZHIPU_API_KEY','User')"],
            capture_output=True, text=True, timeout=10)
        k = r.stdout.strip()
        if k and k != os.environ.get("ZHIPU_API_KEY", ""):
            os.environ["ZHIPU_API_KEY"] = k
    except Exception:
        pass


def call_glm(system_prompt: str, user_prompt: str,
             model: str = "glm-4-flash", max_tokens: int = 1800) -> str:
    """智谱 GLM 文本调用（v4，Bearer api-key 鉴权）。"""
    key = os.environ.get("ZHIPU_API_KEY") or os.environ.get("GLM_API_KEY")
    if not key:
        raise RuntimeError("未设置 ZHIPU_API_KEY 环境变量")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {"model": model, "max_tokens": max_tokens,
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": user_prompt}]}
    resp = requests.post(ZHIPU_URL, headers=headers, json=body, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"GLM HTTP {resp.status_code}: {resp.text[:200]}")
    return resp.json()["choices"][0]["message"]["content"]


_refresh_key()

SYSTEM_PROMPT = """你是资深简历顾问 + ATS（申请人追踪系统）优化专家。
用户给你【旧简历】和【目标岗位 JD】，你输出针对该 JD 优化的简历重写版：
1. 每段工作经历用 STAR + 量化数字重写（补合理的业务指标：规模/百分比/金额/时长，不确定就给保守估算并标*）
2. 自然嵌入 JD 里的关键词（不堆砌）
3. 中文，Markdown，分模块：个人摘要 / 工作经历 / 核心技能 / 教育背景
4. 末尾单起一行：**ATS 关键词匹配度：X/10**，并列出 3 个该 JD 有但简历缺失的关键词
只输出重写后的简历，不要前后缀解释。"""


def _log(event_type: str, extra: dict | None = None) -> None:
    """追加一条事件到 events.jsonl（需求/转化信号，methodology 的真点击口径）。"""
    rec = {"ts": datetime.datetime.now().isoformat(timespec="seconds"), "type": event_type}
    if extra:
        rec.update(extra)
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


@app.route("/")
def index():
    return PAGE


@app.route("/optimize", methods=["POST"])
def optimize():
    data = request.get_json(silent=True) or {}
    resume = (data.get("resume") or "").strip()
    jd = (data.get("jd") or "").strip()
    if not resume or not jd:
        return jsonify({"error": "请填写旧简历和目标 JD"}), 400
    _log("optimize", {"resume_len": len(resume), "jd_len": len(jd)})
    try:
        out = call_glm(SYSTEM_PROMPT,
                       f"【旧简历】\n{resume}\n\n【目标岗位 JD】\n{jd}")
    except Exception as e:
        return jsonify({"error": f"AI 调用失败：{e}"}), 500
    return jsonify({"result": (out or "").strip()})


@app.route("/fake-door", methods=["POST"])
def fake_door():
    """fake-door：用户点了"导出"，记为转化信号，但不真收费（methodology 的真点击口径）。"""
    _log("fake_door", {"ua": (request.headers.get("User-Agent") or "")[:80]})
    return jsonify({"ok": True,
                    "msg": "已记录您的导出意向。本工具处于实测期，暂未开放支付，"
                           "完整导出功能上线后将第一时间通知您。"})


PAGE = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>简历优化器 · AI 一键针对 JD 重写</title>
<style>
  :root{--bg:#0f1115;--card:#171a21;--line:#262b36;--tx:#e6e8ee;--mut:#8a93a6;--acc:#5b8cff;--gold:#f5c451}
  *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:15px/1.6 -apple-system,"PingFang SC","Microsoft YaHei",sans-serif}
  .wrap{max-width:880px;margin:0 auto;padding:32px 20px 80px}
  h1{font-size:26px;margin:0 0 6px}h1 b{color:var(--gold)}
  .sub{color:var(--mut);margin:0 0 24px}
  .row{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:680px){.row{grid-template-columns:1fr}}
  label{display:block;color:var(--mut);font-size:13px;margin:0 0 6px}
  textarea{width:100%;height:170px;background:var(--card);color:var(--tx);border:1px solid var(--line);
    border-radius:10px;padding:12px;resize:vertical;font:inherit}
  button{background:var(--acc);color:#fff;border:0;border-radius:10px;padding:12px 20px;font:inherit;font-weight:600;cursor:pointer;margin-top:14px}
  button:disabled{opacity:.5;cursor:wait}
  .out{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:18px;margin-top:18px;white-space:pre-wrap;word-break:break-word;min-height:60px}
  .pay{display:none;margin-top:14px;padding:14px 16px;background:linear-gradient(135deg,#2a2230,#1c2433);border:1px solid var(--gold);border-radius:12px;color:var(--tx)}
  .pay button{background:var(--gold);color:#1a1300;margin:8px 0 0}
  .err{color:#ff7a7a}.mut{color:var(--mut);font-size:12px}
</style></head><body><div class="wrap">
  <h1>简历优化器 · 一键针对 <b>目标 JD</b> 重写</h1>
  <p class="sub">贴上旧简历 + 目标岗位 JD，AI 输出 ATS 友好、量化成果、关键词匹配的重写版。</p>
  <div class="row">
    <div><label>旧简历</label><textarea id="resume" placeholder="把现有简历全文粘进来…"></textarea></div>
    <div><label>目标岗位 JD（招聘描述）</label><textarea id="jd" placeholder="把目标岗位的招聘 JD 粘进来…"></textarea></div>
  </div>
  <button id="go" onclick="run()">✨ AI 优化简历</button>
  <div id="msg" class="mut"></div>
  <div id="out" class="out mut">优化结果会显示在这里。</div>
  <div id="pay" class="pay">
    <b>📄 导出高清 PDF / Word 版？</b><br>
    <span class="mut">一键导出排版好的简历文件 · <b style="color:var(--gold)">¥9.9</b> 解锁</span>
    <br><button onclick="pay()">¥9.9 解锁导出</button>
    <div id="paymsg" class="mut"></div>
  </div>
</div><script>
async function run(){
  const resume=document.getElementById('resume').value.trim(),jd=document.getElementById('jd').value.trim();
  if(!resume||!jd){document.getElementById('msg').innerHTML='<span class="err">请填旧简历和目标 JD</span>';return}
  const btn=document.getElementById('go');btn.disabled=true;
  document.getElementById('msg').textContent='AI 改写中…（约 8-15 秒）';
  document.getElementById('out').className='out mut';document.getElementById('out').textContent='生成中…';
  document.getElementById('pay').style.display='none';
  try{const r=await fetch('/optimize',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({resume,jd})});
    const d=await r.json();if(d.error){document.getElementById('msg').innerHTML='<span class="err">'+d.error+'</span>';btn.disabled=false;return}
    document.getElementById('out').className='out';document.getElementById('out').textContent=d.result;
    document.getElementById('msg').textContent='';document.getElementById('pay').style.display='block';
  }catch(e){document.getElementById('msg').innerHTML='<span class="err">网络错误，重试</span>'}
  btn.disabled=false;
}
async function pay(){document.getElementById('paymsg').textContent='提交中…';
  try{const r=await fetch('/fake-door',{method:'POST'});const d=await r.json();
    document.getElementById('paymsg').textContent=d.msg}catch(e){document.getElementById('paymsg').textContent='网络错误'}}
</script></body></html>"""


if __name__ == "__main__":
    print("简历优化器 MVP → http://localhost:5011  (Ctrl+C 停止)")
    app.run(host="0.0.0.0", port=5011, debug=False)
