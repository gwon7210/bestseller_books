import subprocess
from datetime import datetime
import pytz
import os

# --- 알라딘 카테고리 목록: (카테고리이름, CID) ---
aladin_categories = [
    ("economics", "170"),
    ("essay", "55889"),
    ("hobbyHealth", "55890"),
    ("cooking&home", "1230"),
    ("coloringBooks", "114988"),
    ("handicraft", "53532"),
    ("webtoons", "7443"),
    ("art", "517"),
]

# --- 교보문고 카테고리 목록: (카테고리이름, clst_code) ---
kyobo_categories = [
    ("economics", "K"),
    ("essay", "C"),
    ("hobbyHealth", "L"),
    ("HomeLife", "H"),
    ("hobbies&sports", "R"),
    ("cooking", "a"),
    ("art", "Q"),
]

# --- 교보문고 카테고리별 베스트셀러 목록: (카테고리이름, clst_code) ---
kyobo_category_codes = [
    ("handicraft", "1103"),  # 취미/실용/스포츠 > 생활공예/DIY
    ("webtoons", "4724"),  # 만화 > 웹툰/카툰에세이
    ("coloringBooks", "230706"),  # 예술/대중문화 > 디자인/색채 > 컬러링북
]

# --- YES24 카테고리 목록: (카테고리이름, category_number) ---
yes24_categories = [
    ("economics", "001001025"),
    ("essay", "001001047"),
    ("hobbyHealth", "001001011"),
    ("home&housekeeping", "001001001"),
    ("coloringBooks", "001001007003011"),
    ("handicraft", "001001011016"),
    ("webtoons", "001001008020"),
    ("art", "001001007"),
]

# --- 영풍문고 카테고리 목록: (카테고리이름, categoryBestCd) ---
ypbooks_categories = [
    ("economics", "A006"),
    ("essay", "A004"),
    ("hobbyHealth", "A011"),
    ("health", "A021"),
    ("hobbies&leisure", "A022"),
    ("art", "A012"),
]

# --- 알라딘 실행 ---
print("\n========== 🛒 알라딘 스크래핑 시작 ==========")
for category_name, category_id in aladin_categories:
    print(f"\n🚀 실행 중: {category_name} (CID={category_id})")
    try:
        subprocess.run(
            ["python", "scrapers/aladin_scraper.py", category_name, category_id],
            check=True,
        )
        print(f"✅ 완료: {category_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {category_name}")
        print(e)

# --- 교보문고 실행 ---
print("\n========== 📚 교보문고 스크래핑 시작 ==========")
for category_name, clst_code in kyobo_categories:
    print(f"\n🚀 실행 중: {category_name} (코드={clst_code})")
    try:
        subprocess.run(
            ["python", "scrapers/kyobo_scraper.py", category_name, clst_code],
            check=True,
        )
        print(f"✅ 완료: {category_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {category_name}")
        print(e)

# --- 교보문고 카테고리별 베스트셀러 실행 ---
print("\n========== 📚 교보문고 카테고리별 베스트셀러 스크래핑 시작 ==========")
for category_name, clst_code in kyobo_category_codes:
    print(f"\n🚀 실행 중: {category_name} (코드={clst_code})")
    try:
        subprocess.run(
            ["python", "scrapers/kyobo_category_scraper.py", category_name, clst_code],
            check=True,
        )
        print(f"✅ 완료: {category_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {category_name}")
        print(e)

# --- YES24 실행 ---
print("\n========== 🧾 YES24 스크래핑 시작 ==========")
for category_name, category_number in yes24_categories:
    print(f"\n🚀 실행 중: {category_name} (카테고리 번호={category_number})")
    try:
        subprocess.run(
            ["python", "scrapers/yes24_scraper.py", category_name, category_number],
            check=True,
        )
        print(f"✅ 완료: {category_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {category_name}")
        print(e)

# --- 영풍문고 실행 ---
print("\n========== 🟩 영풍문고 스크래핑 시작 ==========")
for category_name, category_code in ypbooks_categories:
    print(f"\n🚀 실행 중: {category_name} (categoryBestCd={category_code})")
    try:
        subprocess.run(
            ["python", "scrapers/ypbooks_scraper.py", category_name, category_code],
            check=True,
        )
        print(f"✅ 완료: {category_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {category_name}")
        print(e)


# --- index.html 최근 업데이트 날짜 표시 ---
def update_index_html():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("index.html 파일이 없습니다.")
        return

    kst = pytz.timezone("Asia/Seoul")
    now = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
    update_line = (
        f'<div style="font-size:12px; color:gray;">최근 업데이트: {now}</div>\n'
    )

    # 기존에 이미 업데이트 표시가 있다면 교체, 없으면 맨 위에 추가
    if lines and "최근 업데이트:" in lines[0]:
        lines[0] = update_line
    else:
        lines = [update_line] + lines

    with open("index.html", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("📅 index.html 최근 업데이트 시간 갱신 완료")


update_index_html()
