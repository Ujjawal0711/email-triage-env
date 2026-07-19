# -*- coding: utf-8 -*-
"""Self-contained interactive web demo served at `/`.

The page drives the same environment endpoints (`/reset`, `/step`, `/evaluate`)
that the RL/OpenEnv harness uses, so it is a real demo of the live environment
rather than a mock. All CSS/JS is inline (no external assets)."""

DEMO_HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Email Triage RL — Live Demo</title>
<style>
  :root{--bg:#0b1020;--card:#151b2e;--card2:#1b2338;--line:#2a3350;--txt:#e6ebf5;
    --mut:#8a97b8;--accent:#5b8cff;--green:#37d399;--red:#ff6b6b;--amber:#ffb454}
  *{box-sizing:border-box}
  body{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    background:radial-gradient(1200px 600px at 70% -10%,#182146,transparent),var(--bg);
    color:var(--txt);min-height:100vh}
  .wrap{max-width:880px;margin:0 auto;padding:30px 20px 60px}
  h1{font-size:1.55rem;margin:0 0 4px}
  .sub{color:var(--mut);margin:0 0 22px;font-size:.95rem;line-height:1.5}
  .grid{display:grid;grid-template-columns:1fr;gap:16px}
  @media(min-width:740px){.grid{grid-template-columns:1.35fr .9fr}}
  .card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
  .label{color:var(--mut);font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;margin:0 0 6px}
  .subject{font-weight:600;font-size:1.05rem;margin:0 0 8px}
  .body{color:#cdd6ee;margin:0 0 12px;line-height:1.5}
  .meta{display:flex;gap:8px;flex-wrap:wrap}
  .chip{background:var(--card2);border:1px solid var(--line);border-radius:999px;
    padding:4px 10px;font-size:.78rem;color:var(--mut)}
  .chip.lang{color:var(--accent);border-color:#33406e}
  .stepper{display:flex;gap:6px;margin:16px 0}
  .step{flex:1;text-align:center;padding:8px 4px;border-radius:8px;background:var(--card2);
    border:1px solid var(--line);font-size:.76rem;color:var(--mut)}
  .step.active{color:#fff;border-color:var(--accent);background:linear-gradient(180deg,#26325a,#1b2338)}
  .step.done{color:var(--green);border-color:#2a5748}
  .actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:4px}
  button.act{cursor:pointer;background:var(--card2);color:var(--txt);border:1px solid var(--line);
    border-radius:9px;padding:9px 14px;font-size:.9rem;transition:.15s}
  button.act:hover{border-color:var(--accent);transform:translateY(-1px)}
  button.primary{background:linear-gradient(180deg,#3f6bff,#2f56e6);border-color:#3f6bff;color:#fff;font-weight:600}
  .rewardbox{text-align:center}
  .rnum{font-size:2.4rem;font-weight:800;margin:2px 0}
  .rtot{font-size:.9rem;color:var(--mut)}
  .pos{color:var(--green)}.neg{color:var(--red)}.zero{color:var(--amber)}
  .log{margin-top:14px;font-size:.82rem;color:var(--mut);max-height:150px;overflow:auto;text-align:left}
  .log div{padding:3px 0;border-bottom:1px dashed #222c48}
  .hint{font-size:.8rem;color:var(--mut);margin-top:10px;min-height:1em}
  .base{margin-top:12px;font-size:.85rem;color:var(--mut)}
  .foot{margin-top:24px;color:var(--mut);font-size:.82rem;text-align:center;line-height:1.6}
  a{color:var(--accent)} code{background:#0d1428;color:#9fb2e6;padding:1px 5px;border-radius:4px;font-size:.85em}
</style>
</head>
<body>
<div class="wrap">
  <h1>📬 Email Triage — RL Environment</h1>
  <p class="sub">A bilingual (English + Hinglish) reinforcement-learning environment for customer-support routing.
  <b>You are the routing agent:</b> read the email, classify it, set its priority, and resolve. Correct, in-order routing earns reward (max <b>+2.00</b>); wrong or out-of-order actions are penalised.</p>
  <div class="grid">
    <div class="card">
      <div class="label">Inbound email</div>
      <p class="subject" id="subj">—</p>
      <p class="body" id="body">—</p>
      <div class="meta"><span class="chip" id="sender">—</span><span class="chip lang" id="lang">—</span></div>
      <div class="stepper" id="stepper"></div>
      <div class="label">Your move</div>
      <div class="actions" id="actions"></div>
      <div class="hint" id="hint"></div>
    </div>
    <div class="card rewardbox">
      <div class="label">Last step reward</div>
      <div class="rnum zero" id="reward">0.00</div>
      <div class="rtot">Episode total: <b id="total">0.00</b></div>
      <div class="log" id="log"></div>
      <button class="act primary" style="width:100%;margin-top:12px" onclick="newEmail()">↻ New email</button>
      <button class="act" style="width:100%;margin-top:8px" onclick="runBaseline()">Compare vs random policy</button>
      <div class="base" id="base"></div>
    </div>
  </div>
  <p class="foot">Live RL environment (OpenEnv-compatible). Raw API: <code>POST /reset</code>, <code>POST /step</code>, <code>GET /evaluate</code>.<br>
  Source on <a href="https://github.com/Ujjawal0711/email-triage-env">GitHub</a>.</p>
</div>
<script>
const ORDER=["analyze","classify","priority","resolve"];
const STEPLBL={analyze:"Analyze",classify:"Classify",priority:"Priority",resolve:"Resolve"};
const LABELS={analyze:"🔍 Analyze",resolve:"✅ Resolve",
 classify_urgent:"Urgent",classify_billing:"Billing",classify_support:"Support",classify_spam:"Spam",classify_info:"Info",
 set_priority_high:"High",set_priority_medium:"Medium",set_priority_low:"Low"};
let total=0;
async function post(u,b){const r=await fetch(u,{method:"POST",headers:{"Content-Type":"application/json"},body:b?JSON.stringify(b):null});return r.json();}
function fmt(r){return (r>=0?"+":"")+r.toFixed(2);}
function cls(r){return r>0?"pos":r<0?"neg":"zero";}
function render(obs){
  document.getElementById("subj").textContent=obs.email_subject||"—";
  document.getElementById("body").textContent=obs.email_body||"—";
  document.getElementById("sender").textContent="✉ "+(obs.sender||"unknown");
  document.getElementById("lang").textContent=obs.language==="hi-en"?"Hinglish":"English";
  const st=document.getElementById("stepper");st.innerHTML="";
  const cur=obs.stage;
  ORDER.forEach(k=>{let c="step";
    if(ORDER.indexOf(k)<ORDER.indexOf(cur))c+=" done";
    if(k===cur)c+=" active";
    st.innerHTML+='<div class="'+c+'">'+STEPLBL[k]+'</div>';});
  const a=document.getElementById("actions");a.innerHTML="";
  (obs.valid_actions||[]).forEach(act=>{
    const b=document.createElement("button");
    b.className="act"+((act==="analyze"||act==="resolve")?" primary":"");
    b.textContent=LABELS[act]||act;b.onclick=()=>step(act);a.appendChild(b);});
  const hints={analyze:"Step 1 — analyze the email.",classify:"Step 2 — which category fits?",
    priority:"Step 3 — how urgent is it?",resolve:"Step 4 — lock it in."};
  document.getElementById("hint").textContent=obs.done?"Episode complete — hit “New email” to play again.":(hints[cur]||"");
}
function showReward(r){const el=document.getElementById("reward");el.textContent=fmt(r);el.className="rnum "+cls(r);
  total+=r;const t=document.getElementById("total");t.textContent=fmt(total);t.className=cls(total);}
async function newEmail(){total=0;const t=document.getElementById("total");t.textContent="0.00";t.className="";
  document.getElementById("log").innerHTML="";const rw=document.getElementById("reward");rw.textContent="0.00";rw.className="rnum zero";
  const d=await post("/reset");render(d.observation);}
async function step(act){const d=await post("/step",{action:act});showReward(d.reward);
  const lg=document.getElementById("log");
  lg.innerHTML='<div>'+(LABELS[act]||act)+' → <b class="'+cls(d.reward)+'">'+fmt(d.reward)+'</b></div>'+lg.innerHTML;
  render(d.observation);}
async function runBaseline(){const el=document.getElementById("base");el.textContent="running 50 random episodes…";
  const r=await(await fetch("/evaluate")).json();
  el.innerHTML='Random policy averages <b class="'+cls(r.avg_reward)+'">'+fmt(r.avg_reward)+'</b> over '+r.episodes+' episodes — beat it by routing well!';
  newEmail();}
newEmail();
</script>
</body>
</html>"""
