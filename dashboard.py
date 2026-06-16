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
    /* Watercolour paper background */
    .stApp { background-color: #faf8f4 !important; }
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
     xmlns="http://www.w3.org/2000/svg" opacity="0.88">
<defs>
  <filter id="sf"><feGaussianBlur stdDeviation="1.6"/></filter>
</defs>

<!-- ═══ TOP-LEFT: Blue wildflowers + bellflower ═══ -->
<g transform="translate(108,108)">
  <!-- Stem 1 (tallest, slight lean right) -->
  <path fill="none" stroke="#5a8830" stroke-width="2.2" stroke-linecap="round"
        d="M 20 125 C 18 85 15 42 18 2 C 20 -28 16 -54 18 -88"/>
  <path fill="#7ab850" d="M 18 52 C -8 40 -18 24 -8 17 C 2 13 18 34 18 52"/>
  <path fill="#7ab850" d="M 18 68 C 44 55 56 38 44 32 C 34 27 18 50 18 68"/>
  <!-- Blue flower -->
  <g transform="translate(18,-93)">
    <path fill="#5070d0" d="M 0 -20 C -4 -14 -4 -7 0 -5 C 4 -7 4 -14 0 -20"/>
    <path fill="#5070d0" d="M 12 -16 C 7 -11 7 -5 10 -3 C 13 -4 14 -10 12 -16"/>
    <path fill="#5070d0" d="M 16 -3 C 10 -3 8 3 10 6 C 13 6 16 2 16 -3"/>
    <path fill="#5070d0" d="M 7  7 C 3 5 0 9 1 12 C 4 12 8 10 7 7"/>
    <path fill="#5070d0" d="M -8  7 C -5 5 -1 9 -2 12 C -5 12 -9 10 -8 7"/>
    <path fill="#5070d0" d="M -16 -3 C -10 -3 -8 3 -10 6 C -13 6 -16 2 -16 -3"/>
    <path fill="#5070d0" d="M -12 -16 C -7 -11 -7 -5 -10 -3 C -13 -4 -14 -10 -12 -16"/>
    <circle cx="0" cy="-1" r="8" fill="#f0dc38"/>
    <circle cx="0" cy="-1" r="4" fill="#ccb018"/>
  </g>
  <!-- Stem 2 (left, shorter) -->
  <path fill="none" stroke="#5a8830" stroke-width="1.8" stroke-linecap="round"
        d="M -22 125 C -20 95 -26 62 -28 32 C -30 12 -26 -8 -22 -32"/>
  <path fill="#6aa840" d="M -26 62 C -50 54 -58 38 -46 32 C -36 27 -24 46 -26 62"/>
  <!-- Smaller blue flower -->
  <g transform="translate(-22,-38)">
    <path fill="#6888e0" d="M 0 -14 C -3 -10 -3 -5 0 -3 C 3 -5 3 -10 0 -14"/>
    <path fill="#6888e0" d="M 8 -10 C 5 -8 5 -3 7 -1 C 9 -2 10 -7 8 -10"/>
    <path fill="#6888e0" d="M 10 -2 C 6 -2 5 3 7 5 C 9 4 11 1 10 -2"/>
    <path fill="#6888e0" d="M 4  5 C 1 3 -1 7 0 9 C 2 10 5 7 4 5"/>
    <path fill="#6888e0" d="M -4  5 C -2 3 0 7 -1 9 C -3 10 -5 7 -4 5"/>
    <path fill="#6888e0" d="M -10 -2 C -6 -2 -5 3 -7 5 C -9 4 -11 1 -10 -2"/>
    <path fill="#6888e0" d="M -8 -10 C -5 -8 -5 -3 -7 -1 C -9 -2 -10 -7 -8 -10"/>
    <circle cx="0" cy="-1" r="5.5" fill="#f0dc38"/>
    <circle cx="0" cy="-1" r="2.5" fill="#ccb018"/>
  </g>
  <!-- Stem 3: purple bellflower -->
  <path fill="none" stroke="#5a8830" stroke-width="1.5" stroke-linecap="round"
        d="M 55 125 C 55 92 52 62 55 36 C 57 18 53 0 51 -20"/>
  <path fill="#7ab850" d="M 54 72 C 76 62 84 46 72 42 C 62 38 54 56 54 72"/>
  <!-- Bell -->
  <path fill="#9868d0" d="M 51 -20 C 44 -18 40 -11 40 -3 C 44 5 57 5 61 -3 C 61 -11 57 -18 51 -20"/>
  <path fill="#c0a0f0" d="M 51 -20 C 46 -18 43 -12 43 -5 C 47 2 56 3 60 -3 C 59 -13 55 -20 51 -20" opacity="0.45"/>
  <path fill="#9868d0" d="M 40 -3 C 36 2 36 8 40 10 C 44 8 44 2 40 -3"/>
  <path fill="#9868d0" d="M 61 -3 C 65 2 65 8 61 10 C 57 8 57 2 61 -3"/>
  <path fill="#6aa840" d="M 52 -20 C 64 -30 70 -40 60 -42 C 52 -40 52 -28 52 -20"/>
  <path fill="#6aa840" d="M 49 -20 C 37 -30 31 -40 41 -42 C 49 -40 49 -28 49 -20"/>
</g>

<!-- ═══ TOP-RIGHT: Red apple + branch ═══ -->
<g transform="translate(1348,60)">
  <!-- Main branch -->
  <path fill="none" stroke="#8a6030" stroke-width="2.2" stroke-linecap="round"
        d="M 38 88 C 28 52 20 22 24 -14 C 27 -34 23 -56 18 -78"/>
  <path fill="none" stroke="#8a6030" stroke-width="1.5" stroke-linecap="round"
        d="M 24 -6 C 9 -16 -4 -22 -14 -38"/>
  <path fill="#6aa840" d="M 25 22 C 48 14 56 0 44 -5 C 34 -8 25 10 25 22"/>
  <path fill="#6aa840" d="M 23 6 C 3 -4 -4 -18 8 -22 C 18 -24 23 -8 23 6"/>
  <path fill="#6aa840" d="M -14 -38 C -29 -44 -36 -54 -26 -58 C -16 -60 -13 -46 -14 -38"/>
  <!-- Apple -->
  <g transform="translate(-4,-26)">
    <path fill="#c82424" d="M -24 -5 C -28 -32 -18 -56 0 -58 C 18 -56 28 -32 24 -5 C 18 25 10 36 0 36 C -10 36 -18 25 -24 -5"/>
    <path fill="#e84040" d="M -14 -8 C -17 -30 -8 -50 0 -52 C -12 -46 -18 -26 -14 -8" opacity="0.52"/>
    <path fill="rgba(255,255,255,0.26)" d="M -14 -30 C -16 -24 -14 -14 -8 -11 C -4 -18 -6 -34 -14 -30"/>
    <path fill="#4a9028" d="M 8 -56 C 14 -76 32 -80 28 -64 C 22 -52 10 -50 8 -56"/>
    <path fill="none" stroke="#3a7018" stroke-width="0.9" d="M 8 -56 C 14 -66 24 -74 28 -64"/>
    <path fill="none" stroke="#5a4018" stroke-width="2.2" stroke-linecap="round"
          d="M 0 -58 C -2 -67 1 -75 3 -81"/>
  </g>
  <!-- Small cornflower -->
  <g transform="translate(14,-74)">
    <path fill="none" stroke="#6a8830" stroke-width="1.5" stroke-linecap="round" d="M 0 20 C 0 8 0 -6 0 -18"/>
    <path fill="#5070d0" d="M 0 -18 C -3 -14 -3 -9 0 -7 C 3 -9 3 -14 0 -18"/>
    <path fill="#5070d0" d="M 7 -14 C 4 -10 5 -5 7 -4 C 9 -4 9 -10 7 -14"/>
    <path fill="#5070d0" d="M 9 -6 C 5 -6 4 -2 6 0 C 8 0 10 -3 9 -6"/>
    <path fill="#5070d0" d="M 5 2 C 2 0 0 4 1 6 C 3 7 6 4 5 2"/>
    <path fill="#5070d0" d="M -5 2 C -2 0 0 4 -1 6 C -3 7 -6 4 -5 2"/>
    <path fill="#5070d0" d="M -9 -6 C -5 -6 -4 -2 -6 0 C -8 0 -10 -3 -9 -6"/>
    <path fill="#5070d0" d="M -7 -14 C -4 -10 -5 -5 -7 -4 C -9 -4 -9 -10 -7 -14"/>
    <circle cx="0" cy="-6" r="5" fill="#f0dc38"/>
  </g>
</g>

<!-- ═══ LEFT: Sleeping fox ═══ -->
<g transform="translate(62,458)">
  <!-- Shadow -->
  <ellipse cx="14" cy="96" rx="68" ry="13" fill="rgba(100,58,18,0.09)"/>
  <!-- Tail (behind body) -->
  <path fill="#d06828" d="M -48 20 C -84 -4 -104 34 -96 74 C -88 104 -60 114 -38 90 C -18 68 -35 46 -48 20"/>
  <!-- Tail tip -->
  <ellipse cx="-91" cy="54" rx="22" ry="17" fill="#f0e8e0" transform="rotate(-25,-91,54)"/>
  <!-- Body -->
  <path fill="#e07030" d="M -50 24 C -65 -16 -44 -58 0 -60 C 44 -58 68 -20 64 28 C 58 80 18 96 -18 80 C -56 64 -36 62 -50 24"/>
  <path fill="#f08040" d="M -30 12 C -42 -20 -28 -50 0 -52 C -30 -48 -46 -18 -36 14 C -34 18 -30 12 -30 12" opacity="0.52"/>
  <!-- Belly -->
  <ellipse cx="18" cy="18" rx="30" ry="38" fill="#f6e0c0" transform="rotate(-12,18,18)"/>
  <!-- Head -->
  <circle cx="52" cy="-34" r="33" fill="#e07030"/>
  <path fill="#f08040" d="M 30 -55 C 22 -44 20 -32 28 -24 C 30 -36 32 -48 30 -55" opacity="0.48"/>
  <!-- White face mask -->
  <path fill="#f6e0c0" d="M 52 -28 C 38 -30 32 -20 34 -10 C 38 -2 52 2 66 -4 C 76 -12 74 -26 64 -32 C 60 -34 56 -30 52 -28"/>
  <!-- Ears -->
  <path fill="#e07030" d="M 34 -62 C 30 -80 38 -92 44 -86 C 48 -80 46 -68 42 -62"/>
  <path fill="#f09898" d="M 36 -64 C 33 -78 39 -88 44 -83 C 47 -78 45 -68 42 -64" opacity="0.78"/>
  <path fill="#e07030" d="M 60 -62 C 60 -80 70 -90 74 -84 C 76 -78 72 -66 66 -62"/>
  <path fill="#f09898" d="M 62 -64 C 62 -78 70 -86 74 -80 C 75 -76 72 -68 67 -64" opacity="0.78"/>
  <!-- Sleeping eyes -->
  <path fill="none" stroke="#6a3010" stroke-width="2" stroke-linecap="round" d="M 42 -40 Q 47 -45 52 -40"/>
  <path fill="none" stroke="#6a3010" stroke-width="2" stroke-linecap="round" d="M 58 -40 Q 63 -45 68 -40"/>
  <path fill="none" stroke="#6a3010" stroke-width="1.2" stroke-linecap="round" d="M 42 -41 L 41 -45"/>
  <path fill="none" stroke="#6a3010" stroke-width="1.2" stroke-linecap="round" d="M 52 -44 L 52 -48"/>
  <path fill="none" stroke="#6a3010" stroke-width="1.2" stroke-linecap="round" d="M 58 -41 L 57 -45"/>
  <path fill="none" stroke="#6a3010" stroke-width="1.2" stroke-linecap="round" d="M 68 -44 L 68 -48"/>
  <!-- Nose -->
  <ellipse cx="70" cy="-24" rx="5" ry="3.5" fill="#3a1808"/>
  <!-- Smile -->
  <path fill="none" stroke="#6a3010" stroke-width="1.3" stroke-linecap="round" d="M 66 -20 Q 70 -16 74 -20"/>
  <!-- Whiskers -->
  <path fill="none" stroke="#c09060" stroke-width="0.7" d="M 70 -24 Q 88 -26 96 -24"/>
  <path fill="none" stroke="#c09060" stroke-width="0.7" d="M 70 -22 Q 88 -20 96 -18"/>
  <path fill="none" stroke="#c09060" stroke-width="0.7" d="M 70 -24 Q 52 -26 44 -24"/>
  <!-- Paws -->
  <ellipse cx="50" cy="90" rx="22" ry="10" fill="#e07030"/>
  <ellipse cx="75" cy="92" rx="18" ry="8"  fill="#e07030"/>
  <path fill="none" stroke="#c05020" stroke-width="1" d="M 42 93 L 40 98 M 50 95 L 50 100 M 58 94 L 58 99"/>
</g>

<!-- ═══ BOTTOM-LEFT: Red spotted mushrooms ═══ -->
<g transform="translate(150,900)">
  <!-- Large mushroom -->
  <path fill="#f2eee4" stroke="#d8c8a8" stroke-width="0.9"
        d="M -12 -2 C -14 -34 -12 -60 -10 -83 Q -8 -91 0 -91 Q 8 -91 10 -83 C 12 -60 14 -34 12 -2 Z"/>
  <path fill="#e8e0cc" d="M -18 -40 Q -8 -35 0 -37 Q 8 -35 18 -40 Q 16 -30 0 -32 Q -16 -30 -18 -40"/>
  <ellipse cx="0" cy="-91" rx="46" ry="7" fill="rgba(80,30,10,0.10)" filter="url(#sf)"/>
  <path fill="#d02828" d="M -46 -91 C -48 -132 -22 -160 0 -162 C 22 -160 48 -132 46 -91 Z"/>
  <path fill="#e84040" d="M -22 -96 C -26 -130 -12 -152 0 -154 C -16 -150 -36 -126 -30 -94 Z" opacity="0.52"/>
  <path fill="rgba(255,255,255,0.16)" d="M -36 -102 C -38 -128 -20 -150 -8 -154 C -28 -146 -42 -122 -38 -100 Z"/>
  <circle cx="-18" cy="-130" r="9"   fill="rgba(255,255,255,0.88)"/>
  <circle cx=" 16" cy="-120" r="7.5" fill="rgba(255,255,255,0.88)"/>
  <circle cx="  2" cy="-104" r="6"   fill="rgba(255,255,255,0.85)"/>
  <circle cx=" 28" cy="-140" r="6"   fill="rgba(255,255,255,0.82)"/>
  <circle cx="-35" cy="-114" r="5"   fill="rgba(255,255,255,0.80)"/>
  <!-- Medium mushroom -->
  <path fill="#f2eee4" stroke="#d8c8a8" stroke-width="0.7"
        d="M 44 -2 C 42 -28 44 -50 46 -64 Q 48 -70 54 -70 Q 60 -70 62 -64 C 64 -50 66 -28 64 -2 Z"/>
  <path fill="#d02828" d="M 26 -70 C 24 -100 38 -118 54 -119 C 70 -118 82 -100 80 -70 Z" opacity="0.92"/>
  <path fill="#e84040" d="M 36 -74 C 34 -96 44 -110 54 -112 C 42 -108 34 -92 38 -72 Z" opacity="0.48"/>
  <circle cx="44" cy="-98" r="6"  fill="rgba(255,255,255,0.85)"/>
  <circle cx="64" cy="-90" r="5"  fill="rgba(255,255,255,0.85)"/>
  <circle cx="54" cy="-80" r="4"  fill="rgba(255,255,255,0.80)"/>
  <!-- Small mushroom -->
  <path fill="#f2eee4" stroke="#d8c8a8" stroke-width="0.6"
        d="M -70 -2 C -72 -22 -70 -38 -68 -48 Q -66 -52 -61 -52 Q -56 -52 -55 -48 C -53 -38 -51 -22 -53 -2 Z"/>
  <path fill="#cc2020" d="M -79 -52 C -80 -74 -68 -86 -62 -87 C -56 -86 -44 -74 -46 -52 Z" opacity="0.85"/>
  <circle cx="-64" cy="-74" r="4"  fill="rgba(255,255,255,0.82)"/>
  <circle cx="-53" cy="-64" r="3"  fill="rgba(255,255,255,0.78)"/>
  <!-- Ground grass -->
  <path fill="rgba(88,140,58,0.20)" d="M -92 0 Q -80 -12 -66 0 Q -50 -14 -36 0 Q -22 -12 -8 0 Q 6 -14 20 0 Q 34 -12 50 0 Q 64 -10 78 0 Z"/>
</g>

<!-- ═══ BOTTOM-LEFT-CENTER: Leaf umbrella (partial) ═══ -->
<g transform="translate(278,916)" opacity="0.72">
  <path fill="none" stroke="#8a5828" stroke-width="3.5" stroke-linecap="round"
        d="M 0 0 C 2 -18 0 -40 0 -66"/>
  <path fill="none" stroke="#8a5828" stroke-width="3.5" stroke-linecap="round"
        d="M 0 0 C 10 10 12 22 6 30 C 0 36 -10 32 -8 24"/>
  <path fill="#488030" d="M 0 -66 C -22 -82 -55 -76 -60 -53 C -56 -38 -28 -33 0 -66"/>
  <path fill="#6aaa44" d="M 0 -66 C -18 -84 -48 -82 -54 -60 C -52 -47 -26 -42 0 -66" opacity="0.62"/>
  <path fill="#488030" d="M 0 -66 C 22 -82 55 -76 60 -53 C 56 -38 28 -33 0 -66"/>
  <path fill="#6aaa44" d="M 0 -66 C 18 -84 48 -82 54 -60 C 52 -47 26 -42 0 -66" opacity="0.62"/>
  <circle cx="-40" cy="-58" r="6.5" fill="#e84888"/>
  <circle cx="-40" cy="-58" r="2.8" fill="#f8b8d0"/>
  <circle cx=" 40" cy="-58" r="6.5" fill="#e8a030"/>
  <circle cx=" 40" cy="-58" r="2.8" fill="#f8d888"/>
  <circle cx="-55" cy="-46" r="5"   fill="#5070d0"/>
  <circle cx=" 55" cy="-46" r="5"   fill="#d04888"/>
  <circle cx="  0" cy="-82" r="5"   fill="#e8c030"/>
  <path fill="#6aaa44" d="M -60 -53 C -72 -40 -68 -26 -56 -26 C -46 -26 -46 -40 -60 -53"/>
  <path fill="#6aaa44" d="M  60 -53 C  72 -40  68 -26  56 -26 C  46 -26  46 -40  60 -53"/>
</g>

<!-- ═══ RIGHT EDGE: Dragonfly ═══ -->
<g transform="translate(1422,222)" opacity="0.74">
  <ellipse cx="-22" cy="-8" rx="22" ry="8"  fill="rgba(70,168,220,0.42)" transform="rotate(-20,-22,-8)"/>
  <ellipse cx=" 22" cy="-8" rx="22" ry="8"  fill="rgba(70,168,220,0.42)" transform="rotate(20,22,-8)"/>
  <ellipse cx="-18" cy=" 8" rx="17" ry="6"  fill="rgba(70,168,220,0.32)" transform="rotate(-30,-18,8)"/>
  <ellipse cx=" 18" cy=" 8" rx="17" ry="6"  fill="rgba(70,168,220,0.32)" transform="rotate(30,18,8)"/>
  <path fill="none" stroke="rgba(30,128,180,0.40)" stroke-width="0.7" d="M 0 -2 L -42 -16"/>
  <path fill="none" stroke="rgba(30,128,180,0.30)" stroke-width="0.5" d="M 0  0 L -32  12"/>
  <circle cx="0" cy="0" r="6" fill="#3080b8"/>
  <rect x="-2.8" y="6"  width="5.6" height="12" rx="2.8" fill="#3080b8"/>
  <rect x="-2.4" y="18" width="4.8" height="10" rx="2.4" fill="#2668a0"/>
  <rect x="-2"   y="28" width="4"   height="10" rx="2"   fill="#1e58a0"/>
  <rect x="-1.5" y="38" width="3"   height="8"  rx="1.5" fill="#1e4890"/>
  <ellipse cx="0" cy="50" rx="2" ry="4" fill="#1e4890"/>
  <circle cx="0" cy="-7" r="7" fill="#3080b8"/>
  <circle cx="-5" cy="-8" r="5"   fill="#48c8e8"/>
  <circle cx=" 5" cy="-8" r="5"   fill="#48c8e8"/>
  <circle cx="-5" cy="-8" r="2.5" fill="#0a2058"/>
  <circle cx=" 5" cy="-8" r="2.5" fill="#0a2058"/>
  <circle cx="-4" cy="-9" r="1"   fill="white"/>
  <circle cx=" 6" cy="-9" r="1"   fill="white"/>
</g>

<!-- ═══ BOTTOM-RIGHT: Hedgehog ═══ -->
<g transform="translate(1315,884)">
  <ellipse cx="-14" cy="18" rx="62" ry="11" fill="rgba(80,38,8,0.09)"/>
  <!-- Spiky body -->
  <path fill="#8a6035"
    d="M -64 -10 C -59 -34 -46 -52 -34 -60
       L -28 -76 L -24 -58 L -19 -74 L -14 -58 L -9 -70 L -4 -57
       L 0 -68  L 5 -56  L 10 -66  L 15 -54  L 20 -62  L 24 -50
       L 28 -56  L 31 -44  L 34 -52  L 36 -42
       C 48 -35 54 -20 53 -4 C 51 16 34 28 8 32 C -16 36 -55 26 -64 -10"/>
  <path fill="#aa8050"
    d="M -54 -8 C -49 -28 -38 -44 -26 -50
       L -22 -62 L -18 -48 L -14 -58 L -10 -46 L -6 -54 L -2 -44
       L 2 -52  L 6 -42  L 10 -50  L 14 -40  L 18 -46  L 22 -36
       C 36 -28 44 -14 42 -3 C 40 14 26 24 6 28 C -16 32 -47 18 -54 -8"
    opacity="0.50"/>
  <!-- Face -->
  <ellipse cx="-42" cy="-8" rx="24" ry="20" fill="#d4b080"/>
  <circle cx="-46" cy="-12" r="5.5" fill="#1a1008"/>
  <circle cx="-45" cy="-13" r="2"   fill="white"/>
  <ellipse cx="-23" cy="-2" rx="5.5" ry="4" fill="#2a1408"/>
  <path fill="none" stroke="#5a3018" stroke-width="1.3" stroke-linecap="round"
        d="M -28 2 Q -24 7 -20 2"/>
  <path fill="#c09060" d="M -50 -26 C -50 -36 -44 -40 -40 -36 C -38 -30 -42 -24 -50 -26"/>
  <!-- Belly -->
  <ellipse cx="-8" cy="14" rx="36" ry="15" fill="#e8d0a8" opacity="0.62"/>
  <!-- Feet -->
  <ellipse cx="-20" cy="32" rx="12" ry="6" fill="#c4a060"/>
  <ellipse cx="  8" cy="34" rx="12" ry="6" fill="#c4a060"/>
  <path fill="none" stroke="#8a6028" stroke-width="1" d="M -26 36 L -28 40 M -20 38 L -20 42 M -14 36 L -12 40"/>
  <path fill="none" stroke="#8a6028" stroke-width="1" d="M   2 40 L   0 44 M   8 42 L   8 46 M  14 40 L  16 44"/>
</g>

<!-- ═══ BOTTOM-RIGHT: Small pine tree ═══ -->
<g transform="translate(1422,880)">
  <rect x="-5" y="-62" width="10" height="62" rx="3" fill="#7a5025"/>
  <path fill="#2a7020" d="M -38 -62 C -36 -76 -10 -112 0 -120 C 10 -112 36 -76 38 -62 Z"/>
  <path fill="#4a9038" d="M -32 -64 C -30 -76 -8 -106 0 -114 C 8 -106 30 -76 32 -64 Z" opacity="0.52"/>
  <path fill="#2a7020" d="M -28 -98 C -26 -110 -8 -138 0 -144 C 8 -138 26 -110 28 -98 Z"/>
  <path fill="#4a9038" d="M -23 -100 C -21 -110 -6 -132 0 -138 C 6 -132 21 -110 23 -100 Z" opacity="0.52"/>
  <path fill="#2a7020" d="M -16 -128 C -14 -136 -5 -155 0 -160 C 5 -155 14 -136 16 -128 Z"/>
  <path fill="#4a9038" d="M -12 -130 C -10 -136 -3 -152 0 -157 C 3 -152 10 -136 12 -130 Z" opacity="0.48"/>
  <path fill="rgba(238,248,255,0.68)" d="M -6 -154 C -4 -160 0 -163 0 -160 C 4 -156 6 -148 -6 -154"/>
</g>

<!-- ═══ Pink butterfly (top-left safe zone) ═══ -->
<g transform="translate(284,44)" opacity="0.68">
  <path fill="#e890bc" d="M 0 0 C -18 -24 -44 -20 -40 0 C -36 18 -10 16 0 0"/>
  <path fill="#dd70a0" d="M 0 0 C -15 -20 -38 -16 -34 0 C -30 14 -8 12 0 0" opacity="0.42"/>
  <path fill="#e890bc" d="M 0 0 C 18 -24 44 -20 40 0 C 36 18 10 16 0 0"/>
  <path fill="#dd70a0" d="M 0 0 C 15 -20 38 -16 34 0 C 30 14 8 12 0 0" opacity="0.42"/>
  <path fill="#f0a8cc" d="M 0 0 C -14 14 -28 20 -22 30 C -12 38 -4 24 0 0"/>
  <path fill="#f0a8cc" d="M 0 0 C 14 14 28 20 22 30 C 12 38 4 24 0 0"/>
  <circle cx="-28" cy="-8" r="4" fill="rgba(180,78,138,0.32)"/>
  <circle cx=" 28" cy="-8" r="4" fill="rgba(180,78,138,0.32)"/>
  <ellipse cx="0" cy="8" rx="2.8" ry="13" fill="#6a3060"/>
  <path fill="none" stroke="#6a3060" stroke-width="1.2" stroke-linecap="round"
        d="M -1 -4 C -6 -14 -9 -22 -7 -28"/>
  <circle cx="-7" cy="-28" r="3" fill="#6a3060"/>
  <path fill="none" stroke="#6a3060" stroke-width="1.2" stroke-linecap="round"
        d="M 1 -4 C 6 -14 9 -22 7 -28"/>
  <circle cx="7" cy="-28" r="3" fill="#6a3060"/>
</g>

<!-- Tiny scattered petals -->
<circle cx="350" cy="28"  r="3.5" fill="rgba(220,78,128,0.32)"/>
<circle cx="368" cy="18"  r="2.5" fill="rgba(220,78,128,0.26)"/>
<circle cx="620" cy="38"  r="3"   fill="rgba(80,112,220,0.28)"/>
<circle cx="700" cy="22"  r="2.8" fill="rgba(80,112,220,0.22)"/>
<circle cx="880" cy="30"  r="2.5" fill="rgba(220,175,48,0.28)"/>
<circle cx="1060" cy="20" r="3"   fill="rgba(200,78,158,0.26)"/>
<circle cx="1168" cy="34" r="2.5" fill="rgba(80,112,220,0.24)"/>

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


@st.cache_data(ttl=300, show_spinner=False)
def fetch_market_sparklines() -> dict:
    """30-day daily close history for each market index; returns {sym: {dates, prices}}."""
    import yfinance as yf
    syms = ["^N225","^HSI","^GDAXI","^FTSE","^GSPC","^IXIC","GC=F","BTC-USD"]
    out = {}
    for sym in syms:
        try:
            h = yf.Ticker(sym).history(period="1mo", interval="1d")
            if not h.empty:
                pairs = [(str(d.date()), float(v))
                         for d, v in zip(h.index, h["Close"].values)
                         if not pd.isna(v)]
                out[sym] = {"dates": [p[0] for p in pairs],
                            "prices": [p[1] for p in pairs]}
        except Exception:
            out[sym] = {"dates": [], "prices": []}
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


# ── US market holiday detection ───────────────────────────────────────────────

def is_us_market_closed(check_date) -> tuple:
    """Return (is_closed: bool, reason: str). Checks weekends + NYSE holidays."""
    from datetime import date as _d
    if hasattr(check_date, "date"):
        check_date = check_date.date()
    if check_date.weekday() >= 5:
        return True, "Víkend / Weekend"

    y = check_date.year

    def nth_weekday(yr, mo, n, wd):
        count = 0
        for day in range(1, 32):
            try:
                dt = _d(yr, mo, day)
                if dt.weekday() == wd:
                    count += 1
                    if count == n:
                        return dt
            except ValueError:
                break
        return None

    def last_weekday(yr, mo, wd):
        for day in range(31, 23, -1):
            try:
                dt = _d(yr, mo, day)
                if dt.weekday() == wd:
                    return dt
            except ValueError:
                continue
        return None

    def easter(yr):
        a, b, c = yr % 19, yr // 100, yr % 100
        d2, e = b // 4, b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19*a + b - d2 - g + 15) % 30
        i, k = c // 4, c % 4
        l = (32 + 2*e + 2*i - h - k) % 7
        m2 = (a + 11*h + 22*l) // 451
        mo = (h + l - 7*m2 + 114) // 31
        dy = ((h + l - 7*m2 + 114) % 31) + 1
        return _d(yr, mo, dy)

    def subst(hdate):
        if hdate.weekday() == 5: return hdate - timedelta(days=1)
        if hdate.weekday() == 6: return hdate + timedelta(days=1)
        return hdate

    fixed_holidays = [
        (_d(y, 1, 1),  "New Year's Day / Nový rok"),
        (_d(y, 6, 19), "Juneteenth National Independence Day"),
        (_d(y, 7, 4),  "Independence Day / Deň nezávislosti USA"),
        (_d(y, 12, 25),"Christmas Day / Vianoce"),
    ]
    for hdate, hname in fixed_holidays:
        if check_date == subst(hdate):
            return True, hname

    variable_holidays = [
        (nth_weekday(y, 1, 3, 0),   "Martin Luther King Jr. Day"),
        (nth_weekday(y, 2, 3, 0),   "Presidents' Day"),
        (last_weekday(y, 5, 0),     "Memorial Day"),
        (nth_weekday(y, 9, 1, 0),   "Labor Day"),
        (nth_weekday(y, 11, 4, 3),  "Thanksgiving Day"),
        (easter(y) - timedelta(days=2), "Good Friday / Veľký piatok"),
    ]
    for hdate, hname in variable_holidays:
        if hdate and check_date == hdate:
            return True, hname

    return False, ""


def _briefing_text(b_type: str, markets: list, watchlist_data: dict,
                   us_closed: bool, close_reason: str) -> str:
    """Generate Buffett-style expert commentary for the given briefing period."""
    def _m(sym): return next((m for m in markets if m["sym"] == sym), None)
    sp   = _m("^GSPC"); ndq = _m("^IXIC"); dax = _m("^GDAXI")
    n225 = _m("^N225"); hsi = _m("^HSI")
    gld  = _m("GC=F");  btc = _m("BTC-USD")

    def cs(m): return ("+" if m["chg"] >= 0 else "") + f"{m['chg']:.2f}%" if m else "N/A"
    def sent(chg):
        if chg >  1.5: return "silný rast 📈"
        if chg >  0.3: return "mierny rast 🔼"
        if chg > -0.3: return "stabilný ➡️"
        if chg > -1.5: return "oslabenie 🔽"
        return "výrazný pokles 📉"

    risk_on  = (sp and sp["chg"] > 0.5) or (ndq and ndq["chg"] > 0.5)
    risk_off = (gld and gld["chg"] > 0.6) or (sp and sp["chg"] < -0.5)

    us_banner = (
        f"\n\n> 🏛️ **Pozor — US burzy sú dnes zatvorené: {close_reason}.**  \n"
        "> Objem obchodov na globálnych trhoch bude nižší ako obvykle.\n\n"
    ) if us_closed else ""

    if b_type == "morning":
        asia_bits = [f"Nikkei {cs(n225)}" if n225 else "", f"Hang Seng {cs(hsi)}" if hsi else ""]
        asia_str  = " · ".join(b for b in asia_bits if b) or "dáta sa načítavajú"
        eu_str    = f"DAX {cs(dax)}" if dax else "dáta sa načítavajú"
        tone      = "pozitívna — risk-on" if risk_on else "opatrná — risk-off" if risk_off else "neutrálna"
        gld_note  = (f"\n- 🥇 **Zlato {cs(gld)}** — inštitucionálni investori presúvajú kapitál do bezpečných prístavov. Opatrnosť je na mieste."
                     if gld and gld["chg"] > 0.4 else
                     f"\n- 🥇 **Zlato {cs(gld)}** — odliv z defenzívnych aktív signalizuje chuť do rizika." if gld and gld["chg"] < -0.4 else "")
        btc_note  = (f"\n- ₿ **Bitcoin {cs(btc)}** — silný pohyb krypta potvrduje *risk-on* náladu na trhoch." if btc and btc["chg"] > 2 else "")
        return us_banner + f"""**Celkový sentiment:** {tone}

| | |
|---|---|
| 🌏 Ázia | {asia_str} |
| 🇪🇺 Európa (DAX) | {eu_str} |
{gld_note}{btc_note}

**Odporúčanie:** {
"Sledovať selektívne príležitosti — trhy sú v ofenzívnom móde. Kvalitné spoločnosti s konkurenčnou výhodou sú preferovanou voľbou."
if risk_on else
"Zvýšiť opatrnosť. V neistých časoch je cash pozícia tiež legitímna stratégia — *'Cash is king when opportunities arise.'*"
if risk_off else
"Udržiavať doterajšiu alokáciu a vyhnúť sa reaktívnym rozhodnutiam. Trh hľadá smer."
}

> *„Pravidlo číslo jedna: nikdy nestráťte peniaze. Pravidlo číslo dva: nikdy nezabudnite na pravidlo číslo jedna."* — Warren Buffett"""

    elif b_type == "preopen":
        sp_note = ""
        if us_closed:
            return us_banner + f"""**🔔 US trhy dnes neotvárajú — {close_reason}**

Globálne obchodovanie prebieha v zredukovanom objeme. Európske a ázijské trhy nastavujú smer.
DAX: {cs(dax)} · Zlato: {cs(gld)}

> *„Investovanie je jednoduché, ale nie ľahké."* — Warren Buffett"""
        if sp:
            if sp["chg"] > 0.5:
                sp_note = f"S&P 500 futures naznačujú **pozitívne otvorenie ({cs(sp)})**. Momentum favorizuje býkov — ale prvých 30 minút býva volatilných."
            elif sp["chg"] < -0.5:
                sp_note = f"S&P 500 futures pod tlakom ({cs(sp)}). Nevstupujte impulzívne pri otvorení — počkajte na stabilizáciu ceny."
            else:
                sp_note = f"S&P 500 v neutrálnej zóne ({cs(sp)}). Smer otvorenia nie je jasný — vyčkajte na prvý 15-minútový vývoj."

        tech_note = ""
        if ndq:
            tech_note = f"\n- 💻 **NASDAQ {cs(ndq)}** — technologický sektor " + (
                "vedie rast. Big Tech môže byť katalyzátorom." if ndq["chg"] > 0.8 else
                "pod tlakom. Ocenenia ostávajú citlivé na výnosy dlhopisov." if ndq["chg"] < -0.8 else
                "v úzkom rozmedzí.")

        return us_banner + f"""{sp_note}
{tech_note}
- 🥇 **Zlato {cs(gld)}** — {"defenzívna nálada sa udržuje." if gld and gld["chg"] > 0.3 else "rizikový apetít narastá." if gld and gld["chg"] < -0.3 else "bez výrazného smeru."}

**Sektor focus:** {
"Technológia & rastové akcie — sledujte objem pri otvorení."
if ndq and ndq["chg"] > 0.5 else
"Defenzívne sektory (utility, zdravotníctvo, spotrebné tovary) — ochrana kapitálu v popredí."
if risk_off else
"Selektívny prístup — žiadny sektor nedominuje, hľadajte individuálne príbehy."
}

> *„Cena je to, čo zaplatíte. Hodnota je to, čo dostanete."* — Warren Buffett"""

    else:  # postclose
        if us_closed:
            return us_banner + f"""**🌙 US trhy dnes neobchodovali — {close_reason}**

Globálne trhy fungovali bez amerického objemu. Zajtra sa obchodovanie obnoví v plnom rozsahu.
Európa: DAX {cs(dax)} · Ázia (posledná relácia): Nikkei {cs(n225)}

> *„Čas je priateľom výnimočnej spoločnosti, nepriateľom priemernej."* — Warren Buffett"""

        # ── Index summary ──
        rows = []
        for sym, label in [("^GSPC","S&P 500"),("^IXIC","NASDAQ"),("^GDAXI","DAX"),("^N225","Nikkei 225")]:
            m2 = _m(sym)
            if m2:
                sign2 = "+" if m2["chg"] >= 0 else ""
                arrow2 = "▲" if m2["chg"] >= 0 else "▼"
                rows.append(f"| {label} | {m2['price']:,.0f} | {sign2}{m2['chg']:.2f}% {arrow2} |")

        index_table = ""
        if rows:
            index_table = "| Index | Záver | Zmena |\n|---|---|---|\n" + "\n".join(rows)

        # ── Verdict ──
        verdict = ""
        if sp:
            if sp["chg"] > 1.5:
                verdict = "💚 **Silný býčí deň.** Rally podporená širokým základom — zdravý signál. Dlhodobí investori môžu postupne budovať pozície v kvalitných tituloch."
            elif sp["chg"] > 0.3:
                verdict = "🟢 **Mierny nárast.** Trh si drží pozitívny bias. Bez výrazného katalyzátora nie je dôvod meniť alokáciu."
            elif sp["chg"] < -1.5:
                verdict = "🔴 **Výrazný pokles.** *'Be greedy when others are fearful.'* Zvážte, či súčasné ceny ponúkajú lepšiu vstupnú príležitosť pre kvalitné tituly."
            elif sp["chg"] < -0.3:
                verdict = "🟡 **Mierne oslabenie.** Normálna korekcia bez systémového rizika. Udržujte disciplínu a dlhodobý horizont."
            else:
                verdict = "⚪ **Neutrálny deň.** Trh bez jasného smeru. Konsolidácia po nedávnych pohyboch."

        # ── Alts ──
        alt_lines = []
        if gld and abs(gld["chg"]) > 0.4:
            gld_sign = "+" if gld["chg"] > 0 else ""
            note = "inštitucionálna ochrana pretrváva — risk-off." if gld["chg"] > 0 else "outflow z defenzívy — risk-on nálada."
            alt_lines.append(f"🥇 Zlato {gld_sign}{gld['chg']:.2f}% — {note}")
        if btc and abs(btc["chg"]) > 2:
            btc_sign = "+" if btc["chg"] > 0 else ""
            alt_lines.append(f"₿ Bitcoin {btc_sign}{btc['chg']:.2f}% — krypto {'akcelerovalo, risk-on potvrdený.' if btc['chg'] > 0 else 'korigovalo.'}")
        alt_block = ("\n\n**Alternatívne aktíva:**\n" + "\n".join(f"- {l}" for l in alt_lines)) if alt_lines else ""

        # ── Watchlist movers ──
        wl_lines = []
        for t, d in (watchlist_data or {}).items():
            chg = d.get("chg", 0)
            if abs(chg) >= 1.5:
                em = "📈" if chg > 0 else "📉"
                s2 = "+" if chg > 0 else ""
                wl_lines.append(f"- {em} **{t}** ({d.get('name', t)}): {s2}{chg:.2f}%")

        wl_block = ("\n\n**Vaše sledované tituly — pohyby >1.5%:**\n" + "\n".join(wl_lines)) if wl_lines else ""

        return us_banner + f"""{index_table}

{verdict}{alt_block}{wl_block}

**Výhľad na zajtra:** Sledujte predtrhové futures (22:30–05:00 SEČ) a makroekonomický kalendár. Nereagujte impulzívne na jednodenné pohyby.

> *„Buďte chamtiví, keď sú ostatní vystrašení, a vystrašení, keď sú ostatní chamtiví."* — Warren Buffett"""


# ── Tab 3: Briefing ───────────────────────────────────────────────────────────

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
            f"<small style='color:#6a7a5a'>{pub}{' · ' if pub and tstr else ''}{tstr}</small>",
            unsafe_allow_html=True,
        )
        st.markdown("<hr style='margin:3px 0 5px 0;border:none;border-top:1px solid #d0ddc8'>",
                    unsafe_allow_html=True)


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

    # Determine briefing period
    cet_mins = cet_now.hour * 60 + cet_now.minute
    if 7*60 <= cet_mins < 15*60:
        b_type = "morning"
        b_label = "🌅 Ranný prehľad · 07:00 SEČ"
        b_next  = "Ďalší: Pred-otvorenie US 15:00"
    elif 15*60 <= cet_mins < 22*60 + 30:
        b_type = "preopen"
        b_label = "🔔 Pred-otvorenie US · 15:00 SEČ"
        b_next  = "Ďalší: Záver US 22:30"
    else:
        b_type = "postclose"
        b_label = "🌙 Záver Wall Street · 22:30 SEČ"
        b_next  = "Ďalší: Ranný prehľad 07:00"

    us_closed, close_reason = is_us_market_closed(cet_now)

    st.header("📈 Investment / Investovanie")
    st.markdown(
        f'<p class="bilingual-caption">'
        f'Investičný prehľad · {date_sk} · SEČ {cet_now.strftime("%H:%M")}'
        f' · {b_label}'
        f'{" · 🏛️ US CLOSED" if us_closed else ""}'
        f'</p>',
        unsafe_allow_html=True,
    )

    # ── Markets with sparklines ──
    st.subheader("🌍 Dnešné trhy / Today's Markets")
    with st.spinner("Načítavanie trhov…"):
        markets = fetch_morning_markets()
        sparks  = fetch_market_sparklines()

    for rs in range(0, len(markets), 4):
        row_m = markets[rs:rs + 4]
        cols  = st.columns(len(row_m))
        for col, m in zip(cols, row_m):
            color    = "#2a7a4a" if m["chg"] >= 0 else "#a83232"
            fill_rgb = "42,122,74" if m["chg"] >= 0 else "168,50,50"
            sign     = "+" if m["chg"] >= 0 else ""
            arrow    = "▲" if m["chg"] >= 0 else "▼"
            hist     = sparks.get(m["sym"], {"dates": [], "prices": []})
            prices   = hist["prices"]
            dates    = hist["dates"]
            with col:
                fig = go.Figure()
                if len(prices) > 2:
                    base = min(prices)
                    fig.add_trace(go.Scatter(
                        x=dates, y=[base] * len(dates), mode="lines",
                        line=dict(width=0), showlegend=False, hoverinfo="skip",
                    ))
                    fig.add_trace(go.Scatter(
                        x=dates, y=prices, mode="lines",
                        line=dict(color=color, width=1.6),
                        fill="tonexty",
                        fillcolor=f"rgba({fill_rgb},0.12)",
                        showlegend=False,
                        hovertemplate="%{x|%m/%d}: %{y:,.0f}<extra></extra>",
                    ))
                fig.update_layout(
                    height=120,
                    margin=dict(t=4, b=24, l=42, r=4),
                    plot_bgcolor="rgba(255,255,255,0.55)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(
                        type="date", tickformat="%m/%d", nticks=3,
                        tickangle=0, showgrid=False, zeroline=False,
                        showline=False, tickfont=dict(size=7, color="#999"),
                    ),
                    yaxis=dict(
                        tickformat=".3s", nticks=3, showgrid=True,
                        gridcolor="rgba(150,150,150,0.15)", zeroline=False,
                        showline=False, tickfont=dict(size=7, color="#999"),
                    ),
                )
                st.plotly_chart(fig, use_container_width=True,
                                config={"displayModeBar": False})
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.72);border-radius:8px;
                            padding:5px 4px 7px;text-align:center;margin-top:-10px;
                            box-shadow:0 1px 5px rgba(0,0,0,0.06)">
                  <span style="font-size:16px">{m['flag']}</span>
                  <div style="font-size:10px;font-weight:700;color:#555;margin:1px 0">{m['name']}</div>
                  <div style="font-size:14px;font-weight:700;color:{color}">{sign}{m['chg']:.2f}%&nbsp;{arrow}</div>
                  <div style="font-size:9px;color:#888">{m['price']:,.0f}</div>
                </div>""", unsafe_allow_html=True)

    # ── Briefing ──
    st.markdown("---")
    st.subheader(f"💼 {b_label}")
    st.caption(f"⏭ {b_next}")

    with st.spinner("Generujem prehľad…"):
        raw_wl2    = load_watchlist()
        watchlist2 = [w if isinstance(w, dict) else {"ticker": w, "name": w, "added_by": "", "added_at": ""}
                      for w in raw_wl2]
        wl_data2   = fetch_watchlist_data(tuple(w["ticker"] for w in watchlist2)) if watchlist2 else {}

    briefing_md = _briefing_text(b_type, markets, wl_data2, us_closed, close_reason)
    st.markdown(briefing_md)

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
        "📈 Investment / Investovanie",
    ])
    with tab1:
        tab_sync()
    with tab2:
        tab_dashboard()
    with tab3:
        tab_briefing()


if __name__ == "__main__":
    main()
