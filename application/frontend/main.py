import streamlit as st
import streamlit.components.v1 as components
import requests
import json

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

# Health check untuk backend
try:
    health_response = requests.get("http://127.0.0.1:8000/health", timeout=2)
    if health_response.status_code == 200:
        backend_status = "connected"
    else:
        backend_status = "error"
except:
    backend_status = "disconnected"

# Tampilkan status backend (opsional)
if backend_status != "connected":
    st.warning("⚠️ Backend server not detected. Make sure to run: uvicorn app:app --reload")

HTML = rf"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
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
}}
body{{font-family:'DM Sans',sans-serif;background:var(--dark);height:100vh;overflow:hidden;display:flex;align-items:stretch}}
.app{{display:flex;width:100%;height:100vh;overflow:hidden}}

.sidebar{{width:280px;min-width:280px;background:var(--dark);display:flex;flex-direction:column;padding:2.25rem 1.75rem;position:relative;overflow:hidden}}
.sidebar::after{{content:'';position:absolute;bottom:-60px;left:-40px;width:220px;height:220px;border-radius:50%;background:rgba(124,181,24,.07);pointer-events:none}}
.sidebar::before{{content:'';position:absolute;top:-80px;right:-50px;width:200px;height:200px;border-radius:50%;background:rgba(124,181,24,.05);pointer-events:none}}
.brand{{display:flex;align-items:center;gap:10px;margin-bottom:2.75rem}}
.brand-icon{{width:36px;height:36px;border-radius:9px;background:var(--accent);display:flex;align-items:center;justify-content:center;font-size:17px}}
.brand-name{{font-family:'Lora',serif;font-size:13px;font-weight:600;color:#fff;letter-spacing:.09em;text-transform:uppercase}}
.nav-steps{{flex:1;display:flex;flex-direction:column;gap:2px}}
.nav-item{{display:flex;align-items:center;gap:13px;padding:11px 12px;border-radius:10px;transition:background .2s}}
.nav-item.active{{background:rgba(124,181,24,.13)}}
.nav-dot{{width:26px;height:26px;min-width:26px;border-radius:50%;border:2px solid #2F4A18;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:#4A6030;transition:all .3s}}
.nav-item.active .nav-dot{{border-color:var(--accent);background:var(--accent);color:#fff;font-weight:600}}
.nav-item.done .nav-dot{{border-color:var(--accent);background:transparent;color:var(--accent)}}
.nav-label{{font-size:13px;color:rgba(255,255,255,.3);font-weight:400;transition:color .2s}}
.nav-item.active .nav-label{{color:#fff;font-weight:500}}
.nav-item.done .nav-label{{color:rgba(255,255,255,.5)}}
.nav-line{{width:2px;height:20px;background:#2A3D18;margin-left:24px;transition:background .3s}}
.nav-line.done-line{{background:rgba(124,181,24,.35)}}
.sidebar-bottom{{margin-top:auto;padding-top:1.25rem}}
.save-link{{font-size:13px;color:rgba(255,255,255,.25);cursor:pointer;text-decoration:underline;text-underline-offset:3px;transition:color .2s}}
.save-link:hover{{color:rgba(255,255,255,.5)}}

.content{{flex:1;background:var(--cream);border-radius:20px 0 0 20px;overflow-y:auto;display:flex;flex-direction:column}}
.page{{display:none;flex-direction:column;min-height:100%;padding:2.5rem 3rem}}
.page.active{{display:flex}}
.page-top{{flex:1}}
.step-tag{{display:inline-block;font-size:11px;font-weight:500;color:var(--accent);background:rgba(124,181,24,.11);border-radius:20px;padding:4px 13px;margin-bottom:1.1rem;letter-spacing:.04em;text-transform:uppercase}}
.page-title{{font-family:'Lora',serif;font-size:30px;font-weight:600;color:var(--text);line-height:1.2;margin-bottom:6px}}
.page-sub{{font-size:13px;color:var(--muted);margin-bottom:2rem;padding-bottom:1.5rem;border-bottom:1px solid var(--border)}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:1.1rem 2rem}}
.span2{{grid-column:1/-1}}
.field{{display:flex;flex-direction:column;gap:5px}}
.field label{{font-size:11.5px;font-weight:500;color:var(--muted);letter-spacing:.03em}}
.field input[type=number]{{padding:10px 42px 10px 13px;border:1.5px solid var(--border);border-radius:10px;background:#fff;font-size:14px;color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:border .2s;-moz-appearance:textfield;appearance:textfield;width:100%}}
.field input[type=number]::-webkit-inner-spin-button,.field input[type=number]::-webkit-outer-spin-button{{-webkit-appearance:none}}
.field input[type=number]:focus{{border-color:var(--accent)}}
.input-wrap{{position:relative}}
.input-unit{{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:11px;color:var(--muted);pointer-events:none}}
.seg-group{{display:flex;gap:6px}}
.seg{{flex:1;padding:10px 6px;border:1.5px solid var(--border);border-radius:10px;background:#fff;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;text-align:center;transition:all .2s;font-family:'DM Sans',sans-serif}}
.seg:hover{{border-color:#aac;color:var(--text)}}
.seg.on{{background:var(--dark);border-color:var(--dark);color:var(--accent-light)}}

.review-section{{margin-bottom:1.4rem}}
.review-section-title{{font-size:10.5px;font-weight:500;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:.65rem}}
.review-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}}
.review-item{{background:#fff;border:1px solid var(--border);border-radius:10px;padding:11px 13px}}
.review-key{{font-size:10.5px;color:var(--muted);margin-bottom:4px}}
.review-val{{font-size:14px;font-weight:500;color:var(--text)}}

.result-box{{border-radius:13px;padding:1.25rem 1.25rem;margin-top:1.1rem;display:flex;align-items:center;gap:14px}}
.result-ok{{background:#EFF8D8;border:1.5px solid #A8D44A}}
.result-no{{background:#FFF0F0;border:1.5px solid #FFAAAA}}
.result-icon{{width:42px;height:42px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}}
.result-ok .result-icon{{background:#A8D44A;color:var(--dark)}}
.result-no .result-icon{{background:#FF9B9B;color:#6B0000}}
.r-title{{font-size:15px;font-weight:600}}
.result-ok .r-title{{color:#2A4A00}}
.result-no .r-title{{color:#6B0000}}
.r-sub{{font-size:12px;color:var(--muted);margin-top:3px}}

.page-nav{{display:flex;justify-content:space-between;align-items:center;padding-top:1.5rem;margin-top:1.5rem;border-top:1px solid var(--border)}}
.btn-back{{padding:10px 26px;border:1.5px solid var(--border);border-radius:40px;background:transparent;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}}
.btn-back:hover:not(:disabled){{border-color:var(--dark);color:var(--dark)}}
.btn-back:disabled{{opacity:.3;cursor:not-allowed}}
.btn-next{{padding:10px 34px;border:none;border-radius:40px;background:var(--dark);font-size:13px;font-weight:500;color:var(--accent-light);cursor:pointer;font-family:'DM Sans',sans-serif;transition:all .2s}}
.btn-next:hover{{background:var(--dark2)}}
.btn-next:active{{transform:scale(.98)}}
.btn-next:disabled{{background:var(--border);color:var(--muted);cursor:not-allowed}}
.btn-nav-group{{display:flex;gap:8px}}
.spin{{display:inline-block;width:12px;height:12px;border:2px solid rgba(168,212,74,.3);border-top-color:var(--accent-light);border-radius:50%;animation:sp .7s linear infinite;vertical-align:middle;margin-right:5px}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
</style>
</head>
<body>
<div class="app">

  <div class="sidebar">
    <div class="brand">
      <div class="brand-icon">🌾</div>
      <div class="brand-name">Agro Predictor</div>
    </div>
    <div class="nav-steps">
      <div class="nav-item active" id="nav0">
        <div class="nav-dot" id="dot0">1</div>
        <div class="nav-label">Soil Properties</div>
      </div>
      <div class="nav-line" id="line0"></div>
      <div class="nav-item" id="nav1">
        <div class="nav-dot" id="dot1">2</div>
        <div class="nav-label">Environmental</div>
      </div>
      <div class="nav-line" id="line1"></div>
      <div class="nav-item" id="nav2">
        <div class="nav-dot" id="dot2">3</div>
        <div class="nav-label">Additional Factors</div>
      </div>
      <div class="nav-line" id="line2"></div>
      <div class="nav-item" id="nav3">
        <div class="nav-dot" id="dot3">4</div>
        <div class="nav-label">Confirm & Predict</div>
      </div>
    </div>
    <div class="sidebar-bottom">
      <span class="save-link" onclick="saveToLocal()">💾 Save and exit</span>
    </div>
  </div>

  <div class="content">

    <div class="page active" id="page0">
      <div class="page-top">
        <div class="step-tag">Step 1 of 4</div>
        <div class="page-title">Soil Properties</div>
        <div class="page-sub">Masukkan karakteristik fisik dan kimia tanah kamu</div>
        <div class="grid2">
          <div class="field">
            <label>Bulk Density</label>
            <div class="input-wrap"><input type="number" id="f-bd" value="1.20" min="0" max="3" step="0.05"><span class="input-unit">g/cm³</span></div>
          </div>
          <div class="field">
            <label>Salinity</label>
            <div class="input-wrap"><input type="number" id="f-sal" value="1.00" min="0" max="50" step="0.5"><span class="input-unit">dS/m</span></div>
          </div>
          <div class="field">
            <label>Organic Matter</label>
            <div class="input-wrap"><input type="number" id="f-om" value="5.00" min="0" max="100" step="0.5"><span class="input-unit">%</span></div>
          </div>
          <div class="field">
            <label>Buffering Capacity</label>
            <div class="input-wrap"><input type="number" id="f-buf" value="5.00" min="0" max="50" step="0.5"></div>
          </div>
          <div class="field span2">
            <label>Cation Exchange Capacity</label>
            <div class="input-wrap"><input type="number" id="f-cec" value="10.00" min="0" max="100" step="1"><span class="input-unit">meq/100g</span></div>
          </div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" disabled>Back</button>
        <button class="btn-next" onclick="go(1)">Next</button>
      </div>
    </div>

    <div class="page" id="page1">
      <div class="page-top">
        <div class="step-tag">Step 2 of 4</div>
        <div class="page-title">Environmental Conditions</div>
        <div class="page-sub">Masukkan parameter iklim dan kondisi lingkungan</div>
        <div class="grid2">
          <div class="field">
            <label>Soil Moisture</label>
            <div class="input-wrap"><input type="number" id="f-sm" value="30.00" min="0" max="100" step="1"><span class="input-unit">%</span></div>
          </div>
          <div class="field">
            <label>Light Intensity</label>
            <div class="input-wrap"><input type="number" id="f-li" value="800" min="0" max="2000" step="10"><span class="input-unit">PAR</span></div>
          </div>
          <div class="field">
            <label>Soil Temperature</label>
            <div class="input-wrap"><input type="number" id="f-st" value="25.00" min="0" max="60" step="0.5"><span class="input-unit">°C</span></div>
          </div>
          <div class="field">
            <label>Soil pH</label>
            <div class="input-wrap"><input type="number" id="f-ph" value="6.50" min="0" max="14" step="0.1"></div>
          </div>
          <div class="field span2">
            <label>Air Temperature</label>
            <div class="input-wrap"><input type="number" id="f-at" value="28.00" min="0" max="60" step="0.5"><span class="input-unit">°C</span></div>
          </div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" onclick="go(0)">Back</button>
        <button class="btn-next" onclick="go(2)">Next</button>
      </div>
    </div>

    <div class="page" id="page2">
      <div class="page-top">
        <div class="step-tag">Step 3 of 4</div>
        <div class="page-title">Additional Factors</div>
        <div class="page-sub">Parameter tambahan untuk akurasi prediksi yang lebih baik</div>
        <div class="grid2">
          <div class="field span2">
            <label>Moisture Regime</label>
            <div class="seg-group">
              <button class="seg on" id="mr0" onclick="setSeg('mr',0)">Dry</button>
              <button class="seg" id="mr1" onclick="setSeg('mr',1)">Moderate</button>
              <button class="seg" id="mr2" onclick="setSeg('mr',2)">Wet</button>
            </div>
          </div>
          <div class="field span2">
            <label>Thermal Regime</label>
            <div class="seg-group">
              <button class="seg" id="tr0" onclick="setSeg('tr',0)">Cold</button>
              <button class="seg on" id="tr1" onclick="setSeg('tr',1)">Temperate</button>
              <button class="seg" id="tr2" onclick="setSeg('tr',2)">Hot</button>
            </div>
          </div>
          <div class="field span2">
            <label>Nutrient Balance</label>
            <div class="input-wrap"><input type="number" id="f-nb" value="0.00" min="-100" max="100" step="5"></div>
          </div>
        </div>
      </div>
      <div class="page-nav">
        <button class="btn-back" onclick="go(1)">Back</button>
        <button class="btn-next" onclick="go(3)">Next</button>
      </div>
    </div>

    <div class="page" id="page3">
      <div class="page-top">
        <div class="step-tag">Step 4 of 4</div>
        <div class="page-title">Confirm & Predict</div>
        <div class="page-sub">Periksa semua input sebelum melanjutkan prediksi</div>
        <div class="review-section">
          <div class="review-section-title">Soil Properties</div>
          <div class="review-grid">
            <div class="review-item"><div class="review-key">Bulk Density</div><div class="review-val" id="r-bd">—</div></div>
            <div class="review-item"><div class="review-key">Salinity</div><div class="review-val" id="r-sal">—</div></div>
            <div class="review-item"><div class="review-key">Organic Matter</div><div class="review-val" id="r-om">—</div></div>
            <div class="review-item"><div class="review-key">Buffering Capacity</div><div class="review-val" id="r-buf">—</div></div>
            <div class="review-item"><div class="review-key">CEC</div><div class="review-val" id="r-cec">—</div></div>
          </div>
        </div>
        <div class="review-section">
          <div class="review-section-title">Environmental Conditions</div>
          <div class="review-grid">
            <div class="review-item"><div class="review-key">Soil Moisture</div><div class="review-val" id="r-sm">—</div></div>
            <div class="review-item"><div class="review-key">Light Intensity</div><div class="review-val" id="r-li">—</div></div>
            <div class="review-item"><div class="review-key">Soil Temp</div><div class="review-val" id="r-st">—</div></div>
            <div class="review-item"><div class="review-key">Soil pH</div><div class="review-val" id="r-ph">—</div></div>
            <div class="review-item"><div class="review-key">Air Temp</div><div class="review-val" id="r-at">—</div></div>
          </div>
        </div>
        <div class="review-section">
          <div class="review-section-title">Additional Factors</div>
          <div class="review-grid">
            <div class="review-item"><div class="review-key">Moisture Regime</div><div class="review-val" id="r-mr">—</div></div>
            <div class="review-item"><div class="review-key">Thermal Regime</div><div class="review-val" id="r-tr">—</div></div>
            <div class="review-item"><div class="review-key">Nutrient Balance</div><div class="review-val" id="r-nb">—</div></div>
          </div>
        </div>
        <div id="result-area"></div>
      </div>
      <div class="page-nav">
        <button class="btn-back" onclick="go(2)">Back</button>
        <div class="btn-nav-group">
          <button class="btn-back" onclick="resetAll()">Reset</button>
          <button class="btn-next" id="pred-btn" onclick="runPredict()">Predict</button>
        </div>
      </div>
    </div>

  </div>
</div>

<script>
var segs={{mr:0,tr:1}};
var cur=0;

function go(n){{
  document.getElementById('page'+cur).classList.remove('active');
  document.getElementById('page'+n).classList.add('active');
  for(var i=0;i<4;i++){{
    var nav=document.getElementById('nav'+i);
    var dot=document.getElementById('dot'+i);
    var line=i<3?document.getElementById('line'+i):null;
    if(i<n){{nav.className='nav-item done';dot.innerHTML='✓';}}
    else if(i===n){{nav.className='nav-item active';dot.textContent=i+1;}}
    else{{nav.className='nav-item';dot.textContent=i+1;}}
    if(line) line.className='nav-line'+(i<n?' done-line':'');
  }}
  cur=n;
  if(n===3) fillReview();
}}

function setSeg(g,v){{
  segs[g]=v;
  for(var i=0;i<3;i++) document.getElementById(g+i).className='seg'+(i===v?' on':'');
}}

function gv(id){{return parseFloat(document.getElementById(id).value)||0;}}

function fillReview(){{
  var mr=['Dry','Moderate','Wet'];
  var tr=['Cold','Temperate','Hot'];
  document.getElementById('r-bd').textContent=gv('f-bd').toFixed(2)+' g/cm³';
  document.getElementById('r-sal').textContent=gv('f-sal').toFixed(1)+' dS/m';
  document.getElementById('r-om').textContent=gv('f-om').toFixed(1)+'%';
  document.getElementById('r-buf').textContent=gv('f-buf').toFixed(1);
  document.getElementById('r-cec').textContent=gv('f-cec').toFixed(1)+' meq/100g';
  document.getElementById('r-sm').textContent=gv('f-sm').toFixed(1)+'%';
  document.getElementById('r-li').textContent=gv('f-li').toFixed(0)+' PAR';
  document.getElementById('r-st').textContent=gv('f-st').toFixed(1)+'°C';
  document.getElementById('r-ph').textContent=gv('f-ph').toFixed(1);
  document.getElementById('r-at').textContent=gv('f-at').toFixed(1)+'°C';
  document.getElementById('r-mr').textContent=mr[segs.mr];
  document.getElementById('r-tr').textContent=tr[segs.tr];
  document.getElementById('r-nb').textContent=gv('f-nb').toFixed(1);
}}

function resetAll(){{
  ['f-bd','f-sal','f-om','f-buf','f-cec','f-sm','f-li','f-st','f-ph','f-at','f-nb'].forEach(function(id){{
    var defaults={{'f-bd':'1.20','f-sal':'1.00','f-om':'5.00','f-buf':'5.00','f-cec':'10.00','f-sm':'30.00','f-li':'800','f-st':'25.00','f-ph':'6.50','f-at':'28.00','f-nb':'0.00'}};
    document.getElementById(id).value=defaults[id];
  }});
  setSeg('mr',0); setSeg('tr',1);
  document.getElementById('result-area').innerHTML='';
  document.getElementById('pred-btn').textContent='Predict';
  go(0);
}}

function saveToLocal(){{
  var data = {{
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
  }};
  localStorage.setItem('agro_predictor_data', JSON.stringify(data));
  alert('Data saved locally!');
}}

function loadFromLocal(){{
  var saved = localStorage.getItem('agro_predictor_data');
  if(saved){{
    var data = JSON.parse(saved);
    document.getElementById('f-bd').value = data.bulk_density;
    document.getElementById('f-om').value = data.organic_matter_pct;
    document.getElementById('f-cec').value = data.cation_exchange_capacity;
    document.getElementById('f-sal').value = data.salinity_ec;
    document.getElementById('f-buf').value = data.buffering_capacity;
    document.getElementById('f-sm').value = data.soil_moisture_pct;
    document.getElementById('f-st').value = data.soil_temp_c;
    document.getElementById('f-at').value = data.air_temp_c;
    document.getElementById('f-li').value = data.light_intensity_par;
    document.getElementById('f-ph').value = data.soil_ph;
    setSeg('mr', data.moisture_regime);
    setSeg('tr', data.thermal_regime);
    document.getElementById('f-nb').value = data.nutrient_balance;
    alert('Data loaded from local storage!');
  }}
}}

// Auto-load saved data on page load
window.addEventListener('load', function() {{
  loadFromLocal();
}});

async function runPredict(){{
  var btn=document.getElementById('pred-btn');
  btn.disabled=true;
  btn.innerHTML='<span class="spin"></span>Processing...';
  var payload={{
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
  }};
  var area=document.getElementById('result-area');
  try{{
    var res=await fetch('{API_URL}',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(payload)}});
    if(res.ok){{
      var data=await res.json();
      if('prediction' in data){{
        if(data.prediction===1){{
          area.innerHTML='<div class="result-box result-ok"><div class="result-icon">✓</div><div><div class="r-title">Suitable — Tanaman bisa tumbuh!</div><div class="r-sub">Kondisi lingkungan dan tanah mendukung pertumbuhan tanaman.' + (data.confidence ? ' (Confidence: ' + (data.confidence*100).toFixed(1) + '%)' : '') + '</div></div></div>';
        }} else {{
          area.innerHTML='<div class="result-box result-no"><div class="result-icon">✗</div><div><div class="r-title">Not Suitable — Kondisi kurang mendukung</div><div class="r-sub">Beberapa parameter perlu diperbaiki sebelum menanam.' + (data.confidence ? ' (Confidence: ' + (data.confidence*100).toFixed(1) + '%)' : '') + '</div></div></div>';
        }}
      }} else {{
        area.innerHTML='<div class="result-box result-no"><div class="result-icon">!</div><div><div class="r-title">Terjadi kesalahan</div><div class="r-sub">'+(data.error||'Unknown error')+'</div></div></div>';
      }}
    }} else {{
      area.innerHTML='<div class="result-box result-no"><div class="result-icon">!</div><div><div class="r-title">Backend tidak merespon</div><div class="r-sub">Pastikan server FastAPI berjalan di port 8000. Jalankan: uvicorn app:app --reload</div></div></div>';
    }}
  }} catch(e){{
    area.innerHTML='<div class="result-box result-no"><div class="result-icon">!</div><div><div class="r-title">Tidak dapat terhubung ke backend</div><div class="r-sub">Pastikan server FastAPI berjalan. Error: '+e.message+'</div></div></div>';
  }}
  btn.disabled=false;
  btn.textContent='Predict Again';
}}
</script>
</body>
</html>
"""

components.html(HTML, height=700, scrolling=False)