# Septic System Calculator — Project Files

Ye file har cheez ko simple tareeqe se samjhati hai. VS Code me
poora folder kholo, phir ye padho.

===============================================================
  SABSE ZAROORI BAAT — PEHLE YE SAMJHO
===============================================================

Is project me 2 tarah ki files hain:

  1. SOURCE files  → jinse site banti hai (tum yahan edit karte ho)
  2. OUTPUT files  → jo site banti hai   (ye deploy hoti hai)

  SOURCE                          OUTPUT
  ------                          ------
  build.py          }
  statedata.py      }  se banta   →   site/  (71 HTML files)
  assets/*          }

Jab tum SOURCE badal ke `python3 build.py` chalate ho,
OUTPUT (site/ folder) naya ban jaata hai.

>>> Jo cheez deploy hoti hai wo hamesha `site/` folder hai. <<<


===============================================================
  KAUNSI FILE KYA KARTI HAI
===============================================================

DESIGN / LOOK
-------------
assets/site.css
    Saara design yahan hai — colours, fonts, spacing, mobile
    layout, buttons, sab kuch. Site ka 90% "look" isi file me.
    >> Mobile ke masle yahan fix hote hain. <<
    Ye normal CSS hai. Seedha edit kar sakte ho.

CALCULATOR LOGIC
----------------
assets/calc.js
    Chaaro calculators ki maths aur behaviour. Jab button dabta
    hai, ye file result nikalti hai. Sizing formulas yahan hain.

assets/states.js
    Har state ke NUMBERS: minimum tank size, design flow, cost
    tier. Agar kisi state ka number galat ho to yahan theek karo.

STATE PAGES KA CONTENT
----------------------
statedata.py
    50 state pages ka likha hua content — code citations, soil
    info, county lists, FAQs. Texas ka paragraph badalna hai?
    Yahan `"tx"` dhundo aur edit karo.

PAGE STRUCTURE / TEMPLATES
--------------------------
build.py
    Har page ka HTML dhaancha. Homepage, calculators, state page
    template, footer, header — sab yahan define hote hain. Ye
    sabse "technical" file hai. Layout badalna ho to yahan.

OUTPUT
------
site/
    Ye 71 ready HTML files. YE DEPLOY HOTI HAIN. Inhe seedha
    edit MAT karo agar tum build.py bhi use kar rahe ho — kyunki
    agli baar build chalega to tumhari edit mit jayegi.


===============================================================
  DO WORKFLOWS — APNA CHUNO
===============================================================

--- WORKFLOW A: Bina Python (asaan) ------------------------
Agar tum Python use nahi karna chahte:
  1. Sirf `site/` folder use karo
  2. HTML files seedha edit karo
  3. Design ke liye `site/assets/site.css` edit karo
  4. `site/` folder deploy karo
Nuqsaan: agar ek cheez saari 50 state pages me badalni ho,
to 50 files alag alag badalni padengi.

--- WORKFLOW B: Python ke saath (behtar control) -----------
  1. Source edit karo (statedata.py / build.py / assets)
  2. Terminal me chalao:  python3 build.py
  3. Naya `site/` folder ban jayega
  4. `site/` deploy karo
Faida: ek jagah se saari 50 pages control hoti hain.


===============================================================
  PYTHON KAISE CHALANA HAI (Workflow B ke liye)
===============================================================

1. Python installed hai? Terminal me likho:
       python3 --version
   Agar version dikhe to theek. Nahi to python.org se install karo.

2. Is folder me terminal kholo (VS Code me: Terminal > New Terminal)

3. Chalao:
       python3 build.py

4. "built 71 pages" dikhega. Bas. site/ folder taiyaar.


===============================================================
  MUJHE (CLAUDE KO) KAAM KAISE DENA HAI
===============================================================

Efficient tareeqa (kam credits):

  1. Batao kaunsi FILE aur kya masla
     misaal: "site.css me mobile pe homepage ka calculator
              button screen se bahar ja raha hai"

  2. Ho sake to screenshot bhejo

  3. Main us file ka updated version dunga

  4. Tum purani file ko nayi se replace kar doge

Poori site dobara banane ki zarurat nahi hoti — zyadatar fixes
ek file me hote hain (aksar site.css).


===============================================================
  MOBILE ISSUE — SABSE PEHLE YAHAN DEKHO
===============================================================

Mobile ke 90% masle assets/site.css me in cheezon se hote hain:
  - `.row` grid → chhoti screen pe single column hona chahiye
  - `.hero-grid` → stack hona chahiye
  - Koi fixed width jo screen se bahar ja rahi ho
  - Text size clamp() values

Agar mobile pe kuch toota ho: page ka naam + screenshot bhejo,
main site.css ka fix de dunga.
