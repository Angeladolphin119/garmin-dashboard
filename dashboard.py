import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
from io import StringIO

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

COLORS = px.colors.qualitative.Set2


# ── GitHub 存取 ───────────────────────────────────────────────────────────────

@st.cache_resource
def get_repo():
    from github import Github, GithubException
    token     = st.secrets["GITHUB_TOKEN"]
    repo_name = st.secrets["GITHUB_REPO"]
    g = Github(token)
    return g.get_repo(repo_name)


@st.cache_data(ttl=60, show_spinner=False)
def load_all_data() -> pd.DataFrame:
    from github import GithubException
    repo = get_repo()
    dfs = []
    try:
        contents = repo.get_contents("data")
        for f in contents:
            if f.name.endswith(".csv"):
                df = pd.read_csv(StringIO(f.decoded_content.decode("utf-8")))
                dfs.append(df)
    except GithubException:
        pass

    if not dfs:
        return pd.DataFrame()

    df = pd.concat(dfs, ignore_index=True)
    df["日期"] = pd.to_datetime(df["日期"], errors="coerce")
    df = df.dropna(subset=["日期"])
    for col in ["步數", "總距離(km)", "消耗卡路里", "活動時間(分)", "靜止心率", "睡眠(小時)", "跑步距離(km)"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df.sort_values("日期")


def save_person_data(name: str, new_rows: list[dict]):
    from github import GithubException
    repo = get_repo()
    path = f"data/{name}.csv"
    new_df = pd.DataFrame(new_rows)

    try:
        existing_file = repo.get_contents(path)
        existing_df = pd.read_csv(StringIO(existing_file.decoded_content.decode("utf-8")))
        merged = (
            pd.concat([existing_df, new_df], ignore_index=True)
            .drop_duplicates(subset=["日期"], keep="last")
            .sort_values("日期")
        )
        repo.update_file(path, f"sync: {name}", merged.to_csv(index=False), existing_file.sha)
    except GithubException:
        repo.create_file(path, f"init: {name}", new_df.to_csv(index=False))


# ── Garmin 抓取 ───────────────────────────────────────────────────────────────

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

    sleep_hours = 0.0
    try:
        secs = client.get_sleep_data(date_str).get("dailySleepDTO", {}).get("sleepTimeSeconds", 0) or 0
        sleep_hours = round(secs / 3600, 1)
    except Exception:
        pass

    run_km = 0.0
    try:
        acts   = client.get_activities_by_date(date_str, date_str, "running")
        run_km = round(sum((a.get("distance", 0) or 0) for a in acts) / 1000, 2)
    except Exception:
        pass

    return {
        "日期": date_str,
        "步數": steps,
        "總距離(km)": round(distance_m / 1000, 2),
        "消耗卡路里": calories,
        "活動時間(分)": active_min,
        "靜止心率": resting_hr,
        "睡眠(小時)": sleep_hours,
        "跑步距離(km)": run_km,
    }


# ── Tab 1：同步 ────────────────────────────────────────────────────────────────

def tab_sync():
    st.header("同步我的資料")
    st.caption("輸入 Garmin 帳號，資料會儲存到群組共用的 GitHub 倉庫。密碼只在這次連線使用，不會被儲存。")

    with st.form("sync_form"):
        name  = st.text_input("你的暱稱", placeholder="例：小明")
        email = st.text_input("Garmin 帳號（Email）")
        pw    = st.text_input("Garmin 密碼", type="password")
        c1, c2 = st.columns(2)
        with c1:
            start = st.date_input("開始日期", value=date.today() - timedelta(days=6))
        with c2:
            end   = st.date_input("結束日期", value=date.today())
        submitted = st.form_submit_button("開始同步", type="primary", use_container_width=True)

    if not submitted:
        return

    if not (name and email and pw):
        st.error("請填寫所有欄位")
        return

    date_list = [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range((end - start).days + 1)
    ]

    progress = st.progress(0, text="登入 Garmin 中…")
    results, rows = [], []

    try:
        from garminconnect import Garmin
        st.session_state.pop("garmin_client", None)
        client = Garmin(email, pw)
        client.login()
        st.session_state["garmin_client"] = client
    except Exception as e:
        st.error(f"Garmin 登入失敗：{e}")
        return

    for i, d in enumerate(date_list):
        progress.progress((i + 1) / len(date_list), text=f"抓取 {d}…")
        try:
            row = fetch_garmin(email, pw, d)
            rows.append(row)
            results.append({"日期": d, "步數": f"{row['步數']:,}", "跑步": f"{row['跑步距離(km)']} km",
                            "睡眠": f"{row['睡眠(小時)']} h", "狀態": "✅"})
        except Exception as e:
            results.append({"日期": d, "狀態": f"❌ {e}"})

    progress.empty()

    if rows:
        with st.spinner("儲存到 GitHub…"):
            save_person_data(name, rows)
        st.cache_data.clear()
        st.cache_resource.clear()

    st.success(f"完成！成功同步 {len(rows)} 天")
    st.dataframe(pd.DataFrame(results), use_container_width=True)


# ── Tab 2：Dashboard ───────────────────────────────────────────────────────────

def metric_card(label, value, unit=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>""", unsafe_allow_html=True)


def tab_dashboard():
    st.header("群組 Dashboard")

    with st.spinner("載入資料…"):
        df_all = load_all_data()

    if df_all.empty:
        st.info("還沒有資料，請先到「同步我的資料」頁面輸入帳號同步。")
        return

    c1, c2 = st.columns([2, 3])
    with c1:
        min_d, max_d = df_all["日期"].min().date(), df_all["日期"].max().date()
        dr = st.date_input("日期範圍",
                           value=(max(min_d, max_d - timedelta(days=29)), max_d),
                           min_value=min_d, max_value=max_d)
    with c2:
        members  = sorted(df_all["姓名"].unique()) if "姓名" in df_all.columns else []
        selected = st.multiselect("成員", members, default=members)

    if len(dr) != 2 or not selected:
        return

    df = df_all[
        (df_all["日期"].dt.date >= dr[0]) &
        (df_all["日期"].dt.date <= dr[1])
    ]
    if "姓名" in df.columns:
        df = df[df["姓名"].isin(selected)]

    if df.empty:
        st.warning("沒有符合條件的資料")
        return

    # 計分卡
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: metric_card("平均步數",   f"{int(df['步數'].mean()):,}", "步/天")
    with m2: metric_card("跑步總距離", f"{df['跑步距離(km)'].sum():.1f}", "km")
    with m3: metric_card("平均卡路里", f"{int(df['消耗卡路里'].mean())}", "kcal/天")
    with m4: metric_card("平均睡眠",   f"{df['睡眠(小時)'].mean():.1f}", "小時/天")
    with m5: metric_card("活躍天數",   f"{df[df['步數']>0]['日期'].nunique()}", "天")

    st.markdown("---")

    # 步數趨勢
    fig = px.line(df, x="日期", y="步數", color="姓名", title="每日步數趨勢",
                  color_discrete_sequence=COLORS, markers=True)
    fig.update_layout(hovermode="x unified", height=350)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        rank = df.groupby("姓名")["步數"].sum().reset_index().sort_values("步數")
        fig  = px.bar(rank, x="步數", y="姓名", orientation="h", title="步數排行",
                      color="步數", color_continuous_scale="Blues", text="步數")
        fig.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        run = df[df["跑步距離(km)"] > 0]
        if run.empty:
            st.info("篩選期間沒有跑步紀錄")
        else:
            fig = px.bar(run, x="日期", y="跑步距離(km)", color="姓名",
                         title="跑步距離（每日）", color_discrete_sequence=COLORS, barmode="stack")
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.line(df, x="日期", y="睡眠(小時)", color="姓名", title="睡眠時數",
                      color_discrete_sequence=COLORS, markers=True)
        fig.add_hline(y=7, line_dash="dot", line_color="orange", annotation_text="建議 7h")
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        fig = px.area(df, x="日期", y="消耗卡路里", color="姓名", title="消耗卡路里",
                      color_discrete_sequence=COLORS)
        fig.update_layout(hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)

    # 雷達圖
    metrics = ["步數", "跑步距離(km)", "睡眠(小時)", "活動時間(分)", "消耗卡路里"]
    if "姓名" in df.columns:
        summary = df.groupby("姓名")[metrics].mean()
        norm    = (summary - summary.min()) / (summary.max() - summary.min() + 1e-9)
        labels  = ["步數", "跑步", "睡眠", "活動", "卡路里"]
        fig     = go.Figure()
        for i, (person, row) in enumerate(norm.iterrows()):
            fig.add_trace(go.Scatterpolar(
                r=list(row) + [row.iloc[0]], theta=labels + [labels[0]],
                fill="toself", name=person, line_color=COLORS[i % len(COLORS)],
            ))
        fig.update_layout(title="個人運動輪廓",
                          polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                          height=420)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("📋 原始資料"):
        st.dataframe(df.sort_values("日期", ascending=False).reset_index(drop=True),
                     use_container_width=True)

    if st.button("🔄 重新載入資料"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()


# ── 主程式 ─────────────────────────────────────────────────────────────────────

def main():
    st.title("🏃 運動小組 Dashboard")
    tab1, tab2 = st.tabs(["📥 同步我的資料", "📊 群組 Dashboard"])
    with tab1:
        tab_sync()
    with tab2:
        tab_dashboard()


if __name__ == "__main__":
    main()
