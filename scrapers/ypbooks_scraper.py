import requests
import json
import os
import sys
from datetime import datetime


def scrape_ypbooks_bestsellers(category_name: str, category_code: str):
    books = []

    now = datetime.now()
    year = now.year
    month = now.month

    def get_week_list(y, m):
        week_url = f"https://www.ypbooks.co.kr/back_shop/base_shop/api/v1/best-seller/bestsellerDateList?year={y}&month={m}"
        print(f"📅 week_url 요청 중: {week_url}")
        try:
            res = requests.get(week_url)
            return res.json().get("data", [])
        except:
            return []

    week_list = get_week_list(year, month)

    if not week_list:
        month -= 1
        if month == 0:
            month = 12
            year -= 1
        week_list = get_week_list(year, month)

        if not week_list:
            print("❌ 해당 월의 week 정보를 찾을 수 없습니다.")
            return

    max_week = max(item["week"] for item in week_list)

    url = (
        f"https://www.ypbooks.co.kr/back_shop/base_shop/api/v1/best-seller/bestCd/1/10"
        f"?year={year}&month={month}&week={max_week}"
        f"&searchDiv=W&outOfStock=y&categoryIdKey=&categoryBestCd={category_code}"
    )
    print(f"📘 도서 API 요청: {url}")

    try:
        response = requests.get(url)
        data = response.json()
        data_list = data.get("data", {}).get("dataList", [])
    except Exception as e:
        print(f"❌ 도서 API 요청 실패: {e}")
        return

    for item in data_list:
        try:
            book_info = item.get("bookProductInfo", {})
            item_id = item.get("productCd")
            book_link = (
                f"https://www.ypbooks.co.kr/books/{item_id}" if item_id else None
            )

            books.append(
                {
                    "title": book_info.get("bookTitle"),
                    "image": f"https://cdn.ypbooks.co.kr{book_info.get('bookImgPath')}/{book_info.get('bookImgName')}",
                    "author": book_info.get("sapWriterName"),
                    "publisher": book_info.get("pubCompanyName"),
                    "book_link": book_link,
                }
            )
            print(f"📚 수집 완료: {book_info.get('bookTitle')}")
        except Exception as e:
            print(f"⚠️ 개별 도서 처리 오류: {e}")
            continue

    try:
        # 절대 경로 기반으로 저장 경로 계산
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data_dir = os.path.join(project_root, f"{category_name}_data")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f"ypbooks_{category_name}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 저장 완료: {filename}")
    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python ypbooks_scraper.py [category_name] [category_code]")
        print("예시:  python ypbooks_scraper.py economics A006")
        sys.exit(1)

    category_name = sys.argv[1]
    category_code = sys.argv[2]

    scrape_ypbooks_bestsellers(category_name, category_code)
