import subprocess
import os
from datetime import datetime
import pytz

scripts = [
    "essay/scrape_aladin_essay.py",
    "essay/scrape_kyobo_essay.py",
    "essay/scrape_yes24_essay.py",
    "essay/scrape_ypbooks_essay.py",
    "hobbyHealth/scrape_aladin_hobbyHealth.py",
    "hobbyHealth/scrape_kyobo_hobbyHealth.py",
    "hobbyHealth/scrape_yes24_hobbyHealth.py",
    "hobbyHealth/scrape_ypbooks_hobbyHealth.py",
    "economics/scrape_aladin_economics.py",
    "economics/scrape_kyobo_economics.py",
    "economics/scrape_yes24_economics.py",
    "economics/scrape_ypbooks_economics.py",
    "coloringBooks/scrape_aladin_coloringBooks.py",
    "coloringBooks/scrape_yes24_coloringBooks.py",
    "handicraft/scrape_aladin_handicraft.py",
    "handicraft/scrape_yes24_handicraft.py",
    "webtoons/scrape_aladin_webtoons.py",
    "webtoons/scrape_yes24_webtoons.py",
]

for script in scripts:
    print(f"\n🚀 실행 중: {script}")
    try:
        script_dir = os.path.dirname(script) or "."
        subprocess.run(
            ["python", os.path.basename(script)],
            cwd=script_dir,  # ✅ 해당 디렉토리로 이동해서 실행
            check=True,
        )
        print(f"✅ 완료: {script}")
    except subprocess.CalledProcessError as e:
        print(f"❌ 오류 발생: {script}")
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


update_index_html()
