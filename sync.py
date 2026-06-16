"""
Garmin 運動資料自動同步工具
────────────────────────────
首次使用前請完成以下設定：

【Step 1】安裝套件
    pip install -r requirements.txt

【Step 2】Google Sheets API 設定
    1. 前往 https://console.cloud.google.com/
    2. 建立新專案 → 啟用「Google Sheets API」和「Google Drive API」
    3. 左側選單 → IAM → 服務帳戶 → 建立服務帳戶
    4. 下載金鑰（JSON 格式），重新命名為 credentials.json 放進本資料夾
    5. 開啟你的 Google Sheet → 右上角「共用」→ 貼上服務帳戶的 email（編輯者）

【Step 3】設定帳號
    複製 .env.example 為 .env，填入朋友的 Garmin 帳密和 Sheet ID

【Step 4】執行
    python sync.py
    python sync.py --date 2026-06-15   # 指定日期補跑
"""

import os
import sys
import datetime
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ── 讀取 .env 裡所有 USERn 設定 ──────────────────────────────────────────────

def load_users():
    users = []
    i = 1
    while True:
        name  = os.getenv(f"USER{i}_NAME")
        email = os.getenv(f"USER{i}_EMAIL")
        pw    = os.getenv(f"USER{i}_PASS")
        if not (name and email and pw):
            break
        users.append({"name": name, "email": email, "password": pw})
        i += 1
    return users


# ── Garmin 資料抓取 ───────────────────────────────────────────────────────────

def garmin_login(email: str, password: str, token_dir: str = "tokens"):
    from garminconnect import Garmin, GarminConnectAuthenticationError

    token_path = Path(token_dir) / email.replace("@", "_").replace(".", "_")

    client = Garmin(email, password)
    try:
        if token_path.exists():
            client.login(str(token_path))
            log.info(f"  Token 登入成功")
        else:
            client.login()
            token_path.parent.mkdir(exist_ok=True)
            client.garth.dump(str(token_path))
            log.info(f"  帳密登入成功，已儲存 token")
    except GarminConnectAuthenticationError:
        # Token 過期時重新登入
        client.login()
        token_path.parent.mkdir(exist_ok=True)
        client.garth.dump(str(token_path))
        log.info(f"  Token 已更新")
    except Exception:
        client.login()
        log.info(f"  帳密登入成功")

    return client


def fetch_data(email: str, password: str, date_str: str) -> dict:
    client = garmin_login(email, password)

    # 每日總覽（步數、距離、卡路里、活動時間、心率）
    stats = client.get_stats(date_str)

    steps        = stats.get("totalSteps", 0) or 0
    distance_m   = stats.get("totalDistance", 0) or 0
    calories     = stats.get("activeKilocalories", 0) or 0
    active_min   = round((stats.get("activeSeconds", 0) or 0) / 60)
    resting_hr   = stats.get("restingHeartRate", 0) or 0

    # 睡眠（秒 → 小時）
    sleep_hours = 0.0
    try:
        sleep = client.get_sleep_data(date_str)
        secs = sleep.get("dailySleepDTO", {}).get("sleepTimeSeconds", 0) or 0
        sleep_hours = round(secs / 3600, 1)
    except Exception:
        pass

    # 跑步距離（公里）
    run_km = 0.0
    try:
        activities = client.get_activities_by_date(date_str, date_str, "running")
        run_km = round(sum((a.get("distance", 0) or 0) for a in activities) / 1000, 2)
    except Exception:
        pass

    return {
        "steps":      steps,
        "distance_km": round(distance_m / 1000, 2),
        "calories":   calories,
        "active_min": active_min,
        "resting_hr": resting_hr,
        "sleep_h":    sleep_hours,
        "run_km":     run_km,
    }


# ── Google Sheets 寫入 ────────────────────────────────────────────────────────

HEADERS = ["日期", "姓名", "步數", "總距離(km)", "消耗卡路里",
           "活動時間(分)", "靜止心率", "睡眠(小時)", "跑步距離(km)"]


def get_sheet():
    import gspread
    from google.oauth2.service_account import Credentials

    creds_file = "credentials.json"
    if not Path(creds_file).exists():
        log.error("找不到 credentials.json，請依照腳本頂端說明完成 Google API 設定")
        sys.exit(1)

    creds = Credentials.from_service_account_file(
        creds_file,
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    gc = gspread.authorize(creds)

    sheet_id = os.getenv("SHEET_ID", "").strip()
    if not sheet_id:
        log.error(".env 裡沒有設定 SHEET_ID")
        sys.exit(1)

    sheet = gc.open_by_key(sheet_id).sheet1

    # 如果是空白表格，自動加標題列
    if sheet.row_count == 0 or not sheet.row_values(1):
        sheet.insert_row(HEADERS, 1)
        log.info("已建立標題列")

    return sheet


def already_synced(sheet, date_str: str, name: str) -> bool:
    """避免重複寫入同一天同一人的資料"""
    records = sheet.get_all_values()
    for row in records[1:]:
        if len(row) >= 2 and row[0] == date_str and row[1] == name:
            return True
    return False


def write_row(sheet, date_str: str, name: str, data: dict):
    row = [
        date_str,
        name,
        data["steps"],
        data["distance_km"],
        data["calories"],
        data["active_min"],
        data["resting_hr"],
        data["sleep_h"],
        data["run_km"],
    ]
    sheet.append_row(row, value_input_option="USER_ENTERED")


# ── 主流程 ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="同步 Garmin 資料到 Google Sheets")
    parser.add_argument("--date", default=datetime.date.today().strftime("%Y-%m-%d"),
                        help="指定日期，格式 YYYY-MM-DD（預設今天）")
    args = parser.parse_args()
    date_str = args.date

    log.info(f"同步日期：{date_str}")

    users = load_users()
    if not users:
        log.error(".env 裡沒有設定任何使用者（USER1_NAME / USER1_EMAIL / USER1_PASS）")
        sys.exit(1)

    sheet = get_sheet()

    for user in users:
        log.info(f"▶ {user['name']} ({user['email']})")
        try:
            if already_synced(sheet, date_str, user["name"]):
                log.info(f"  已有資料，略過")
                continue

            data = fetch_data(user["email"], user["password"], date_str)
            write_row(sheet, date_str, user["name"], data)

            log.info(
                f"  步數:{data['steps']:,}  跑步:{data['run_km']}km  "
                f"卡路里:{data['calories']}  睡眠:{data['sleep_h']}h  ✓ 已寫入"
            )
        except Exception as e:
            log.error(f"  失敗：{e}")

    log.info("完成")


if __name__ == "__main__":
    main()
