import streamlit as st
import requests
import base64

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Agro Predictor",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
#MainMenu,footer,header,[data-testid="stToolbar"]{visibility:hidden;display:none}
.main .block-container{padding:0!important;max-width:100%!important}
[data-testid="stSidebar"]{display:none}
</style>
""", unsafe_allow_html=True)

# Cek koneksi ke backend
try:
    health_response = requests.get("http://127.0.0.1:8000/health", timeout=2)
    backend_status = "connected" if health_response.status_code == 200 else "error"
    if backend_status == "connected":
        st.success("✅ Backend terhubung!")
except:
    backend_status = "disconnected"
    st.warning("⚠️ Backend server not detected. Make sure to run: uvicorn main:app --reload")

# HTML content yang sudah diperbaiki
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --dark:#1C2B0E;
  --dark2:#253912;
  --dark3:#2F4A18;
  --accent:#7CB518;
  --accent-light:#A8D44A;
  --cream:#F7F4EE;
  --cream2:#EEE9DF;
  --text:#1C2B0E;
  --muted:#6B7A5A;
  --border:#D8D3C8;
}
body{font-family:'DM Sans',sans-serif;background:var(--dark);height:100vh;overflow:hidden;display:flex;align-items:stretch;margin:0;padding:0}
.app{display:flex;width:100%;height:100vh;overflow:hidden}

/* SIDEBAR */
.sidebar{width:280px;min-width:280px;background:var(--dark);display:flex;flex-direction:column;padding:2.25rem 1.75rem;position:relative;overflow:hidden}
.sidebar::after{content:'';position:absolute;bottom:-60px;left:-40px;width:220px;height:220px;border-radius:50%;background:rgba(124,181,24,.07);pointer-events:none}
.sidebar::before{content:'';position:absolute;top:-80px;right:-50px;width:200px;height:200px;border-radius:50%;background:rgba(124,181,24,.05);pointer-events:none}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:2.75rem}
.brand-icon{width:36px;height:36px;border-radius:9px;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:17px}
.brand-name{font-family:'Lora',serif;font-size:13px;font-weight:600;color:#fff;letter-spacing:.09em;text-transform:uppercase}
.nav-steps{flex:1;display:flex;flex-direction:column;gap:2px}
.nav-item{display:flex;align-items:center;gap:13px;padding:11px 12px;border-radius:10px;transition:background .2s;cursor:pointer}
.nav-item.active{background:rgba(124,181,24,.13)}
.nav-dot{width:26px;height:26px;min-width:26px;border-radius:50%;border:2px solid #2F4A18;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#4A6030;transition:all .3s}
.nav-item.active .nav-dot{border-color:var(--accent);background:var(--accent);color:#fff;font-weight:700}
.nav-item.done .nav-dot{border-color:var(--accent);background:transparent;color:var(--accent)}
.nav-label{font-size:13px;color:rgba(255,255,255,.3);font-weight:400;transition:color .2s}
.nav-item.active .nav-label{color:#fff;font-weight:700}
.nav-item.done .nav-label{color:rgba(255,255,255,.5)}
.nav-line{width:2px;height:20px;background:#2A3D18;margin-left:24px;transition:background .3s}
.nav-line.done-line{background:rgba(124,181,24,.35)}
.sidebar-bottom{margin-top:auto;padding-top:1.25rem}
.save-link{font-size:13px;color:rgba(255,255,255,.25);cursor:pointer;text-decoration:underline;text-underline-offset:3px;transition:color .2s}
.save-link:hover{color:rgba(255,255,255,.5)}
.sidebar.landing-mode .nav-steps{opacity:.3;pointer-events:none}

/* CONTENT */
.content{flex:1;background:var(--cream);border-radius:20px 0 0 20px;overflow-y:auto;display:flex;flex-direction:column}
.page{display:none;flex-direction:column;min-height:100%;padding:2.5rem 3rem}
.page.active{display:flex}
.page-top{flex:1}
.step-tag{display:inline-block;font-size:11px;font-weight:700;color:var(--accent);background:rgba(124,181,24,.11);border-radius:20px;padding:4px 13px;margin-bottom:1.1rem;letter-spacing:.04em;text-transform:uppercase}
.page-title{font-family:'Lora',serif;font-size:30px;font-weight:600;color:var(--text);line-height:1.2;margin-bottom:6px}
.page-sub{font-size:13px;color:var(--muted);margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem 2rem}
.span2{grid-column:1/-1}
.field{display:flex;flex-direction:column;gap:5px}
.field label{font-size:11.5px;font-weight:700;color:var(--muted);letter-spacing:.03em}
.field input[type=number]{padding:10px 42px 10px 13px;border:1.5px solid var(--border);border-radius:10px;background:#fff;font-size:14px;color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:border .2s;width:100%}
.field input[type=number]:focus{border-color:var(--accent)}
.input-wrap{position:relative}
.input-unit{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:11px;color:var(--muted);pointer-events:none}
.seg-group{display:flex;gap:6px}
.seg{flex:1;padding:10px 6px;border:1.5px solid var(--border);border-radius:10px;background:#fff;font-size:13px;font-weight:700;color:var(--muted);cursor:pointer;text-align:center;transition:all .2s;font-family:'DM Sans',sans-serif}
.seg:hover{border-color:#aac;color:var(--text)}
.seg.on{background:var(--dark);border-color:var(--dark);color:var(--accent-light)}

/* REVIEW */
.review-section{margin-bottom:1.4rem}
.review-section-title{font-size:10.5px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.65rem}
.review-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.review-item{background:#fff;border:1px solid var(--border);border-radius:10px;padding:11px 13px}
.review-key{font-size:10.5px;color:var(--muted);margin-bottom:4px}
.review-val{font-size:14px;font-weight:700;color:var(--text)}

/* RESULT */
.result-box{border-radius:13px;padding:1.25rem;margin-top:1.1rem;display:flex;align-items:center;gap:14px}
.result-ok{background:#EFF8D8;border:1.5px solid #A8D44A}
.result-no{background:#FFF0F0;border:1.5px solid #FFAAAA}
.result-icon{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.result-ok .result-icon{background:#A8D44A;color:var(--dark)}
.result-no .result-icon{background:#FF9B9B;color:#6B0000}
.r-title{font-size:15px;font-weight:700}
.result-ok .r-title{color:#2A4A00}
.result-no .r-title{color:#6B0000}
.r-sub{font-size:12px;color:var(--muted);margin-top:3px}

/* BUTTONS */
.page-nav{display:flex;justify-content:space-between;align-items:center;padding-top:1.5rem;margin-top:1.5rem;border-top:1px solid var(--border)}
.btn-back{padding:10px 26px;border:1.5px solid var(--border);border-radius:40px;background:transparent;font-size:13px;font-weight:700;color:var(--muted);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}
.btn-back:hover:not(:disabled){border-color:var(--dark);color:var(--dark)}
.btn-back:disabled{opacity:.3;cursor:not-allowed}
.btn-next{padding:10px 34px;border:none;border-radius:40px;background:var(--dark);font-size:13px;font-weight:700;color:var(--accent-light);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}
.btn-next:hover{background:var(--dark2)}
.btn-next:active{transform:scale(.98)}
.action-bar{display:flex;align-items:center;justify-content:space-between;padding:1.25rem 1.5rem;background:#fff;border:1px solid var(--border);border-radius:14px;margin-top:1.5rem}
.action-bar-left{display:flex;align-items:center;gap:10px}
.action-bar-right{display:flex;align-items:center;gap:10px}
.btn-reset-soft{padding:10px 22px;border:1.5px solid var(--border);border-radius:40px;background:transparent;font-size:13px;font-weight:700;color:var(--muted);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;display:flex;align-items:center;gap:7px}
.btn-reset-soft:hover{border-color:#c0392b;color:#c0392b}
.btn-predict{padding:11px 36px;border:none;border-radius:40px;background:var(--dark);font-size:14px;font-weight:700;color:var(--accent-light);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;display:flex;align-items:center;gap:8px}
.btn-predict:hover{background:var(--dark2)}
.btn-predict:disabled{background:var(--border);color:var(--muted);cursor:not-allowed}
.spin{display:inline-block;width:12px;height:12px;border:2px solid rgba(168,212,74,.3);border-top-color:var(--accent-light);border-radius:50%;animation:sp .7s linear infinite;vertical-align:middle;margin-right:5px}
@keyframes sp{to{transform:rotate(360deg)}}

/* LANDING PAGE */
#page-landing{background:var(--cream);justify-content:center;padding:2.75rem 3rem}
.landing-tag{display:inline-block;font-size:11px;font-weight:700;color:var(--accent);background:rgba(124,181,24,.11);border-radius:20px;padding:4px 14px;margin-bottom:1.4rem;letter-spacing:.05em;text-transform:uppercase}
.landing-headline{font-family:'Lora',serif;font-size:36px;font-weight:600;color:var(--text);line-height:1.2;margin-bottom:.65rem;max-width:460px}
.landing-headline em{font-style:italic;color:var(--accent)}
.landing-desc{font-size:13.5px;color:var(--muted);line-height:1.7;max-width:420px;margin-bottom:1.75rem}
.landing-divider{width:44px;height:3px;background:var(--accent-light);border-radius:2px;margin:1.1rem 0}
.landing-cta-row{display:flex;align-items:center;gap:16px;margin-bottom:2rem}
.btn-start{padding:13px 34px;border:none;border-radius:40px;background:var(--dark);font-size:14px;font-weight:700;color:var(--accent-light);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s;display:flex;align-items:center;gap:9px}
.btn-start:hover{background:var(--dark2)}
.btn-start-arrow{font-size:15px;transition:transform .2s}
.btn-start:hover .btn-start-arrow{transform:translateX(3px)}
.landing-note{font-size:12px;color:var(--muted);font-weight:500}

/* FEATURE CARDS */
.feat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:580px}
.feat-card{border-radius:14px;padding:18px 16px;position:relative;overflow:hidden;transition:transform .2s}
.feat-card:hover{transform:translateY(-2px)}
.feat-card-soil{background:#1C2B0E;border:1px solid #2F4A18}
.feat-card-env{background:#EAF3D4;border:1px solid #C0DD97}
.feat-card-extra{background:#F0EBE0;border:1px solid #D8D3C8}
.feat-card-deco{position:absolute;top:-18px;right:-18px;width:70px;height:70px;border-radius:50%;opacity:.18}
.feat-card-soil .feat-card-deco{background:#A8D44A}
.feat-card-env .feat-card-deco{background:#3B6D11}
.feat-card-extra .feat-card-deco{background:#BA7517}
.feat-badge{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:10px;margin-bottom:12px;font-size:16px}
.feat-card-soil .feat-badge{background:rgba(168,212,74,.15)}
.feat-card-env .feat-badge{background:rgba(59,109,17,.12)}
.feat-card-extra .feat-badge{background:rgba(186,117,23,.12)}
.feat-title{font-size:13px;font-weight:700;margin-bottom:5px}
.feat-card-soil .feat-title{color:#A8D44A}
.feat-card-env .feat-title{color:#27500A}
.feat-card-extra .feat-title{color:#633806}
.feat-desc{font-size:11.5px;line-height:1.55}
.feat-card-soil .feat-desc{color:rgba(168,212,74,.6)}
.feat-card-env .feat-desc{color:#6B7A5A}
.feat-card-extra .feat-desc{color:#888070}
</style>
</head>
<body>
<div class="app">

  <!-- SIDEBAR -->
  <div class="sidebar landing-mode" id="sidebar">
    <div class="brand">
      <div class="brand-icon">🌾</div>
      <div class="brand-name">Agro Predictor</div>
    </div>
    <div class="nav-steps">
      <div class="nav-item" id="nav0"><div class="nav-dot" id="dot0">1</div><div class="nav-label">Soil Properties</div></div>
      <div class="nav-line" id="line0"></div>
      <div class="nav-item" id="nav1"><div class="nav-dot" id="dot1">2</div><div class="nav-label">Environmental</div></div>
      <div class="nav-line" id="line1"></div>
      <div class="nav-item" id="nav2"><div class="nav-dot" id="dot2">3</div><div class="nav-label">Additional Factors</div></div>
      <div class="nav-line" id="line2"></div>
      <div class="nav-item" id="nav3"><div class="nav-dot" id="dot3">4</div><div class="nav-label">Confirm & Predict</div></div>
    </div>
    <div class="sidebar-bottom">
      <span class="save-link" onclick="saveToLocal()">💾 Save and exit</span>
    </div>
  </div>

  <!-- CONTENT -->
  <div class="content">

    <!-- LANDING -->
    <div class="page active" id="page-landing">
      <div>
        <div class="landing-tag">Machine Learning · Agro Tool</div>
        <div class="landing-headline">Apakah lahanmu <em>siap</em> ditanami?</div>
        <div class="landing-divider"></div>
        <div class="landing-desc">Masukkan kondisi tanah dan lingkungan — kami akan memprediksi apakah tanamanmu bisa tumbuh optimal menggunakan model machine learning.</div>
        <div class="landing-cta-row">
          <button class="btn-start" onclick="startForm()">
            Mulai Prediksi <span class="btn-start-arrow">→</span>
          </button>
          <span class="landing-note">4 langkah · ~2 menit</span>
        </div>
        <div class="feat-grid">
          <div class="feat-card feat-card-soil">
            <div class="feat-card-deco"></div>
            <div class="feat-badge">🪱</div>
            <div class="feat-title">Properti Tanah</div>
            <div class="feat-desc">Karakteristik fisik & kimia lahan kamu</div>
          </div>
          <div class="feat-card feat-card-env">
            <div class="feat-card-deco"></div>
            <div class="feat-badge">🌤</div>
            <div class="feat-title">Kondisi Iklim</div>
            <div class="feat-desc">Parameter lingkungan sekitar lahan</div>
          </div>
          <div class="feat-card feat-card-extra">
            <div class="feat-card-deco"></div>
            <div class="feat-badge">⚗️</div>
            <div class="feat-title">Faktor Tambahan</div>
            <div class="feat-desc">Parameter pendukung akurasi prediksi</div>
          </div>
        </div>
      </div>
    </div>

    <!-- STEP 1 -->
    <div class="page" id="page0">
      <div class="page-top">
        <div class="step-tag">Step 1 of 4</div>
        <div class="page-title">Soil Properties</div>
        <div class="page-sub">Masukkan karakteristik fisik dan kimia tanah kamu</div>
        <div class="grid2">
          <div class="field"><label>Bulk Density</label><div class="input-wrap"><input type="number" id="f-bd" value="1.20" min="0" max="3" step="0.05"><span class="input-unit">g/cm³</span></div></div>
          <div class="field"><label>Salinity</label><div class="input-wrap"><input type="number" id="f-sal" value="1.00" min="0" max="50" step="0.5"><span class="input-unit">dS/m</span></div></div>
          <div class="field"><label>Organic Matter</label><div class="input-wrap"><input type="number" id="f-om" value="5.00" min="0" max="100" step="0.5"><span class="input-unit">%</span></div></div>
          <div class="field"><label>Buffering Capacity</label><div class="input-wrap"><input type="number" id="f-buf" value="5.00" min="0" max="50" step="0.5"></div></div>
          <div class="field span2"><label>Cation Exchange Capacity</label><div class="input-wrap"><input type="number" id="f-cec" value="10.00" min="0" max="100" step="1"><span class="input-unit">meq/100g</span></div></div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" disabled>Back</button>
        <button class="btn-next" onclick="go(1)">Next</button>
      </div>
    </div>

    <!-- STEP 2 -->
    <div class="page" id="page1">
      <div class="page-top">
        <div class="step-tag">Step 2 of 4</div>
        <div class="page-title">Environmental Conditions</div>
        <div class="page-sub">Masukkan parameter iklim dan kondisi lingkungan</div>
        <div class="grid2">
          <div class="field"><label>Soil Moisture</label><div class="input-wrap"><input type="number" id="f-sm" value="30.00" min="0" max="100" step="1"><span class="input-unit">%</span></div></div>
          <div class="field"><label>Light Intensity</label><div class="input-wrap"><input type="number" id="f-li" value="800" min="0" max="2000" step="10"><span class="input-unit">PAR</span></div></div>
          <div class="field"><label>Soil Temperature</label><div class="input-wrap"><input type="number" id="f-st" value="25.00" min="0" max="60" step="0.5"><span class="input-unit">°C</span></div></div>
          <div class="field"><label>Soil pH</label><div class="input-wrap"><input type="number" id="f-ph" value="6.50" min="0" max="14" step="0.1"></div></div>
          <div class="field span2"><label>Air Temperature</label><div class="input-wrap"><input type="number" id="f-at" value="28.00" min="0" max="60" step="0.5"><span class="input-unit">°C</span></div></div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" onclick="go(0)">Back</button>
        <button class="btn-next" onclick="go(2)">Next</button>
      </div>
    </div>

    <!-- STEP 3 -->
    <div class="page" id="page2">
      <div class="page-top">
        <div class="step-tag">Step 3 of 4</div>
        <div class="page-title">Additional Factors</div>
        <div class="page-sub">Parameter tambahan untuk akurasi prediksi yang lebih baik</div>
        <div class="grid2">
          <div class="field span2"><label>Moisture Regime</label><div class="seg-group"><button class="seg on" id="mr0" onclick="setSeg('mr',0)">Dry</button><button class="seg" id="mr1" onclick="setSeg('mr',1)">Moderate</button><button class="seg" id="mr2" onclick="setSeg('mr',2)">Wet</button></div></div>
          <div class="field span2"><label>Thermal Regime</label><div class="seg-group"><button class="seg" id="tr0" onclick="setSeg('tr',0)">Cold</button><button class="seg on" id="tr1" onclick="setSeg('tr',1)">Temperate</button><button class="seg" id="tr2" onclick="setSeg('tr',2)">Hot</button></div></div>
          <div class="field span2"><label>Nutrient Balance</label><div class="input-wrap"><input type="number" id="f-nb" value="0.00" min="-100" max="100" step="5"></div></div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" onclick="go(1)">Back</button>
        <button class="btn-next" onclick="go(3)">Next</button>
      </div>
    </div>

    <!-- STEP 4 -->
    <div class="page" id="page3">
      <div class="page-top">
        <div class="step-tag">Step 4 of 4</div>
        <div class="page-title">Confirm & Predict</div>
        <div class="page-sub">Periksa semua input sebelum melanjutkan prediksi</div>
        <div id="review-container"></div>
        <div id="result-area"></div>
        <div class="action-bar">
          <div class="action-bar-left">
            <button class="btn-back" onclick="go(2)">← Back</button>
            <button class="btn-reset-soft" onclick="resetAll()">↺ Reset semua</button>
          </div>
          <div class="action-bar-right">
            <button class="btn-predict" id="pred-btn" onclick="runPredict()">
              <span id="pred-label">Jalankan Prediksi</span>
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
var segs = {mr: 0, tr: 1};
var cur = 'landing';
var API_URL = 'http://127.0.0.1:8000/predict';

function startForm() {
  document.getElementById('page-landing').classList.remove('active');
  document.getElementById('page0').classList.add('active');
  document.getElementById('sidebar').classList.remove('landing-mode');
  updateNav(0);
  cur = 0;
}

function updateNav(n) {
  for (var i = 0; i < 4; i++) {
    var nav = document.getElementById('nav' + i);
    var dot = document.getElementById('dot' + i);
    var line = i < 3 ? document.getElementById('line' + i) : null;
    if (i < n) {
      nav.className = 'nav-item done';
      dot.innerHTML = '✓';
    } else if (i === n) {
      nav.className = 'nav-item active';
      dot.textContent = i + 1;
    } else {
      nav.className = 'nav-item';
      dot.textContent = i + 1;
    }
    if (line) line.className = 'nav-line' + (i < n ? ' done-line' : '');
  }
}

function go(n) {
  document.getElementById('page' + cur).classList.remove('active');
  document.getElementById('page' + n).classList.add('active');
  updateNav(n);
  cur = n;
  if (n === 3) fillReview();
}

function setSeg(g, v) {
  segs[g] = v;
  for (var i = 0; i < 3; i++) {
    document.getElementById(g + i).className = 'seg' + (i === v ? ' on' : '');
  }
}

function gv(id) {
  return parseFloat(document.getElementById(id).value) || 0;
}

function fillReview() {
  var mr = ['Dry', 'Moderate', 'Wet'];
  var tr = ['Cold', 'Temperate', 'Hot'];
  var html = `
    <div class="review-section">
      <div class="review-section-title">Soil Properties</div>
      <div class="review-grid">
        <div class="review-item"><div class="review-key">Bulk Density</div><div class="review-val">${gv('f-bd').toFixed(2)} g/cm³</div></div>
        <div class="review-item"><div class="review-key">Salinity</div><div class="review-val">${gv('f-sal').toFixed(1)} dS/m</div></div>
        <div class="review-item"><div class="review-key">Organic Matter</div><div class="review-val">${gv('f-om').toFixed(1)}%</div></div>
        <div class="review-item"><div class="review-key">Buffering Capacity</div><div class="review-val">${gv('f-buf').toFixed(1)}</div></div>
        <div class="review-item"><div class="review-key">CEC</div><div class="review-val">${gv('f-cec').toFixed(1)} meq/100g</div></div>
      </div>
    </div>
    <div class="review-section">
      <div class="review-section-title">Environmental Conditions</div>
      <div class="review-grid">
        <div class="review-item"><div class="review-key">Soil Moisture</div><div class="review-val">${gv('f-sm').toFixed(1)}%</div></div>
        <div class="review-item"><div class="review-key">Light Intensity</div><div class="review-val">${gv('f-li').toFixed(0)} PAR</div></div>
        <div class="review-item"><div class="review-key">Soil Temp</div><div class="review-val">${gv('f-st').toFixed(1)}°C</div></div>
        <div class="review-item"><div class="review-key">Soil pH</div><div class="review-val">${gv('f-ph').toFixed(1)}</div></div>
        <div class="review-item"><div class="review-key">Air Temp</div><div class="review-val">${gv('f-at').toFixed(1)}°C</div></div>
      </div>
    </div>
    <div class="review-section">
      <div class="review-section-title">Additional Factors</div>
      <div class="review-grid">
        <div class="review-item"><div class="review-key">Moisture Regime</div><div class="review-val">${mr[segs.mr]}</div></div>
        <div class="review-item"><div class="review-key">Thermal Regime</div><div class="review-val">${tr[segs.tr]}</div></div>
        <div class="review-item"><div class="review-key">Nutrient Balance</div><div class="review-val">${gv('f-nb').toFixed(1)}</div></div>
      </div>
    </div>
  `;
  document.getElementById('review-container').innerHTML = html;
}

function resetAll() {
  if (!confirm('Reset semua data ke nilai awal?')) return;
  var d = {
    'f-bd': '1.20', 'f-sal': '1.00', 'f-om': '5.00', 'f-buf': '5.00',
    'f-cec': '10.00', 'f-sm': '30.00', 'f-li': '800', 'f-st': '25.00',
    'f-ph': '6.50', 'f-at': '28.00', 'f-nb': '0.00'
  };
  Object.keys(d).forEach(function(id) {
    document.getElementById(id).value = d[id];
  });
  setSeg('mr', 0);
  setSeg('tr', 1);
  document.getElementById('result-area').innerHTML = '';
  document.getElementById('pred-label').textContent = 'Jalankan Prediksi';
  document.getElementById('pred-btn').disabled = false;
  document.getElementById('page' + cur).classList.remove('active');
  document.getElementById('page-landing').classList.add('active');
  document.getElementById('sidebar').classList.add('landing-mode');
  updateNav(-1);
  cur = 'landing';
}

function saveToLocal() {
  var data = {
    bulk_density: gv('f-bd'),
    organic_matter_pct: gv('f-om'),
    cation_exchange_capacity: gv('f-cec'),
    salinity_ec: gv('f-sal'),
    buffering_capacity: gv('f-buf'),
    soil_moisture_pct: gv('f-sm'),
    soil_temp_c: gv('f-st'),
    air_temp_c: gv('f-at'),
    light_intensity_par: gv('f-li'),
    soil_ph: gv('f-ph'),
    moisture_regime: segs.mr,
    thermal_regime: segs.tr,
    nutrient_balance: gv('f-nb')
  };
  try {
    localStorage.setItem('agro_data', JSON.stringify(data));
    alert('Data tersimpan!');
  } catch(e) {}
}

window.addEventListener('load', function() {
  try {
    var saved = localStorage.getItem('agro_data');
    if (saved) {
      var d = JSON.parse(saved);
      var map = {
        'f-bd': 'bulk_density', 'f-om': 'organic_matter_pct',
        'f-cec': 'cation_exchange_capacity', 'f-sal': 'salinity_ec',
        'f-buf': 'buffering_capacity', 'f-sm': 'soil_moisture_pct',
        'f-st': 'soil_temp_c', 'f-at': 'air_temp_c',
        'f-li': 'light_intensity_par', 'f-ph': 'soil_ph',
        'f-nb': 'nutrient_balance'
      };
      Object.keys(map).forEach(function(id) {
        if (d[map[id]] !== undefined) document.getElementById(id).value = d[map[id]];
      });
      if (d.moisture_regime !== undefined) setSeg('mr', d.moisture_regime);
      if (d.thermal_regime !== undefined) setSeg('tr', d.thermal_regime);
    }
  } catch(e) {}
});

// PERBAIKAN UTAMA ADA DI SINI!
// Menghapus wrapper 'inputs' dan mengirim data langsung
async function runPredict() {
  var btn = document.getElementById('pred-btn');
  var lbl = document.getElementById('pred-label');
  btn.disabled = true;
  lbl.innerHTML = '<span class="spin"></span>Memproses...';
  
  var payload = {
    bulk_density: gv('f-bd'),
    organic_matter_pct: gv('f-om'),
    cation_exchange_capacity: gv('f-cec'),
    salinity_ec: gv('f-sal'),
    buffering_capacity: gv('f-buf'),
    soil_moisture_pct: gv('f-sm'),
    soil_temp_c: gv('f-st'),
    air_temp_c: gv('f-at'),
    light_intensity_par: gv('f-li'),
    soil_ph: gv('f-ph'),
    moisture_regime: segs.mr,
    thermal_regime: segs.tr,
    nutrient_balance: gv('f-nb')
  };
  
  // DEBUG: Tampilkan payload di console browser
  console.log("📤 PAYLOAD YANG DIKIRIM:", payload);
  
  var area = document.getElementById('result-area');
  try {
    var response = await fetch(API_URL, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(payload)
    });
    
    if (response.ok) {
      var data = await response.json();
      console.log("📥 RESPONSE DARI BACKEND:", data);
      
      var conf = data.confidence ? ` (confidence: ${(data.confidence * 100).toFixed(1)}%)` : '';
      
      if (data.result === 'Tumbuh') {
        area.innerHTML = '<div class="result-box result-ok"><div class="result-icon">✓</div><div><div class="r-title">✅ Suitable — Tanaman bisa tumbuh!' + conf + '</div><div class="r-sub">Kondisi lingkungan dan tanah mendukung pertumbuhan tanaman.</div></div></div>';
      } else {
        area.innerHTML = '<div class="result-box result-no"><div class="result-icon">✗</div><div><div class="r-title">❌ Not Suitable — Kondisi kurang mendukung' + conf + '</div><div class="r-sub">Beberapa parameter perlu diperbaiki sebelum menanam.</div></div></div>';
      }
    } else {
      var errorData = await response.json();
      area.innerHTML = '<div class="result-box result-no"><div class="result-icon">!</div><div><div class="r-title">Error ' + response.status + '</div><div class="r-sub">' + (errorData.detail || 'Terjadi kesalahan pada server') + '</div></div></div>';
    }
  } catch(e) {
    area.innerHTML = '<div class="result-box result-no"><div class="result-icon">!</div><div><div class="r-title">Koneksi Gagal</div><div class="r-sub">' + e.message + '</div></div></div>';
  }
  btn.disabled = false;
  lbl.textContent = 'Prediksi Ulang';
}
</script>
</body>
</html>
"""

# Tampilkan HTML
if backend_status == "connected":
    html_base64 = base64.b64encode(HTML_CONTENT.encode()).decode()
    st.iframe(
        src=f"data:text/html;base64,{html_base64}",
        height=750
    )