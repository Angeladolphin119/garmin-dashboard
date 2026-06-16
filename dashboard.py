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
    /* Aged-paper background */
    .stApp { background-color: #f5eedc !important; }
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
     xmlns="http://www.w3.org/2000/svg" opacity="0.68">
<defs>
  <style>
    /* Sepia ink palette */
    .ink  { stroke:#3a2010; fill:none; stroke-linecap:round; stroke-linejoin:round; }
    .ink2 { stroke:#5a3520; fill:none; stroke-linecap:round; stroke-linejoin:round; }
    .wsh  { fill:rgba(195,160,110,0.18); stroke:#5a3520; stroke-width:0.7; }
    .wsh2 { fill:rgba(195,160,110,0.28); stroke:#5a3520; stroke-width:0.5; }
    .drk  { fill:#3a2010; stroke:none; }
    .med  { fill:#5a3520; stroke:none; }
    .lbl  { fill:#5a3520; font-family:Georgia,serif; font-size:9px; font-style:italic; }
    .lbl2 { fill:#5a3520; font-family:Georgia,serif; font-size:7.5px; }
    .lbl3 { fill:#8a5535; font-family:Georgia,serif; font-size:7px; }
    .box  { fill:none; stroke:#5a3520; stroke-width:0.8; }
    .msr  { stroke:#8a5535; stroke-width:0.7; fill:none; }
    .leaf { fill:rgba(90,53,32,0.12); stroke:#5a3520; stroke-width:0.9; }
    .vein { stroke:#5a3520; stroke-width:0.5; fill:none; opacity:0.6; }
    .stem { stroke:#5a3520; stroke-width:1.4; fill:none; stroke-linecap:round; }
    .pin  { fill:#6a4030; stroke:#3a2010; stroke-width:0.8; }
  </style>
  <!-- Faint aged-paper texture pattern -->
  <pattern id="grain" x="0" y="0" width="80" height="80" patternUnits="userSpaceOnUse">
    <line x1="0" y1="40" x2="80" y2="40" stroke="#c8a878" stroke-width="0.3" opacity="0.18"/>
    <line x1="40" y1="0" x2="40" y2="80" stroke="#c8a878" stroke-width="0.3" opacity="0.12"/>
  </pattern>
</defs>

<!-- Subtle grid overlay (museum tray) -->
<rect width="1440" height="900" fill="url(#grain)"/>


<!-- ══════════════════════════════════════════════════════════
     TOP-CENTER: Papilio machaon — hero pinned specimen
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(720,155)">
  <!-- pin -->
  <line x1="0" y1="-120" x2="0" y2="-18" class="ink" stroke-width="0.9"/>
  <circle cx="0" cy="-122" r="3.5" class="pin"/>
  <!-- right upper forewing -->
  <path class="wsh" d="M 2 -12 C 20 -50 68 -88 95 -80 C 118 -72 122 -44 110 -18 C 95 2 52 10 2 -12"/>
  <!-- right upper forewing veins -->
  <path class="vein" d="M 2 -12 C 35 -40 75 -62 95 -80"/>
  <path class="vein" d="M 2 -12 C 28 -30 60 -38 85 -28"/>
  <path class="vein" d="M 2 -12 C 18 -18 40 -12 65 -4"/>
  <path class="vein" d="M 2 -12 C 40 -50 72 -78 110 -18"/>
  <!-- right upper forewing dark border -->
  <path fill="rgba(58,32,16,0.22)" stroke="none" d="M 95 -80 C 118 -72 122 -44 110 -18 C 100 -10 82 0 68 -2 C 90 -20 105 -50 95 -80"/>
  <!-- right lower hindwing -->
  <path class="wsh" d="M 2 -8 C 25 2 72 16 90 38 C 104 56 98 78 82 84 C 62 90 38 76 24 58 C 10 40 2 14 2 -8"/>
  <!-- hindwing tail -->
  <path class="wsh2" d="M 68 82 C 72 94 74 106 70 115 C 66 118 62 115 63 107 C 62 96 62 86 68 82"/>
  <!-- right lower hindwing veins -->
  <path class="vein" d="M 2 -8 C 40 20 75 55 82 84"/>
  <path class="vein" d="M 2 -8 C 30 14 55 38 62 68"/>
  <path class="vein" d="M 2 -8 C 18 8 32 26 38 50"/>
  <!-- hindwing spots row -->
  <circle cx="46" cy="72" r="5" fill="rgba(58,32,16,0.20)"/>
  <circle cx="60" cy="68" r="4" fill="rgba(58,32,16,0.20)"/>
  <circle cx="74" cy="60" r="3.5" fill="rgba(58,32,16,0.18)"/>
  <!-- left upper forewing (mirror) -->
  <path class="wsh" d="M -2 -12 C -20 -50 -68 -88 -95 -80 C -118 -72 -122 -44 -110 -18 C -95 2 -52 10 -2 -12"/>
  <path class="vein" d="M -2 -12 C -35 -40 -75 -62 -95 -80"/>
  <path class="vein" d="M -2 -12 C -28 -30 -60 -38 -85 -28"/>
  <path class="vein" d="M -2 -12 C -18 -18 -40 -12 -65 -4"/>
  <path class="vein" d="M -2 -12 C -40 -50 -72 -78 -110 -18"/>
  <path fill="rgba(58,32,16,0.22)" stroke="none" d="M -95 -80 C -118 -72 -122 -44 -110 -18 C -100 -10 -82 0 -68 -2 C -90 -20 -105 -50 -95 -80"/>
  <!-- left lower hindwing (mirror) -->
  <path class="wsh" d="M -2 -8 C -25 2 -72 16 -90 38 C -104 56 -98 78 -82 84 C -62 90 -38 76 -24 58 C -10 40 -2 14 -2 -8"/>
  <path class="wsh2" d="M -68 82 C -72 94 -74 106 -70 115 C -66 118 -62 115 -63 107 C -62 96 -62 86 -68 82"/>
  <path class="vein" d="M -2 -8 C -40 20 -75 55 -82 84"/>
  <path class="vein" d="M -2 -8 C -30 14 -55 38 -62 68"/>
  <path class="vein" d="M -2 -8 C -18 8 -32 26 -38 50"/>
  <circle cx="-46" cy="72" r="5" fill="rgba(58,32,16,0.20)"/>
  <circle cx="-60" cy="68" r="4" fill="rgba(58,32,16,0.20)"/>
  <circle cx="-74" cy="60" r="3.5" fill="rgba(58,32,16,0.18)"/>
  <!-- body -->
  <ellipse cx="0" cy="-4" rx="3.5" ry="28" fill="rgba(58,32,16,0.55)" stroke="#3a2010" stroke-width="0.8"/>
  <!-- antennae -->
  <path d="M -2 -26 Q -22 -80 -28 -112" class="ink2" stroke-width="0.9"/>
  <path d="M  2 -26 Q  22 -80  28 -112" class="ink2" stroke-width="0.9"/>
  <ellipse cx="-28" cy="-113" rx="3" ry="2" class="med" transform="rotate(-20,-28,-113)"/>
  <ellipse cx=" 28" cy="-113" rx="3" ry="2" class="med" transform="rotate( 20, 28,-113)"/>
  <!-- measurement bracket -->
  <line x1="-122" y1="130" x2="122" y2="130" class="msr"/>
  <line x1="-122" y1="125" x2="-122" y2="135" class="msr"/>
  <line x1=" 122" y1="125" x2=" 122" y2="135" class="msr"/>
  <text x="0" y="127" class="lbl3" text-anchor="middle">← 82 mm →</text>
  <!-- collection number box -->
  <rect x="-76" y="-138" width="36" height="14" class="box"/>
  <text x="-58" y="-128" class="lbl2" text-anchor="middle">No. 001</text>
  <!-- label lines -->
  <line x1="0" y1="138" x2="0" y2="155" class="msr"/>
  <text x="0" y="168" class="lbl" text-anchor="middle">Papilio machaon Linnaeus, 1758</text>
  <text x="0" y="179" class="lbl3" text-anchor="middle">Swallowtail Butterfly / Vidlochvost feniklový</text>
</g>

<!-- ══════════════════════════════════════════════════════════
     LEFT: Rosa canina botanical branch
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(62,340)">
  <!-- main stem with slight curve -->
  <path class="stem" d="M -20 280 C -10 220 0 150 18 80 C 28 30 42 -18 55 -60"/>
  <!-- thorn marks -->
  <path class="ink2" stroke-width="1.2" d="M 0 220 L -8 212"/>
  <path class="ink2" stroke-width="1.2" d="M 8 180 L 16 172"/>
  <path class="ink2" stroke-width="1.2" d="M 2 140 L -8 132"/>
  <!-- compound leaf set 1 (low) — 5 leaflets -->
  <path class="stem" d="M -5 240 C -22 228 -40 220 -52 210"/>
  <path class="leaf" d="M -52 210 C -70 196 -72 176 -58 172 C -44 170 -36 186 -52 210"/>
  <path class="vein" d="M -52 210 C -60 196 -62 180 -58 172"/>
  <path class="leaf" d="M -34 220 C -48 206 -48 186 -34 184 C -22 184 -16 200 -34 220"/>
  <path class="vein" d="M -34 220 C -38 208 -38 192 -34 184"/>
  <path class="leaf" d="M -18 228 C -28 214 -26 196 -12 196 C -2 198 2 214 -18 228"/>
  <!-- compound leaf set 2 (mid) -->
  <path class="stem" d="M 10 160 C 28 148 50 140 64 130"/>
  <path class="leaf" d="M 64 130 C 82 116 84 96 70 92 C 56 90 48 106 64 130"/>
  <path class="vein" d="M 64 130 C 72 116 74 100 70 92"/>
  <path class="leaf" d="M 46 138 C 62 124 62 104 48 102 C 36 102 30 118 46 138"/>
  <path class="vein" d="M 46 138 C 52 126 52 110 48 102"/>
  <path class="leaf" d="M 30 146 C 44 132 44 114 30 112 C 18 114 14 130 30 146"/>
  <!-- compound leaf set 3 (high) -->
  <path class="stem" d="M 28 80 C 14 68 -4 56 -16 44"/>
  <path class="leaf" d="M -16 44 C -32 28 -30 10 -16 8 C -4 8 4 26 -16 44"/>
  <path class="vein" d="M -16 44 C -24 30 -22 14 -16 8"/>
  <path class="leaf" d="M 2 54 C -10 38 -8 20 6 20 C 18 22 22 40 2 54"/>
  <!-- rose flower (5 petals, open) -->
  <g transform="translate(55,-62)">
    <path class="wsh2" d="M 0 0 C -14 -16 -18 -36 -6 -42 C 6 -46 16 -32 0 0"/>
    <path class="wsh2" d="M 0 0 C 14 -16 18 -36 6 -42 C -6 -46 -16 -32 0 0"/>
    <path class="wsh2" d="M 0 0 C 20 -8 38 -4 36 10 C 34 22 18 22 0 0"/>
    <path class="wsh2" d="M 0 0 C -20 -8 -38 -4 -36 10 C -34 22 -18 22 0 0"/>
    <path class="wsh2" d="M 0 0 C 4 20 16 32 6 40 C -4 46 -14 34 0 0"/>
    <!-- stamens -->
    <circle cx="0" cy="-2" r="8" fill="rgba(90,53,32,0.18)" stroke="#5a3520" stroke-width="0.7"/>
    <line x1="-5" y1="-6" x2="-7" y2="-14" class="ink2" stroke-width="0.6"/>
    <line x1="0"  y1="-6" x2="0"  y2="-15" class="ink2" stroke-width="0.6"/>
    <line x1="5"  y1="-6" x2="7"  y2="-14" class="ink2" stroke-width="0.6"/>
    <circle cx="-7" cy="-14" r="1.2" class="med"/>
    <circle cx=" 0" cy="-15" r="1.2" class="med"/>
    <circle cx=" 7" cy="-14" r="1.2" class="med"/>
  </g>
  <!-- rose hip (oval fruit) -->
  <ellipse cx="-8" cy="268" rx="8" ry="12" fill="rgba(90,53,32,0.20)" stroke="#5a3520" stroke-width="0.9"/>
  <path class="stem" d="M -8 256 C -10 260 -10 264 -8 268"/>
  <!-- label -->
  <text x="72" y="270" class="lbl" text-anchor="start">Rosa canina L.</text>
  <line x1="55" y1="265" x2="70" y2="268" class="msr"/>
</g>

<!-- ══════════════════════════════════════════════════════════
     RIGHT: Lucanus cervus — stag beetle pinned specimen
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(1270,310)">
  <!-- pin -->
  <line x1="0" y1="-88" x2="0" y2="-38" class="ink" stroke-width="0.9"/>
  <circle cx="0" cy="-90" r="3.5" class="pin"/>
  <!-- mandibles (large, curved outward) -->
  <path class="wsh2" d="M -8 -32 C -22 -44 -46 -48 -52 -36 C -56 -26 -48 -12 -32 -10 C -20 -8 -8 -18 -8 -32"/>
  <path class="vein" d="M -8 -32 C -28 -40 -48 -40 -52 -36"/>
  <path class="wsh2" d="M  8 -32 C  22 -44  46 -48  52 -36 C  56 -26  48 -12  32 -10 C  20 -8  8 -18  8 -32"/>
  <path class="vein" d="M  8 -32 C  28 -40  48 -40  52 -36"/>
  <!-- small tooth on mandibles -->
  <path class="ink2" stroke-width="1" d="M -30 -36 L -34 -28"/>
  <path class="ink2" stroke-width="1" d="M  30 -36 L  34 -28"/>
  <!-- head -->
  <ellipse cx="0" cy="-20" rx="14" ry="11" fill="rgba(58,32,16,0.38)" stroke="#3a2010" stroke-width="1"/>
  <!-- compound eyes -->
  <ellipse cx="-12" cy="-22" rx="4" ry="5" class="drk" opacity="0.7"/>
  <ellipse cx=" 12" cy="-22" rx="4" ry="5" class="drk" opacity="0.7"/>
  <!-- antennae (elbowed) -->
  <path class="ink2" stroke-width="0.8" d="M -8 -28 Q -20 -42 -18 -52 Q -14 -60 -10 -62"/>
  <path class="ink2" stroke-width="0.8" d="M  8 -28 Q  20 -42  18 -52 Q  14 -60  10 -62"/>
  <!-- pronotum (thorax shield) -->
  <path class="wsh2" d="M -18 -10 C -20 -2 -18 8 0 10 C 18 8 20 -2 18 -10 C 14 -16 -14 -16 -18 -10"/>
  <!-- elytra (wing covers) -->
  <path class="wsh" d="M -18 8 C -22 20 -20 50 -16 72 C -12 84 -6 90 0 90 C 6 90 12 84 16 72 C 20 50 22 20 18 8 C 14 4 -14 4 -18 8"/>
  <!-- elytra suture line -->
  <line x1="0" y1="8" x2="0" y2="90" class="ink2" stroke-width="0.8"/>
  <!-- elytra texture lines -->
  <path class="vein" d="M -14 16 Q -10 50 -8 80"/>
  <path class="vein" d="M  14 16 Q  10 50  8 80"/>
  <!-- legs (3 pairs) -->
  <path class="ink2" stroke-width="1.1" d="M -16 0 C -28 -2 -42 8 -48 18"/>
  <path class="ink2" stroke-width="1.1" d="M  16 0 C  28 -2  42 8  48 18"/>
  <path class="ink2" stroke-width="1.1" d="M -18 20 C -32 24 -46 38 -50 48"/>
  <path class="ink2" stroke-width="1.1" d="M  18 20 C  32 24  46 38  50 48"/>
  <path class="ink2" stroke-width="1.1" d="M -18 42 C -34 50 -46 64 -48 76"/>
  <path class="ink2" stroke-width="1.1" d="M  18 42 C  34 50  46 64  48 76"/>
  <!-- tarsal claws -->
  <path class="ink" stroke-width="0.7" d="M -48 18 L -54 22 M -48 18 L -52 24"/>
  <path class="ink" stroke-width="0.7" d="M  48 18 L  54 22 M  48 18 L  52 24"/>
  <!-- measurement -->
  <line x1="-60" y1="104" x2="60" y2="104" class="msr"/>
  <line x1="-60" y1="99" x2="-60" y2="109" class="msr"/>
  <line x1=" 60" y1="99" x2=" 60" y2="109" class="msr"/>
  <text x="0" y="101" class="lbl3" text-anchor="middle">← 65 mm →</text>
  <!-- label -->
  <rect x="-52" y="-108" width="38" height="14" class="box"/>
  <text x="-33" y="-98" class="lbl2" text-anchor="middle">No. 002</text>
  <line x1="0" y1="112" x2="0" y2="126" class="msr"/>
  <text x="0" y="138" class="lbl" text-anchor="middle">Lucanus cervus Linnaeus, 1758</text>
  <text x="0" y="149" class="lbl3" text-anchor="middle">Stag Beetle / Roháč obyčajný</text>
</g>

<!-- ══════════════════════════════════════════════════════════
     TOP-RIGHT: Aeshna cyanea — dragonfly pinned
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(1120,88) rotate(-18)">
  <!-- pin -->
  <line x1="0" y1="-70" x2="0" y2="-20" class="ink" stroke-width="0.8"/>
  <circle cx="0" cy="-72" r="3" class="pin"/>
  <!-- head (large, round, compound eyes) -->
  <circle cx="0" cy="-14" r="10" fill="rgba(58,32,16,0.32)" stroke="#3a2010" stroke-width="0.9"/>
  <ellipse cx="-6" cy="-16" rx="5" ry="6" class="drk" opacity="0.55"/>
  <ellipse cx=" 6" cy="-16" rx="5" ry="6" class="drk" opacity="0.55"/>
  <!-- thorax -->
  <ellipse cx="0" cy="2" rx="9" ry="12" fill="rgba(58,32,16,0.32)" stroke="#3a2010" stroke-width="0.9"/>
  <!-- abdomen (10 segments, tapering) -->
  <path class="wsh" d="M -7 12 C -8 22 -7 32 -5 40 C -3 50 0 56 0 56 C 0 56 3 50 5 40 C 7 32 8 22 7 12 C 4 10 -4 10 -7 12"/>
  <line x1="-6" y1="18" x2="6" y2="18" class="vein"/>
  <line x1="-6" y1="24" x2="6" y2="24" class="vein"/>
  <line x1="-5" y1="30" x2="5" y2="30" class="vein"/>
  <line x1="-5" y1="36" x2="5" y2="36" class="vein"/>
  <line x1="-4" y1="42" x2="4" y2="42" class="vein"/>
  <line x1="-4" y1="48" x2="4" y2="48" class="vein"/>
  <!-- tip -->
  <ellipse cx="0" cy="60" rx="3" ry="5" fill="rgba(58,32,16,0.40)" stroke="#3a2010" stroke-width="0.7"/>
  <!-- upper wings (pair) with venation network -->
  <path class="wsh" d="M -8 2 C -30 -8 -72 -12 -80 0 C -86 10 -72 20 -48 20 C -28 20 -10 12 -8 2"/>
  <path class="wsh" d="M  8 2 C  30 -8  72 -12  80 0 C  86 10  72 20  48 20 C  28 20  10 12  8 2"/>
  <!-- upper wing veins -->
  <path class="vein" d="M -8 2 C -36 -4 -65 -8 -80 0"/>
  <path class="vein" d="M -8 2 C -28 4 -50 8 -65 14"/>
  <path class="vein" d="M -40 -6 L -42 14"/>
  <path class="vein" d="M -58 -4 L -60 12"/>
  <path class="vein" d="M  8 2 C  36 -4  65 -8  80 0"/>
  <path class="vein" d="M  8 2 C  28 4  50 8  65 14"/>
  <path class="vein" d="M  40 -6 L  42 14"/>
  <path class="vein" d="M  58 -4 L  60 12"/>
  <!-- lower wings -->
  <path class="wsh" d="M -8 8 C -28 16 -65 24 -70 36 C -74 46 -60 52 -40 46 C -22 40 -8 24 -8 8"/>
  <path class="wsh" d="M  8 8 C  28 16  65 24  70 36 C  74 46  60 52  40 46 C  22 40  8 24  8 8"/>
  <path class="vein" d="M -8 8 C -36 20 -62 34 -70 36"/>
  <path class="vein" d="M -40 22 L -44 44"/>
  <path class="vein" d="M  8 8 C  36 20  62 34  70 36"/>
  <path class="vein" d="M  40 22 L  44 44"/>
  <!-- pterostigma (wing spot) -->
  <rect x="-80" y="-4" width="10" height="5" fill="rgba(58,32,16,0.35)" stroke="#3a2010" stroke-width="0.5"/>
  <rect x=" 70" y="-4" width="10" height="5" fill="rgba(58,32,16,0.35)" stroke="#3a2010" stroke-width="0.5"/>
  <!-- collection tag -->
  <rect x="-30" y="-94" width="36" height="14" class="box"/>
  <text x="-12" y="-84" class="lbl2" text-anchor="middle">No. 003</text>
  <!-- label (rotated back to read horizontally) -->
  <g transform="rotate(18)">
    <text x="88" y="10" class="lbl" text-anchor="start">Aeshna cyanea</text>
    <text x="88" y="20" class="lbl3" text-anchor="start">Müller, 1764</text>
  </g>
</g>

<!-- ══════════════════════════════════════════════════════════
     BOTTOM-LEFT: Dryopteris fern fronds
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(50,780)">
  <!-- frond 1 -->
  <path class="stem" d="M 0 120 C 10 88 20 55 32 20 C 40 0 50 -20 58 -38"/>
  <!-- pinnae (pairs along frond) -->
  <path class="leaf" d="M 10 100 C 24 90 36 88 36 98 C 34 106 18 108 10 100"/>
  <path class="vein" d="M 10 100 C 22 94 34 92 36 98"/>
  <path class="leaf" d="M 8 100 C -4 92 -14 92 -12 102 C -10 110 4 110 8 100"/>
  <path class="vein" d="M 8 100 C -2 94 -10 94 -12 102"/>
  <path class="leaf" d="M 16 80 C 30 70 42 68 42 78 C 40 86 24 88 16 80"/>
  <path class="leaf" d="M 14 80 C 2 72 -8 72 -6 82 C -4 90 10 90 14 80"/>
  <path class="leaf" d="M 22 60 C 36 50 48 48 48 58 C 46 66 30 68 22 60"/>
  <path class="leaf" d="M 20 60 C 8 52 -2 52 0 62 C 2 70 18 70 20 60"/>
  <path class="leaf" d="M 30 40 C 44 30 54 30 52 40 C 50 48 36 50 30 40"/>
  <path class="leaf" d="M 28 40 C 18 32 8 34 10 44 C 12 52 26 50 28 40"/>
  <path class="leaf" d="M 38 20 C 50 12 58 12 56 22 C 54 30 42 32 38 20"/>
  <path class="leaf" d="M 36 20 C 28 12 18 14 20 24 C 22 32 34 30 36 20"/>
  <!-- frond 2 (angled) -->
  <path class="stem" d="M 0 120 C 24 100 48 72 72 42 C 86 26 100 10 112 -6" opacity="0.75"/>
  <path class="leaf" d="M 38 90 C 52 78 66 76 66 88 C 62 96 46 98 38 90" opacity="0.75"/>
  <path class="leaf" d="M 36 90 C 24 82 12 84 14 94 C 16 102 32 100 36 90" opacity="0.75"/>
  <path class="leaf" d="M 62 66 C 76 54 90 52 90 64 C 86 72 70 74 62 66" opacity="0.68"/>
  <path class="leaf" d="M 60 66 C 50 58 38 60 40 70 C 42 78 58 76 60 66" opacity="0.68"/>
  <path class="leaf" d="M 84 44 C 96 34 108 32 106 44 C 104 52 90 54 84 44" opacity="0.62"/>
  <!-- sori dots (spore clusters on underside — shown as tiny dots) -->
  <circle cx="28" cy="96" r="1.2" class="med" opacity="0.5"/>
  <circle cx="25" cy="88" r="1.2" class="med" opacity="0.5"/>
  <circle cx="32" cy="72" r="1.2" class="med" opacity="0.5"/>
</g>

<!-- ══════════════════════════════════════════════════════════
     BOTTOM-RIGHT: Apis mellifera — bee specimen
     ══════════════════════════════════════════════════════════ -->
<g transform="translate(1060,810)">
  <!-- pin -->
  <line x1="0" y1="-72" x2="0" y2="-30" class="ink" stroke-width="0.8"/>
  <circle cx="0" cy="-74" r="3" class="pin"/>
  <!-- head -->
  <circle cx="0" cy="-22" r="12" fill="rgba(58,32,16,0.28)" stroke="#3a2010" stroke-width="0.9"/>
  <!-- compound eyes -->
  <ellipse cx="-8" cy="-24" rx="5" ry="6" class="drk" opacity="0.5"/>
  <ellipse cx=" 8" cy="-24" rx="5" ry="6" class="drk" opacity="0.5"/>
  <!-- antennae (elbowed) -->
  <path class="ink2" stroke-width="0.8" d="M -4 -32 Q -14 -48 -12 -60"/>
  <path class="ink2" stroke-width="0.8" d="M  4 -32 Q  14 -48  12 -60"/>
  <!-- thorax (fuzzy — shown with short hatch lines) -->
  <ellipse cx="0" cy="-6" rx="12" ry="14" fill="rgba(58,32,16,0.30)" stroke="#3a2010" stroke-width="0.9"/>
  <path class="vein" d="M -10 -10 Q 0 -12 10 -10"/>
  <path class="vein" d="M -11 -6  Q 0 -8  11 -6"/>
  <path class="vein" d="M -11 -2  Q 0 -4  11 -2"/>
  <path class="vein" d="M -10  2  Q 0  0  10  2"/>
  <!-- abdomen (striped) -->
  <ellipse cx="0" cy="22" rx="11" ry="20" fill="rgba(58,32,16,0.18)" stroke="#3a2010" stroke-width="0.9"/>
  <!-- stripes as filled bands -->
  <path fill="rgba(58,32,16,0.30)" stroke="none" d="M -10 14 Q 0 12 10 14 Q 10 18 0 18 Q -10 18 -10 14"/>
  <path fill="rgba(58,32,16,0.30)" stroke="none" d="M -11 22 Q 0 20 11 22 Q 11 26 0 26 Q -11 26 -11 22"/>
  <path fill="rgba(58,32,16,0.30)" stroke="none" d="M -10 30 Q 0 28 10 30 Q 10 34 0 34 Q -10 34 -10 30"/>
  <!-- stinger tip -->
  <path class="ink2" stroke-width="0.8" d="M 0 40 Q 0 46 0 50"/>
  <!-- wings -->
  <path class="wsh" d="M -10 -8 C -30 -16 -62 -10 -64 2 C -64 12 -48 18 -28 14 C -14 10 -8 4 -10 -8"/>
  <path class="wsh" d="M  10 -8 C  30 -16  62 -10  64 2 C  64 12  48 18  28 14 C  14 10  8 4  10 -8"/>
  <path class="wsh" d="M -10 0 C -26 4 -50 12 -52 22 C -50 30 -36 30 -22 24 C -12 18 -8 8 -10 0"/>
  <path class="wsh" d="M  10 0 C  26 4  50 12  52 22 C  50 30  36 30  22 24 C  12 18  8 8  10 0"/>
  <!-- wing veins -->
  <path class="vein" d="M -10 -8 C -36 -12 -60 -4 -64 2"/>
  <path class="vein" d="M -36 -10 L -38 14"/>
  <path class="vein" d="M  10 -8 C  36 -12  60 -4  64 2"/>
  <path class="vein" d="M  36 -10 L  38 14"/>
  <!-- legs -->
  <path class="ink2" stroke-width="0.9" d="M -10 -8 C -18 -4 -26 6 -28 16"/>
  <path class="ink2" stroke-width="0.9" d="M  10 -8 C  18 -4  26 6  28 16"/>
  <path class="ink2" stroke-width="0.9" d="M -11 4 C -20 14 -28 28 -30 38"/>
  <path class="ink2" stroke-width="0.9" d="M  11 4 C  20 14  28 28  30 38"/>
  <!-- pollen basket on hind leg -->
  <ellipse cx="-28" cy="38" rx="4" ry="6" fill="rgba(58,32,16,0.20)" stroke="#5a3520" stroke-width="0.7"/>
  <!-- measurement -->
  <line x1="-68" y1="62" x2="68" y2="62" class="msr"/>
  <line x1="-68" y1="57" x2="-68" y2="67" class="msr"/>
  <line x1=" 68" y1="57" x2=" 68" y2="67" class="msr"/>
  <text x="0" y="59" class="lbl3" text-anchor="middle">← 15 mm →</text>
  <!-- collection box -->
  <rect x="-46" y="-92" width="36" height="14" class="box"/>
  <text x="-28" y="-82" class="lbl2" text-anchor="middle">No. 004</text>
  <line x1="0" y1="70" x2="0" y2="82" class="msr"/>
  <text x="0" y="92" class="lbl" text-anchor="middle">Apis mellifera Linnaeus, 1758</text>
  <text x="0" y="102" class="lbl3" text-anchor="middle">Honey Bee / Včela medonosná</text>
</g>

<!-- ══════════════════════════════════════════════════════════
     SCATTERED: small field notes, leaf specimens, dots
     ══════════════════════════════════════════════════════════ -->

<!-- small isolated leaf specimen top-left (collected single leaf) -->
<g transform="translate(320,220)">
  <path class="stem" d="M 0 20 Q 0 10 0 -2"/>
  <path class="leaf" d="M 0 -2 C -20 -18 -22 -42 -8 -46 C 4 -48 12 -32 0 -2"/>
  <path class="vein" d="M 0 -2 C -10 -18 -14 -36 -8 -46"/>
  <path class="vein" d="M -4 -20 L -14 -24"/>
  <path class="vein" d="M -4 -30 L -16 -34"/>
</g>

<!-- small moth (simple ink sketch) mid-left -->
<g transform="translate(220,560)" opacity="0.6">
  <ellipse cx="0" cy="2" rx="3" ry="8" fill="rgba(58,32,16,0.35)" stroke="#5a3520" stroke-width="0.7"/>
  <path class="wsh" d="M 0 -2 C -12 -10 -26 -6 -26 2 C -24 10 -12 8 0 -2"/>
  <path class="wsh" d="M 0 -2 C  12 -10  26 -6  26 2 C  24 10  12 8  0 -2"/>
  <path class="wsh" d="M 0 2 C -10 6 -20 14 -18 20 C -14 26 -6 18 0 2"/>
  <path class="wsh" d="M 0 2 C  10 6  20 14  18 20 C  14 26  6 18  0 2"/>
  <path class="ink2" stroke-width="0.7" d="M -1 -8 Q -5 -16 -6 -20"/>
  <path class="ink2" stroke-width="0.7" d="M  1 -8 Q  5 -16  6 -20"/>
</g>

<!-- tiny collector's note card -->
<g transform="translate(380,80)" opacity="0.55">
  <rect x="0" y="0" width="80" height="52" class="box" rx="2"/>
  <text x="8" y="16" class="lbl2">Collected: VI.2024</text>
  <text x="8" y="28" class="lbl3">Locality: field margin</text>
  <text x="8" y="40" class="lbl3">Alt.: 240 m a.s.l.</text>
  <line x1="8" y1="44" x2="72" y2="44" stroke="#8a5535" stroke-width="0.4"/>
</g>

<!-- small beetle (Coleoptera) sketch — top area scattered -->
<g transform="translate(960,80)" opacity="0.5">
  <ellipse cx="0" cy="-6" rx="6" ry="5" fill="rgba(58,32,16,0.35)" stroke="#5a3520" stroke-width="0.7"/>
  <path class="wsh" d="M -5 2 C -6 12 -5 22 0 26 C 5 22 6 12 5 2 C 3 0 -3 0 -5 2"/>
  <line x1="0" y1="2" x2="0" y2="26" class="vein"/>
  <path class="ink2" stroke-width="0.7" d="M -4 -8 Q -10 -16 -12 -22"/>
  <path class="ink2" stroke-width="0.7" d="M  4 -8 Q  10 -16  12 -22"/>
  <path class="ink2" stroke-width="0.8" d="M -5 6 L -14 4"/>
  <path class="ink2" stroke-width="0.8" d="M  5 6 L  14 4"/>
  <path class="ink2" stroke-width="0.8" d="M -5 14 L -14 18"/>
  <path class="ink2" stroke-width="0.8" d="M  5 14 L  14 18"/>
  <text x="0" y="40" class="lbl3" text-anchor="middle">No. 005</text>
</g>

<!-- scattered pencil dots (compass marks, measurement points) -->
<circle cx="505" cy="340" r="1.5" class="med" opacity="0.25"/>
<circle cx="620" cy="480" r="1.5" class="med" opacity="0.22"/>
<circle cx="840" cy="260" r="1.5" class="med" opacity="0.22"/>
<circle cx="1180" cy="560" r="1.5" class="med" opacity="0.20"/>
<circle cx="780" cy="700" r="1.5" class="med" opacity="0.20"/>

<!-- faint specimen divider lines (museum tray dividers) -->
<line x1="420" y1="0"   x2="420" y2="900" stroke="#c8a878" stroke-width="0.5" opacity="0.10"/>
<line x1="1020" y1="0"  x2="1020" y2="900" stroke="#c8a878" stroke-width="0.5" opacity="0.10"/>
<line x1="0"   y1="380" x2="1440" y2="380" stroke="#c8a878" stroke-width="0.5" opacity="0.10"/>
<line x1="0"   y1="640" x2="1440" y2="640" stroke="#c8a878" stroke-width="0.5" opacity="0.10"/>

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
