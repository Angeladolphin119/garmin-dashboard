import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from io import StringIO

st.set_page_config(
    page_title="Fitness Group Dashboard",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* Cream botanical background */
    .stApp { background-color: #fdf8f0 !important; }
    .stApp > header { background-color: transparent !important; }
    .main .block-container { position: relative; z-index: 1; }

    /* Metric cards — semi-transparent white so botanical bg shows through */
    .metric-card {
        background: rgba(255,255,255,0.82); border-radius: 12px;
        padding: 16px 20px; text-align: center;
        box-shadow: 0 2px 8px rgba(90,110,80,0.08);
    }
    .metric-label    { font-size: 12px; color: #6b7c5a; margin-bottom: 2px; }
    .metric-label-sk { font-size: 11px; color: #9aab8a; margin-bottom: 6px; font-style: italic; }
    .metric-value    { font-size: 28px; font-weight: 700; color: #4a7c5a; }
    .metric-unit     { font-size: 12px; color: #9aab8a; }
    .stTabs [data-baseweb="tab"] { font-size: 15px; padding: 10px 20px; }
    .bilingual-caption { color: #7a8a6a; font-size: 13px; }

    /* Fixed botanical illustration layer */
    .botanical-layer {
        position: fixed; top: 0; left: 0;
        width: 100vw; height: 100vh;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
</style>

<div class="botanical-layer">
<svg width="100%" height="100%" viewBox="0 0 1440 900"
     preserveAspectRatio="xMidYMid slice"
     xmlns="http://www.w3.org/2000/svg" opacity="0.52">
<defs>
  <style>
    .lf  { fill: #8aab7a; }
    .lf2 { fill: #6b8f5e; }
    .lf3 { fill: #a8c5a0; }
    .stm { stroke: #6b8f5e; stroke-width: 1.8; fill: none; stroke-linecap: round; }
    .pk  { fill: #e8b4b8; }
    .lv  { fill: #f5e0a8; }
    .pp  { fill: #c9b8d9; }
    .fc  { fill: #d4956a; }
    .bw1 { fill: #c4956a; }
    .bw2 { fill: #d4a870; }
    .bw3 { fill: #7a9eb8; }
    .bw4 { fill: #9ab8d0; }
    .bd  { fill: #4a3018; }
    .dw  { fill: rgba(154,181,168,0.25); stroke: #9ab5a8; stroke-width: 0.8; }
    .db  { fill: #7ab5c8; }
  </style>
</defs>

<!-- ── TOP-LEFT: large fern branch + butterfly ── -->

<path class="stm" d="M -20 -20 C 20 80 60 160 80 320"/>
<!-- fern leaflets -->
<path class="lf2" d="M 8 28 C 28 12 55 18 50 35 C 35 42 10 38 8 28" opacity=".75"/>
<path class="lf2" d="M 8 28 C -10 12 -30 20 -24 38 C -12 44 6 38 8 28" opacity=".75"/>
<path class="lf"  d="M 20 70 C 44 52 72 58 68 76 C 50 85 22 80 20 70" opacity=".75"/>
<path class="lf"  d="M 20 70 C 0 54 -24 62 -18 80 C -4 88 18 82 20 70" opacity=".75"/>
<path class="lf2" d="M 34 114 C 60 96 90 102 86 120 C 68 130 36 124 34 114" opacity=".7"/>
<path class="lf2" d="M 34 114 C 12 98 -16 106 -10 124 C 4 132 32 126 34 114" opacity=".7"/>
<path class="lf"  d="M 48 158 C 76 140 108 146 104 164 C 84 175 50 168 48 158" opacity=".65"/>
<path class="lf"  d="M 48 158 C 24 142 -4 150 2 168 C 18 177 46 170 48 158" opacity=".65"/>
<path class="lf3" d="M 60 200 C 84 184 112 190 108 206 C 90 216 62 210 60 200" opacity=".6"/>
<path class="lf3" d="M 60 200 C 38 186 14 194 20 210 C 36 220 58 212 60 200" opacity=".6"/>
<path class="lf3" d="M 70 238 C 92 224 116 230 112 244 C 96 252 72 246 70 238" opacity=".55"/>
<path class="lf3" d="M 70 238 C 50 224 28 232 34 246 C 50 254 68 248 70 238" opacity=".55"/>
<!-- secondary small fern -->
<path class="stm" d="M 130 55 C 158 88 172 140 176 200" opacity=".55"/>
<path class="lf3" d="M 146 90 C 164 76 186 82 182 96 C 166 105 148 99 146 90" opacity=".5"/>
<path class="lf3" d="M 146 90 C 128 78 108 86 114 100 C 128 108 144 102 146 90" opacity=".5"/>
<path class="lf3" d="M 158 124 C 174 112 194 118 190 130 C 176 138 160 132 158 124" opacity=".45"/>
<path class="lf3" d="M 158 124 C 142 114 124 120 130 132 C 142 140 156 134 158 124" opacity=".45"/>
<!-- round leaf cluster -->
<ellipse cx="200" cy="44"  rx="18" ry="11" class="lf"  transform="rotate(-20,200,44)"  opacity=".6"/>
<ellipse cx="220" cy="28"  rx="14" ry="9"  class="lf2" transform="rotate(12,220,28)"   opacity=".55"/>
<ellipse cx="178" cy="34"  rx="16" ry="10" class="lf3" transform="rotate(-40,178,34)"  opacity=".55"/>
<path class="stm" d="M 198 50 Q 188 64 178 60" opacity=".5"/>
<path class="stm" d="M 198 50 Q 208 64 220 36" opacity=".5"/>
<!-- butterfly (warm orange) -->
<g transform="translate(248,108) rotate(-15)">
  <path class="bw1" d="M 0 0 C -12 -28 -46 -22 -41 1 C -35 16 -12 12 0 0"/>
  <path class="bw1" d="M 0 0 C 12 -28 46 -22 41 1 C 35 16 12 12 0 0"/>
  <path class="bw2" d="M 0 0 C -10 8 -33 16 -29 30 C -18 39 -5 23 0 0"/>
  <path class="bw2" d="M 0 0 C 10 8 33 16 29 30 C 18 39 5 23 0 0"/>
  <path d="M 0 0 C -20 -10 -38 -8 -41 1" stroke="#a06828" stroke-width=".6" fill="none" opacity=".5"/>
  <path d="M 0 0 C 20 -10 38 -8 41 1"  stroke="#a06828" stroke-width=".6" fill="none" opacity=".5"/>
  <ellipse cx="0" cy="4" rx="2.5" ry="14" class="bd"/>
  <path d="M -2 -8 Q -14 -26 -18 -33" stroke="#4a3018" stroke-width="1" fill="none"/>
  <path d="M  2 -8 Q  14 -26  18 -33" stroke="#4a3018" stroke-width="1" fill="none"/>
  <circle cx="-18" cy="-33" r="2" class="bd"/>
  <circle cx=" 18" cy="-33" r="2" class="bd"/>
</g>
<!-- scattered tiny leaves top-left -->
<ellipse cx="318" cy="182" rx="14" ry="8"  class="lf3" transform="rotate(30,318,182)"  opacity=".4"/>
<ellipse cx="295" cy="225" rx="12" ry="7"  class="lf"  transform="rotate(-20,295,225)" opacity=".38"/>
<ellipse cx="340" cy="255" rx="10" ry="6"  class="lf2" transform="rotate(50,340,255)"  opacity=".35"/>

<!-- ── TOP-RIGHT: wildflowers + dragonfly ── -->

<!-- stem 1 → pink daisy -->
<path class="stm" d="M 1318 330 C 1316 268 1310 205 1306 142" opacity=".7"/>
<path class="lf"  d="M 1312 202 C 1330 186 1352 192 1347 210 C 1335 220 1313 214 1312 202" opacity=".65"/>
<g transform="translate(1306,135)">
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(0)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(45)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(90)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(135)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(180)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(225)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(270)"/>
  <ellipse cx="0" cy="-14" rx="5"   ry="11"  class="pk" transform="rotate(315)"/>
  <circle cx="0" cy="0" r="7" class="fc"/>
</g>
<!-- stem 2 → lavender -->
<path class="stm" d="M 1368 330 C 1364 268 1357 212 1350 166" opacity=".7"/>
<path class="lf2" d="M 1356 232 C 1338 217 1320 224 1325 242 C 1338 252 1355 246 1356 232" opacity=".65"/>
<g transform="translate(1350,158)">
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(0)"/>
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(60)"/>
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(120)"/>
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(180)"/>
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(240)"/>
  <ellipse cx="0" cy="-12" rx="4.5" ry="10"  class="pp" transform="rotate(300)"/>
  <circle cx="0" cy="0" r="6" class="fc"/>
</g>
<!-- stem 3 → yellow -->
<path class="stm" d="M 1408 330 C 1404 278 1400 228 1396 186" opacity=".65"/>
<g transform="translate(1396,178)">
  <ellipse cx="0" cy="-10" rx="4"   ry="9"   class="lv" transform="rotate(0)"/>
  <ellipse cx="0" cy="-10" rx="4"   ry="9"   class="lv" transform="rotate(72)"/>
  <ellipse cx="0" cy="-10" rx="4"   ry="9"   class="lv" transform="rotate(144)"/>
  <ellipse cx="0" cy="-10" rx="4"   ry="9"   class="lv" transform="rotate(216)"/>
  <ellipse cx="0" cy="-10" rx="4"   ry="9"   class="lv" transform="rotate(288)"/>
  <circle cx="0" cy="0" r="5.5" fill="#c8802a"/>
</g>
<!-- bud on side branch -->
<path class="stm" d="M 1318 280 C 1340 264 1360 257 1370 248" opacity=".55"/>
<path class="lf2" d="M 1370 244 C 1374 235 1382 234 1384 242 C 1382 251 1374 252 1370 244" opacity=".7"/>
<!-- grass blades -->
<path class="stm" d="M 1298 330 C 1293 302 1288 278 1282 258" opacity=".48"/>
<path class="stm" d="M 1432 330 C 1430 296 1434 272 1440 250" opacity=".48"/>
<ellipse cx="1282" cy="253" rx="8" ry="5" class="lf3" transform="rotate(-22,1282,253)" opacity=".5"/>
<!-- scattered leaves top-right -->
<ellipse cx="1258" cy="202" rx="14" ry="8"  class="lf"  transform="rotate(-30,1258,202)" opacity=".42"/>
<ellipse cx="1238" cy="242" rx="12" ry="7"  class="lf2" transform="rotate(20,1238,242)"  opacity=".38"/>
<ellipse cx="1278" cy="262" rx="10" ry="6"  class="lf3" transform="rotate(-45,1278,262)" opacity=".35"/>
<!-- dragonfly -->
<g transform="translate(1198,78) rotate(20)">
  <circle cx="0" cy="-22" r="8" class="db"/>
  <circle cx="-4" cy="-24" r="3" fill="#1a4858"/>
  <circle cx=" 4" cy="-24" r="3" fill="#1a4858"/>
  <ellipse cx="0" cy="-8"  rx="5" ry="9"  class="db"/>
  <ellipse cx="0" cy=" 10" rx="4" ry="10" fill="#6aa5b8"/>
  <ellipse cx="0" cy=" 26" rx="3" ry="8"  fill="#5a95a8"/>
  <ellipse cx="0" cy=" 38" rx="2.5" ry="7" fill="#4a85a0"/>
  <ellipse cx="0" cy=" 49" rx="2" ry="5"  fill="#3a7590"/>
  <ellipse cx="-30" cy="-5" rx="26" ry="9" class="dw" transform="rotate(-10,-30,-5)"/>
  <ellipse cx=" 30" cy="-5" rx="26" ry="9" class="dw" transform="rotate( 10, 30,-5)"/>
  <ellipse cx="-26" cy=" 8" rx="22" ry="7" class="dw" transform="rotate(-15,-26, 8)"/>
  <ellipse cx=" 26" cy=" 8" rx="22" ry="7" class="dw" transform="rotate( 15, 26, 8)"/>
</g>

<!-- ── BOTTOM-LEFT: fern cluster + bee ── -->

<path class="stm" d="M 0 900 C 22 858 42 820 62 778" opacity=".62"/>
<path class="lf2" d="M 20 866 C 38 852 60 858 56 872 C 42 882 22 876 20 866" opacity=".65"/>
<path class="lf2" d="M 20 866 C 4 854 -14 862 -8 876 C 4 886 18 880 20 866" opacity=".65"/>
<path class="lf"  d="M 36 836 C 56 822 78 828 74 842 C 58 852 38 846 36 836" opacity=".6"/>
<path class="lf"  d="M 36 836 C 18 824 -2 832 4 846 C 18 856 34 850 36 836" opacity=".6"/>
<path class="lf3" d="M 50 808 C 68 796 86 802 82 814 C 68 824 52 818 50 808" opacity=".55"/>
<path class="lf3" d="M 50 808 C 34 798 18 806 24 818 C 38 828 48 820 50 808" opacity=".55"/>
<!-- second frond -->
<path class="stm" d="M 82 900 C 108 858 130 820 150 778" opacity=".48"/>
<path class="lf3" d="M 98 868 C 118 854 140 860 136 874 C 120 884 100 878 98 868" opacity=".48"/>
<path class="lf3" d="M 98 868 C 80 856 60 864 66 878 C 80 888 96 882 98 868" opacity=".48"/>
<path class="lf3" d="M 118 836 C 136 824 156 830 152 842 C 138 852 120 846 118 836" opacity=".42"/>
<path class="lf3" d="M 118 836 C 102 826 84 834 90 846 C 102 856 116 850 118 836" opacity=".42"/>
<!-- round leaves -->
<ellipse cx="192" cy="856" rx="20" ry="12" class="lf"  transform="rotate(-15,192,856)" opacity=".58"/>
<ellipse cx="170" cy="838" rx="16" ry="10" class="lf2" transform="rotate(25,170,838)"  opacity=".52"/>
<ellipse cx="212" cy="828" rx="18" ry="11" class="lf3" transform="rotate(-40,212,828)" opacity=".48"/>
<ellipse cx="146" cy="868" rx="14" ry="9"  class="lf"  transform="rotate(10,146,868)"  opacity=".48"/>
<path class="stm" d="M 190 866 Q 186 846 170 840" opacity=".48"/>
<path class="stm" d="M 190 866 Q 196 844 212 831" opacity=".48"/>
<!-- small pink flower bottom-left -->
<path class="stm" d="M 252 900 C 250 874 246 848 242 818" opacity=".6"/>
<path class="lf2" d="M 246 858 C 262 844 278 850 274 862 C 262 872 246 866 246 858" opacity=".58"/>
<g transform="translate(242,812)">
  <ellipse cx="0" cy="-10" rx="4" ry="8" class="pk" transform="rotate(0)"   opacity=".8"/>
  <ellipse cx="0" cy="-10" rx="4" ry="8" class="pk" transform="rotate(72)"  opacity=".8"/>
  <ellipse cx="0" cy="-10" rx="4" ry="8" class="pk" transform="rotate(144)" opacity=".8"/>
  <ellipse cx="0" cy="-10" rx="4" ry="8" class="pk" transform="rotate(216)" opacity=".8"/>
  <ellipse cx="0" cy="-10" rx="4" ry="8" class="pk" transform="rotate(288)" opacity=".8"/>
  <circle cx="0" cy="0" r="5" class="fc"/>
</g>
<!-- bee -->
<g transform="translate(182,768) rotate(-30)">
  <ellipse cx="0" cy="0" rx="7" ry="12" fill="#d4a820"/>
  <rect x="-7" y="-5"   width="14" height="3.5" fill="#2a1a08" rx="1"/>
  <rect x="-7" y=" 1.5" width="14" height="3.5" fill="#2a1a08" rx="1"/>
  <ellipse cx="0" cy="-16" rx="6" ry="7" fill="#4a3808"/>
  <circle  cx="0" cy="-26" r="5.5"        fill="#3a2a08"/>
  <path d="M -3 -30 Q -10 -40 -12 -46" stroke="#2a1a08" stroke-width="1" fill="none"/>
  <path d="M  3 -30 Q  10 -40  12 -46" stroke="#2a1a08" stroke-width="1" fill="none"/>
  <circle cx="-12" cy="-46" r="1.5" fill="#2a1a08"/>
  <circle cx=" 12" cy="-46" r="1.5" fill="#2a1a08"/>
  <ellipse cx="-16" cy="-14" rx="14" ry="6" fill="rgba(200,220,240,.32)" stroke="rgba(100,150,200,.45)" stroke-width=".8" transform="rotate(-20,-16,-14)"/>
  <ellipse cx=" 16" cy="-14" rx="14" ry="6" fill="rgba(200,220,240,.32)" stroke="rgba(100,150,200,.45)" stroke-width=".8" transform="rotate( 20, 16,-14)"/>
  <ellipse cx="-12" cy=" -8" rx="10" ry="4.5" fill="rgba(200,220,240,.28)" stroke="rgba(100,150,200,.38)" stroke-width=".7" transform="rotate(-25,-12,-8)"/>
  <ellipse cx=" 12" cy=" -8" rx="10" ry="4.5" fill="rgba(200,220,240,.28)" stroke="rgba(100,150,200,.38)" stroke-width=".7" transform="rotate( 25, 12,-8)"/>
</g>

<!-- ── BOTTOM-RIGHT: trailing vine + butterfly ── -->

<path class="stm" d="M 1440 900 C 1400 858 1360 828 1330 788 C 1310 758 1290 728 1280 698" opacity=".65"/>
<!-- vine leaves -->
<path class="lf"  d="M 1402 868 C 1420 854 1442 860 1438 876 C 1426 887 1402 881 1402 868" opacity=".68"/>
<path class="lf2" d="M 1380 848 C 1362 834 1342 842 1348 858 C 1360 869 1379 863 1380 848" opacity=".63"/>
<path class="lf"  d="M 1356 822 C 1376 808 1398 814 1394 830 C 1380 841 1358 835 1356 822" opacity=".63"/>
<path class="lf3" d="M 1330 796 C 1312 782 1292 790 1298 806 C 1312 817 1328 811 1330 796" opacity=".58"/>
<path class="lf2" d="M 1310 770 C 1330 756 1350 764 1344 780 C 1332 791 1312 785 1310 770" opacity=".58"/>
<path class="lf"  d="M 1288 746 C 1270 732 1252 740 1258 756 C 1272 767 1286 761 1288 746" opacity=".52"/>
<!-- tendrils -->
<path d="M 1384 840 Q 1397 836 1406 846" stroke="#6b8f5e" stroke-width="1" fill="none" opacity=".48"/>
<path d="M 1347 812 Q 1360 806 1370 816" stroke="#6b8f5e" stroke-width="1" fill="none" opacity=".48"/>
<!-- small yellow flower bottom-right -->
<path class="stm" d="M 1440 852 C 1436 830 1428 806 1420 786" opacity=".58"/>
<g transform="translate(1420,780)">
  <ellipse cx="0" cy="-9" rx="3.5" ry="8" class="lv" transform="rotate(0)"   opacity=".8"/>
  <ellipse cx="0" cy="-9" rx="3.5" ry="8" class="lv" transform="rotate(72)"  opacity=".8"/>
  <ellipse cx="0" cy="-9" rx="3.5" ry="8" class="lv" transform="rotate(144)" opacity=".8"/>
  <ellipse cx="0" cy="-9" rx="3.5" ry="8" class="lv" transform="rotate(216)" opacity=".8"/>
  <ellipse cx="0" cy="-9" rx="3.5" ry="8" class="lv" transform="rotate(288)" opacity=".8"/>
  <circle cx="0" cy="0" r="5" fill="#c08028"/>
</g>
<!-- butterfly (blue) -->
<g transform="translate(1342,858) rotate(25)">
  <path class="bw3" d="M 0 0 C -10 -24 -40 -18 -36 4 C -30 16 -10 10 0 0"/>
  <path class="bw3" d="M 0 0 C  10 -24  40 -18  36 4 C  30 16  10 10 0 0"/>
  <path class="bw4" d="M 0 0 C -8 8 -28 14 -24 26 C -15 34 -4 20 0 0"/>
  <path class="bw4" d="M 0 0 C  8 8  28 14  24 26 C  15 34  4 20 0 0"/>
  <circle cx="-20" cy="-6" r="3" fill="rgba(255,255,255,.45)"/>
  <circle cx=" 20" cy="-6" r="3" fill="rgba(255,255,255,.45)"/>
  <ellipse cx="0" cy="4" rx="2" ry="12" class="bd"/>
  <path d="M -1.5 -7 Q -12 -22 -15 -28" stroke="#4a3018" stroke-width=".8" fill="none"/>
  <path d="M  1.5 -7 Q  12 -22  15 -28" stroke="#4a3018" stroke-width=".8" fill="none"/>
  <circle cx="-15" cy="-28" r="1.5" class="bd"/>
  <circle cx=" 15" cy="-28" r="1.5" class="bd"/>
</g>

<!-- ── SCATTERED ACCENTS ── -->

<!-- floating petals -->
<ellipse cx="452" cy="152" rx="5"   ry="3"   class="pk" transform="rotate(30,452,152)"   opacity=".3"/>
<ellipse cx="682" cy="82"  rx="4"   ry="2.5" class="lv" transform="rotate(-20,682,82)"   opacity=".28"/>
<ellipse cx="824" cy="202" rx="5"   ry="3"   class="pp" transform="rotate(50,824,202)"   opacity=".28"/>
<ellipse cx="962" cy="122" rx="4"   ry="2.5" class="pk" transform="rotate(-15,962,122)"  opacity=".28"/>
<!-- tiny isolated leaves mid-screen -->
<path class="lf3" d="M 502 302 C 514 292 528 296 526 306 C 518 312 502 310 502 302" opacity=".32"/>
<path class="lf3" d="M 742 482 C 754 472 768 476 766 486 C 758 492 742 490 742 482" opacity=".28"/>
<path class="lf2" d="M 1052 402 C 1064 392 1078 396 1076 406 C 1068 412 1052 410 1052 402" opacity=".28"/>
<!-- pollen dots -->
<circle cx="382" cy="422" r="2"   fill="#d4956a" opacity=".22"/>
<circle cx="602" cy="582" r="1.5" fill="#d4956a" opacity=".18"/>
<circle cx="902" cy="352" r="2"   fill="#c9b8d9" opacity=".22"/>
<circle cx="1102" cy="602" r="1.5" fill="#e8b4b8" opacity=".18"/>
<!-- distant small butterfly (centre) -->
<g transform="translate(1082,442) scale(.55)" opacity=".28">
  <path class="bw1" d="M 0 0 C -10 -22 -38 -16 -34 4 C -28 15 -10 9 0 0"/>
  <path class="bw1" d="M 0 0 C  10 -22  38 -16  34 4 C  28 15  10 9 0 0"/>
  <path class="bw2" d="M 0 0 C -8 7 -26 13 -22 25 C -14 32 -4 19 0 0"/>
  <path class="bw2" d="M 0 0 C  8 7  26 13  22 25 C  14 32  4 19 0 0"/>
  <ellipse cx="0" cy="4" rx="2" ry="11" class="bd"/>
</g>

</svg>
</div>
""", unsafe_allow_html=True)

COLORS = px.colors.qualitative.Set2

# Column name mapping (internal → display "EN / SK")
COL = {
    "date":        "Date / Dátum",
    "name":        "Name / Meno",
    "steps":       "Steps / Kroky",
    "distance_km": "Distance / Vzdialenosť (km)",
    "calories":    "Calories / Kalórie",
    "active_min":  "Active min / Aktívne min",
    "resting_hr":  "Resting HR / Pokojová TF",
    "sleep_h":     "Sleep / Spánok (h)",
    "run_km":      "Running / Beh (km)",
}


# ── GitHub storage ────────────────────────────────────────────────────────────

@st.cache_resource
def get_repo():
    from github import Github
    g = Github(st.secrets["GITHUB_TOKEN"])
    return g.get_repo(st.secrets["GITHUB_REPO"])


@st.cache_data(ttl=60, show_spinner=False)
def load_all_data() -> pd.DataFrame:
    from github import GithubException
    repo = get_repo()
    dfs = []
    try:
        for f in repo.get_contents("data"):
            if f.name.endswith(".csv"):
                dfs.append(pd.read_csv(StringIO(f.decoded_content.decode("utf-8"))))
    except GithubException:
        pass

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    for col in ["steps", "distance_km", "calories", "active_min", "resting_hr", "sleep_h", "run_km"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df.sort_values("date")


def save_person_data(name: str, rows: list[dict]):
    from github import GithubException
    repo = get_repo()
    path = f"data/{name}.csv"
    new_df = pd.DataFrame(rows)

    try:
        f = repo.get_contents(path)
        existing = pd.read_csv(StringIO(f.decoded_content.decode("utf-8")))
        merged = (
            pd.concat([existing, new_df], ignore_index=True)
            .drop_duplicates(subset=["date"], keep="last")
            .sort_values("date")
        )
        repo.update_file(path, f"sync: {name}", merged.to_csv(index=False), f.sha)
    except GithubException:
        repo.create_file(path, f"init: {name}", new_df.to_csv(index=False))


# ── Garmin fetch ──────────────────────────────────────────────────────────────

def fetch_garmin(email: str, password: str, date_str: str) -> dict:
    from garminconnect import Garmin
    if "garmin_client" not in st.session_state:
        client = Garmin(email, password)
        client.login()
        st.session_state["garmin_client"] = client
    client = st.session_state["garmin_client"]

    stats      = client.get_stats(date_str)
    steps      = stats.get("totalSteps", 0) or 0
    distance_m = stats.get("totalDistance", 0) or 0
    calories   = stats.get("activeKilocalories", 0) or 0
    active_min = round((stats.get("activeSeconds", 0) or 0) / 60)
    resting_hr = stats.get("restingHeartRate", 0) or 0

    sleep_h = 0.0
    try:
        secs   = client.get_sleep_data(date_str).get("dailySleepDTO", {}).get("sleepTimeSeconds", 0) or 0
        sleep_h = round(secs / 3600, 1)
    except Exception:
        pass

    run_km = 0.0
    try:
        acts   = client.get_activities_by_date(date_str, date_str, "running")
        run_km = round(sum((a.get("distance", 0) or 0) for a in acts) / 1000, 2)
    except Exception:
        pass

    return {
        "date":        date_str,
        "name":        None,  # filled by caller
        "steps":       steps,
        "distance_km": round(distance_m / 1000, 2),
        "calories":    calories,
        "active_min":  active_min,
        "resting_hr":  resting_hr,
        "sleep_h":     sleep_h,
        "run_km":      run_km,
    }


# ── Tab 1: Sync / Synchronizovať ─────────────────────────────────────────────

def tab_sync():
    st.header("Sync My Data / Synchronizovať moje dáta")
    st.markdown(
        '<p class="bilingual-caption">'
        "Enter your Garmin credentials to sync data to the shared group repository. "
        "Your password is used only during this session and is never stored.<br>"
        "<i>Zadajte prihlasovacie údaje Garmin na synchronizáciu dát. "
        "Heslo sa používa iba počas tohto sedenia a nikdy sa neukladá.</i>"
        "</p>",
        unsafe_allow_html=True,
    )

    with st.form("sync_form"):
        name  = st.text_input(
            "Nickname / Prezývka",
            placeholder="e.g. Peter / napr. Peter",
        )
        email = st.text_input("Garmin Email")
        pw    = st.text_input("Garmin Password / Heslo", type="password")

        c1, c2 = st.columns(2)
        with c1:
            start = st.date_input("Start date / Dátum začiatku", value=date.today() - timedelta(days=6))
        with c2:
            end   = st.date_input("End date / Dátum konca",      value=date.today())

        submitted = st.form_submit_button(
            "Start Sync / Začať synchronizáciu",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return
    if not (name and email and pw):
        st.error("Please fill in all fields. / Vyplňte všetky polia.")
        return

    date_list = [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end - start).days + 1)
    ]

    progress = st.progress(0, text="Logging into Garmin / Prihlasovanie do Garmin…")
    results, rows = [], []

    try:
        from garminconnect import Garmin
        st.session_state.pop("garmin_client", None)
        client = Garmin(email, pw)
        client.login()
        st.session_state["garmin_client"] = client
    except Exception as e:
        st.error(f"Garmin login failed / Prihlasovanie zlyhalo: {e}")
        return

    for i, d in enumerate(date_list):
        progress.progress(
            (i + 1) / len(date_list),
            text=f"Fetching / Načítavanie {d}…",
        )
        try:
            row = fetch_garmin(email, pw, d)
            row["name"] = name
            rows.append(row)
            results.append({
                "Date / Dátum":    d,
                "Steps / Kroky":   f"{row['steps']:,}",
                "Run / Beh (km)":  row["run_km"],
                "Sleep / Spánok":  f"{row['sleep_h']} h",
                "Status / Stav":   "✅",
            })
        except Exception as e:
            results.append({"Date / Dátum": d, "Status / Stav": f"❌ {e}"})

    progress.empty()

    if rows:
        with st.spinner("Saving to GitHub / Ukladanie na GitHub…"):
            save_person_data(name, rows)
        st.cache_data.clear()
        st.cache_resource.clear()

    st.success(
        f"Done! Synced {len(rows)} days. / "
        f"Hotovo! Synchronizovaných {len(rows)} dní."
    )
    st.dataframe(pd.DataFrame(results), use_container_width=True)


# ── Tab 2: Dashboard ──────────────────────────────────────────────────────────

def metric_card(label_en: str, label_sk: str, value, unit: str = ""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label_en}</div>
        <div class="metric-label-sk">{label_sk}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>""", unsafe_allow_html=True)


def tab_dashboard():
    st.header("Group Dashboard / Skupinový prehľad")

    with st.spinner("Loading data / Načítavanie dát…"):
        df_all = load_all_data()

    if df_all.empty:
        st.info(
            "No data yet — go to **Sync My Data** tab to add your Garmin account.\n\n"
            "*Zatiaľ žiadne dáta — prejdite na záložku Synchronizovať a pridajte účet Garmin.*"
        )
        return

    c1, c2 = st.columns([2, 3])
    with c1:
        min_d, max_d = df_all["date"].min().date(), df_all["date"].max().date()
        dr = st.date_input(
            "Date range / Časové obdobie",
            value=(max(min_d, max_d - timedelta(days=29)), max_d),
            min_value=min_d, max_value=max_d,
        )
    with c2:
        members  = sorted(df_all["name"].unique()) if "name" in df_all.columns else []
        selected = st.multiselect("Members / Členovia", members, default=members)

    if len(dr) != 2 or not selected:
        return

    df = df_all[
        (df_all["date"].dt.date >= dr[0]) &
        (df_all["date"].dt.date <= dr[1]) &
        (df_all["name"].isin(selected))
    ]

    if df.empty:
        st.warning("No data for the selected filters. / Žiadne dáta pre zvolené filtre.")
        return

    # Metric cards
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: metric_card("Avg Steps",    "Priem. kroky",   f"{int(df['steps'].mean()):,}",          "steps/day · krokov/deň")
    with m2: metric_card("Total Running","Celkový beh",    f"{df['run_km'].sum():.1f}",              "km")
    with m3: metric_card("Avg Calories", "Priem. kalórie", f"{int(df['calories'].mean())}",          "kcal/day · deň")
    with m4: metric_card("Avg Sleep",    "Priem. spánok",  f"{df['sleep_h'].mean():.1f}",            "h/day · deň")
    with m5: metric_card("Active Days",  "Aktívne dni",    f"{df[df['steps']>0]['date'].nunique()}", "days · dní")

    st.markdown("---")

    # Daily steps trend
    fig = px.line(
        df, x="date", y="steps", color="name",
        title="Daily Steps Trend / Denný trend krokov",
        labels={"date": "Date / Dátum", "steps": "Steps / Kroky", "name": "Name / Meno"},
        color_discrete_sequence=COLORS, markers=True,
    )
    fig.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        rank = df.groupby("name")["steps"].sum().reset_index().sort_values("steps")
        fig  = px.bar(
            rank, x="steps", y="name", orientation="h",
            title="Steps Ranking / Rebríček krokov",
            labels={"steps": "Steps / Kroky", "name": "Name / Meno"},
            color="steps", color_continuous_scale="Blues", text="steps",
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        run = df[df["run_km"] > 0]
        if run.empty:
            st.info("No running records in this period.\n\n*Žiadne záznamy behu v tomto období.*")
        else:
            fig = px.bar(
                run, x="date", y="run_km", color="name",
                title="Daily Running Distance / Denná vzdialenosť behu",
                labels={"date": "Date / Dátum", "run_km": "km", "name": "Name / Meno"},
                color_discrete_sequence=COLORS, barmode="stack",
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.line(
            df, x="date", y="sleep_h", color="name",
            title="Sleep Hours / Hodiny spánku",
            labels={"date": "Date / Dátum", "sleep_h": "Hours / Hodiny", "name": "Name / Meno"},
            color_discrete_sequence=COLORS, markers=True,
        )
        fig.add_hline(
            y=7, line_dash="dot", line_color="orange",
            annotation_text="Recommended 7h / Odporúčané 7h",
        )
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = px.area(
            df, x="date", y="calories", color="name",
            title="Calories Burned / Spálené kalórie",
            labels={"date": "Date / Dátum", "calories": "kcal", "name": "Name / Meno"},
            color_discrete_sequence=COLORS,
        )
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # Radar chart
    if "name" in df.columns:
        metrics = ["steps", "run_km", "sleep_h", "active_min", "calories"]
        summary = df.groupby("name")[metrics].mean()
        norm    = (summary - summary.min()) / (summary.max() - summary.min() + 1e-9)
        labels  = ["Steps\nKroky", "Running\nBeh", "Sleep\nSpánok", "Active\nAktívny", "Calories\nKalórie"]
        fig     = go.Figure()
        for i, (person, row) in enumerate(norm.iterrows()):
            fig.add_trace(go.Scatterpolar(
                r=list(row) + [row.iloc[0]],
                theta=labels + [labels[0]],
                fill="toself", name=person,
                line_color=COLORS[i % len(COLORS)],
            ))
        fig.update_layout(
            title="Personal Fitness Profile / Osobný fitness profil",
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            height=420,
        )
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 Raw Data / Surové dáta"):
        display_df = df.sort_values("date", ascending=False).reset_index(drop=True)
        display_df.columns = [COL.get(c, c) for c in display_df.columns]
        st.dataframe(display_df, use_container_width=True)

    if st.button("🔄 Reload / Obnoviť"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.title("🏃 Fitness Group Dashboard / Skupinový fitness prehľad")
    tab1, tab2 = st.tabs([
        "📥 Sync My Data / Synchronizovať dáta",
        "📊 Group Dashboard / Skupinový prehľad",
    ])
    with tab1:
        tab_sync()
    with tab2:
        tab_dashboard()


if __name__ == "__main__":
    main()
