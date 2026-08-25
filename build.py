#!/usr/bin/env python3
"""Builds the full septicsystemcostcalculator.com static site."""
import os, re, json, shutil
from statedata import SC

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
SITE = "https://septicsystemcostcalculator.com"
BRAND = "Septic System Cost Calculator"

STATES = {}
with open(os.path.join(ROOT, "assets", "states.js")) as f:
    src = f.read()
for m in re.finditer(r'^\s*(\w{2}):\{n:"([^"]+)",gpd:(\d+),min:(\d+),tier:([\d.]+),ag:"([^"]+)"\}', src, re.M):
    a, n, g, mn, t, ag = m.groups()
    STATES[a] = dict(n=n, gpd=int(g), min=int(mn), tier=float(t), ag=ag)
assert len(STATES) == 50, len(STATES)

SOILS = [
    ("Gravel / coarse sand", "Under 5", "1.20"),
    ("Sand", "5 – 15", "0.80"),
    ("Sandy loam", "16 – 30", "0.60"),
    ("Loam", "31 – 45", "0.45"),
    ("Silt loam", "46 – 60", "0.30"),
    ("Clay loam", "61 – 90", "0.20"),
    ("Clay", "Over 90", "0.10"),
]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700'
         '&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap" rel="stylesheet">')


def page(path, title, desc, body, depth=0, extra_head="", schema=None):
    up = "../" * depth
    d = os.path.dirname(path)
    base = "/" + (d + "/" if d else "")
    canon_path = path[:-5] if path.endswith(".html") else path
    if canon_path.endswith("index"): canon_path = canon_path[:-5]
    canon = f"{SITE}/{canon_path}".rstrip("/") or SITE
    if canon == SITE: canon = SITE + "/"
    sch = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<base href="{base}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#102A42">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="shortcut icon" href="/favicon.svg">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-09QK62LXNY"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-09QK62LXNY');</script>

{FONTS}
<link rel="stylesheet" href="{up}assets/site.css">
{extra_head}{sch}
</head>
<body>
{header(up)}
{body}
{footer(up)}
<script src="{up}assets/states.js"></script>
<script src="{up}assets/calc.js"></script>
</body>
</html>"""
    html = re.sub(r'href="([^"]*?)index\.html"', lambda m: 'href="' + (m.group(1) or "./") + '"', html)
    html = re.sub(r'href="([^"]*?)\.html"', r'href="\1"', html)
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as fh:
        fh.write(html)


def header(up):
    return f"""<div class="util"><div class="shell">
<span><b>All 50 states</b> covered</span>
<span>Sizing from published state code</span>
<span>Free quotes, no obligation</span>
</div></div>
<header class="masthead"><div class="shell">
<a class="brand" href="{up}index.html"><span class="mk"></span>Septic System<br>Cost Calculator</a>
<button class="navtoggle" aria-label="Menu" aria-expanded="false" onclick="this.classList.toggle('open');this.setAttribute('aria-expanded',this.classList.contains('open'));document.getElementById('nav').classList.toggle('open')"><span></span><span></span><span></span></button>
<nav class="nav" id="nav">
  <a href="{up}calculator/cost.html">Cost</a>
  <a href="{up}calculator/replacement.html">Replacement</a>
  <a href="{up}calculator/index.html">Tank size</a>
  <a href="{up}states/index.html">States</a>
  <a href="{up}guides/index.html">Guides</a>
  <a class="btn" href="{up}septic-installers-near-me.html">Get quotes</a>
</nav></div></header>"""


def footer(up):
    return f"""<footer class="foot"><div class="shell">
<div class="grid g4">
  <div>
    <a class="brand" href="{up}index.html" style="color:#fff"><span class="mk"></span>Septic System Cost Calculator</a>
    <p style="margin-top:14px">Tank sizing, drainfield area, install cost, and pump-out timing — worked from the code minimums in all 50 states.</p>
  </div>
  <div><h4>Calculators</h4><ul>
    <li><a href="{up}calculator/cost.html">Installation cost</a></li>
    <li><a href="{up}calculator/replacement.html">Replacement cost</a></li>
    <li><a href="{up}calculator/pumping-cost.html">Pumping cost</a></li>
    <li><a href="{up}calculator/index.html">Tank size</a></li>
    <li><a href="{up}calculator/drainfield.html">Drainfield size</a></li>
    <li><a href="{up}calculator/pump-schedule.html">Pump-out schedule</a></li>
  </ul></div>
  <div><h4>Guides</h4><ul>
    <li><a href="{up}guides/septic-basics.html">How septic systems work</a></li>
    <li><a href="{up}guides/drainfield.html">Drainfields explained</a></li>
    <li><a href="{up}guides/costs.html">What it really costs</a></li>
    <li><a href="{up}guides/maintenance.html">Maintenance schedule</a></li>
    <li><a href="{up}guides/soil-testing.html">Perc and soil testing</a></li>
    <li><a href="{up}guides/troubleshooting.html">Failure symptoms</a></li>
  </ul></div>
  <div><h4>Reference</h4><ul>
    <li><a href="{up}states/index.html">State requirements</a></li>
    <li><a href="{up}tank-size-chart.html">Tank size chart</a></li>
    <li><a href="{up}septic-tank-dimensions.html">Tank dimensions</a></li>
    <li><a href="{up}septic-installers-near-me.html">Find installers</a></li>
    <li><a href="{up}faq.html">Questions</a></li>
    <li><a href="{up}about.html">About</a></li>
    <li><a href="{up}privacy.html">Privacy</a></li>
    <li><a href="{up}terms.html">Terms</a></li>
  </ul></div>
</div>
<p class="disc"><b>Estimates only.</b> This site works from published state minimums and standard engineering practice. It is not a system design and it does not replace a soil evaluation, a licensed designer, or your local health department, all of which can require more than the state minimum. Confirm every figure before you dig, order, or sign.<br><br>© 2026 Septic System Cost Calculator.</p>
</div></footer>"""


def crumb(up, items):
    parts = [f'<a href="{up}index.html">Home</a>']
    for label, href in items[:-1]:
        parts.append(f'<a href="{up}{href}">{label}</a>')
    parts.append(items[-1][0])
    return f'<div class="shell"><div class="crumb">{" / ".join(parts)}</div></div>'


# ---------------------------------------------------------------- signature
SOIL_PROFILE = """
<figure class="profile">
<svg viewBox="0 0 560 380" role="img" aria-label="Cross-section of a septic system showing the tank, distribution box, and drainfield trenches through soil layers">
  <defs>
    <pattern id="grit" width="7" height="7" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="0.9" fill="#00000018"/><circle cx="5.5" cy="5" r="0.7" fill="#00000012"/>
    </pattern>
  </defs>
  <rect x="0" y="0" width="560" height="66" fill="#F3F6F8"/>
  <rect x="0" y="66" width="560" height="52" fill="#6E5B43"/>
  <rect x="0" y="118" width="560" height="86" fill="#8A7355"/>
  <rect x="0" y="204" width="560" height="96" fill="#A98F6B"/>
  <rect x="0" y="300" width="560" height="80" fill="#7E8B93"/>
  <rect x="0" y="66" width="560" height="314" fill="url(#grit)"/>

  <!-- house -->
  <path d="M34 62 L34 34 L58 16 L82 34 L82 62 Z" fill="#17242F"/>
  <rect x="52" y="44" width="12" height="18" fill="#DE5A0C"/>
  <!-- sewer line -->
  <path d="M82 58 L128 70" stroke="#17242F" stroke-width="4" fill="none"/>

  <!-- tank -->
  <rect x="128" y="70" width="128" height="86" rx="4" fill="#102A42"/>
  <rect x="136" y="112" width="112" height="38" fill="#1C4067"/>
  <rect x="136" y="104" width="112" height="8" fill="#DE5A0C" opacity=".85"/>
  <rect x="152" y="58" width="16" height="14" fill="#17242F"/>
  <rect x="216" y="58" width="16" height="14" fill="#17242F"/>

  <!-- d-box -->
  <rect x="286" y="96" width="28" height="26" rx="3" fill="#17242F"/>
  <path d="M256 112 L286 110" stroke="#17242F" stroke-width="4"/>

  <!-- trenches -->
  <g fill="#C6D2DB">
    <rect x="344" y="140" width="188" height="20" rx="3"/>
    <rect x="344" y="176" width="188" height="20" rx="3"/>
    <rect x="344" y="212" width="188" height="20" rx="3"/>
  </g>
  <g fill="#102A42">
    <rect x="352" y="146" width="172" height="8" rx="4"/>
    <rect x="352" y="182" width="172" height="8" rx="4"/>
    <rect x="352" y="218" width="172" height="8" rx="4"/>
  </g>
  <path d="M314 108 L336 108 L336 150 M336 150 L336 186 M336 186 L336 222" stroke="#17242F" stroke-width="4" fill="none"/>

  <!-- percolation arrows -->
  <g stroke="#17242F" stroke-width="1.6" opacity=".45">
    <path d="M380 236 L380 264 M420 236 L420 272 M460 236 L460 264 M500 236 L500 270"/>
  </g>
  <g fill="#17242F" opacity=".45">
    <path d="M380 268 l-4 -8 h8 Z"/><path d="M420 276 l-4 -8 h8 Z"/>
    <path d="M460 268 l-4 -8 h8 Z"/><path d="M500 274 l-4 -8 h8 Z"/>
  </g>

  <!-- water table -->
  <path d="M0 306 H560" stroke="#DE5A0C" stroke-width="2" stroke-dasharray="7 5"/>

  <!-- labels -->
  <g font-family="IBM Plex Mono, monospace" font-size="10.5" fill="#17242F" letter-spacing=".06em">
    <text x="132" y="176">TANK</text>
    <text x="278" y="140">D-BOX</text>
    <text x="392" y="130">ABSORPTION TRENCHES</text>
    <text x="8" y="322" fill="#F3F6F8">SEASONAL HIGH WATER TABLE</text>
    <text x="470" y="60" fill="#8A9AA6">GRADE</text>
  </g>
</svg>
<figcaption><span>Conventional gravity system</span><span>Section view</span></figcaption>
</figure>"""


def quote_form(context="a new septic system", state=""):
    return f"""<form class="quote js-quote" action="https://formsubmit.co/bossdynamo61@gmail.com" method="POST">
<input type="hidden" name="_subject" value="New septic lead \u2014 septicsystemcostcalculator.com">
<input type="hidden" name="_captcha" value="false">
<input type="hidden" name="_template" value="table">
<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
<input type="hidden" name="page_state" value="{state}">
<h3>Compare local installers</h3>
<p>Send these numbers to licensed contractors near you and get quotes for {context}. Free, and no obligation to hire.</p>
<div class="field" style="margin-bottom:14px"><label style="color:#fff">What do you need?</label>
<select name="service" required>
  <option value="">Select service type</option>
  <option>New installation</option>
  <option>Full system replacement</option>
  <option>Tank or drainfield repair</option>
  <option>Pumping / maintenance</option>
  <option>Inspection (buying or selling)</option>
</select></div>
<div class="row">
  <input type="text" name="name" placeholder="Full name" required aria-label="Full name">
  <input type="tel" name="phone" placeholder="Phone (10-digit US)" required aria-label="Phone" inputmode="tel" pattern="\\(?[2-9][0-9]{{2}}\\)?[\\-. ]?[0-9]{{3}}[\\-. ]?[0-9]{{4}}" title="Enter a 10-digit US phone number, e.g. 555-123-4567" maxlength="14">
</div>
<div class="row">
  <input type="email" name="email" placeholder="Email" required aria-label="Email">
  <input type="text" name="zip" placeholder="ZIP code" required aria-label="ZIP code" pattern="[0-9]{{5}}">
</div>
<button class="btn" type="submit">Get free quotes</button>
<p class="fine">Your details go to installers serving your ZIP code, and to no one else.</p>
</form>"""


# ---------------------------------------------------------------- calculators# ---------------------------------------------------------------- calculators
def tank_tool(preset=""):
    p = f' data-preset="{preset}"' if preset else ""
    return f"""<div class="tool">
<div class="tool-head"><strong>Tank size calculator</strong><span>Step 1 of 1</span></div>
<div class="tool-body">
  <p class="err" id="e-tank"></p>
  <div class="row">
    <div class="field"><label for="state">State</label>
      <select id="state" class="js-states"{p}><option value="">Select a state</option></select>
      <p class="hint">Sets the design flow and the legal minimum.</p></div>
    <div class="field"><label for="beds">Bedrooms</label>
      <div class="stepper"><button type="button" data-step="down" aria-label="Fewer bedrooms">−</button>
      <input id="beds" type="number" value="3" min="1" max="8" inputmode="numeric">
      <button type="button" data-step="up" aria-label="More bedrooms">+</button></div>
      <p class="hint">Code sizes on bedrooms, not people.</p></div>
  </div>
  <div class="field"><label for="soil">Soil type</label>
    <select id="soil" class="js-soils"></select>
    <p class="hint">Used to size the matching drainfield. Unsure? Sandy loam is the common default.</p></div>
  <div class="field">
    <label><input type="checkbox" id="disposal" style="width:auto;margin-right:8px"> Kitchen garbage disposal</label>
    <label style="margin-top:8px"><input type="checkbox" id="extras" style="width:auto;margin-right:8px"> Whirlpool tub or water softener discharge</label>
  </div>
  <button class="btn" id="go-tank" type="button">Calculate tank size</button>
</div>
<div class="spec" id="t-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="t-figure"></div></div>
  <div class="spec-list" id="t-rows"></div>
  <p class="note" id="t-note"></p>
</div>{quote_form("a tank this size")}</div>
</div>"""


FIELD_TOOL = """<div class="tool">
<div class="tool-head"><strong>Drainfield size calculator</strong><span>Absorption area</span></div>
<div class="tool-body">
  <p class="err" id="e-field"></p>
  <div class="row">
    <div class="field"><label for="dstate">State</label>
      <select id="dstate" class="js-states"><option value="">Select a state</option></select></div>
    <div class="field"><label for="dbeds">Bedrooms</label>
      <div class="stepper"><button type="button" data-step="down" aria-label="Fewer">−</button>
      <input id="dbeds" type="number" value="3" min="1" max="8" inputmode="numeric">
      <button type="button" data-step="up" aria-label="More">+</button></div></div>
  </div>
  <div class="field"><label for="dsoil">Soil texture at trench depth</label>
    <select id="dsoil" class="js-soils"></select>
    <p class="hint">From your perc test or soil evaluation. The number in brackets is minutes per inch.</p></div>
  <div class="field"><label for="dwidth">Trench width</label>
    <select id="dwidth"><option value="2">2 ft</option><option value="3" selected>3 ft</option><option value="4">4 ft</option><option value="5">5 ft</option></select></div>
  <button class="btn" id="go-field" type="button">Calculate absorption area</button>
</div>
<div class="spec" id="d-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="d-figure"></div></div>
  <div class="spec-list" id="d-rows"></div>
  <p class="note" id="d-note"></p>
</div>""" + quote_form("a drainfield of this size") + "</div>"

COST_TOOL = """<div class="tool">
<div class="tool-head"><strong>Installation cost estimator</strong><span>Materials, labour, permits</span></div>
<div class="tool-body">
  <p class="err" id="e-cost"></p>
  <div class="row">
    <div class="field"><label for="cstate">State</label>
      <select id="cstate" class="js-states"><option value="">Select a state</option></select></div>
    <div class="field"><label for="cbeds">Bedrooms</label>
      <div class="stepper"><button type="button" data-step="down" aria-label="Fewer">−</button>
      <input id="cbeds" type="number" value="3" min="1" max="8" inputmode="numeric">
      <button type="button" data-step="up" aria-label="More">+</button></div></div>
  </div>
  <div class="row">
    <div class="field"><label for="csoil">Soil type</label><select id="csoil" class="js-soils"></select></div>
    <div class="field"><label for="ctype">System type</label>
      <select id="ctype">
        <option value="conventional">Conventional gravity trenches</option>
        <option value="chamber">Chamber drainfield</option>
        <option value="mound">Mound system</option>
        <option value="aerobic">Aerobic treatment unit</option>
      </select>
      <p class="hint">Poor soil or a high water table usually forces a mound or aerobic system.</p></div>
  </div>
  <button class="btn" id="go-cost" type="button">Estimate cost</button>
</div>
<div class="spec" id="c-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="c-figure"></div></div>
  <div class="spec-list" id="c-rows"></div>
  <p class="note" id="c-note"></p>
</div>""" + quote_form("this installation") + "</div>"

REPL_TOOL = """<div class="tool">
<div class="tool-head"><strong>Septic replacement cost calculator</strong><span>Tank, field, or full system</span></div>
<div class="tool-body">
  <p class="err" id="e-repl"></p>
  <div class="row">
    <div class="field"><label for="rstate">State</label>
      <select id="rstate" class="js-states"><option value="">Select a state</option></select></div>
    <div class="field"><label for="rbeds">Bedrooms</label>
      <div class="stepper"><button type="button" data-step="down" aria-label="Fewer">&minus;</button>
      <input id="rbeds" type="number" value="3" min="1" max="8" inputmode="numeric">
      <button type="button" data-step="up" aria-label="More">+</button></div></div>
  </div>
  <div class="row">
    <div class="field"><label for="rscope">What needs replacing?</label>
      <select id="rscope">
        <option value="tank">Tank only</option>
        <option value="field">Drainfield only</option>
        <option value="full" selected>Complete system</option>
      </select>
      <p class="hint">Most failures are the drainfield. A cracked or collapsed tank is rarer.</p></div>
    <div class="field"><label for="rsoil">Soil type</label><select id="rsoil" class="js-soils"></select></div>
  </div>
  <button class="btn" id="go-repl" type="button">Estimate replacement cost</button>
</div>
<div class="spec" id="r-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="r-figure"></div></div>
  <div class="spec-list" id="r-rows"></div>
  <p class="note" id="r-note"></p>
</div>""" + quote_form("this replacement") + "</div>"

PCOST_TOOL = """<div class="tool">
<div class="tool-head"><strong>Septic tank pumping cost calculator</strong><span>Service pricing</span></div>
<div class="tool-body">
  <p class="err" id="e-pcost"></p>
  <div class="row">
    <div class="field"><label for="pcstate">State</label>
      <select id="pcstate" class="js-states"><option value="">Select a state</option></select></div>
    <div class="field"><label for="pctank">Tank size</label>
      <select id="pctank">
        <option>750</option><option selected>1000</option><option>1250</option>
        <option>1500</option><option>2000</option><option>2500</option>
      </select></div>
  </div>
  <div class="field">
    <label><input type="checkbox" id="pcdig" style="width:auto;margin-right:8px"> Lid is buried (needs locating and digging)</label>
    <label style="margin-top:8px"><input type="checkbox" id="pcfilter" style="width:auto;margin-right:8px"> Clean the effluent filter too</label>
  </div>
  <button class="btn" id="go-pcost" type="button">Estimate pumping cost</button>
</div>
<div class="spec" id="pc-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="pc-figure"></div></div>
  <div class="spec-list" id="pc-rows"></div>
  <p class="note" id="pc-note"></p>
</div>""" + quote_form("a pump-out") + "</div>"

PUMP_TOOL = """<div class="tool">
<div class="tool-head"><strong>Pump-out schedule calculator</strong><span>Service interval</span></div>
<div class="tool-body">
  <p class="err" id="e-pump"></p>
  <div class="row">
    <div class="field"><label for="ptank">Tank capacity</label>
      <select id="ptank">
        <option>750</option><option selected>1000</option><option>1250</option>
        <option>1500</option><option>2000</option><option>2500</option><option>3000</option>
      </select>
      <p class="hint">On the permit, or stamped on the tank lid.</p></div>
    <div class="field"><label for="people">People in the house</label>
      <div class="stepper"><button type="button" data-step="down" aria-label="Fewer">−</button>
      <input id="people" type="number" value="4" min="1" max="12" inputmode="numeric">
      <button type="button" data-step="up" aria-label="More">+</button></div></div>
  </div>
  <div class="field"><label><input type="checkbox" id="pdisposal" style="width:auto;margin-right:8px"> Garbage disposal in regular use</label></div>
  <button class="btn" id="go-pump" type="button">Calculate interval</button>
</div>
<div class="spec" id="p-spec"><div class="spec-inner">
  <div class="spec-top"><div class="figure" id="p-figure"></div></div>
  <div class="spec-list" id="p-rows"></div>
  <p class="note" id="p-note"></p>
</div>""" + quote_form("a pump-out and inspection") + "</div>"


# ---------------------------------------------------------------- pages
def build_home():
    chips = "".join(
        f'<a class="chip" href="states/{k}.html">{v["n"]}<b>{k.upper()}</b></a>'
        for k, v in sorted(STATES.items(), key=lambda x: x[1]["n"]))
    body = f"""
<section class="hero"><div class="shell"><div class="hero-grid">
  <div>
    <p class="eyebrow o">Free septic calculator</p>
    <h1>What will a septic system <span>cost you?</span></h1>
    <p class="lede">Answer two questions. Get the tank size, the drainfield area, and a real installed price range for your state — before a contractor quotes you.</p>
    <div class="hero-cta">
      <a class="btn" href="calculator/cost.html">Estimate my cost</a>
      <a class="btn ghost" href="calculator/index.html">Size a tank</a>
    </div>
    <div class="trust">
      <div><b>50</b>states covered</div>
      <div><b>4</b>calculators</div>
      <div><b>$0</b>to use</div>
    </div>
  </div>
  {SOIL_PROFILE}
</div></div></section>

<section class="band"><div class="shell">
  {COST_TOOL}
</div></section>

<section class="band white"><div class="shell">
  <div class="band-head"><p class="eyebrow">Four calculators</p><h2>Each one answers a different question</h2>
  <p>Pick the one closest to what you are trying to settle. Each has a companion guide that explains the reasoning behind the number.</p></div>
  <div class="grid g4">
    <a class="card" href="calculator/index.html"><p class="kicker">Sizing</p><h3>Tank size</h3><p>Capacity from bedrooms and your state's minimum.</p></a>
    <a class="card" href="calculator/drainfield.html"><p class="kicker">Absorption</p><h3>Drainfield size</h3><p>Square footage and trench length from your soil.</p></a>
    <a class="card" href="calculator/cost.html"><p class="kicker">Budget</p><h3>Install cost</h3><p>Tank, field, excavation, permits, by region.</p></a>
    <a class="card" href="calculator/replacement.html"><p class="kicker">Replacement</p><h3>Replacement cost</h3><p>Tank, drainfield, or full system \u2014 with removal.</p></a>
  </div>
  <div class="grid g3" style="margin-top:14px">
    <a class="card" href="calculator/pumping-cost.html"><p class="kicker">Service</p><h3>Pumping cost</h3><p>What a pump-out runs, by tank size and state.</p></a>
    <a class="card" href="calculator/pump-schedule.html"><p class="kicker">Upkeep</p><h3>Pump schedule</h3><p>How many years between pump-outs, and why.</p></a>
    <a class="card" href="septic-installers-near-me.html"><p class="kicker">Local quotes</p><h3>Find installers near you</h3><p>Free quotes from licensed contractors in your ZIP.</p></a>
  </div>
</div></section>

<section class="band ink"><div class="shell">
  <div class="band-head"><p class="eyebrow">Why the number matters</p><h2>An undersized tank is a drainfield problem, not a tank problem</h2>
  <p>Wastewater needs roughly two days in the tank for solids to settle and grease to rise. Take that time away and the solids leave with the effluent.</p></div>
  <div class="scroll"><table class="tbl">
    <tr><th>Effect</th><th>Undersized</th><th>Correctly sized</th><th>Oversized</th></tr>
    <tr><td>Retention time</td><td>Under 24 hours</td><td><b>24 – 48 hours</b></td><td>Over 72 hours</td></tr>
    <tr><td>What reaches the field</td><td>Solids and grease</td><td><b>Settled effluent</b></td><td>Settled effluent</td></tr>
    <tr><td>Pump-out interval</td><td>1 – 2 years</td><td><b>3 – 5 years</b></td><td>5 – 7 years</td></tr>
    <tr><td>Field service life</td><td>Cut short, often badly</td><td><b>20 – 30 years</b></td><td>20 – 30 years</td></tr>
    <tr><td>Cost over 25 years</td><td>Highest — a field replacement</td><td><b>Lowest</b></td><td>Higher up front, no gain</td></tr>
  </table></div>
  <p style="margin-top:20px;max-width:62ch;color:#9FADA6">Replacing a clogged drainfield runs many times the price of the extra tank capacity that would have prevented it. That is the whole argument for getting the sizing right the first time.</p>
</div></section>

<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">State code</p><h2>Requirements change at every state line</h2>
  <p>Minimum tank size, design flow per bedroom, setbacks, and who issues the permit all vary. Pick your state for the rules that actually apply.</p></div>
  <div class="chips">{chips}</div>
</div></section>

<section class="band white"><div class="shell">
  <div class="band-head"><p class="eyebrow">Background</p><h2>Read before you commit money</h2></div>
  <div class="grid g3">
    <a class="card" href="guides/septic-basics.html"><p class="kicker">Guide</p><h3>How a septic system works</h3><p>Tank, distribution box, drainfield, and soil — what each part does.</p></a>
    <a class="card" href="guides/soil-testing.html"><p class="kicker">Guide</p><h3>Perc tests and soil evaluation</h3><p>The test that decides what system you are allowed to build.</p></a>
    <a class="card" href="guides/costs.html"><p class="kicker">Guide</p><h3>Where the money goes</h3><p>A line-by-line breakdown, plus the extras that blow up quotes.</p></a>
    <a class="card" href="guides/drainfield.html"><p class="kicker">Guide</p><h3>Drainfields explained</h3><p>Five field types, and how to get 25 years out of one.</p></a>
    <a class="card" href="guides/maintenance.html"><p class="kicker">Guide</p><h3>Maintenance that matters</h3><p>The short list of habits that decide system life.</p></a>
    <a class="card" href="guides/troubleshooting.html"><p class="kicker">Guide</p><h3>Reading the symptoms</h3><p>Slow drains, wet spots, odours — what each one means.</p></a>
  </div>
</div></section>

<section class="band"><div class="shell narrow">
  <div class="band-head"><p class="eyebrow">Common questions</p><h2>Quick answers</h2></div>
  {faq_block(FAQS[:5])}
  <p style="margin-top:20px"><a href="faq.html">All questions →</a></p>
</div></section>
"""
    page("index.html", "Septic System Cost Calculator — All 50 States",
         "What does a septic system cost? Free calculators for installation cost, replacement cost, tank size and drainfield area — adjusted for all 50 states.",
         body, 0, schema=faq_schema(FAQS[:5]))


FAQS = [
    ("What size septic tank do I need for a 3 bedroom house?",
     "In most states a three-bedroom home requires a minimum 1,000 gallon tank. That figure comes from a design flow of about 150 gallons per bedroom per day and a two-day retention requirement. Massachusetts sets a 1,500 gallon floor, California commonly requires 1,200, and a handful of states allow 900. A garbage disposal, a whirlpool tub, or a water softener discharging to the tank each push the requirement up a size."),
    ("How is design flow calculated?",
     "Design flow is bedrooms multiplied by the gallons per bedroom per day your state allows — usually 150, though Massachusetts uses 110 and North Carolina and Washington commonly use 120. Codes size on bedrooms rather than occupants because the house outlives the household, and a bedroom count is what a future buyer inherits."),
    ("How often should a septic tank be pumped?",
     "Every three to five years for a typical family of four on a 1,000 gallon tank. The real driver is how fast solids fill the tank: roughly 30 gallons per person per year, half again as much with a garbage disposal in regular use. Pumping is due once solids occupy about a third of the volume. Small tank plus large household can mean every two years."),
    ("What decides drainfield size?",
     "Two things: your design flow, and how quickly the soil accepts water. Absorption area equals daily flow divided by the soil application rate. Sandy loam accepts about 0.60 gallons per square foot per day; clay accepts around 0.10. Same house, same flow — the clay site needs roughly six times the field area, if a conventional field is permitted there at all."),
    ("Do I need a permit to install a septic system?",
     "Yes, everywhere in the United States. A permit for a new system normally requires a soil evaluation or perc test, a site plan showing setbacks from wells, property lines and surface water, a system design, and an inspection before the trenches are backfilled. Installing without one risks fines and an order to dig it up."),
    ("Can I install a septic system myself?",
     "Some states allow a homeowner to install a system on property they occupy; many require a licensed installer. Even where self-installation is legal, the design, the soil evaluation, and the inspections still have to be done by qualified parties, and a failed inspection after backfilling is expensive. Check with the agency listed on your state page before planning around it."),
    ("How long does a septic system last?",
     "A well-sized tank lasts 30 to 40 years in concrete, longer in plastic or fibreglass if it was installed correctly. The drainfield is the part that fails: 20 to 30 years is normal, and far less if it takes solids from a neglected tank, sits under vehicle traffic, or receives more water than it was designed for."),
    ("What is a perc test?",
     "A percolation test measures how many minutes the soil takes to absorb one inch of water. The result, expressed in minutes per inch, sets the application rate used to size your drainfield. Many states have moved to a full soil morphology evaluation instead — a licensed evaluator digs a pit and reads the soil profile, which gives a more reliable answer than a single hole."),
    ("Does a bigger tank mean I can pump less often?",
     "Yes, up to a point. Doubling capacity roughly doubles the interval between pump-outs, because solids accumulate at a rate set by the household, not the tank. What a bigger tank does not do is let you skip inspections, and beyond a certain size the extra volume buys nothing except a larger bill."),
    ("Where can the drainfield not go?",
     "Typical setbacks keep the field at least 100 feet from a well, 50 feet from surface water, 10 feet from property lines, and clear of driveways, parking, and building foundations. Trees within about 30 feet are a risk because roots find the trenches. Your state and county set the exact distances, and they are not negotiable at inspection."),
]


def faq_block(items):
    return "".join(
        f'<details class="faq"><summary>{q}</summary><div class="body">{a}</div></details>'
        for q, a in items)


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def build_calculators():
    page("calculator/index.html", "Septic Tank Size Calculator by State & Bedrooms",
         "Work out the septic tank size you need from bedroom count and your state's minimum. Returns capacity, design flow, matching drainfield area and pump interval.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Tank size", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Calculator</p><h1>Septic tank size calculator</h1>
  <p>Capacity is set by design flow and a two-day retention requirement, then raised to whichever standard tank size clears your state's minimum.</p></div>
  {tank_tool()}
</div></section>
<section class="band white"><div class="shell narrow prose">
  <h2>How the number is worked out</h2>
  <p>Three steps, in this order.</p>
  <ol>
    <li><b>Design flow.</b> Bedrooms times the gallons per bedroom per day your state allows — 150 in most, 110 in Massachusetts, 120 in North Carolina and Washington. Codes count bedrooms rather than people because a house outlives its household.</li>
    <li><b>Working volume.</b> Two days of design flow, so solids have time to settle and grease has time to rise. A garbage disposal adds about 250 gallons; a whirlpool tub or a water softener discharging to the tank adds a similar amount.</li>
    <li><b>Code floor.</b> Whichever is larger — the calculated volume or the state minimum — rounded up to the next tank actually manufactured: 750, 1,000, 1,250, 1,500, 2,000 gallons and up.</li>
  </ol>
  <h2>What this does not include</h2>
  <p>Counties and health districts routinely set stricter rules than the state, and a soil evaluation can change the design entirely. Treat the result as the number to walk into that conversation with, not the number to order a tank against.</p>
  <p><a href="../guides/septic-basics.html">How septic systems work →</a></p>
</div></section>""", 1)

    page("calculator/drainfield.html", "Drainfield Size Calculator by Soil Type",
         "Calculate the drainfield absorption area and trench length you need, from design flow and soil texture. Covers all seven soil classes and all 50 states.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Drainfield", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Calculator</p><h1>Drainfield size calculator</h1>
  <p>Absorption area is daily flow divided by how fast the soil accepts water. Soil texture matters more here than anything else on the site.</p></div>
  {FIELD_TOOL}
</div></section>
<section class="band white"><div class="shell prose">
  <h2>Application rates by soil texture</h2>
  <p>These are conventional trench loading rates. Your state may publish slightly different figures, and a soil evaluator's reading of the actual profile always wins.</p>
  <div class="scroll"><table class="tbl">
  <tr><th>Soil texture</th><th>Perc rate (min/inch)</th><th>Application rate (gpd/sq ft)</th><th>Area for 450 gpd</th></tr>
  """ + "".join(
             f"<tr><td>{n}</td><td>{p}</td><td><b>{r}</b></td><td>{round(450/float(r)):,} sq ft</td></tr>"
             for n, p, r in SOILS) + """
  </table></div>
  <h2>Reserve area</h2>
  <p>Most states require a second area of equal size, kept clear and undisturbed, as the replacement field. It is part of the permit even though nothing is built there. Plan the driveway, the shed and the pool around it, because a lot is only buildable if both areas fit.</p>
  <p><a href="../guides/drainfield.html">Full drainfield guide →</a></p>
</div></section>""", 1)

    page("calculator/cost.html", "Septic System Cost Calculator by State",
         "Estimate what a septic system installation costs: tank, drainfield, excavation, soil evaluation and permits, adjusted for your state and system type.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Cost", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Calculator</p><h1>Septic system cost estimator</h1>
  <p>A range for a new install on accessible ground, built up from tank, field, excavation, soil evaluation and permits, then adjusted for regional labour.</p></div>
  {COST_TOOL}
</div></section>
<section class="band white"><div class="shell prose">
  <h2>What drives the price</h2>
  <p>Soil and system type, far more than house size. The same three-bedroom house costs one figure on sandy loam with a gravity field, and two to three times that on clay where a mound is the only permitted option.</p>
  <h2>What pushes a quote past the estimate</h2>
  <ul>
    <li>Rock or a high water table found during excavation</li>
    <li>Removing and decommissioning an old tank</li>
    <li>Long or steep access for heavy equipment</li>
    <li>A pump chamber, when the field sits above the house</li>
    <li>Engineered designs where a county requires a stamped plan</li>
    <li>Restoring lawn, drive or landscaping afterwards</li>
  </ul>
  <h2>Comparing quotes properly</h2>
  <p>Get three, and make each one itemise the tank size and material, the absorption area in square feet, the system type, and who pulls the permit. A cheap quote is usually a smaller field or an excluded permit, not a better deal. Ask what happens if rock is hit — a fixed price and an hourly rate are very different bids.</p>
  <p><a href="../guides/costs.html">Full cost guide →</a></p>
</div></section>""", 1)

    page("calculator/pump-schedule.html", "Septic Tank Pumping Frequency Calculator",
         "Work out how many years between septic tank pump-outs, based on tank capacity, household size and whether you run a garbage disposal.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Pump schedule", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Calculator</p><h1>Pump-out schedule calculator</h1>
  <p>Solids build at a rate set by the household, not the tank. Pumping is due once they reach about a third of capacity.</p></div>
  {PUMP_TOOL}
</div></section>
<section class="band white"><div class="shell prose">
  <h2>Typical intervals</h2>
  <div class="scroll"><table class="tbl">
  <tr><th>Tank</th><th>2 people</th><th>4 people</th><th>6 people</th></tr>
  """ + "".join(
             f"<tr><td><b>{g:,} gal</b></td>" + "".join(
                 f"<td>{round((0.32*g)/(30*p),1)} yrs</td>" for p in (2, 4, 6)) + "</tr>"
             for g in (750, 1000, 1250, 1500, 2000)) + """
  </table></div>
  <p>Subtract roughly a third from these if a garbage disposal runs daily.</p>
  <h2>Why the interval is not optional</h2>
  <p>Pumping costs a few hundred dollars. What it protects is the drainfield, which costs thousands to replace and cannot be unclogged once solids have sealed the soil surface. Everything else in septic maintenance is secondary to this one habit.</p>
  <p><a href="../guides/maintenance.html">Full maintenance guide →</a></p>
</div></section>""", 1)


def build_new_pages():
    # ---- REPLACEMENT COST (18K volume cluster, competitor weak) ----
    page("calculator/replacement.html",
         "Septic System Replacement Cost Calculator",
         "What does it cost to replace a septic tank, a failed drainfield, or a complete septic system? State-adjusted estimates including old-system removal and re-permitting.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Replacement cost", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow o">Replacement</p><h1>Septic system replacement cost</h1>
  <p>Replacing costs more than building new: the old system has to come out, crews work around an occupied home, and the new design must meet today's code \u2014 not the code your old system was built under.</p></div>
  {REPL_TOOL}
</div></section>
<section class="band white"><div class="shell prose">
  <h2>Septic tank replacement cost</h2>
  <p>A tank-only replacement typically runs <b>$3,500 to $9,500</b>: the new tank itself, pumping and crushing the old one in place or hauling it out, excavation, reconnecting inlet and outlet lines, and a permit with inspection. Concrete tanks cost more to remove than plastic. If the drainfield is healthy, nothing else changes.</p>
  <h2>Drainfield replacement cost</h2>
  <p>This is the expensive one \u2014 usually <b>$7,000 to $22,000</b>, and more where soil forces a mound or aerobic system. A failed field cannot be repaired once the soil surface has sealed with solids; it is abandoned and a new field is built in the reserve area. If your permit never set aside a reserve area, a new soil evaluation decides what is possible, and that uncertainty is why quotes vary so widely.</p>
  <h2>Complete system replacement</h2>
  <p>Everything: new tank, new field, old-system decommissioning, and a fresh permit. Expect <b>$12,000 to $35,000</b> depending on soil and state, at the top of that range where a conventional field is no longer permitted on your soil and an engineered system takes its place.</p>
  <h2>Why replacement exceeds new-construction cost</h2>
  <ul>
    <li><b>Removal.</b> Pumping, crushing or extracting the old tank adds $1,000\u2013$2,500.</li>
    <li><b>Occupied site.</b> Equipment works around the house, landscaping, driveway and utilities that did not exist when the original was built.</li>
    <li><b>Current code.</b> Many states require the replacement to meet today's standards \u2014 often a larger field, more separation, or added treatment.</li>
    <li><b>Urgency.</b> A failed system is not a project you can schedule for the off-season.</li>
  </ul>
  <h2>Signs you need replacement, not repair</h2>
  <p>Sewage surfacing over the field, backups that return after pumping, and persistently saturated ground point to a failed field. But rule out the cheap causes first: a tank overdue for pumping, a clogged effluent filter, or a settled distribution box produce identical symptoms and cost a few hundred dollars, not twenty thousand. Insist on a proper inspection before accepting a replacement quote.</p>
</div></section>""", 1)

    # ---- PUMPING COST (7K cluster) ----
    page("calculator/pumping-cost.html",
         "Septic Tank Pumping Cost Calculator",
         "How much does it cost to pump a septic tank? Estimate your pump-out price by tank size and state, including digging fees and filter cleaning.",
         crumb("../", [("Calculators", "calculator/index.html"), ("Pumping cost", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow o">Service pricing</p><h1>Septic tank pumping cost</h1>
  <p>Most households pay $300 to $650 for a pump-out. Tank size, region, and whether the truck can reach the lid decide where you land in that range.</p></div>
  {PCOST_TOOL}
</div></section>
<section class="band white"><div class="shell prose">
  <h2>What the pump-out includes</h2>
  <p>A proper service removes both liquid and solids \u2014 the sludge layer is the whole point \u2014 checks the baffles or effluent filter, and notes the condition of the tank. A truck that takes only the liquid and leaves compacted sludge behind has not pumped your tank, whatever the invoice says.</p>
  <h2>What adds to the price</h2>
  <ul>
    <li><b>Buried lids.</b> Locating and hand-digging to the lid commonly adds $100\u2013$250. Risers installed once eliminate this fee forever.</li>
    <li><b>Distance.</b> If the truck cannot park within roughly 100 feet of the tank, extra hose lengths add cost.</li>
    <li><b>Neglect.</b> A tank pumped after ten years instead of four has compacted sludge that takes longer to remove.</li>
    <li><b>Second compartment or second tank.</b> Two-compartment tanks and aerobic systems take more time.</li>
  </ul>
  <h2>How often it is due</h2>
  <p>Every three to five years for a family of four on a 1,000 gallon tank; sooner with a garbage disposal or a smaller tank. The <a href="pump-schedule.html">pump schedule calculator</a> works out your exact interval. Skipping the interval does not save money \u2014 it moves the cost to the drainfield, at roughly thirty times the price.</p>
</div></section>""", 1)

    # ---- TANK DIMENSIONS (12K cluster: "1500 gallon septic tank", "septic tank dimensions") ----
    dims = [
        ("750",  "4' x 8'",   "5' \u2013 5'6\"", "approx. 8,000 lb",  "1\u20132 bedroom homes, small cabins"),
        ("1000", "5' x 8'6\"","5' \u2013 6'",    "approx. 10,500 lb", "the standard 3-bedroom tank in most states"),
        ("1250", "5'6\" x 9'","5'6\" \u2013 6'","approx. 12,000 lb", "4-bedroom homes"),
        ("1500", "6' x 10'",  "5'6\" \u2013 6'6\"","approx. 14,000 lb","5-bedroom homes; the Massachusetts minimum"),
        ("2000", "6' x 12'",  "6' \u2013 7'",    "approx. 17,500 lb", "large homes, small commercial"),
    ]
    rows_html = "".join(
        f"<tr><td><b>{g} gal</b></td><td>{fp}</td><td>{h}</td><td>{w}</td><td>{use}</td></tr>"
        for g, fp, h, w, use in dims)
    page("septic-tank-dimensions.html",
         "Septic Tank Dimensions: 750 to 2,000 Gallons",
         "Standard septic tank dimensions: footprint, height, and weight for 750, 1000, 1250, 1500 and 2000 gallon concrete tanks, and how to know which size your home needs.",
         crumb("", [("Tank dimensions", "")]) + f"""
<section class="band"><div class="shell prose">
  <p class="eyebrow">Reference</p><h1>Septic tank dimensions</h1>
  <p class="lede" style="margin:18px 0 30px">Concrete tank dimensions vary a little by manufacturer, but the standard sizes cluster tightly. These are typical single-compartment concrete figures \u2014 plastic and fibreglass tanks run similar footprints at a fraction of the weight.</p>
  <div class="scroll"><table class="tbl">
    <tr><th>Capacity</th><th>Footprint (W x L)</th><th>Height</th><th>Weight (concrete)</th><th>Typical use</th></tr>{rows_html}
  </table></div>

  <h2>1000 gallon septic tank</h2>
  <p>The workhorse. Roughly 5 feet wide, 8 and a half feet long, and about 5 feet tall, weighing around five tons in concrete. It is the legal minimum for a three-bedroom home in most states, which makes it the most manufactured and usually the cheapest per gallon.</p>
  <h2>1500 gallon septic tank</h2>
  <p>About 6 by 10 feet and up to 6 and a half feet tall. It is the minimum for five-bedroom homes in most states \u2014 and the minimum for <em>every</em> home in Massachusetts under Title 5. If you are between sizes, the incremental cost of stepping up to 1,500 is small against the drainfield it protects.</p>
  <h2>How deep is a septic tank buried?</h2>
  <p>Typically the lid sits 4 inches to 4 feet below grade. Deeper burial needs risers to bring access to the surface \u2014 worth specifying on any new install, because every future pump-out otherwise starts with a shovel.</p>
  <h2>What size does your home need?</h2>
  <p>Capacity is set by bedrooms and your state's minimum, not by the tank that happens to fit the hole. Run the <a href="calculator/index.html">tank size calculator</a> for your state's figure, and see the <a href="tank-size-chart.html">size chart</a> for the full bedroom table.</p>
  <h2>Will it fit? Site clearances</h2>
  <p>The excavation runs about 2 feet larger than the tank on every side, and the delivery truck needs to park within boom reach \u2014 usually 15 feet of the hole for a standard boom truck. Tight urban lots sometimes dictate two smaller tanks in series, or a plastic tank that can be carried in.</p>
</div></section>""", 0)

    # ---- NEAR ME lead page (3.6K volume, competitor absent) ----
    page("septic-installers-near-me.html",
         "Septic Tank Installation Near Me \u2014 Free Quotes",
         "Find licensed septic system installers near you. Compare free quotes from local contractors for installation, replacement, repair and pumping.",
         crumb("", [("Find installers", "")]) + f"""
<section class="band"><div class="shell">
  <div class="hero-grid">
    <div>
      <p class="eyebrow o">Local quotes</p>
      <h1>Septic installers <span style="color:var(--orange)">near you</span></h1>
      <p class="lede">Tell us your ZIP code and what you need. Licensed septic contractors serving your area follow up with quotes \u2014 free, and nothing is booked until you choose one.</p>
      <div class="trust">
        <div><b>Free</b>quotes</div>
        <div><b>Licensed</b>contractors</div>
        <div><b>No</b>obligation</div>
      </div>
    </div>
    <div>{quote_form("your project")}</div>
  </div>
</div></section>
<section class="band white"><div class="shell prose">
  <h2>What to have ready before you call</h2>
  <p>Quotes get sharper when you can answer three questions: how many bedrooms the house has, what your soil is like (or whether a perc test exists), and whether this is new construction, a replacement, or a repair. Five minutes with the <a href="calculator/cost.html">cost calculator</a> arms you with the numbers a contractor will otherwise control.</p>
  <h2>How to compare septic quotes</h2>
  <p>Make every bid itemise the same four things: tank size and material, absorption area in square feet, system type, and who pulls the permit. A quote that is thousands cheaper is almost always one of those four being quietly smaller. Ask what happens if rock is found during excavation \u2014 a fixed price and an hourly rate are very different bids.</p>
  <h2>Checking a contractor properly</h2>
  <ul>
    <li>Licence for onsite/septic work in your state \u2014 most states license installers separately from general contractors, and your <a href="states/index.html">state page</a> names the licensing agency.</li>
    <li>Liability insurance, confirmed in writing.</li>
    <li>Local references from the last year \u2014 soil is local, and a contractor who works your county knows what the inspector wants to see.</li>
    <li>Who attends the inspection: the installer should be on site when the health department sees the open trenches.</li>
  </ul>
</div></section>""", 0)


def build_states():
    rows = "".join(
        f'<tr><td><a href="{k}.html">{v["n"]}</a></td><td><b>{v["min"]:,} gal</b></td>'
        f'<td><b>{v["gpd"]} gpd</b></td><td>{SC[k]["code"].split(",")[0]}</td></tr>'
        for k, v in sorted(STATES.items(), key=lambda x: x[1]["n"]))
    chips = "".join(
        f'<a class="chip" href="{k}.html">{v["n"]}<b>{k.upper()}</b></a>'
        for k, v in sorted(STATES.items(), key=lambda x: x[1]["n"]))
    page("states/index.html", "Septic Tank Requirements by State (All 50)",
         "Minimum septic tank size, design flow per bedroom, governing regulation and permitting authority for every US state.",
         crumb("../", [("State requirements", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Reference</p><h1>Septic requirements by state</h1>
  <p>Minimum tank size, design flow, and the governing regulation for all 50 states. Each page also covers local geology, which system types actually get built there, and the counties where the rules bite hardest.</p></div>
  <div class="chips" style="margin-bottom:34px">{chips}</div>
  <div class="scroll"><table class="tbl">
    <tr><th>State</th><th>Min tank (1–3 BR)</th><th>Design flow / bedroom</th><th>Governing regulation</th></tr>{rows}
  </table></div>
</div></section>""", 1)

    for k, v in STATES.items():
        c = SC[k]
        nm = v["n"]
        three = max(v["min"], 1000 if v["gpd"] * 3 * 2 <= 1000 else round(v["gpd"] * 3 * 2 / 250) * 250)
        four = max(1250, round(v["gpd"] * 4 * 2 / 250) * 250, v["min"])
        five = max(1500, round(v["gpd"] * 5 * 2 / 250) * 250, v["min"])
        two = v["min"]
        tbl = "".join(
            f"<tr><td>{b} bedroom{'s' if b > 1 else ''}</td><td>{v['gpd']*max(b,2):,} gpd</td><td><b>{s:,} gal</b></td><td>{s+250:,} gal</td></tr>"
            for b, s in [(1, two), (2, two), (3, three), (4, four), (5, five)])
        counties = "".join(
            f"<tr><td><b>{cn}</b></td><td>{note}</td></tr>" for cn, note in c["counties"])
        faqs = faq_block(c["faq"])
        flow3 = v["gpd"] * 3
        lo = int(round(9000 * v["tier"] / 100) * 100)
        hi = int(round(16000 * v["tier"] / 100) * 100)

        body = crumb("../", [("States", "states/index.html"), (nm, "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">{nm} · {c['code'].split(',')[0]}</p>
  <h1>Septic system requirements in {nm}</h1>
  <p>{c['frame']}</p></div>
  <div class="grid g3" style="margin-bottom:34px">
    <div class="card"><p class="kicker">Minimum tank</p><h3>{v['min']:,} gallons</h3><p>One to three bedroom dwelling.</p></div>
    <div class="card"><p class="kicker">Design flow</p><h3>{v['gpd']} gpd per bedroom</h3><p>Held two days for settling.</p></div>
    <div class="card"><p class="kicker">Cost index</p><h3>{int(round(v['tier']*100))}% of baseline</h3><p>Regional labour and permits.</p></div>
  </div>
  {tank_tool(k)}
</div></section>

<section class="band white"><div class="shell prose">
  <h2>The ground you are actually building on</h2>
  <p>{c['geology']}</p>

  <h2>What gets installed in {nm}</h2>
  <p>{c['systems']}</p>

  <h2>Tank size by bedroom count</h2>
  <div class="scroll"><table class="tbl">
    <tr><th>Dwelling</th><th>Design flow</th><th>Minimum tank</th><th>With disposal</th></tr>{tbl}
  </table></div>

  <h2>Getting a system permitted</h2>
  <p>{c['permit']}</p>
  <ol>
    <li><b>Soil evaluation.</b> On the actual field location, before design. It decides what you are allowed to build.</li>
    <li><b>Design and site plan.</b> Tank size, absorption area, and setbacks from wells, lines, water and foundations.</li>
    <li><b>Permit application.</b> Submitted with the soil report. Allow weeks, more in the spring rush.</li>
    <li><b>Installation.</b> By a licensed installer where {nm} requires one.</li>
    <li><b>Inspection before backfill.</b> Trenches must be seen open.</li>
  </ol>

  <h2>Counties where the local rules matter most</h2>
  <p>The state sets a floor. These {nm} counties are where the largest septic populations sit, and where local requirements most often exceed it.</p>
  <div class="scroll"><table class="tbl">
    <tr><th>County</th><th>What makes it different</th></tr>{counties}
  </table></div>

  <h2>Drainfield sizing in {nm}</h2>
  <p>A three-bedroom home at {v['gpd']} gallons per bedroom produces {flow3:,} gallons per day of design flow. On sandy loam that needs roughly {round(flow3/0.6):,} square feet of absorption area. On clay loam it rises to about {round(flow3/0.2):,} square feet, and on clay a conventional field is usually not permitted at all. Run your own soil class through the <a href="../calculator/drainfield.html">drainfield calculator</a>.</p>

  <h2>Maintenance and inspection</h2>
  <p>{c['pump']} Use the <a href="../calculator/pump-schedule.html">pump schedule calculator</a> to work out the interval for your tank size and household.</p>

  <h2>Septic system cost in {nm}</h2>
  <p>Regional labour and permit costs in {nm} run about {int(round(v['tier']*100))}% of the national baseline. Here is what typical installations land at for a three-bedroom home:</p>
  <div class="scroll"><table class="tbl">
    <tr><th>System type</th><th>Typical installed cost in {nm}</th><th>When it applies</th></tr>
    <tr><td>Conventional gravity</td><td><b>${lo:,} \u2013 ${hi:,}</b></td><td>Good soil, adequate depth to water</td></tr>
    <tr><td>Chamber system</td><td><b>${int(round(lo*1.1/100)*100):,} \u2013 ${int(round(hi*1.15/100)*100):,}</b></td><td>Alternative to gravel trenches</td></tr>
    <tr><td>Mound system</td><td><b>${int(round(lo*1.9/100)*100):,} \u2013 ${int(round(hi*2.1/100)*100):,}</b></td><td>Shallow water table or thin soil</td></tr>
    <tr><td>Aerobic treatment</td><td><b>${int(round(lo*1.6/100)*100):,} \u2013 ${int(round(hi*1.8/100)*100):,}</b></td><td>Clay soil or small lots</td></tr>
    <tr><td>Tank pump-out (service)</td><td><b>${int(round(320*v['tier']/10)*10):,} \u2013 ${int(round(650*v['tier']/10)*10):,}</b></td><td>Every 3\u20135 years</td></tr>
  </table></div>
  <p>Replacing an existing system costs more than these figures \u2014 old-system removal and re-permitting add to every line. The <a href="../calculator/replacement.html">replacement cost calculator</a> covers that case, and the <a href="../calculator/cost.html">cost estimator</a> adjusts all of the above for your bedroom count and soil.</p>

  <h2>Questions specific to {nm}</h2>
  {faqs}

  <p class="note" style="border-left:3px solid var(--marker);background:var(--white);padding:14px 16px;margin-top:32px">
  <b>Verify before you build.</b> The figures above are state minimums compiled for planning, drawn from {c['code']}. County and health district rules routinely exceed them, code text changes, and only {v['ag']} or your local health department can confirm what applies to your parcel.</p>
</div></section>

<section class="band"><div class="shell narrow">
  <div class="band-head"><h2>Get quotes in {nm}</h2>
  <p>Send your sizing numbers to installers who work under {nm} rules every day.</p></div>
  {quote_form('a system in ' + nm, k)}
</div></section>"""
        page(f"states/{k}.html",
             f"{nm} Septic Requirements: Tank Size & Cost",
             f"Septic requirements in {nm}: {v['min']:,} gallon minimum tank, {v['gpd']} gpd per bedroom, permitting under {c['code'].split(',')[0]}, local soil conditions and county rules.",
             body, 1, schema=faq_schema(c["faq"]))


GUIDES = [
    ("septic-basics", "How Septic Systems Work", "How a septic system works — tank, distribution box, drainfield and soil, and what each part actually does.", """
<h2>Four parts, one job</h2>
<p>A septic system takes everything that leaves the house through one pipe and returns it to the ground as water clean enough that the soil can finish the work. It does this with no power, no chemicals and no moving parts in a conventional design. The whole thing is gravity and time.</p>
<h3>1. The tank</h3>
<p>A watertight box, usually concrete, sized so that a couple of days of wastewater sit in it before anything leaves. In that time three layers form. Grease and light solids float to the top as scum. Heavy solids sink as sludge. Between them sits a band of relatively clear liquid, and that middle band is the only part that should ever leave the tank. An outlet baffle or effluent filter enforces this.</p>
<p>Bacteria in the sludge break some of it down, but not all. The remainder accumulates, which is why the tank has to be pumped.</p>
<h3>2. The distribution box</h3>
<p>A small chamber that splits the outgoing effluent evenly between the drainfield trenches. Boxes settle out of level over the years and send everything to one trench, which is a common and very fixable cause of a field that appears to be failing.</p>
<h3>3. The drainfield</h3>
<p>A set of shallow trenches with perforated pipe laid in gravel or in plastic chambers. Effluent trickles out along the length of the pipe and soaks downward. The field is not a disposal pit — it is a distribution device, spreading the water thin enough that soil can treat it.</p>
<h3>4. The soil</h3>
<p>The actual treatment happens here. As effluent moves down through unsaturated soil, a biological layer at the trench bottom digests organic matter while the soil column filters pathogens. Two to four feet of unsaturated soil between the trench and groundwater is what makes the system safe, which is why the seasonal high water table decides so much about a design.</p>

<h2>Why sizing follows bedrooms</h2>
<p>A code cannot size for a household, because households change. It sizes for the house. Bedrooms are a durable proxy for how many people could live there, and the number a future buyer inherits. Two people in a four-bedroom house still need a four-bedroom system.</p>

<h2>Where systems actually fail</h2>
<p>Almost never the tank. The drainfield is the vulnerable part, and it fails in three ways: solids escape a neglected tank and seal the trench bottoms; the field is hydraulically overloaded by more water than it was sized for; or it is compacted by vehicles and building. All three are avoidable.</p>
<p><a href="../calculator/index.html">Size a tank →</a></p>
"""),
    ("drainfield", "Understanding Your Drainfield", "Drainfield types, sizing, setbacks and the habits that decide whether a field lasts eight years or thirty.", """
<h2>The field is the expensive part</h2>
<p>Tanks are cheap and durable. Drainfields are neither. Replacing one means new excavation, often a new permit, sometimes a soil evaluation that says the original design is no longer allowed. Everything in septic maintenance is really about protecting this component.</p>

<h2>Five field types</h2>
<h3>Conventional gravity trenches</h3>
<p>Perforated pipe in gravel-filled trenches, fed by gravity. Cheapest, simplest, longest-lived. Needs decent soil and enough depth to groundwater.</p>
<h3>Chamber systems</h3>
<p>Arched plastic chambers replace the gravel. More expensive per foot, but no gravel hauling, a larger open infiltration surface, and easier installation on awkward sites.</p>
<h3>Pressure distribution</h3>
<p>A pump doses effluent through small orifices so the whole field is loaded evenly rather than the first few feet taking everything. Extends field life on marginal sites, at the cost of a pump that will eventually need replacing.</p>
<h3>Mound systems</h3>
<p>Where soil is too shallow, too tight, or the water table too high, the field is built above grade in imported sand. Effective and expensive — typically two to three times a conventional field.</p>
<h3>Aerobic treatment units</h3>
<p>Air is blown through the effluent so aerobic bacteria treat it before it reaches the soil. The resulting effluent is clean enough that the absorption area can be roughly halved, which is why these appear on small or difficult lots. They need power, an annual service contract, and they fail quietly when neglected.</p>

<h2>Sizing, in one line</h2>
<p>Absorption area equals daily design flow divided by the soil application rate. A three-bedroom house at 450 gallons per day needs 750 square feet on sandy loam and 4,500 on clay. Same house. The soil is the variable that matters.</p>

<h2>Setbacks</h2>
<div class="scroll"><table class="tbl">
<tr><th>From</th><th>Typical minimum</th></tr>
<tr><td>Private well</td><td><b>100 ft</b></td></tr>
<tr><td>Stream, pond, wetland</td><td><b>50 – 100 ft</b></td></tr>
<tr><td>Property line</td><td><b>10 ft</b></td></tr>
<tr><td>Building foundation</td><td><b>10 – 20 ft</b></td></tr>
<tr><td>Driveway or parking</td><td><b>Not permitted over</b></td></tr>
</table></div>
<p>Your county sets the real numbers. Check before you buy a lot, not after.</p>

<h2>Getting thirty years out of a field</h2>
<ul>
<li>Pump the tank on schedule. This is the whole ballgame.</li>
<li>Keep vehicles, trailers, sheds and pools off it, permanently.</li>
<li>Divert roof and surface water away from the field area.</li>
<li>Spread laundry through the week instead of six loads on Saturday.</li>
<li>Fix running toilets — one can add hundreds of gallons a day.</li>
<li>Plant grass over it, nothing with roots that go looking for water.</li>
</ul>
<p><a href="../calculator/drainfield.html">Calculate absorption area →</a></p>
"""),
    ("costs", "What a Septic System Really Costs", "A line-by-line breakdown of septic installation cost, plus the site conditions that push quotes past the estimate.", """
<h2>The line items</h2>
<div class="scroll"><table class="tbl">
<tr><th>Item</th><th>Typical range</th><th>Notes</th></tr>
<tr><td>Soil evaluation / perc test</td><td><b>$450 – $1,200</b></td><td>First expense, and it decides the design</td></tr>
<tr><td>Design and permit</td><td><b>$400 – $1,600</b></td><td>Higher where a stamped engineered plan is required</td></tr>
<tr><td>Tank, supplied and set</td><td><b>$1,200 – $2,800</b></td><td>1,000 to 1,500 gallon concrete</td></tr>
<tr><td>Conventional drainfield</td><td><b>$4,000 – $12,000</b></td><td>Scales directly with soil quality</td></tr>
<tr><td>Excavation and labour</td><td><b>$2,500 – $6,000</b></td><td>Access and ground conditions drive this</td></tr>
<tr><td>Mound system, in place of a field</td><td><b>$15,000 – $30,000</b></td><td>Imported sand, plus a pump</td></tr>
<tr><td>Aerobic treatment unit</td><td><b>$9,000 – $20,000</b></td><td>Plus annual service contract</td></tr>
</table></div>

<h2>Why identical houses get different quotes</h2>
<p>Soil first. A site that percs well takes a gravity field; a site that does not takes a mound, and that single fact can double the project. Then depth to groundwater or bedrock, then access for equipment, then how far the field sits from the house, then regional labour rates.</p>

<h2>The extras that show up mid-job</h2>
<ul>
<li><b>Rock.</b> Blasting or hammering trenches is billed by the hour and it adds up fast.</li>
<li><b>An old tank.</b> Pumping, crushing and filling a decommissioned tank is a separate line.</li>
<li><b>A pump chamber.</b> Needed whenever the field sits uphill of the house. Adds $1,500 to $3,000 and a maintenance item.</li>
<li><b>Restoration.</b> A new system leaves a construction site behind. Ask whether grading and seeding are included.</li>
</ul>

<h2>Reading three quotes properly</h2>
<p>Make every bid state the same four things: tank size and material, absorption area in square feet, system type, and who pulls the permit. If one quote is much cheaper, one of those four is smaller. Ask directly what happens if rock is hit and whether the price is fixed or hourly — that single question separates careful contractors from optimistic ones.</p>

<h2>Where you can genuinely save</h2>
<p>Get the soil evaluation done before you commit to a lot or a house, so the answer informs the price you pay. Schedule off-season if you can; spring is the busiest window. And size the tank correctly rather than minimally — the incremental cost of the next size up is small against a field replacement.</p>
<p><a href="../calculator/cost.html">Estimate your cost →</a></p>
"""),
    ("maintenance", "Septic Maintenance That Matters", "The short list of septic maintenance habits that decide whether a system lasts a decade or three.", """
<h2>The schedule</h2>
<div class="scroll"><table class="tbl">
<tr><th>Task</th><th>How often</th></tr>
<tr><td>Pump the tank</td><td><b>Every 3 – 5 years</b></td></tr>
<tr><td>Inspect sludge and scum depth</td><td><b>Annually, or at half the pump interval</b></td></tr>
<tr><td>Clean the effluent filter, if fitted</td><td><b>Annually</b></td></tr>
<tr><td>Check the distribution box is level</td><td><b>Every few years</b></td></tr>
<tr><td>Service an aerobic unit</td><td><b>Per contract, usually twice a year</b></td></tr>
<tr><td>Walk the field looking for wet spots</td><td><b>Seasonally</b></td></tr>
</table></div>

<h2>What goes down the drain</h2>
<p>The tank runs on bacteria. Anything that kills them or will not break down is a problem.</p>
<p><b>Never flush:</b> wipes of any description, including the ones labelled flushable; sanitary products; paper towels; cat litter; grease and cooking oil; paint, solvents and pesticides; unused medication. <b>Go easy on:</b> bleach in quantity, antibacterial cleaners, and back-to-back laundry loads.</p>
<p>Additives sold to "restore" a tank do not remove the sludge that has already accumulated, and some can push solids out toward the field. Pumping is the only thing that empties a tank.</p>

<h2>Water use is a maintenance item</h2>
<p>The field is sized for a daily volume. Exceed it consistently and the soil stays saturated, the biological layer suffocates, and the field starts to fail. Spread laundry across the week, fix running toilets immediately, and keep roof runoff and sump discharge away from the field.</p>

<h2>Protecting the field surface</h2>
<p>No vehicles, no trailers, no sheds, no above-ground pools, no raised beds, no trees within about thirty feet. Compaction and roots are both permanent damage. Grass, and nothing else.</p>

<h2>Records</h2>
<p>Keep the permit, the as-built drawing showing where everything is buried, and the dates of every pump-out. It is worth real money when you sell, and it saves an hour of probing with a steel rod every time someone needs to find the lids.</p>
<p><a href="../calculator/pump-schedule.html">Calculate your pump interval →</a></p>
"""),
    ("soil-testing", "Perc Tests and Soil Evaluation", "What a perc test measures, how soil evaluation differs, and why the result decides your entire system design.", """
<h2>The test that decides everything</h2>
<p>Before a system can be designed, someone has to establish how fast the soil at the field location accepts water and how far it is to groundwater or rock. That answer sets the application rate, which sets the absorption area, which — along with what the site cannot support — sets the system type and most of the cost.</p>

<h2>Percolation test</h2>
<p>Holes are bored to trench depth, pre-soaked so the soil is at field capacity, then filled with water. The drop is timed and reported in minutes per inch. Fast rates mean sandy, permeable soil; slow rates mean tight soil that needs a much larger field.</p>
<div class="scroll"><table class="tbl">
<tr><th>Perc rate</th><th>Reading</th><th>Implication</th></tr>
<tr><td>Under 5 min/inch</td><td>Very fast</td><td>May need extra separation to groundwater</td></tr>
<tr><td>5 – 30 min/inch</td><td>Good</td><td>Conventional gravity field</td></tr>
<tr><td>31 – 60 min/inch</td><td>Moderate</td><td>Larger field, still conventional</td></tr>
<tr><td>61 – 90 min/inch</td><td>Slow</td><td>Very large field or an alternative system</td></tr>
<tr><td>Over 90 min/inch</td><td>Failing</td><td>Mound or aerobic, usually</td></tr>
</table></div>

<h2>Soil morphology evaluation</h2>
<p>Many states have moved away from perc tests toward a soil profile evaluation. A licensed evaluator digs a pit, reads the horizons, and records texture, structure, and the redoximorphic features that mark the seasonal high water table. It is more reliable, because a single hole full of water tells you very little about what the soil does across a wet spring.</p>

<h2>Getting a useful result</h2>
<ul>
<li>Test where the field will actually go, not where it is convenient to dig.</li>
<li>Test in the wet season if your state allows it — that is the condition that governs.</li>
<li>Have the reserve area evaluated at the same time. You will need it on the permit.</li>
<li>Do this before you buy. A failed evaluation on a lot you already own is an expensive surprise.</li>
</ul>

<h2>If the site fails</h2>
<p>A failure is rarely absolute. The usual paths forward are a mound system, an aerobic treatment unit with a reduced field, pressure distribution to spread the load, or relocating the field to a better part of the parcel. All cost more. None are impossible.</p>
<p><a href="../calculator/drainfield.html">Size a field from your perc rate →</a></p>
"""),
    ("troubleshooting", "Reading Septic Failure Symptoms", "Slow drains, wet spots, odours and gurgling — what each septic symptom points to and how urgent it is.", """
<h2>Symptoms and what they mean</h2>
<div class="scroll"><table class="tbl">
<tr><th>Symptom</th><th>Likely cause</th><th>Urgency</th></tr>
<tr><td>Every drain slow at once</td><td>Tank full, or blockage between house and tank</td><td><b>Days</b></td></tr>
<tr><td>One fixture slow</td><td>Local clog, not the system</td><td>Low</td></tr>
<tr><td>Gurgling drains</td><td>Restricted flow or a blocked vent</td><td><b>Weeks</b></td></tr>
<tr><td>Soggy ground over the field</td><td>Field saturated or failing</td><td><b>Immediate</b></td></tr>
<tr><td>Unusually green strip over the trenches</td><td>Effluent surfacing near grade</td><td><b>Immediate</b></td></tr>
<tr><td>Sewage odour outdoors</td><td>Surfacing effluent, or a broken lid</td><td><b>Immediate</b></td></tr>
<tr><td>Sewage odour indoors</td><td>Dry trap or vent issue, usually not the tank</td><td>Low</td></tr>
<tr><td>Backup after heavy rain only</td><td>Groundwater flooding the field</td><td><b>Weeks</b></td></tr>
</table></div>

<h2>The cheap causes worth ruling out first</h2>
<p>Before anyone quotes you for a new field, check three things: whether the tank is simply due for pumping, whether the effluent filter is clogged, and whether the distribution box has settled and is sending everything to one trench. Any of the three can produce symptoms that look exactly like field failure, and all three are inexpensive to fix.</p>

<h2>When it is genuinely the field</h2>
<p>Effluent surfacing, persistent saturation, and backups that continue after a pump-out point to a field that has lost its ability to accept water. Sometimes the trench bottoms are sealed by solids from years of skipped pumping; sometimes the field was undersized from the start; sometimes it is simply thirty years old.</p>
<p>Resting a field by drastically reducing water use for several weeks occasionally helps a marginal case. More often the answer is a new field, in the reserve area that should have been kept clear.</p>

<h2>Do not wait it out</h2>
<p>Surfacing sewage is a health hazard, not an inconvenience, and continuing to load a failing field makes the eventual repair larger. Call a licensed inspector, and call your health department if effluent is reaching the surface or a watercourse.</p>
<p><a href="../guides/maintenance.html">Maintenance guide →</a></p>
"""),
]


def build_guides():
    cards = "".join(
        f'<a class="card" href="{s}.html"><p class="kicker">Guide</p><h3>{t}</h3><p>{d}</p></a>'
        for s, t, d, _ in GUIDES)
    page("guides/index.html", "Septic System Guides — Sizing, Soil, Cost and Maintenance",
         "Practical guides to septic systems: how they work, drainfields, soil testing, installation cost, maintenance and failure symptoms.",
         crumb("../", [("Guides", "")]) + f"""
<section class="band"><div class="shell">
  <div class="band-head"><p class="eyebrow">Reference</p><h1>Guides</h1>
  <p>Six guides covering the reasoning behind every number the calculators produce.</p></div>
  <div class="grid g3">{cards}</div>
</div></section>""", 1)
    for slug, title, desc, html in GUIDES:
        page(f"guides/{slug}.html", f"{title} — Guide", desc,
             crumb("../", [("Guides", "guides/index.html"), (title, "")]) + f"""
<section class="band"><div class="shell narrow">
  <p class="eyebrow">Guide</p><h1>{title}</h1>
  <p class="lede" style="margin-top:18px">{desc}</p>
</div></section>
<section class="band white"><div class="shell narrow prose">{html}</div></section>""", 1)


def build_misc():
    page("faq.html", "Septic System Questions Answered",
         "Answers to the most common septic questions: tank size for a 3 bedroom house, pumping frequency, drainfield sizing, permits and system lifespan.",
         crumb("", [("Questions", "")]) + f"""
<section class="band"><div class="shell narrow">
  <p class="eyebrow">Reference</p><h1>Questions</h1>
  <p class="lede" style="margin:18px 0 34px">The things people ask before they size, budget, or buy.</p>
  {faq_block(FAQS)}
</div></section>""", 0, schema=faq_schema(FAQS))

    rows = "".join(
        f"<tr><td><b>{b} bedroom{'s' if b > 1 else ''}</b></td><td>{450 if b<=3 else 150*b} gpd</td>"
        f"<td><b>{s:,} gal</b></td><td>{s+250:,} gal</td></tr>"
        for b, s in [(1, 1000), (2, 1000), (3, 1000), (4, 1250), (5, 1500), (6, 2000), (7, 2500)])
    page("tank-size-chart.html", "Septic Tank Size Chart by Bedrooms",
         "Septic tank size chart: minimum capacity by bedroom count, with and without a garbage disposal, plus matching drainfield areas by soil type.",
         crumb("", [("Tank size chart", "")]) + f"""
<section class="band"><div class="shell prose">
  <p class="eyebrow">Reference</p><h1>Septic tank size chart</h1>
  <p class="lede" style="margin:18px 0 30px">The standard sizing most states start from. Massachusetts, California and a few others set higher floors — check your <a href="states/index.html">state page</a>.</p>
  <div class="scroll"><table class="tbl">
    <tr><th>Dwelling</th><th>Design flow</th><th>Minimum tank</th><th>With garbage disposal</th></tr>{rows}
  </table></div>
  <h2>Matching drainfield area, 3 bedrooms at 450 gpd</h2>
  <div class="scroll"><table class="tbl">
    <tr><th>Soil</th><th>Application rate</th><th>Absorption area</th><th>Trench length at 3 ft</th></tr>
    """ + "".join(
             f"<tr><td>{n}</td><td>{r} gpd/sq ft</td><td><b>{round(450/float(r)):,} sq ft</b></td><td>{round(450/float(r)/3):,} ft</td></tr>"
             for n, p, r in SOILS) + """
  </table></div>
  <p><a href="calculator/index.html">Run your own numbers →</a></p>
</div></section>""", 0)

    legal = {
        "about.html": ("About", """
<h2>What this site does</h2>
<p>It answers one question well: what size septic system does this house need, and what will it cost. The calculators work from published state minimums and standard onsite wastewater engineering practice — two-day retention for tank volume, soil application rates for absorption area, solids accumulation for pump intervals.</p>
<h2>Where the figures come from</h2>
<p>State minimum tank sizes and design flow rates are compiled from state onsite wastewater codes. Soil application rates follow conventional trench loading practice. Cost ranges are built from typical component and labour costs adjusted by regional index, and are estimates rather than quotes.</p>
<h2>What it is not</h2>
<p>It is not a system design and it does not replace a soil evaluation, a licensed designer, or your local health department. County rules sit on top of state minimums and are frequently stricter. Every figure here should be confirmed locally before money is spent.</p>
<h2>Contact</h2>
<p>Corrections to state data are welcome and taken seriously. If a figure on your state page is out of date, tell us and cite the code section.</p>"""),
        "privacy.html": ("Privacy Policy", """
<p>This policy explains what is collected and why.</p>
<h2>Calculator inputs</h2>
<p>Bedroom counts, soil types and states entered into the calculators are processed in your browser. They are not transmitted or stored by this site.</p>
<h2>Quote requests</h2>
<p>If you submit the contractor quote form, the name, phone, email and ZIP code you provide are shared with licensed septic contractors serving that ZIP code so they can contact you with quotes. They are not sold to anyone else, and there is no obligation to hire.</p>
<h2>Analytics and advertising</h2>
<p>Aggregate traffic analytics are used to understand which pages are useful. Advertising partners, where present, may set cookies to serve relevant ads. You can disable cookies in your browser without losing calculator functionality.</p>
<h2>Your choices</h2>
<p>You can request deletion of a quote submission at any time through the contact page. Residents of states with applicable privacy statutes may request access to, correction of, or deletion of personal information held about them, and may opt out of its sale or sharing.</p>"""),
        "terms.html": ("Terms of Service", """
<h2>Use of this site</h2>
<p>You may use these calculators and guides for personal and professional planning. You may not scrape, republish, or resell the content or the state dataset.</p>
<h2>Accuracy</h2>
<p>Every figure is an estimate produced from published minimums and standard practice. Codes change, counties add requirements, and site conditions override generic sizing. No warranty is given that a result matches what your jurisdiction will approve.</p>
<h2>Liability</h2>
<p>Decisions about septic design, purchase and installation are yours and your licensed professionals'. This site accepts no liability for costs, damages or code violations arising from reliance on its output.</p>
<h2>Third-party contractors</h2>
<p>Contractors contacted through the quote form are independent businesses. This site does not perform work, does not supervise it, and is not party to any agreement you reach with them. Verify licensing and insurance yourself.</p>"""),
        "contact.html": ("Contact", """
<p>For corrections to state data, cite the code section and the state — those get fixed quickly. For anything else, use the same address.</p>
<h2>What we cannot do</h2>
<p>We cannot approve a design, tell you what your county will accept, or diagnose a failing system remotely. Those need a licensed local professional and your health department.</p>
<h2>Contractors</h2>
<p>If you install septic systems and want quote requests from your service area, get in touch with your licence number and the counties you cover.</p>"""),
        "disclaimer.html": ("Disclaimer", """
<p>The calculators, charts and guides on this site provide planning estimates only. They are not a septic system design, an engineering opinion, or a code determination.</p>
<h2>Always required</h2>
<p>A soil evaluation or percolation test on the actual site, a design meeting local rules, a permit from your county or district health department, and inspection before backfill. Nothing on this site substitutes for any of those.</p>
<h2>Local rules control</h2>
<p>State figures shown here are minimums. Counties, health districts, watershed authorities and homeowner associations can and do require more. Where they differ from anything on this site, they control.</p>
<h2>Health and safety</h2>
<p>Septic tanks contain gases that can be fatal within seconds. Never enter a tank, and never leave a lid unsecured. Surfacing sewage is a health hazard — contact your health department.</p>"""),
        "ccpa.html": ("Your Privacy Choices", """
<p>Residents of California and other states with comprehensive privacy laws have specific rights over personal information collected through this site.</p>
<h2>Your rights</h2>
<ul>
<li>Know what personal information has been collected and how it has been used or shared</li>
<li>Request a copy of that information</li>
<li>Request correction of inaccurate information</li>
<li>Request deletion, subject to legal retention requirements</li>
<li>Opt out of the sale or sharing of personal information</li>
<li>Be free from discrimination for exercising any of these rights</li>
</ul>
<h2>How to exercise them</h2>
<p>Submit a request through the contact page stating which right you are exercising and the email or phone number used on this site so the request can be matched to a record. Requests are answered within the period the applicable statute allows.</p>
<h2>What is collected</h2>
<p>Only what you enter into the quote form, plus standard analytics. Calculator inputs never leave your browser.</p>"""),
    }
    for path, (title, html) in legal.items():
        page(path, f"{title} — {BRAND}", f"{title} for {BRAND}.",
             crumb("", [(title, "")]) + f"""
<section class="band"><div class="shell narrow">
  <p class="eyebrow">{BRAND}</p><h1>{title}</h1>
</div></section>
<section class="band white"><div class="shell narrow prose">{html}</div></section>""", 0)


def build_meta():
    # vercel.json — makes /states/tx resolve to states/tx.html (clean URLs) and sets a 404
    vercel = {
        "cleanUrls": True,
        "trailingSlash": False
    }
    open(os.path.join(OUT, "vercel.json"), "w").write(json.dumps(vercel, indent=2))

    urls = []
    for dirpath, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(dirpath, f), OUT).replace("\\", "/")
                rel = rel[:-5]
                if rel.endswith("index"): rel = rel[:-5].rstrip("/")
                urls.append(rel)
    urls.sort()
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pri = "1.0" if u == "" else ("0.9" if u.startswith("calculator") else "0.7")
        xml.append(f"<url><loc>{SITE}/{u}</loc><priority>{pri}</priority></url>")
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(xml))
    open(os.path.join(OUT, "robots.txt"), "w").write(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


if __name__ == "__main__":
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    build_home(); build_calculators(); build_new_pages(); build_states(); build_guides(); build_misc(); build_meta()
    n = sum(len([f for f in fs if f.endswith(".html")]) for _, _, fs in os.walk(OUT))
    print(f"built {n} pages")
