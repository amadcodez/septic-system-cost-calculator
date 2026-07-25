/* ------------------------------------------------------------------
   Sizing engine. Every function returns plain numbers so the same
   maths can be reused by any page that loads this file.
   ------------------------------------------------------------------ */
(function () {
  var S = window.STATES, SOIL = window.SOILS;
  var TANKS = [750, 1000, 1250, 1500, 2000, 2500, 3000];

  function $(id) { return document.getElementById(id); }
  function usd(n) { return "$" + Math.round(n).toLocaleString("en-US"); }
  function num(n) { return Math.round(n).toLocaleString("en-US"); }
  function stepUp(size) { for (var i = 0; i < TANKS.length; i++) if (TANKS[i] >= size) return TANKS[i]; return Math.ceil(size / 500) * 500; }

  /* ---- core maths ---- */
  function designFlow(st, beds) { return (S[st] ? S[st].gpd : 150) * Math.max(beds, 2); }

  function tankSize(st, beds, disposal, extras) {
    var flow = designFlow(st, beds);
    var need = flow * 2;                    // two-day retention, the near-universal rule
    if (disposal) need += 250;              // garbage disposal allowance
    if (extras) need += 250;                // whirlpool tub, water softener discharge
    var floor = S[st] ? S[st].min : 1000;
    if (beds >= 4) floor = Math.max(floor, 1250);
    if (beds >= 5) floor = Math.max(floor, 1500);
    if (beds >= 7) floor = Math.max(floor, 2000);
    return { size: stepUp(Math.max(need, floor)), flow: flow, floor: floor, calc: need };
  }

  function fieldArea(flow, soil, trenchWidth) {
    var rate = SOIL[soil].rate;
    var area = flow / rate;
    var w = trenchWidth || 3;
    return { area: area, rate: rate, length: area / w, width: w };
  }

  function pumpYears(gal, people, disposal) {
    var sludge = 30 * (disposal ? 1.5 : 1);   // gallons of solids per person per year
    var y = (0.32 * gal) / (sludge * Math.max(people, 1));
    return Math.max(0.6, Math.min(y, 12));
  }

  function costOf(st, beds, soil, type) {
    var t = tankSize(st, beds, false, false);
    var f = fieldArea(t.flow, soil, 3);
    var tier = S[st] ? S[st].tier : 1;
    var tank = 700 + t.size * 0.75;
    var perSf = { conventional: 8, chamber: 10, mound: 22, aerobic: 9 }[type];
    var field = f.area * perSf;
    var unit = type === "aerobic" ? 6200 : 0;
    if (type === "aerobic") field *= 0.5;      // aerobic effluent allows a smaller field
    var dig = 2600 + (SOIL[soil].rate < 0.3 ? 1800 : 0);
    var soft = 700 /* soil evaluation */ + 620 /* permit and design */;
    var sub = (tank + field + unit + dig) * tier + soft;
    return { low: sub * 0.82, high: sub * 1.24, mid: sub, tank: tank * tier, field: (field + unit) * tier, dig: dig * tier, soft: soft, area: f.area, size: t.size };
  }

  window.SepticMath = { designFlow: designFlow, tankSize: tankSize, fieldArea: fieldArea, pumpYears: pumpYears, costOf: costOf, usd: usd, num: num };

  /* ---- shared UI helpers ---- */
  function fillStates(sel) {
    if (!sel) return;
    var keys = Object.keys(S).sort(function (a, b) { return S[a].n.localeCompare(S[b].n); });
    keys.forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = S[k].n; sel.appendChild(o);
    });
    var pre = sel.getAttribute("data-preset");
    if (pre && S[pre]) sel.value = pre;
  }
  function fillSoils(sel) {
    if (!sel) return;
    Object.keys(SOIL).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k; o.textContent = SOIL[k].n + " — " + SOIL[k].perc; sel.appendChild(o);
    });
    sel.value = "sandyloam";
  }
  function stepper(id) {
    var input = $(id); if (!input) return;
    var wrap = input.parentNode;
    wrap.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        var v = parseInt(input.value, 10) || 1;
        var d = b.getAttribute("data-step") === "up" ? 1 : -1;
        var min = parseInt(input.min, 10), max = parseInt(input.max, 10);
        input.value = Math.max(min, Math.min(max, v + d));
      });
    });
  }
  function show(id) {
    var e = $(id); if (!e) return;
    var inner = e.querySelector(".spec-inner");
    if (inner && !inner.querySelector(".printbar")) {
      var brand = document.createElement("div");
      brand.className = "print-brand";
      brand.textContent = "Septic System Cost Calculator \u2014 septicsystemcostcalculator.com \u2014 estimate generated " + new Date().toLocaleDateString("en-US");
      inner.insertBefore(brand, inner.firstChild);
      var bar = document.createElement("div");
      bar.className = "printbar";
      bar.innerHTML = '<button type="button" class="btn ghost">\u2913 Download PDF / Print</button>';
      inner.appendChild(bar);
      bar.querySelector("button").addEventListener("click", function () {
        var tool = e.closest(".tool");
        tool.classList.add("print-target");
        window.print();
        setTimeout(function () { tool.classList.remove("print-target"); }, 600);
      });
    }
    e.classList.add("on");
    e.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  function rows(el, list) {
    el.innerHTML = list.map(function (r) { return "<div><span>" + r[0] + "</span><b>" + r[1] + "</b></div>"; }).join("");
  }
  function fail(id, msg) { var e = $(id); if (!e) return; e.textContent = msg; e.classList.add("on"); }
  function clearFail(id) { var e = $(id); if (e) e.classList.remove("on"); }

  /* ---- wire up whichever calculator is on the page ---- */
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("select.js-states").forEach(fillStates);
    document.querySelectorAll("select.js-soils").forEach(fillSoils);
    ["beds", "cbeds", "people", "dbeds"].forEach(stepper);

    /* TANK SIZE */
    var f1 = $("go-tank");
    if (f1) f1.addEventListener("click", function () {
      var st = $("state").value;
      if (!st) return fail("e-tank", "Choose a state first — minimum tank sizes are set by state code.");
      clearFail("e-tank");
      var beds = parseInt($("beds").value, 10);
      var r = tankSize(st, beds, $("disposal").checked, $("extras").checked);
      var fld = fieldArea(r.flow, $("soil").value, 3);
      $("t-figure").innerHTML = num(r.size) + " gal<small>Recommended minimum tank capacity</small>";
      rows($("t-rows"), [
        ["Design flow (" + beds + " bedrooms)", num(r.flow) + " gpd"],
        ["Required working volume", num(r.calc) + " gal"],
        [S[st].n + " code floor", num(r.floor) + " gal"],
        ["Nearest standard tank", num(r.size) + " gal"],
        ["Matching drainfield area", num(fld.area) + " sq ft"],
        ["Approx. trench length (3 ft wide)", num(fld.length) + " ft"],
        ["Pump-out interval, 4 occupants", pumpYears(r.size, 4, false).toFixed(1) + " years"]
      ]);
      $("t-note").innerHTML = "Sized against " + S[st].ag + ". Counties often set stricter rules than the state minimum, so confirm before you order a tank.";
      show("t-spec");
    });

    /* DRAINFIELD */
    var f2 = $("go-field");
    if (f2) f2.addEventListener("click", function () {
      var st = $("dstate").value;
      if (!st) return fail("e-field", "Choose a state first — design flow per bedroom varies by code.");
      clearFail("e-field");
      var beds = parseInt($("dbeds").value, 10);
      var soil = $("dsoil").value;
      var w = parseFloat($("dwidth").value);
      var flow = designFlow(st, beds);
      var r = fieldArea(flow, soil, w);
      $("d-figure").innerHTML = num(r.area) + " sq ft<small>Absorption area required</small>";
      rows($("d-rows"), [
        ["Design flow", num(flow) + " gpd"],
        ["Soil texture", SOIL[soil].n],
        ["Application rate", r.rate.toFixed(2) + " gpd per sq ft"],
        ["Trench width", w + " ft"],
        ["Total trench length", num(r.length) + " ft"],
        ["Suggested layout", Math.max(2, Math.ceil(r.length / 100)) + " trenches at " + num(Math.min(r.length, 100)) + " ft"],
        ["Land needed with 6 ft spacing", num(r.area * 2.6) + " sq ft"]
      ]);
      $("d-note").textContent = SOIL[soil].risk + " Reserve an equal second area for a future replacement field — most states require it on the permit.";
      show("d-spec");
    });

    /* COST */
    var f3 = $("go-cost");
    if (f3) f3.addEventListener("click", function () {
      var st = $("cstate").value;
      if (!st) return fail("e-cost", "Choose a state first — labour and permit costs swing widely by region.");
      clearFail("e-cost");
      var beds = parseInt($("cbeds").value, 10);
      var soil = $("csoil").value, type = $("ctype").value;
      var c = costOf(st, beds, soil, type);
      $("c-figure").innerHTML = usd(c.low) + " – " + usd(c.high) + "<small>Installed cost in " + S[st].n + "</small>";
      rows($("c-rows"), [
        ["Tank, delivered and set", usd(c.tank)],
        ["Drainfield or treatment unit", usd(c.field)],
        ["Excavation and labour", usd(c.dig)],
        ["Soil evaluation, permit, design", usd(c.soft)],
        ["Tank size assumed", num(c.size) + " gal"],
        ["Absorption area assumed", num(c.area) + " sq ft"],
        ["Midpoint estimate", usd(c.mid)]
      ]);
      $("c-note").textContent = "Estimates cover a straightforward new install on accessible ground. Rock, high water table, long driveways, and old-system removal are the four things that most often push a quote past the top of this range.";
      show("c-spec");
    });

    /* PUMP SCHEDULE */
    var f4 = $("go-pump");
    if (f4) f4.addEventListener("click", function () {
      clearFail("e-pump");
      var gal = parseInt($("ptank").value, 10);
      var ppl = parseInt($("people").value, 10);
      var y = pumpYears(gal, ppl, $("pdisposal").checked);
      var next = new Date(); next.setMonth(next.getMonth() + Math.round(y * 12));
      $("p-figure").innerHTML = y.toFixed(1) + " years<small>Between pump-outs at this household size</small>";
      rows($("p-rows"), [
        ["Tank capacity", num(gal) + " gal"],
        ["Occupants", ppl],
        ["Solids accumulating", num(30 * ($("pdisposal").checked ? 1.5 : 1) * ppl) + " gal per year"],
        ["Pump when solids reach", num(gal * 0.30) + " gal"],
        ["If pumped today, next service", next.toLocaleDateString("en-US", { month: "long", year: "numeric" })],
        ["Typical pump-out cost", "$320 – $650"]
      ]);
      $("p-note").textContent = y < 2
        ? "Under two years is short. Either the tank is undersized for this household or water use is high — both shorten drainfield life, so it is worth checking."
        : "Have the tank inspected at the halfway point. Measuring the sludge layer is cheap; a drainfield ruined by carry-over solids is not.";
      show("p-spec");
    });

    /* REPLACEMENT COST */
    var f5 = $("go-repl");
    if (f5) f5.addEventListener("click", function () {
      var st = $("rstate").value;
      if (!st) return fail("e-repl", "Choose a state first \u2014 removal and labour costs vary by region.");
      clearFail("e-repl");
      var beds = parseInt($("rbeds").value, 10);
      var soil = $("rsoil").value, scope = $("rscope").value;
      var c = costOf(st, beds, soil, "conventional");
      var tier = S[st].tier;
      var decom = 1400 * tier;                 // pump, crush, fill old tank
      var permit = 500;                        // re-permit
      var lo, hi, items;
      if (scope === "tank") {
        lo = c.tank * 0.9 + decom + permit + 1800 * tier;
        hi = c.tank * 1.25 + decom * 1.3 + permit + 2600 * tier;
        items = [["New tank, delivered and set", usd(c.tank)],
                 ["Old tank decommissioning", usd(decom)],
                 ["Excavation and reconnection", usd(2200 * tier)],
                 ["Permit and inspection", usd(permit)]];
      } else if (scope === "field") {
        var fld = c.field * 1.15;              // working around existing system
        lo = fld * 0.85 + permit + 2200 * tier;
        hi = fld * 1.3 + permit + 3400 * tier;
        items = [["New drainfield, installed", usd(fld)],
                 ["Old field abandonment", usd(900 * tier)],
                 ["Excavation premium (occupied site)", usd(2800 * tier)],
                 ["Soil evaluation and permit", usd(permit + 700)]];
      } else {
        lo = c.low + decom + permit;
        hi = c.high + decom * 1.3 + permit + 1500 * tier;
        items = [["Complete new system", usd(c.mid)],
                 ["Old tank decommissioning", usd(decom)],
                 ["Old field abandonment", usd(900 * tier)],
                 ["Re-permit and inspection", usd(permit)]];
      }
      $("r-figure").innerHTML = usd(lo) + " \u2013 " + usd(hi) + "<small>Replacement cost in " + S[st].n + "</small>";
      rows($("r-rows"), items.concat([["Typical timeline", scope === "tank" ? "2 \u2013 4 days" : "1 \u2013 3 weeks"]]));
      $("r-note").textContent = "Replacement usually costs more than the same system built new: the old components have to come out, equipment works around an occupied home, and many states require the system to be brought up to current code \u2014 which can mean a larger field than the one that failed.";
      show("r-spec");
    });

    /* PUMPING COST */
    var f6 = $("go-pcost");
    if (f6) f6.addEventListener("click", function () {
      var st = $("pcstate").value;
      if (!st) return fail("e-pcost", "Choose a state first \u2014 pumping rates vary by region.");
      clearFail("e-pcost");
      var gal = parseInt($("pctank").value, 10);
      var tier = S[st].tier;
      var base = 250 + gal * 0.13;             // national base by size
      var lo = base * tier * 0.85, hi = base * tier * 1.35;
      var dig = $("pcdig").checked ? 150 * tier : 0;
      var filt = $("pcfilter").checked ? 60 : 0;
      lo += dig + filt; hi += dig * 1.6 + filt;
      $("pc-figure").innerHTML = usd(lo) + " \u2013 " + usd(hi) + "<small>Pump-out cost in " + S[st].n + "</small>";
      rows($("pc-rows"), [
        ["Tank size", num(gal) + " gal"],
        ["Base pumping service", usd(base * tier)],
        ["Locating and digging to the lid", dig ? usd(dig) : "Included / not needed"],
        ["Effluent filter cleaning", filt ? usd(filt) : "Not requested"],
        ["Typical service time", "45 \u2013 90 minutes"],
        ["Recommended interval", "3 \u2013 5 years for most households"]
      ]);
      $("pc-note").textContent = "Prices climb if the truck cannot get within about 100 feet of the tank, if the lid is buried deep, or if the tank has not been pumped for many years and the sludge has compacted. Having risers installed at pump-out time saves the digging fee on every future visit.";
      show("pc-spec");
    });

    /* quote capture */
    document.querySelectorAll(".js-quote").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var btn = form.querySelector("button[type=submit]");
        if (btn) { btn.disabled = true; btn.textContent = "Sending\u2026"; }
        fetch(form.action.replace("formsubmit.co/", "formsubmit.co/ajax/"), {
          method: "POST",
          body: new FormData(form),
          headers: { "Accept": "application/json" }
        }).then(function (r) { return r.json(); }).then(function () {
          if (typeof gtag === "function") {
            var svc = form.querySelector("select[name=service]");
            gtag("event", "generate_lead", {
              service_type: svc ? svc.value : "unknown",
              page_state: form.querySelector("input[name=page_state]") ? form.querySelector("input[name=page_state]").value : ""
            });
          }
          form.innerHTML = '<h3>Request received</h3><p>Up to three licensed installers in your area will follow up, usually within one business day. Nothing is booked and nothing is owed until you accept a quote.</p>';
        }).catch(function () {
          if (btn) { btn.disabled = false; btn.textContent = "Get free quotes"; }
          var err = document.createElement("p");
          err.className = "fine"; err.style.color = "#FCA98B";
          err.textContent = "Something went wrong \u2014 please try again.";
          form.appendChild(err);
        });
      });
    });
  });
})();
