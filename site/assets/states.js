/* State sizing baselines.
   gpd  = design flow allowed per bedroom (gallons per day)
   min  = minimum septic tank size permitted for a 1-3 bedroom dwelling (gallons)
   tier = regional cost index applied to installation estimates
   Figures are state minimums. County and health-district rules are frequently
   stricter and always control. Verify with the agency listed before you build. */
window.STATES = {
  al:{n:"Alabama",gpd:150,min:1000,tier:0.92,ag:"Alabama Department of Public Health — Onsite Sewage Program"},
  ak:{n:"Alaska",gpd:150,min:1000,tier:1.45,ag:"Alaska DEC — Wastewater Discharge Program"},
  az:{n:"Arizona",gpd:150,min:1000,tier:1.00,ag:"Arizona DEQ — On-site Wastewater Program"},
  ar:{n:"Arkansas",gpd:150,min:1000,tier:0.88,ag:"Arkansas Department of Health — Onsite Wastewater"},
  ca:{n:"California",gpd:150,min:1200,tier:1.38,ag:"State Water Resources Control Board — OWTS Policy"},
  co:{n:"Colorado",gpd:150,min:1000,tier:1.12,ag:"Colorado CDPHE — OWTS Program (Reg 43)"},
  ct:{n:"Connecticut",gpd:150,min:1000,tier:1.25,ag:"Connecticut DPH — Subsurface Sewage Disposal"},
  de:{n:"Delaware",gpd:150,min:1000,tier:1.08,ag:"Delaware DNREC — Groundwater Discharges Section"},
  fl:{n:"Florida",gpd:150,min:900,tier:0.98,ag:"Florida DEP — Onsite Sewage Programs"},
  ga:{n:"Georgia",gpd:150,min:1000,tier:0.92,ag:"Georgia DPH — Environmental Health, Onsite Sewage"},
  hi:{n:"Hawaii",gpd:150,min:1000,tier:1.55,ag:"Hawaii DOH — Wastewater Branch"},
  id:{n:"Idaho",gpd:150,min:1000,tier:1.02,ag:"Idaho DEQ — Subsurface Sewage Disposal"},
  il:{n:"Illinois",gpd:150,min:1000,tier:1.06,ag:"Illinois DPH — Private Sewage Disposal Program"},
  in:{n:"Indiana",gpd:150,min:1000,tier:0.96,ag:"Indiana DOH — Residential Onsite Sewage Systems"},
  ia:{n:"Iowa",gpd:150,min:1000,tier:0.95,ag:"Iowa DNR — Onsite Wastewater Systems"},
  ks:{n:"Kansas",gpd:150,min:1000,tier:0.90,ag:"Kansas DHE — Onsite Wastewater Program"},
  ky:{n:"Kentucky",gpd:150,min:1000,tier:0.90,ag:"Kentucky DPH — Onsite Sewage Program"},
  la:{n:"Louisiana",gpd:150,min:1000,tier:0.90,ag:"Louisiana DOH — Sanitarian Services"},
  me:{n:"Maine",gpd:150,min:1000,tier:1.12,ag:"Maine DHHS — Subsurface Wastewater Program"},
  md:{n:"Maryland",gpd:150,min:1000,tier:1.18,ag:"Maryland DOE — Onsite Systems Division"},
  ma:{n:"Massachusetts",gpd:110,min:1500,tier:1.42,ag:"Massachusetts DEP — Title 5 Program"},
  mi:{n:"Michigan",gpd:150,min:1000,tier:0.98,ag:"Michigan EGLE — Onsite Wastewater Program"},
  mn:{n:"Minnesota",gpd:150,min:1000,tier:1.05,ag:"Minnesota PCA — Subsurface Sewage Treatment Systems"},
  ms:{n:"Mississippi",gpd:150,min:1000,tier:0.86,ag:"Mississippi State DOH — Onsite Wastewater"},
  mo:{n:"Missouri",gpd:150,min:1000,tier:0.90,ag:"Missouri DHSS — Onsite Sewage Program"},
  mt:{n:"Montana",gpd:150,min:1000,tier:1.00,ag:"Montana DEQ — Subdivisions and Onsite Program"},
  ne:{n:"Nebraska",gpd:150,min:1000,tier:0.92,ag:"Nebraska DEE — Onsite Wastewater Treatment"},
  nv:{n:"Nevada",gpd:150,min:1000,tier:1.14,ag:"Nevada DEP — Bureau of Water Pollution Control"},
  nh:{n:"New Hampshire",gpd:150,min:1000,tier:1.20,ag:"New Hampshire DES — Subsurface Systems Bureau"},
  nj:{n:"New Jersey",gpd:150,min:1000,tier:1.30,ag:"New Jersey DEP — Bureau of Nonpoint Pollution Control"},
  nm:{n:"New Mexico",gpd:150,min:1000,tier:0.95,ag:"New Mexico Environment Department — Liquid Waste Program"},
  ny:{n:"New York",gpd:150,min:1000,tier:1.34,ag:"New York State DOH — Residential Onsite Systems"},
  nc:{n:"North Carolina",gpd:120,min:1000,tier:0.94,ag:"North Carolina DHHS — On-Site Water Protection"},
  nd:{n:"North Dakota",gpd:150,min:1000,tier:0.96,ag:"North Dakota DEQ — Onsite Wastewater"},
  oh:{n:"Ohio",gpd:150,min:1000,tier:0.96,ag:"Ohio Department of Health — Sewage Treatment Systems"},
  ok:{n:"Oklahoma",gpd:150,min:1000,tier:0.88,ag:"Oklahoma DEQ — Individual Sewage Disposal"},
  or:{n:"Oregon",gpd:150,min:1000,tier:1.16,ag:"Oregon DEQ — Onsite Wastewater Management"},
  pa:{n:"Pennsylvania",gpd:150,min:1000,tier:1.08,ag:"Pennsylvania DEP — Sewage Facilities Program"},
  ri:{n:"Rhode Island",gpd:150,min:1000,tier:1.28,ag:"Rhode Island DEM — Onsite Wastewater Treatment Systems"},
  sc:{n:"South Carolina",gpd:150,min:1000,tier:0.92,ag:"South Carolina DES — Onsite Wastewater Program"},
  sd:{n:"South Dakota",gpd:150,min:1000,tier:0.94,ag:"South Dakota DANR — Wastewater Program"},
  tn:{n:"Tennessee",gpd:150,min:1000,tier:0.92,ag:"Tennessee TDEC — Subsurface Sewage Disposal Systems"},
  tx:{n:"Texas",gpd:150,min:1000,tier:0.94,ag:"Texas TCEQ — On-Site Sewage Facilities Program"},
  ut:{n:"Utah",gpd:150,min:1000,tier:1.02,ag:"Utah DEQ — Division of Water Quality, Onsite Program"},
  vt:{n:"Vermont",gpd:140,min:1000,tier:1.18,ag:"Vermont DEC — Drinking Water and Groundwater Protection"},
  va:{n:"Virginia",gpd:150,min:1000,tier:1.02,ag:"Virginia VDH — Onsite Sewage Program"},
  wa:{n:"Washington",gpd:120,min:1000,tier:1.22,ag:"Washington State DOH — Wastewater Management Section"},
  wv:{n:"West Virginia",gpd:150,min:1000,tier:0.90,ag:"West Virginia DHHR — Environmental Health Services"},
  wi:{n:"Wisconsin",gpd:150,min:1000,tier:1.02,ag:"Wisconsin DSPS — Private Onsite Wastewater Treatment"},
  wy:{n:"Wyoming",gpd:150,min:1000,tier:0.98,ag:"Wyoming DEQ — Water Quality Division, Small Wastewater"}
};

/* Soil application rates, gallons per day per square foot of absorption area.
   Based on conventional trench loading rates for each USDA texture class. */
window.SOILS = {
  gravel:{n:"Gravel or coarse sand",rate:1.20,perc:"Under 5 min/inch",risk:"Fast. Some states require extra separation to groundwater."},
  sand:{n:"Sand",rate:0.80,perc:"5 to 15 min/inch",risk:"Good drainage, straightforward install."},
  sandyloam:{n:"Sandy loam",rate:0.60,perc:"16 to 30 min/inch",risk:"The ideal case for a conventional field."},
  loam:{n:"Loam",rate:0.45,perc:"31 to 45 min/inch",risk:"Workable, larger field than sandy loam."},
  siltloam:{n:"Silt loam",rate:0.30,perc:"46 to 60 min/inch",risk:"Field size climbs sharply. Check seasonal water table."},
  clayloam:{n:"Clay loam",rate:0.20,perc:"61 to 90 min/inch",risk:"Often pushes the design toward a mound or aerobic system."},
  clay:{n:"Clay",rate:0.10,perc:"Over 90 min/inch",risk:"Conventional field usually fails. Expect an engineered system."}
};
