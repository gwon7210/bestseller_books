import requests
from bs4 import BeautifulSoup
import json
import os
import re
import sys


def scrape_yes24_bestsellers(category_name: str, category_number: str):
    books = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    url = (
        f"https://www.yes24.com/product/category/monthweekbestseller?"
        f"pageNumber=1&pageSize=24&categoryNumber={category_number}&"
        f"type=week&saleYear=2025"
    )

    try:
        print(f"📦 예스24 '{category_name}' 베스트셀러 수집 시작...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        book_items = soup.select("div.itemUnit")[:10]  # 상위 10개만

        for item in book_items:
            try:
                img_tag = item.select_one("img.lazy")
                img = img_tag.get("data-original") or img_tag.get("src", "")
                if not img.startswith("http"):
                    img = "https:" + img

                title = img_tag.get("alt", "").strip()

                author_tag = item.select_one('a[href*="author"]')
                author = author_tag.text.strip() if author_tag else "정보 없음"

                publisher_tag = item.select_one('a[href*="company"]')
                publisher = publisher_tag.text.strip() if publisher_tag else "정보 없음"

                price_element = item.select_one("span.txt_num em.yes_m")
                price = (
                    price_element.text.strip().replace(",", "")
                    if price_element
                    else "0"
                )

                release_date_element = item.select_one("span.info_date")
                release_date = (
                    release_date_element.text.strip()
                    if release_date_element
                    else "정보 없음"
                )

                sales_element = item.select_one("span.saleNum")
                sales_index = (
                    sales_element.text.strip().replace("판매지수 ", "").replace(",", "")
                    if sales_element
                    else "0"
                )

                match = re.search(r"/goods/(\d+)", img)
                goods_id = match.group(1) if match else ""
                book_link = (
                    f"https://www.yes24.com/product/goods/{goods_id}"
                    if goods_id
                    else ""
                )

                book_info = {
                    "img": img,
                    "title": title,
                    "author": author,
                    "publisher": publisher,
                    "price": price,
                    "release_date": release_date,
                    "sales_index": sales_index,
                    "book_link": book_link,
                }

                books.append(book_info)
                print(f"📚 수집 완료: {title}")

            except Exception as e:
                print(f"⚠️ 개별 도서 오류: {e}")
                continue

    except Exception as e:
        print(f"❌ 페이지 오류: {e}")

    try:
        # 프로젝트 루트 기준으로 디렉터리 설정
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data_dir = os.path.join(project_root, f"{category_name}_data")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f"yes24_{category_name}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        print(f"✅ 총 {len(books)}권 수집 완료 → {filename}")

    except Exception as e:
        print(f"❌ 파일 저장 오류: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python yes24_scraper.py [category_name] [category_number]")
        print("예시:  python yes24_scraper.py economics 001001025")
        sys.exit(1)

    category_name = sys.argv[1]
    category_number = sys.argv[2]

    scrape_yes24_bestsellers(category_name, category_number)
