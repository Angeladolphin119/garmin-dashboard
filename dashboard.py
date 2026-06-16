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
    /* Forest-morning background */
    .stApp { background-color: #f0f4ee !important; }
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
     xmlns="http://www.w3.org/2000/svg" opacity="0.70">
<defs>
  <style>
    /* Japanese hand-drawn palette */
    .tr   { fill:none; stroke:#2a4020; stroke-linecap:round; stroke-linejoin:round; }
    .lf   { fill:#6a9050; stroke:#3a5828; stroke-width:0.6; }
    .lf2  { fill:#8ab870; stroke:#4a6838; stroke-width:0.5; }
    .lf3  { fill:#b0d090; stroke:#6a8850; stroke-width:0.4; }
    .lf4  { fill:#4a6830; stroke:#2a4018; stroke-width:0.7; }
    .stm  { fill:none; stroke:#3a5828; stroke-linecap:round; }
    .msh  { fill:#d06840; stroke:#904828; stroke-width:0.9; stroke-linecap:round; }
    .msh2 { fill:#f8c898; stroke:#d06840; stroke-width:0.6; }
    .cl_s { fill:rgba(230,248,232,0.92); stroke:#5a9060; stroke-width:1.1; }
    .cl_p { fill:#c8de50; stroke:#88a028; stroke-width:0.8; }
    .cl_l { fill:#4a8038; stroke:#2a5820; stroke-width:1.0; }
    .bt_h { fill:#161008; stroke:#080604; stroke-width:0.8; }
    .bt_e { fill:#201808; stroke:#100804; stroke-width:0.7; }
    .bt_l { fill:#382018; stroke:#180808; stroke-width:0.6; }
    .ow_b { fill:#b88040; stroke:#7a5020; stroke-width:0.8; }
    .ow_f { fill:#f0e8c0; stroke:#c8a860; stroke-width:0.6; }
    .pd_w { fill:#f0f0ee; stroke:#c8c8c0; stroke-width:0.8; }
    .pd_b { fill:#181818; stroke:#080808; stroke-width:0.5; }
    .bam  { fill:#68a038; stroke:#3a6818; stroke-width:1.2; }
    .bam2 { fill:#90c860; stroke:#5a8838; stroke-width:0.7; }
    .rb_b { fill:#e8e0d8; stroke:#a09080; stroke-width:0.7; }
    .rb_i { fill:#f4c8c0; stroke:#d8a098; stroke-width:0.5; }
    .fx   { fill:#d07030; stroke:#904820; stroke-width:0.7; }
    .fx_w { fill:#f4ece8; stroke:#c8a890; stroke-width:0.5; }
    .dw   { fill:rgba(180,225,215,0.45); stroke:rgba(120,180,165,0.55); stroke-width:0.6; }
    .grd  { fill:rgba(120,165,85,0.12); stroke:none; }
  </style>
</defs>

<!-- Subtle meadow wash -->
<ellipse cx="720" cy="920" rx="900" ry="140" class="grd"/>
<ellipse cx="200" cy="892" rx="250" ry="80" class="grd" opacity="0.6"/>
<ellipse cx="1280" cy="892" rx="220" ry="70" class="grd" opacity="0.6"/>


<!-- ═══════════════════════════════════════════
     LEFT: Forest tree with owl (日系手繪)
     ═══════════════════════════════════════════ -->
<g transform="translate(88,0)">
  <path class="tr" stroke-width="14" d="M 0 910 C 4 780 -6 650 2 500 C 8 380 -4 260 12 110 C 16 65 14 28 16 0"/>
  <path stroke="#2a4020" stroke-width="1.0" fill="none" d="M -4 760 Q 7 755 3 746"/>
  <path stroke="#2a4020" stroke-width="1.0" fill="none" d="M -1 692 Q 9 688 5 679"/>
  <path stroke="#2a4020" stroke-width="1.0" fill="none" d="M  3 624 Q 13 620 9 611"/>
  <path stroke="#2a4020" stroke-width="0.8" fill="none" d="M -2 555 Q 8 552 4 543"/>
  <path class="tr" stroke-width="7" d="M 2 480 C -28 442 -68 405 -96 365"/>
  <path class="tr" stroke-width="5" d="M -96 365 C -122 330 -130 298 -118 268"/>
  <path class="tr" stroke-width="4" d="M -96 365 C -75 342 -58 318 -48 288"/>
  <path class="tr" stroke-width="7" d="M 6 420 C 38 382 78 348 108 318"/>
  <path class="tr" stroke-width="4" d="M 108 318 C 130 298 138 278 132 252"/>
  <path class="tr" stroke-width="3" d="M 108 318 C 118 304 132 290 148 274"/>
  <path class="tr" stroke-width="5" d="M 10 300 C -18 265 -38 235 -28 205"/>
  <path class="tr" stroke-width="4" d="M 10 300 C 38 268 58 242 72 218"/>
  <ellipse cx="-120" cy="262" rx="36" ry="26" class="lf"  transform="rotate(-12,-120,262)"/>
  <ellipse cx="-102" cy="246" rx="28" ry="20" class="lf2" transform="rotate(10,-102,246)"/>
  <ellipse cx="-138" cy="278" rx="24" ry="17" class="lf3" transform="rotate(-28,-138,278)"/>
  <ellipse cx="-56"  cy="282" rx="24" ry="17" class="lf"  transform="rotate(22,-56,282)"/>
  <ellipse cx="135"  cy="246" rx="34" ry="24" class="lf2" transform="rotate(14,135,246)"/>
  <ellipse cx="150"  cy="268" rx="24" ry="17" class="lf3" transform="rotate(32,150,268)"/>
  <ellipse cx="118"  cy="234" rx="28" ry="20" class="lf"  transform="rotate(-8,118,234)"/>
  <ellipse cx="74"   cy="212" rx="28" ry="20" class="lf2" transform="rotate(24,74,212)"/>
  <ellipse cx="-28"  cy="196" rx="34" ry="24" class="lf"  transform="rotate(-6,-28,196)"/>
  <ellipse cx="-10"  cy="178" rx="26" ry="18" class="lf2" transform="rotate(14,-10,178)"/>
  <ellipse cx="14"   cy="88"  rx="42" ry="30" class="lf2" transform="rotate(-2,14,88)"/>
  <ellipse cx="-10"  cy="72"  rx="32" ry="23" class="lf"  transform="rotate(-18,-10,72)"/>
  <ellipse cx="36"   cy="70"  rx="28" ry="20" class="lf3" transform="rotate(18,36,70)"/>
  <ellipse cx="16"   cy="50"  rx="24" ry="17" class="lf4" transform="rotate(-8,16,50)"/>
  <path class="msh" d="M -30 872 C -30 856 -18 848 -16 854 C -14 848 -2 856 -2 872"/>
  <rect x="-22" y="867" width="13" height="20" class="msh2" rx="2"/>
  <circle cx="-16" cy="852" r="2.2" fill="rgba(255,255,255,0.5)"/>
  <circle cx="-10" cy="856" r="1.5" fill="rgba(255,255,255,0.4)"/>
  <path class="msh" d="M -52 880 C -52 866 -42 860 -40 864 C -38 860 -28 866 -28 880" opacity="0.8"/>
  <rect x="-46" y="875" width="11" height="16" class="msh2" rx="2" opacity="0.8"/>
  <path class="stm" stroke-width="1.3" d="M -65 910 C -62 892 -54 878 -44 862"/>
  <ellipse cx="-42" cy="860" rx="11" ry="6" class="lf3" transform="rotate(-28,-42,860)"/>
  <path class="stm" stroke-width="1.3" d="M -85 910 C -80 888 -70 870 -58 852"/>
  <ellipse cx="-55" cy="850" rx="9"  ry="5"  class="lf2" transform="rotate(25,-55,850)"/>
  <path class="stm" stroke-width="1.1" d="M -48 910 C -46 898 -40 886 -34 874"/>
  <ellipse cx="-32" cy="872" rx="8"  ry="5"  class="lf3" transform="rotate(-15,-32,872)"/>
</g>

<!-- OWL on left branch -->
<g transform="translate(12,348)">
  <ellipse cx="0" cy="0" rx="22" ry="28" class="ow_b"/>
  <path stroke="#7a5020" stroke-width="0.7" fill="none" d="M -18 -8 Q -10 -6 -18 2"/>
  <path stroke="#7a5020" stroke-width="0.7" fill="none" d="M -18  4 Q -10  6 -18 14"/>
  <path stroke="#7a5020" stroke-width="0.7" fill="none" d="M  18 -8 Q  10 -6  18 2"/>
  <path stroke="#7a5020" stroke-width="0.7" fill="none" d="M  18  4 Q  10  6  18 14"/>
  <ellipse cx="0" cy="-5" rx="15" ry="14" class="ow_f"/>
  <path class="ow_b" d="M -8 -18 C -10 -28 -6 -34 -4 -27 C -2 -20 -4 -16 -8 -18"/>
  <path class="ow_b" d="M  8 -18 C  10 -28  6 -34  4 -27 C  2 -20  4 -16  8 -18"/>
  <circle cx="-6" cy="-7" r="6.5" fill="#e8c028" stroke="#a07820" stroke-width="0.8"/>
  <circle cx=" 6" cy="-7" r="6.5" fill="#e8c028" stroke="#a07820" stroke-width="0.8"/>
  <circle cx="-5" cy="-7" r="3.8" fill="#181808"/>
  <circle cx=" 7" cy="-7" r="3.8" fill="#181808"/>
  <circle cx="-4" cy="-8.5" r="1.3" fill="white"/>
  <circle cx=" 8" cy="-8.5" r="1.3" fill="white"/>
  <path fill="#c8a038" d="M -3 0 Q 0 5 3 0 Q 0 2 -3 0"/>
  <path stroke="#7a5020" stroke-width="1.5" fill="none" d="M -8 27 Q -10 33 -15 37"/>
  <path stroke="#7a5020" stroke-width="1.5" fill="none" d="M -8 27 Q  -8 35  -8 39"/>
  <path stroke="#7a5020" stroke-width="1.5" fill="none" d="M  8 27 Q  10 33  15 37"/>
  <path stroke="#7a5020" stroke-width="1.5" fill="none" d="M  8 27 Q   8 35   8 39"/>
</g>

<!-- ═══════════════════════════════════════════
     RHINOCEROS BEETLE (独角仙) — center hero
     ═══════════════════════════════════════════ -->
<g transform="translate(720,135)">
  <path class="cl_l" d="M -90 90 C -68 72 0 68 68 78 C 88 85 80 102 56 100 C 32 96 -32 96 -60 100 C -84 103 -96 97 -90 90"/>
  <path stroke="#2a5820" stroke-width="0.7" fill="none" d="M -25 88 Q -55 100 -75 100"/>
  <path stroke="#2a5820" stroke-width="0.7" fill="none" d="M  8 86 Q  -8  98 -20 100"/>
  <path stroke="#2a5820" stroke-width="0.7" fill="none" d="M 38 88 Q  28  98  18 100"/>
  <path class="bt_h" d="M -6 -52 C -10 -76 -6 -115 4 -140 C 8 -150 14 -140 10 -122 C 14 -138 22 -145 24 -132 C 22 -116 10 -94 8 -72 C 6 -64 -2 -56 -6 -52"/>
  <path class="bt_h" d="M 12 -42 C 16 -56 22 -64 24 -72 C 28 -78 30 -70 26 -62 C 22 -54 18 -48 12 -42"/>
  <ellipse cx="4" cy="-32" rx="20" ry="15" class="bt_h"/>
  <circle cx="-12" cy="-34" r="5.5" fill="#382018" stroke="#080808" stroke-width="0.6"/>
  <circle cx=" 18" cy="-34" r="5.5" fill="#382018" stroke="#080808" stroke-width="0.6"/>
  <circle cx="-11" cy="-35" r="2.2" fill="#907060" opacity="0.5"/>
  <circle cx=" 19" cy="-35" r="2.2" fill="#907060" opacity="0.5"/>
  <path class="bt_e" d="M -24 -18 C -28 -8 -26 6 -22 14 C -18 20 18 20 22 14 C 26 6 28 -8 24 -18 C 18 -26 -18 -26 -24 -18"/>
  <path class="bt_e" d="M -24 12 C -28 30 -26 58 -20 75 C -16 84 -4 88 0 88 C 4 88 16 84 20 75 C 26 58 28 30 24 12 C 16 5 -16 5 -24 12"/>
  <line x1="0" y1="12" x2="0" y2="88" stroke="#080808" stroke-width="1.2"/>
  <circle cx="-13" cy="28"  r="1.8" fill="#080808" opacity="0.4"/>
  <circle cx="-11" cy="46"  r="1.8" fill="#080808" opacity="0.4"/>
  <circle cx=" -9" cy="64"  r="1.8" fill="#080808" opacity="0.4"/>
  <circle cx=" 13" cy="28"  r="1.8" fill="#080808" opacity="0.4"/>
  <circle cx=" 11" cy="46"  r="1.8" fill="#080808" opacity="0.4"/>
  <circle cx="  9" cy="64"  r="1.8" fill="#080808" opacity="0.4"/>
  <path fill="rgba(255,255,255,0.16)" stroke="none" d="M -18 14 C -20 24 -18 40 -12 44 C -8 42 -10 26 -12 14 C -14 10 -18 12 -18 14"/>
  <path class="bt_l" stroke-width="2.2" stroke-linecap="round" d="M -22 -12 C -40 -16 -56 -8 -66 0"/>
  <path class="bt_l" stroke-width="2.2" stroke-linecap="round" d="M  22 -12 C  40 -16  56 -8  66 0"/>
  <path class="bt_l" stroke-width="2.2" stroke-linecap="round" d="M -24  4  C -44  8 -62 20 -70 32"/>
  <path class="bt_l" stroke-width="2.2" stroke-linecap="round" d="M  24  4  C  44  8  62 20  70 32"/>
  <path class="bt_l" stroke-width="2.0" stroke-linecap="round" d="M -22 20 C -42 30 -58 48 -64 62"/>
  <path class="bt_l" stroke-width="2.0" stroke-linecap="round" d="M  22 20 C  42 30  58 48  64 62"/>
  <path stroke="#080808" stroke-width="1.5" fill="none" stroke-linecap="round" d="M -66 0 L -73 5 M -66 0 L -71 -6"/>
  <path stroke="#080808" stroke-width="1.5" fill="none" stroke-linecap="round" d="M  66 0 L  73 5 M  66 0 L  71 -6"/>
  <path stroke="#080808" stroke-width="1.5" fill="none" stroke-linecap="round" d="M -70 32 L -78 36 M -70 32 L -76 26"/>
  <path stroke="#080808" stroke-width="1.5" fill="none" stroke-linecap="round" d="M  70 32 L  78 36 M  70 32 L  76 26"/>
  <text x="0" y="120" font-family="serif" font-size="8.5" fill="#4a6830" text-anchor="middle" font-style="italic">Allomyrina dichotoma　独角仙</text>
</g>

<!-- ═══════════════════════════════════════════
     CALLA LILY (海芋) cluster — bottom left
     ═══════════════════════════════════════════ -->
<g transform="translate(195,715)">
  <path class="cl_l" d="M -80 185 C -56 148 -28 108 22 62 C 52 40 72 50 64 72 C 54 94 12 114 -20 145 C -50 175 -68 184 -80 185"/>
  <path stroke="#2a5820" stroke-width="0.8" fill="none" d="M -80 185 C -50 158 -8 118 32 80"/>
  <path stroke="#4a7835" stroke-width="0.5" fill="none" d="M -32 162 C -22 144  2 122 22 102"/>
  <path stroke="#4a7835" stroke-width="0.5" fill="none" d="M -58 174 C -46 156 -24 132 -4 112"/>
  <path stroke="#3a6025" stroke-width="5" fill="none" stroke-linecap="round" d="M -8 185 C -6 162 -3 140 2 118 C 7 96 10 76 12 55"/>
  <path class="cl_s" d="M 12 55 C -8 36 -18 16 -8 -4 C -3 -18 8 -23 15 -17 C 22 -11 28 2 30 22 C 34 43 32 58 12 55"/>
  <path class="cl_p" d="M 14 50 C 16 36 18 18 17 2 C 16 -10 20 -14 22 -4 C 24 8 22 32 20 50"/>
  <path stroke="#3a6025" stroke-width="4" fill="none" stroke-linecap="round" d="M 52 185 C 54 158 57 132 62 108 C 66 86 70 66 74 48"/>
  <path class="cl_s" d="M 74 48 C 60 30 54 12 64 -6 C 70 -18 80 -22 86 -16 C 92 -9 94 6 92 26 C 90 46 86 56 74 48" transform="rotate(10,74,48)"/>
  <path class="cl_p" d="M 78 44 C 80 26 82 10 80 -4 C 79 -14 84 -16 86 -6 C 88 6 86 28 82 44" transform="rotate(10,78,44)"/>
  <path class="cl_l" d="M 105 185 C 126 154 136 112 124 76 C 118 56 102 50 92 63 C 82 76 90 112 94 144 C 97 168 100 180 105 185"/>
  <path stroke="#2a5820" stroke-width="0.8" fill="none" d="M 105 185 C 110 154 114 116 106 80"/>
  <circle cx="98"  cy="110" r="3.5" class="dw"/>
  <circle cx="110" cy="132" r="2.8" class="dw"/>
  <circle cx="-36" cy="148" r="3.0" class="dw"/>
  <circle cx="18"  cy="170" r="2.5" class="dw"/>
</g>

<!-- RABBIT near calla lily -->
<g transform="translate(100,808)">
  <ellipse cx="0"  cy="0"   rx="24" ry="20" class="rb_b"/>
  <ellipse cx="14" cy="-22" rx="17" ry="15" class="rb_b"/>
  <path class="rb_b" d="M  7 -35 C  5 -58  7 -72 10 -70 C 13 -67 13 -54 11 -36"/>
  <path class="rb_i" d="M  8 -36 C  7 -54  8 -67 10 -65 C 12 -62 11 -52 11 -36"/>
  <path class="rb_b" d="M 20 -35 C 20 -58 24 -72 26 -68 C 28 -64 26 -52 24 -36"/>
  <path class="rb_i" d="M 21 -36 C 21 -54 24 -66 26 -63 C 27 -60 25 -50 24 -36"/>
  <circle cx="16" cy="-24" r="3.2" fill="#181818"/>
  <circle cx="17" cy="-25" r="1.1" fill="white"/>
  <circle cx="24" cy="-17" r="2.2" fill="#e0a0a0"/>
  <path stroke="#888080" stroke-width="0.5" fill="none" d="M 24 -18 Q 36 -20 42 -19"/>
  <path stroke="#888080" stroke-width="0.5" fill="none" d="M 24 -17 Q 36 -14 42 -12"/>
  <path stroke="#888080" stroke-width="0.5" fill="none" d="M 24 -18 Q 14 -20  8 -19"/>
  <circle cx="-22" cy="5" r="10" class="rb_b"/>
  <ellipse cx="18" cy="16" rx="9" ry="5" class="rb_b"/>
</g>

<!-- ═══════════════════════════════════════════
     RIGHT: Forest tree
     ═══════════════════════════════════════════ -->
<g transform="translate(1362,0)">
  <path class="tr" stroke-width="16" d="M 0 910 C 4 780 -4 652 6 502 C 14 382 4 255 -6 108 C -10 62 -6 26 -2 0"/>
  <path stroke="#2a4020" stroke-width="1.0" fill="none" d="M 2 762 Q 12 757 8 748"/>
  <path stroke="#2a4020" stroke-width="1.0" fill="none" d="M -1 690 Q 10 686 6 677"/>
  <path stroke="#2a4020" stroke-width="0.9" fill="none" d="M 2 620 Q 12 616 8 607"/>
  <path class="tr" stroke-width="8" d="M 4 452 C -28 413 -64 378 -92 342"/>
  <path class="tr" stroke-width="5" d="M -92 342 C -116 316 -122 286 -112 258"/>
  <path class="tr" stroke-width="4" d="M -92 342 C  -72 320  -56 298  -46 272"/>
  <path class="tr" stroke-width="6" d="M -1 382 C 22 352 48 332 60 312"/>
  <path class="tr" stroke-width="5" d="M -3 284 C -28 252 -48 226 -38 198"/>
  <path class="tr" stroke-width="4" d="M -3 284 C  18 256  38 236  44 208"/>
  <ellipse cx="-114" cy="252" rx="36" ry="26" class="lf"  transform="rotate(-10,-114,252)"/>
  <ellipse cx="-96"  cy="238" rx="28" ry="20" class="lf2" transform="rotate(14,-96,238)"/>
  <ellipse cx="-130" cy="268" rx="24" ry="17" class="lf3" transform="rotate(-24,-130,268)"/>
  <ellipse cx="-50"  cy="266" rx="26" ry="18" class="lf2" transform="rotate(20,-50,266)"/>
  <ellipse cx="46"   cy="202" rx="32" ry="22" class="lf"  transform="rotate(14,46,202)"/>
  <ellipse cx="62"   cy="306" rx="26" ry="18" class="lf2" transform="rotate(20,62,306)"/>
  <ellipse cx="-40"  cy="192" rx="34" ry="24" class="lf"  transform="rotate(-7,-40,192)"/>
  <ellipse cx="-20"  cy="176" rx="28" ry="20" class="lf2" transform="rotate(12,-20,176)"/>
  <ellipse cx="-4"   cy="88"  rx="40" ry="28" class="lf2" transform="rotate(-4,-4,88)"/>
  <ellipse cx="16"   cy="72"  rx="30" ry="21" class="lf3" transform="rotate(20,16,72)"/>
  <ellipse cx="-22"  cy="70"  rx="26" ry="18" class="lf"  transform="rotate(-18,-22,70)"/>
  <path class="msh" d="M 22 868 C 22 854 32 848 34 852 C 36 848 46 854 46 868"/>
  <rect x="31" y="863" width="12" height="20" class="msh2" rx="2"/>
  <circle cx="34" cy="850" r="2" fill="rgba(255,255,255,0.5)"/>
</g>

<!-- ═══════════════════════════════════════════
     PANDA (動物園) with bamboo — bottom right
     ═══════════════════════════════════════════ -->
<g transform="translate(1222,782)">
  <path class="bam" stroke-width="9"  d="M -55 118 C -53 80 -55 42 -53 0 C -51 -40 -55 -72 -54 -102"/>
  <path stroke="#3a6818" stroke-width="1.2" fill="none" d="M -55 78 Q -44 74 -55 70"/>
  <path stroke="#3a6818" stroke-width="1.2" fill="none" d="M -54 38 Q -43 34 -54 30"/>
  <path stroke="#3a6818" stroke-width="1.2" fill="none" d="M -53 -2 Q -42 -6 -53 -10"/>
  <path class="bam2" d="M -55 56 C -46 44 -30 42 -28 50 C -26 58 -40 62 -55 56"/>
  <path class="bam2" d="M -55 16 C -64  4 -78  2 -80 10 C -82 18 -68 22 -55 16"/>
  <path class="bam2" d="M -54 -32 C -45 -44 -28 -48 -26 -40 C -24 -32 -38 -26 -54 -32"/>
  <path class="bam" stroke-width="7"  d="M 75 118 C 75 80 77 42 75 0"/>
  <path stroke="#3a6818" stroke-width="1.1" fill="none" d="M 75 62 Q 86 58 75 54"/>
  <path class="bam2" d="M 75 32 C 84 20 98 18 100 26 C 102 34 88 38 75 32"/>
  <ellipse cx="0"  cy="20" rx="52" ry="47" class="pd_w"/>
  <circle  cx="0"  cy="-40" r="44" class="pd_w"/>
  <circle  cx="-30" cy="-78" r="16" class="pd_b"/>
  <circle  cx=" 30" cy="-78" r="16" class="pd_b"/>
  <ellipse cx="-14" cy="-48" rx="13" ry="11" class="pd_b" transform="rotate(-15,-14,-48)"/>
  <ellipse cx=" 14" cy="-48" rx="13" ry="11" class="pd_b" transform="rotate(15,14,-48)"/>
  <circle cx="-12" cy="-49" r="6"   fill="white"/>
  <circle cx=" 12" cy="-49" r="6"   fill="white"/>
  <circle cx="-10" cy="-49" r="3.5" fill="#181818"/>
  <circle cx=" 14" cy="-49" r="3.5" fill="#181818"/>
  <circle cx=" -9" cy="-50" r="1.3" fill="white"/>
  <circle cx=" 15" cy="-50" r="1.3" fill="white"/>
  <ellipse cx="0" cy="-30" rx="6.5" ry="4.5" fill="#282018"/>
  <path stroke="#282018" stroke-width="1.3" fill="none" d="M -5 -25 Q 0 -20 5 -25"/>
  <path class="pd_b" d="M -48  8 C -62 -2 -68 18 -62 34 C -57 44 -46 32 -42 18"/>
  <path class="pd_b" d="M  48  8 C  62 -2  68 18  62 34 C  57 44  46 32  42 18"/>
  <ellipse cx="-26" cy="64" rx="21" ry="15" class="pd_b"/>
  <ellipse cx=" 26" cy="64" rx="21" ry="15" class="pd_b"/>
  <ellipse cx="-36" cy="72" rx="16" ry="11" class="pd_w"/>
  <ellipse cx=" 36" cy="72" rx="16" ry="11" class="pd_w"/>
  <path class="bam" stroke-width="5" d="M -50 -12 C -48 8 -46 32 -48 52"/>
</g>

<!-- FOX (狐) — center bottom -->
<g transform="translate(720,848)" opacity="0.80">
  <ellipse cx="0"  cy="0"   rx="28" ry="18" class="fx"/>
  <ellipse cx="22" cy="-18" rx="18" ry="15" class="fx"/>
  <path class="fx"   d="M 14 -30 C 12 -46 17 -54 20 -50 C 23 -46 22 -34 20 -30"/>
  <path fill="#f4ece8" d="M 15 -32 C 14 -44 18 -50 20 -47 C 22 -44 21 -36 20 -32"/>
  <path class="fx"   d="M 28 -30 C 28 -46 33 -54 35 -50 C 37 -46 35 -34 30 -30"/>
  <path fill="#f4ece8" d="M 29 -32 C 29 -44 33 -50 35 -47 C 37 -44 34 -36 30 -32"/>
  <path class="fx_w" d="M 22 -22 C 14 -24 10 -16 12 -8 C 14 0 22 4 30 0 C 38 -6 38 -20 30 -24 C 28 -26 24 -24 22 -22"/>
  <circle cx="22" cy="-18" r="4"   fill="#181808"/>
  <circle cx="23" cy="-19" r="1.5" fill="white"/>
  <circle cx="36" cy="-12" r="2.5" fill="#181808"/>
  <path class="fx"   d="M -28 0 C -48 -8 -65 -5 -70 8 C -75 20 -62 30 -45 28 C -28 26 -14 16 -28 0"/>
  <path class="fx_w" d="M -64 6 C -72 12 -74 22 -66 28 C -58 32 -48 28 -46 22 C -48 16 -58 10 -64 6"/>
</g>

<!-- Flying birds -->
<g transform="translate(475,86)" opacity="0.65">
  <path fill="#4a6830" d="M 0 0 C -8 -7 -18 -5 -22 0"/>
  <path fill="#4a6830" d="M 0 0 C  8 -7  18 -5  22 0"/>
  <ellipse cx="0" cy="2" rx="4" ry="3" fill="#3a5820"/>
</g>
<g transform="translate(965,62)" opacity="0.60">
  <path fill="#4a6830" d="M 0 0 C -6 -5 -14 -4 -18 0"/>
  <path fill="#4a6830" d="M 0 0 C  6 -5  14 -4  18 0"/>
  <ellipse cx="0" cy="2" rx="3.5" ry="2.5" fill="#3a5820"/>
</g>
<g transform="translate(790,148)" opacity="0.50">
  <path fill="#6a8850" d="M 0 0 C -5 -4 -12 -3 -15 0"/>
  <path fill="#6a8850" d="M 0 0 C  5 -4  12 -3  15 0"/>
  <ellipse cx="0" cy="2" rx="3" ry="2" fill="#5a7840"/>
</g>
<g transform="translate(295,155)" opacity="0.45">
  <path fill="#5a7840" d="M 0 0 C -5 -4 -11 -3 -14 0"/>
  <path fill="#5a7840" d="M 0 0 C  5 -4  11 -3  14 0"/>
  <ellipse cx="0" cy="2" rx="3" ry="2" fill="#4a6830"/>
</g>

<!-- Floating leaves -->
<ellipse cx="410"  cy="198" rx="12" ry="7"  class="lf2" transform="rotate(38,410,198)"   opacity="0.48"/>
<ellipse cx="628"  cy="285" rx="10" ry="6"  class="lf3" transform="rotate(-18,628,285)"  opacity="0.42"/>
<ellipse cx="856"  cy="322" rx="11" ry="6"  class="lf"  transform="rotate(52,856,322)"   opacity="0.38"/>
<ellipse cx="1108" cy="245" rx="10" ry="6"  class="lf2" transform="rotate(-28,1108,245)" opacity="0.40"/>
<ellipse cx="528"  cy="465" rx="9"  ry="5"  class="lf3" transform="rotate(25,528,465)"   opacity="0.35"/>
<ellipse cx="932"  cy="418" rx="11" ry="6"  class="lf"  transform="rotate(-42,932,418)"  opacity="0.36"/>

<!-- Morning dewdrops -->
<circle cx="355"  cy="452" r="4.0" class="dw"/>
<circle cx="585"  cy="628" r="3.2" class="dw"/>
<circle cx="898"  cy="542" r="3.5" class="dw"/>
<circle cx="1188" cy="490" r="3.0" class="dw"/>
<circle cx="480"  cy="328" r="2.8" class="dw"/>
<circle cx="1048" cy="368" r="2.6" class="dw"/>

<!-- Small ferns -->
<g transform="translate(718,852)" opacity="0.55">
  <path stroke="#3a6028" stroke-width="1.5" fill="none" stroke-linecap="round" d="M 0 48 C 2 28 5 8 8 -12"/>
  <path class="lf3" d="M  4 28 C 15 20 24 20 23 28 C 21 35 11 35  4 28"/>
  <path class="lf3" d="M  4 28 C -5 20 -13 20 -12 28 C -10 35 0 35  4 28"/>
  <path class="lf2" d="M  6 12 C 17  5 26  5 25 13 C 23 20 13 20  6 12"/>
  <path class="lf2" d="M  6 12 C -2  5 -10  5 -9 13 C  -7 20 3 20  6 12"/>
  <path class="lf3" d="M  8 -2 C 17 -8 24 -8 23  0 C 21  7 13  7  8 -2"/>
  <path class="lf3" d="M  8 -2 C  1 -8  -5 -8 -4  0 C  -2  7 6  7  8 -2"/>
</g>
<g transform="translate(344,882)" opacity="0.48">
  <path stroke="#3a6028" stroke-width="1.2" fill="none" stroke-linecap="round" d="M 0 18 C 1 4 3 -10 5 -26"/>
  <path class="lf3" d="M  2 4 C 10 -2 16 -2 16  5 C 14 11  7 11  2  4"/>
  <path class="lf3" d="M  2 4 C -4 -2 -9 -2 -9  5 C  -7 11 0 11  2  4"/>
  <path class="lf2" d="M  4 -11 C 11 -17 16 -17 16 -10 C 14 -4  8 -4  4 -11"/>
  <path class="lf2" d="M  4 -11 C -1 -17 -6 -17 -6 -10 C  -4 -4 2 -4  4 -11"/>
</g>
<g transform="translate(1095,875)" opacity="0.45">
  <path stroke="#3a6028" stroke-width="1.2" fill="none" stroke-linecap="round" d="M 0 18 C 1 4 3 -10 5 -26"/>
  <path class="lf3" d="M  2 4 C 10 -2 16 -2 16  5 C 14 11  7 11  2  4"/>
  <path class="lf3" d="M  2 4 C -4 -2 -9 -2 -9  5 C  -7 11 0 11  2  4"/>
  <path class="lf2" d="M  4 -11 C 11 -17 16 -17 16 -10 C 14 -4  8 -4  4 -11"/>
  <path class="lf2" d="M  4 -11 C -1 -17 -6 -17 -6 -10 C  -4 -4 2 -4  4 -11"/>
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


# ── Watchlist (shared, stored in GitHub) ──────────────────────────────────────

@st.cache_data(ttl=30, show_spinner=False)
def load_watchlist() -> list:
    import json
    from github import GithubException
    repo = get_repo()
    try:
        f = repo.get_contents("data/watchlist.json")
        return json.loads(f.decoded_content.decode("utf-8"))
    except GithubException:
        return []


def save_watchlist(tickers: list):
    import json
    from github import GithubException
    repo = get_repo()
    path = "data/watchlist.json"
    content = json.dumps(tickers)
    try:
        f = repo.get_contents(path)
        repo.update_file(path, "watchlist update", content, f.sha)
    except GithubException:
        repo.create_file(path, "watchlist init", content)


# ── Market data (yfinance) ────────────────────────────────────────────────────

@st.cache_data(ttl=300, show_spinner=False)
def fetch_market_indices() -> list:
    import yfinance as yf
    indices = [("^GSPC", "S&P 500"), ("^IXIC", "NASDAQ"), ("^DJI", "Dow Jones")]
    out = []
    for sym, name in indices:
        try:
            h = yf.Ticker(sym).history(period="2d")
            if len(h) >= 2:
                prev, curr = float(h["Close"].iloc[-2]), float(h["Close"].iloc[-1])
                chg = (curr - prev) / prev * 100
            else:
                curr, chg = 0.0, 0.0
        except Exception:
            curr, chg = 0.0, 0.0
        out.append({"sym": sym, "name": name, "price": curr, "chg": chg})
    return out


@st.cache_data(ttl=300, show_spinner=False)
def fetch_watchlist_data(tickers: tuple) -> dict:
    import yfinance as yf
    result = {}
    for t in tickers:
        try:
            tk = yf.Ticker(t)
            h = tk.history(period="2d")
            if len(h) >= 2:
                prev, curr = float(h["Close"].iloc[-2]), float(h["Close"].iloc[-1])
                chg = (curr - prev) / prev * 100
            else:
                curr, chg = 0.0, 0.0
            info = {}
            try:
                info = tk.info or {}
            except Exception:
                pass
            news = []
            try:
                parsed = _parse_yf_news(tk.news or [])[:5]
                news = [{"title": p["title"], "link": p["link"],
                         "publisher": p["publisher"], "ts": p["providerPublishTime"]}
                        for p in parsed]
            except Exception:
                pass
            result[t] = {
                "name": info.get("shortName", t),
                "price": curr,
                "chg": chg,
                "currency": info.get("currency", "USD"),
                "news": news,
            }
        except Exception as e:
            result[t] = {
                "name": t, "price": 0.0, "chg": 0.0,
                "currency": "USD", "news": [], "error": str(e),
            }
    return result



# ── Additional market helpers ─────────────────────────────────────────────────

def format_large_num(n) -> str:
    if not n:
        return "N/A"
    n = float(n)
    if n >= 1e12: return f"{n/1e12:.2f} T"
    if n >= 1e9:  return f"{n/1e9:.2f} B"
    if n >= 1e6:  return f"{n/1e6:.2f} M"
    return f"{n:,.0f}"


def get_cet_now():
    from datetime import datetime, timezone, timedelta
    utc = datetime.now(timezone.utc)
    offset = 2 if 3 <= utc.month <= 10 else 1
    return utc + timedelta(hours=offset)


@st.cache_data(ttl=300, show_spinner=False)
def search_companies(query: str) -> list:
    import yfinance as yf
    try:
        s = yf.Search(query, max_results=8)
        results = getattr(s, "quotes", None) or []
        return [
            {"symbol": r.get("symbol", ""),
             "name": r.get("shortname") or r.get("longname", "") or r.get("symbol", "")}
            for r in results
            if r.get("symbol") and r.get("quoteType", "EQUITY") in ("EQUITY", "ETF", "INDEX", "")
        ]
    except Exception:
        return []


@st.cache_data(ttl=300, show_spinner=False)
def fetch_morning_markets() -> list:
    import yfinance as yf
    symbols = [
        ("^N225",   "Nikkei 225",  "🇯🇵"),
        ("^HSI",    "Hang Seng",   "🇭🇰"),
        ("^GDAXI",  "DAX",         "🇩🇪"),
        ("^FTSE",   "FTSE 100",    "🇬🇧"),
        ("^GSPC",   "S&P 500",     "🇺🇸"),
        ("^IXIC",   "NASDAQ",      "🇺🇸"),
        ("GC=F",    "Zlato/Gold",  "🥇"),
        ("BTC-USD", "Bitcoin",     "₿"),
    ]
    out = []
    for sym, name, flag in symbols:
        try:
            h = yf.Ticker(sym).history(period="2d")
            if len(h) >= 2:
                prev, curr = float(h["Close"].iloc[-2]), float(h["Close"].iloc[-1])
                chg = (curr - prev) / prev * 100
            else:
                curr, chg = 0.0, 0.0
        except Exception:
            curr, chg = 0.0, 0.0
        out.append({"sym": sym, "name": name, "flag": flag, "price": curr, "chg": chg})
    return out


def _parse_yf_news(raw_list: list) -> list:
    """Normalize yfinance news items — handles both old and new (content-nested) formats."""
    out = []
    for n in (raw_list or []):
        if not isinstance(n, dict):
            continue
        content = n.get("content")
        if content and isinstance(content, dict):
            title = content.get("title", "")
            url_obj = content.get("canonicalUrl", {})
            link = (url_obj.get("url", "") if isinstance(url_obj, dict) else str(url_obj or "")) or "#"
            prov = content.get("provider", {})
            pub  = prov.get("displayName", "") if isinstance(prov, dict) else str(prov or "")
            ts   = 0
            pd_s = content.get("pubDate", "")
            if pd_s:
                try:
                    from datetime import datetime
                    ts = int(datetime.fromisoformat(pd_s.replace("Z", "+00:00")).timestamp())
                except Exception:
                    pass
        else:
            title = n.get("title", "")
            link  = n.get("link", "#") or "#"
            pub   = n.get("publisher", "")
            ts    = n.get("providerPublishTime", 0) or 0
        if title:
            out.append({"title": title, "link": link, "publisher": pub,
                        "providerPublishTime": ts, "uuid": n.get("uuid", link)})
    return out


def _fetch_rss_news(limit: int = 20) -> list:
    """Fallback: fetch financial news via RSS feeds."""
    try:
        import feedparser
        from datetime import datetime
        import time as _time
        feeds = [
            ("Reuters Business",  "https://feeds.reuters.com/reuters/businessNews"),
            ("MarketWatch",       "https://feeds.marketwatch.com/marketwatch/topstories/"),
            ("Yahoo Finance",     "https://finance.yahoo.com/rss/topstories"),
            ("CNBC Markets",      "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100003114"),
        ]
        seen, items = set(), []
        for pub, url in feeds:
            try:
                feed = feedparser.parse(url)
                for e in (feed.entries or []):
                    title = e.get("title", "")
                    link  = e.get("link", "#")
                    if not title or link in seen:
                        continue
                    seen.add(link)
                    ts = 0
                    if e.get("published_parsed"):
                        ts = int(_time.mktime(e.published_parsed))
                    items.append({"title": title, "link": link, "publisher": pub,
                                  "providerPublishTime": ts, "uuid": link})
            except Exception:
                continue
        return items
    except Exception:
        return []


@st.cache_data(ttl=900, show_spinner=False)
def fetch_global_news(limit: int = 15) -> list:
    import yfinance as yf
    sources = ["SPY", "QQQ", "GLD", "BTC-USD", "AAPL", "MSFT", "TSLA", "^VIX", "TLT"]
    seen, all_news = set(), []
    for sym in sources:
        try:
            raw = yf.Ticker(sym).news or []
            for item in _parse_yf_news(raw):
                uid = item.get("uuid") or item.get("link", "")
                if uid and uid not in seen:
                    seen.add(uid)
                    all_news.append(item)
        except Exception:
            continue

    # Supplement with RSS if yfinance returned fewer than 8 items
    if len(all_news) < 8:
        for item in _fetch_rss_news():
            uid = item.get("uuid") or item.get("link", "")
            if uid and uid not in seen:
                seen.add(uid)
                all_news.append(item)

    all_news.sort(key=lambda x: x.get("providerPublishTime", 0), reverse=True)
    return all_news[:limit]


@st.cache_data(ttl=300, show_spinner=False)
def fetch_company_detail(ticker: str, period: str) -> dict:
    import yfinance as yf
    tk = yf.Ticker(ticker)
    hist_records = []
    _intervals = {"5d": "1h", "1mo": "1d", "3mo": "1d", "1y": "1wk", "5y": "1mo"}
    try:
        h = tk.history(period=period, interval=_intervals.get(period, "1d"))
        if not h.empty:
            cols = [c for c in ["Date", "Open", "High", "Low", "Close", "Volume"] if c in h.reset_index().columns]
            tmp = h.reset_index()[cols].copy()
            tmp["Date"] = tmp["Date"].dt.strftime("%Y-%m-%d %H:%M")
            hist_records = tmp.to_dict("records")
    except Exception:
        pass
    info = {}
    try:
        info = tk.info or {}
    except Exception:
        pass
    news = []
    try:
        news = _parse_yf_news(tk.news or [])[:10]
    except Exception:
        pass
    divs = []
    try:
        d = tk.dividends
        if not d.empty:
            tmp = d.reset_index().tail(20).copy()
            tmp["Date"] = tmp["Date"].dt.strftime("%Y-%m-%d")
            divs = tmp.to_dict("records")
    except Exception:
        pass
    return {"hist": hist_records, "info": info, "news": news, "divs": divs}


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


# ── Tab 3: Ranný prehľad ──────────────────────────────────────────────────────

def stock_card(ticker: str, name: str, price: float, chg: float,
               currency: str, added_by: str = ""):
    color  = "#2a7a4a" if chg >= 0 else "#a83232"
    arrow  = "▲" if chg >= 0 else "▼"
    sign   = "+" if chg >= 0 else ""
    by_tag = (f'<div style="font-size:10px;color:#9a7560;margin-top:3px">'
              f'➕ {added_by}</div>') if added_by else ""
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-label" style="font-size:15px;font-weight:700">{ticker}</div>
      <div class="metric-label-sk" style="font-size:11px">{name}</div>
      <div class="metric-value" style="color:{color};font-size:22px">{price:,.2f}</div>
      <div class="metric-unit">{currency}&nbsp;
        <span style="color:{color};font-weight:600">{sign}{chg:.2f}%&nbsp;{arrow}</span>
      </div>
      {by_tag}
    </div>""", unsafe_allow_html=True)


def _show_company_detail(ticker: str):
    from datetime import datetime as dt
    if st.button("← Späť / Back", key="back_btn"):
        st.session_state["detail_ticker"] = None
        st.rerun()

    st.header(f"📊 {ticker} — Detailný prehľad / Company Detail")
    per_map   = {"5 dní": "5d", "1 mesiac": "1mo", "3 mesiace": "3mo", "1 rok": "1y", "5 rokov": "5y"}
    per_label = st.radio("Obdobie / Period", list(per_map.keys()), horizontal=True, key="det_period")

    with st.spinner("Načítavanie…"):
        data = fetch_company_detail(ticker, per_map[per_label])

    info = data["info"]

    if data["hist"]:
        hdf = pd.DataFrame(data["hist"])
        hdf["Date"] = pd.to_datetime(hdf["Date"])
        has_ohlc = all(c in hdf.columns for c in ["Open", "High", "Low", "Close"])
        title_str = f"{ticker} — {info.get('shortName', ticker)} — K-line / Vývoj ceny"

        if has_ohlc:
            from plotly.subplots import make_subplots
            rows = 2 if "Volume" in hdf.columns else 1
            row_h = [0.72, 0.28] if rows == 2 else [1]
            fig = make_subplots(rows=rows, cols=1, shared_xaxes=True,
                                row_heights=row_h, vertical_spacing=0.02,
                                subplot_titles=[title_str, "Objem / Volume"] if rows == 2 else [title_str])
            fig.add_trace(go.Candlestick(
                x=hdf["Date"], open=hdf["Open"], high=hdf["High"],
                low=hdf["Low"], close=hdf["Close"],
                increasing_line_color="#2a7a4a", decreasing_line_color="#a83232",
                name="Cena",
            ), row=1, col=1)
            if rows == 2:
                colors = ["#2a7a4a" if (c >= o) else "#a83232"
                          for c, o in zip(hdf["Close"], hdf["Open"])]
                fig.add_trace(go.Bar(x=hdf["Date"], y=hdf["Volume"],
                                     marker_color=colors, name="Objem"), row=2, col=1)
            fig.update_layout(height=400, showlegend=False,
                              xaxis_rangeslider_visible=False,
                              plot_bgcolor="rgba(248,242,232,0.6)")
            fig.update_yaxes(gridcolor="rgba(180,160,130,0.2)")
        else:
            fig = px.area(hdf, x="Date", y="Close", title=title_str,
                          color_discrete_sequence=["#5a3520"])
            fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: st.metric("Trhová kap.", format_large_num(info.get("marketCap")))
    with c2: st.metric("P/E",  f"{info.get('trailingPE',0):.1f}" if info.get("trailingPE") else "N/A")
    with c3: st.metric("EPS",  f"{info.get('trailingEps',0):.2f}" if info.get("trailingEps") else "N/A")
    with c4:
        dy = info.get("dividendYield")
        st.metric("Dividenda", f"{dy*100:.2f}%" if dy else "N/A")
    with c5: st.metric("52T max", f"{info.get('fiftyTwoWeekHigh',0):.2f}" if info.get("fiftyTwoWeekHigh") else "N/A")
    with c6: st.metric("52T min", f"{info.get('fiftyTwoWeekLow',0):.2f}"  if info.get("fiftyTwoWeekLow")  else "N/A")

    e1, e2, e3 = st.columns(3)
    with e1: st.metric("Beta",   f"{info.get('beta',0):.2f}" if info.get("beta") else "N/A")
    with e2: st.metric("Sektor", info.get("sector", "N/A"))
    with e3: st.metric("Burza",  info.get("exchange", "N/A"))

    if info.get("longBusinessSummary"):
        with st.expander("O spoločnosti / About"):
            st.write(info["longBusinessSummary"])

    if data["divs"]:
        st.markdown("---")
        st.subheader("💰 História dividendy / Dividend History")
        ddf = pd.DataFrame(data["divs"])
        ddf["Date"] = pd.to_datetime(ddf["Date"])
        fig2 = px.bar(ddf, x="Date", y="Dividends",
                      title="Dividendy na akciu / Dividends per share",
                      color_discrete_sequence=["#4a7a3a"])
        fig2.update_layout(height=240)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.subheader("📰 Správy / News")
    for n in data["news"]:
        title = n.get("title", "")
        link  = n.get("link", "#")
        pub   = n.get("publisher", "")
        ts    = n.get("providerPublishTime", 0)
        tstr  = dt.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M") if ts else ""
        st.markdown(
            f"**[{title}]({link})**  \n"
            f"<small style='color:#8a5535'>{pub}{' · ' if pub and tstr else ''}{tstr}</small>",
            unsafe_allow_html=True,
        )
        st.markdown("&nbsp;")


def tab_briefing():
    from datetime import datetime as dt

    if "detail_ticker" not in st.session_state:
        st.session_state["detail_ticker"] = None

    if st.session_state["detail_ticker"]:
        _show_company_detail(st.session_state["detail_ticker"])
        return

    SK_MONTHS = ["januára","februára","marca","apríla","mája","júna",
                 "júla","augusta","septembra","októbra","novembra","decembra"]
    today   = date.today()
    date_sk = f"{today.day}. {SK_MONTHS[today.month - 1]} {today.year}"
    cet_now = get_cet_now()

    st.header("📈 Ranný prehľad / Morning Briefing")
    st.markdown(
        f'<p class="bilingual-caption">'
        f'Investičný prehľad · {date_sk} · SEČ {cet_now.strftime("%H:%M")}'
        f'{"&nbsp;· ✅ Ranný prehľad zo 07:00" if cet_now.hour >= 7 else "&nbsp;· ⏳ Ranný prehľad bude o 07:00"}'
        f'</p>',
        unsafe_allow_html=True,
    )

    # ── Markets ──
    st.subheader("🌍 Dnešné trhy / Today's Markets")
    with st.spinner("Načítavanie trhov…"):
        markets = fetch_morning_markets()

    for rs in range(0, len(markets), 4):
        row = markets[rs:rs + 4]
        cols = st.columns(len(row))
        for col, m in zip(cols, row):
            color = "#2a7a4a" if m["chg"] >= 0 else "#a83232"
            sign  = "+" if m["chg"] >= 0 else ""
            arrow = "▲" if m["chg"] >= 0 else "▼"
            with col:
                st.markdown(f"""
                <div class="metric-card" style="text-align:center;padding:10px 4px">
                  <div style="font-size:20px">{m['flag']}</div>
                  <div class="metric-label" style="font-weight:700;font-size:11px">{m['name']}</div>
                  <div style="font-size:16px;font-weight:700;color:{color}">{sign}{m['chg']:.2f}%&nbsp;{arrow}</div>
                  <div class="metric-unit">{m['price']:,.0f}</div>
                </div>""", unsafe_allow_html=True)

    # ── Investment highlights ──
    if cet_now.hour >= 7:
        st.markdown("---")
        st.subheader("💡 Investičné príležitosti dnes / Today's Highlights")
        bullish = [m for m in markets if m["chg"] >  0.5]
        bearish = [m for m in markets if m["chg"] < -0.5]
        if bullish:
            st.success("📈 **Rastúce trhy:** " +
                       " · ".join(f"{m['name']} (+{m['chg']:.2f}%)" for m in bullish))
        if bearish:
            st.warning("📉 **Zvýšená opatrnosť:** " +
                       " · ".join(f"{m['name']} ({m['chg']:.2f}%)" for m in bearish))
        if not bullish and not bearish:
            st.info("📊 Trhy v úzkom rozmedzí — čakajte na jasnejší signál.")
        gold = next((m for m in markets if m["sym"] == "GC=F"), None)
        btc  = next((m for m in markets if m["sym"] == "BTC-USD"), None)
        if gold and gold["chg"] > 0.5:
            st.info(f"🥇 Zlato rastie (+{gold['chg']:.2f}%) — obranná nálada / risk-off sentiment.")
        if btc and btc["chg"] > 2:
            st.info(f"₿ Bitcoin silný (+{btc['chg']:.2f}%) — chuť do rizika / risk-on signal.")
    else:
        mins_left = 7 * 60 - cet_now.hour * 60 - cet_now.minute
        st.info(f"⏰ Ranný prehľad bude dostupný od **07:00 SEČ** (za {mins_left} min).")

    st.markdown("---")

    # ── Watchlist ──
    st.subheader("⭐ Sledovaný zoznam / Watchlist")

    with st.expander("🔍 Vyhľadať podľa názvu spoločnosti / Search by company name"):
        q = st.text_input("Názov / Name", placeholder="napr. Apple, Samsung, ASML…", key="sq")
        if q and len(q) >= 2:
            with st.spinner("Hľadám…"):
                candidates = search_companies(q)
            if candidates:
                choice = st.radio("Vyberte ticker:", [f"{c['symbol']} — {c['name']}" for c in candidates], key="sq_c")
                adder  = st.text_input("Vaša prezývka / Nickname", key="sq_adder", placeholder="napr. Peter")
                if st.button("➕ Pridať do zoznamu", type="primary", key="sq_add"):
                    idx = [f"{c['symbol']} — {c['name']}" for c in candidates].index(choice)
                    sel = candidates[idx]
                    wl  = load_watchlist()
                    ex  = [w["ticker"] if isinstance(w, dict) else w for w in wl]
                    if sel["symbol"] not in ex:
                        wl.append({"ticker": sel["symbol"], "name": sel["name"],
                                   "added_by": adder or "?", "added_at": today.isoformat()})
                        with st.spinner("Ukladám…"):
                            save_watchlist(wl)
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.warning(f"{sel['symbol']} je už v zozname.")
            else:
                st.info("Nenašli sa výsledky — skúste zadať ticker priamo.")

    with st.expander("➕ Pridať priamo kódom / Add by ticker"):
        ca, cb, cc = st.columns([3, 2, 1])
        with ca: mt = st.text_input("Ticker", placeholder="napr. AAPL", key="mt", label_visibility="collapsed")
        with cb: ma = st.text_input("Prezývka", placeholder="napr. Peter", key="ma", label_visibility="collapsed")
        with cc:
            if st.button("➕", type="primary", key="mt_add", use_container_width=True):
                t = mt.upper().strip()
                if t:
                    wl = load_watchlist()
                    ex = [w["ticker"] if isinstance(w, dict) else w for w in wl]
                    if t not in ex:
                        wl.append({"ticker": t, "name": t,
                                   "added_by": ma or "?", "added_at": today.isoformat()})
                        with st.spinner("Ukladám…"):
                            save_watchlist(wl)
                        st.cache_data.clear()
                        st.rerun()

    raw_wl    = load_watchlist()
    watchlist = [w if isinstance(w, dict) else
                 {"ticker": w, "name": w, "added_by": "", "added_at": ""}
                 for w in raw_wl]

    if not watchlist:
        st.info("Sledovaný zoznam je prázdny. / Watchlist is empty.")
    else:
        with st.spinner("Načítavanie akcií…"):
            stock_data = fetch_watchlist_data(tuple(w["ticker"] for w in watchlist))

        n_per = min(len(watchlist), 4)
        for rs in range(0, len(watchlist), n_per):
            row_items = watchlist[rs:rs + n_per]
            cols      = st.columns(n_per)
            for col, item in zip(cols, row_items):
                t = item["ticker"]
                d = stock_data.get(t, {})
                with col:
                    if d.get("error") and d.get("price", 0) == 0.0:
                        st.error(f"**{t}**: dáta nedostupné")
                    else:
                        stock_card(t, d.get("name", item["name"]),
                                   d.get("price", 0), d.get("chg", 0),
                                   d.get("currency", "USD"), item.get("added_by", ""))
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("📊 Detail", key=f"det_{t}", use_container_width=True):
                            st.session_state["detail_ticker"] = t
                            st.rerun()
                    with b2:
                        if st.button("🗑️ Odstrániť", key=f"rm_{t}", use_container_width=True):
                            new_wl = [w for w in raw_wl
                                      if (w["ticker"] if isinstance(w, dict) else w) != t]
                            with st.spinner("Ukladám…"):
                                save_watchlist(new_wl)
                            st.cache_data.clear()
                            st.rerun()

    st.markdown("---")

    # ── Top 15 news ──
    st.subheader("📰 Medzinárodné správy — Top 15 / International Financial News")
    with st.spinner("Načítavanie správ…"):
        news_items = fetch_global_news(15)

    if not news_items:
        st.info("Správy momentálne nie sú dostupné. / News currently unavailable.")
    else:
        for i, n in enumerate(news_items, 1):
            title = n.get("title", "")
            link  = n.get("link", "#")
            pub   = n.get("publisher", "")
            ts    = n.get("providerPublishTime", 0)
            tstr  = dt.fromtimestamp(ts).strftime("%d.%m.%Y %H:%M") if ts else ""
            if not title:
                continue
            st.markdown(
                f"**{i}.** &nbsp;**[{title}]({link})**  \n"
                f"<small style='color:#8a5535'>{pub}{' · ' if pub and tstr else ''}{tstr}</small>",
                unsafe_allow_html=True,
            )
            st.markdown("<hr style='margin:3px 0 5px 0;border:none;border-top:1px solid #e0d5c5'>", unsafe_allow_html=True)

    if st.button("🔄 Obnoviť / Refresh", key="br_refresh"):
        st.cache_data.clear()
        st.rerun()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    st.title("🏃 Fitness Group Dashboard / Skupinový fitness prehľad")
    tab1, tab2, tab3 = st.tabs([
        "📥 Synchronizovať / Sync My Data",
        "📊 Skupinový prehľad / Group Dashboard",
        "📈 Ranný prehľad / Morning Briefing",
    ])
    with tab1:
        tab_sync()
    with tab2:
        tab_dashboard()
    with tab3:
        tab_briefing()


if __name__ == "__main__":
    main()
