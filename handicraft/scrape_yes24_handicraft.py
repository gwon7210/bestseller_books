import requests
from bs4 import BeautifulSoup
import json
import os
import re


# 건강취미 > 공예
def scrape_yes24_bestsellers():
    books = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    url = "https://www.yes24.com/product/category/monthweekbestseller?pageNumber=1&pageSize=24&categoryNumber=001001011016&type=week&saleYear=2025"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        book_items = soup.select("div.itemUnit")[:10]  # 상위 10개만 선택

        for item in book_items:
            try:
                # 이미지 URL
                img_tag = item.select_one("img.lazy")
                img = img_tag.get("data-original") or img_tag.get("src", "")
                if not img.startswith("http"):
                    img = "https:" + img

                # 제목
                title = img_tag.get("alt", "").strip()

                # 저자
                author_tag = item.select_one('a[href*="author"]')
                author = author_tag.text.strip() if author_tag else "정보 없음"

                # 출판사
                publisher_tag = item.select_one('a[href*="company"]')
                publisher = publisher_tag.text.strip() if publisher_tag else "정보 없음"

                # 가격
                price_element = item.select_one("span.txt_num em.yes_m")
                price = (
                    price_element.text.strip().replace(",", "")
                    if price_element
                    else "0"
                )

                # 출간일
                release_date_element = item.select_one("span.info_date")
                release_date = (
                    release_date_element.text.strip()
                    if release_date_element
                    else "정보 없음"
                )

                # 판매지수
                sales_element = item.select_one("span.saleNum")
                sales_index = (
                    sales_element.text.strip().replace("판매지수 ", "").replace(",", "")
                    if sales_element
                    else "0"
                )

                # 이미지에서 상품 ID 추출 → book_link 생성
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
                print(f"수집 완료: {title}")

            except Exception as e:
                print(f"개별 도서 처리 중 오류 발생: {e}")
                continue

    except Exception as e:
        print(f"페이지 처리 중 오류 발생: {e}")

    # handicraft_data 폴더에 저장
    data_dir = "../handicraft_data"
    os.makedirs(data_dir, exist_ok=True)
    filename = os.path.join(data_dir, "yes24_handicraft.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    print(f"총 {len(books)}개의 도서 정보를 수집하여 {filename}에 저장했습니다.")


if __name__ == "__main__":
    scrape_yes24_bestsellers()
