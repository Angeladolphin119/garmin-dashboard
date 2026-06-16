import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import gspread
from google.oauth2.service_account import Credentials
import os
from pathlib import Path

st.set_page_config(
    page_title="運動小組 Dashboard",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    .metric-card {
        background: #f0f2f6; border-radius: 12px;
        padding: 16px 20px; text-align: center;
    }
    .metric-label { font-size: 13px; color: #666; margin-bottom: 4px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #1f77b4; }
    .metric-unit  { font-size: 12px; color: #999; }
    .stTabs [data-baseweb="tab"] { font-size: 16px; padding: 10px 20px; }
</style>
""", unsafe_allow_html=True)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]
COLORS = px.colors.qualitative.Set2


# ── Google Sheets 連線 ────────────────────────────────────────────────────────

@st.cache_resource
def get_sheet():
    try:
        info = dict(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(info, scopes=SCOPES)
        sheet_id = st.secrets["SHEET_ID"]
    except Exception:
        cred_file = Path("credentials.json")
        if not cred_file.exists():
            st.error("找不到 credentials.json，請先完成 Google API 設定")
            st.stop()
        creds = Credentials.from_service_account_file(str(cred_file), scopes=SCOPES)
        sheet_id = os.getenv("SHEET_ID", "")
        if not sheet_id:
            st.error(".env 裡沒有設定 SHEET_ID")
            st.stop()

    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(sheet_id).sheet1

    # 第一次使用時自動建立標題列
    if not sheet.row_values(1):
        sheet.insert_row(
            ["日期", "姓名", "步數", "總距離(km)", "消耗卡路里",
             "活動時間(分)", "靜止心率", "睡眠(小時)", "跑步距離(km)"], 1
        )
    return sheet


@st.cache_data(ttl=60)
def load_df(_sheet) -> pd.DataFrame:
    records = _sheet.get_all_records()
    if not records:
        return pd.DataFrame()
    df = pd.DataFrame(records)
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["日期"])
    for col in ["步數", "總距離(km)", "消耗卡路里", "活動時間(分)", "靜止心率", "睡眠(小時)", "跑步距離(km)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df.sort_values("日期")


# ── Garmin 資料抓取 ───────────────────────────────────────────────────────────

def fetch_garmin(email: str, password: str, date_str: str) -> dict:
    from garminconnect import Garmin
    client = Garmin(email, password)
    client.login()

    stats = client.get_stats(date_str)
    steps      = stats.get("totalSteps", 0) or 0
    distance_m = stats.get("totalDistance", 0) or 0
    calories   = stats.get("activeKilocalories", 0) or 0
    active_min = round((stats.get("activeSeconds", 0) or 0) / 60)
    resting_hr = stats.get("restingHeartRate", 0) or 0

    sleep_hours = 0.0
    try:
        sleep = client.get_sleep_data(date_str)
        secs = sleep.get("dailySleepDTO", {}).get("sleepTimeSeconds", 0) or 0
        sleep_hours = round(secs / 3600, 1)
    except Exception:
        pass

    run_km = 0.0
    try:
        acts = client.get_activities_by_date(date_str, date_str, "running")
        run_km = round(sum((a.get("distance", 0) or 0) for a in acts) / 1000, 2)
    except Exception:
        pass

    return {
        "steps": steps,
        "distance_km": round(distance_m / 1000, 2),
        "calories": calories,
        "active_min": active_min,
        "resting_hr": resting_hr,
        "sleep_h": sleep_hours,
        "run_km": run_km,
    }


def already_synced(sheet, date_str: str, name: str) -> bool:
    records = sheet.get_all_values()
    return any(r[0] == date_str and r[1] == name for r in records[1:] if len(r) >= 2)


def write_row(sheet, date_str: str, name: str, d: dict):
    sheet.append_row(
        [date_str, name, d["steps"], d["distance_km"], d["calories"],
         d["active_min"], d["resting_hr"], d["sleep_h"], d["run_km"]],
        value_input_option="USER_ENTERED"
    )


# ── Tab 1：同步我的資料 ────────────────────────────────────────────────────────

def tab_sync(sheet):
    st.header("同步我的資料")
    st.caption("輸入你的 Garmin 帳號，資料會寫入共用的 Google Sheet，密碼不會被儲存。")

    with st.form("sync_form"):
        name  = st.text_input("你的暱稱（群組裡顯示用）", placeholder="例：小明")
        email = st.text_input("Garmin 帳號（Email）")
        pw    = st.text_input("Garmin 密碼", type="password")

        today = date.today()
        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("同步開始日期", value=today - timedelta(days=6))
        with col2:
            end   = st.date_input("同步結束日期", value=today)

        submitted = st.form_submit_button("開始同步", type="primary", use_container_width=True)

    if submitted:
        if not (name and email and pw):
            st.error("暱稱、帳號、密碼都必須填寫")
            return

        date_list = [
            (start + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range((end - start).days + 1)
        ]

        progress = st.progress(0, text="登入 Garmin 中…")
        results = []

        try:
            from garminconnect import Garmin, GarminConnectAuthenticationError
            client = Garmin(email, pw)
            client.login()
        except Exception as e:
            st.error(f"Garmin 登入失敗：{e}")
            return

        for i, d in enumerate(date_list):
            progress.progress((i + 1) / len(date_list), text=f"抓取 {d}…")
            if already_synced(sheet, d, name):
                results.append({"日期": d, "狀態": "已有資料，略過"})
                continue
            try:
                data = fetch_garmin(email, pw, d)
                write_row(sheet, d, name, data)
                results.append({
                    "日期": d,
                    "步數": f"{data['steps']:,}",
                    "跑步": f"{data['run_km']} km",
                    "睡眠": f"{data['sleep_h']} h",
                    "狀態": "✅ 已寫入",
                })
            except Exception as e:
                results.append({"日期": d, "狀態": f"❌ {e}"})

        progress.empty()
        st.success(f"同步完成！共處理 {len(date_list)} 天")
        st.dataframe(pd.DataFrame(results), use_container_width=True)
        st.cache_data.clear()


# ── Tab 2：群組 Dashboard ──────────────────────────────────────────────────────

def metric_card(label, value, unit=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>""", unsafe_allow_html=True)


def tab_dashboard(sheet):
    st.header("群組 Dashboard")

    df_all = load_df(sheet)
    if df_all.empty:
        st.info("還沒有資料，請先到「同步我的資料」頁面輸入帳號同步。")
        return

    # 篩選器
    col_f1, col_f2 = st.columns([2, 3])
    with col_f1:
        min_d, max_d = df_all["日期"].min().date(), df_all["日期"].max().date()
        date_range = st.date_input(
            "日期範圍",
            value=(max(min_d, max_d - timedelta(days=29)), max_d),
            min_value=min_d, max_value=max_d,
        )
    with col_f2:
        members = sorted(df_all["姓名"].unique())
        selected = st.multiselect("成員", members, default=members)

    if len(date_range) != 2 or not selected:
        return

    df = df_all[
        (df_all["日期"].dt.date >= date_range[0]) &
        (df_all["日期"].dt.date <= date_range[1]) &
        (df_all["姓名"].isin(selected))
    ]
    if df.empty:
        st.warning("沒有符合條件的資料")
        return

    # 計分卡
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("平均步數",   f"{int(df['步數'].mean()):,}", "步/天")
    with c2: metric_card("跑步總距離", f"{df['跑步距離(km)'].sum():.1f}", "km")
    with c3: metric_card("平均卡路里", f"{int(df['消耗卡路里'].mean())}", "kcal/天")
    with c4: metric_card("平均睡眠",   f"{df['睡眠(小時)'].mean():.1f}", "小時/天")
    with c5: metric_card("活躍天數",   f"{df[df['步數']>0]['日期'].nunique()}", "天")

    st.markdown("---")

    # 每日步數趨勢
    fig = px.line(df, x="日期", y="步數", color="姓名",
                  title="每日步數趨勢", color_discrete_sequence=COLORS, markers=True)
    fig.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig, use_container_width=True)

    # 步數排行 + 跑步距離
    c1, c2 = st.columns(2)
    with c1:
        rank = df.groupby("姓名")["步數"].sum().reset_index().sort_values("步數")
        fig = px.bar(rank, x="步數", y="姓名", orientation="h",
                     title="步數總排行", color="步數",
                     color_continuous_scale="Blues", text="步數")
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        run = df[df["跑步距離(km)"] > 0]
        if run.empty:
            st.info("篩選期間沒有跑步紀錄")
        else:
            fig = px.bar(run, x="日期", y="跑步距離(km)", color="姓名",
                         title="跑步距離（每日）",
                         color_discrete_sequence=COLORS, barmode="stack")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    # 睡眠 + 卡路里
    c3, c4 = st.columns(2)
    with c3:
        fig = px.line(df, x="日期", y="睡眠(小時)", color="姓名",
                      title="睡眠時數", color_discrete_sequence=COLORS, markers=True)
        fig.add_hline(y=7, line_dash="dot", line_color="orange",
                      annotation_text="建議 7h")
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = px.area(df, x="日期", y="消耗卡路里", color="姓名",
                      title="消耗卡路里", color_discrete_sequence=COLORS)
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # 雷達圖
    metrics = ["步數", "跑步距離(km)", "睡眠(小時)", "活動時間(分)", "消耗卡路里"]
    summary = df.groupby("姓名")[metrics].mean()
    norm = (summary - summary.min()) / (summary.max() - summary.min() + 1e-9)
    labels = ["步數", "跑步", "睡眠", "活動", "卡路里"]
    fig = go.Figure()
    for i, (name, row) in enumerate(norm.iterrows()):
        vals = list(row) + [row.iloc[0]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=labels + [labels[0]],
            fill="toself", name=name,
            line_color=COLORS[i % len(COLORS)],
        ))
    fig.update_layout(title="個人運動輪廓",
                      polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                      height=420)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 原始資料"):
        st.dataframe(df.sort_values("日期", ascending=False).reset_index(drop=True),
                     use_container_width=True)

    if st.button("🔄 重新載入"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()


# ── 主程式 ─────────────────────────────────────────────────────────────────────

def main():
    st.title("🏃 運動小組 Dashboard")

    sheet = get_sheet()
    tab1, tab2 = st.tabs(["📥 同步我的資料", "📊 群組 Dashboard"])

    with tab1:
        tab_sync(sheet)
    with tab2:
        tab_dashboard(sheet)


if __name__ == "__main__":
    main()
