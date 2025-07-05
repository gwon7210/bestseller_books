import requests
from bs4 import BeautifulSoup
import json
import os
import re


# 건강/취미 > 공예
def scrape_aladin_bestsellers():
    """
    알라딘 건강/취미 > 공예 베스트셀러 페이지에서 상위 10개 도서 정보를 스크래핑합니다.
    """
    url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=53532"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = "utf-8"

        soup = BeautifulSoup(response.text, "html.parser")

        bestseller_items = soup.find_all("div", class_="ss_book_box")[:10]

        books = []

        for item in bestseller_items:
            try:
                img_tag = item.find("img", class_="front_cover")
                image_url = img_tag["src"] if img_tag else ""

                title_tag = item.find("a", class_="bo3")
                title = title_tag.get_text(strip=True) if title_tag else ""

                subtitle_tag = item.find("span", class_="ss_f_g2")
                subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else ""

                category_tag = item.find("span", class_="tit_category")
                category = category_tag.get_text(strip=True) if category_tag else ""

                book_link = title_tag["href"] if title_tag else ""
                if book_link and not book_link.startswith("http"):
                    book_link = "https://www.aladin.co.kr" + book_link

                price_info = {}
                price_li = None
                for li in item.find_all("li"):
                    if "원" in li.get_text():
                        price_li = li
                        break
                if price_li:
                    spans = price_li.find_all("span")
                    if len(spans) > 0 and not spans[0].get("class"):
                        price_info["original_price"] = (
                            spans[0].get_text(strip=True) + "원"
                        )
                    discount_span = price_li.find("span", class_="ss_p2")
                    if discount_span and discount_span.find("em"):
                        price_info["discount_price"] = discount_span.find(
                            "em"
                        ).get_text(strip=True)
                    ss_p_spans = price_li.find_all("span", class_="ss_p")
                    for s in ss_p_spans:
                        txt = s.get_text(strip=True)
                        if "%" in txt:
                            price_info["discount_rate"] = txt
                        elif txt.replace(",", "").isdigit():
                            price_info["mileage"] = txt + "원"

                sales_point_tag = item.find("span", class_="sales_point")
                sales_point = (
                    sales_point_tag.get_text(strip=True) if sales_point_tag else ""
                )

                authors, translators, publisher, publish_date = [], [], "", ""
                for li in item.find_all("li"):
                    li_text = li.get_text()
                    for a in li.find_all("a"):
                        href = a.get("href", "")
                        name = a.get_text(strip=True)
                        if "AuthorSearch" in href:
                            if "(지은이)" in li_text and name not in authors:
                                authors.append(name)
                            elif "(옮긴이)" in li_text and name not in translators:
                                translators.append(name)
                        elif "PublisherSearch" in href:
                            publisher = name
                    date_match = re.search(r"(\d{4}년\s*\d{1,2}월)", li_text)
                    if date_match:
                        publish_date = date_match.group(1)

                book_info = {
                    "rank": len(books) + 1,
                    "title": title,
                    "author": ", ".join(authors),
                    "publisher": publisher,
                    "sales_point": sales_point,
                    "release_date": publish_date,
                    "category": category,
                    "img": image_url,
                    "book_link": book_link,
                }
                if price_info.get("original_price"):
                    book_info["price"] = price_info["original_price"]
                if price_info.get("discount_price"):
                    book_info["discount_price"] = price_info["discount_price"]
                if price_info.get("discount_rate"):
                    book_info["discount_rate"] = price_info["discount_rate"]
                if price_info.get("mileage"):
                    book_info["mileage"] = price_info["mileage"]
                books.append(book_info)

            except Exception as e:
                print(f"도서 정보 추출 중 오류 발생: {e}")
                continue

        # handicraft_data 폴더에 저장
        data_dir = "../handicraft_data"
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, "aladin_handicraft.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)

        print(
            f"알라딘 베스트셀러 상위 {len(books)}개 도서 정보를 {filename}에 저장했습니다."
        )
        return books

    except requests.RequestException as e:
        print(f"페이지 요청 중 오류 발생: {e}")
        return None
    except Exception as e:
        print(f"스크래핑 중 오류 발생: {e}")
        return None


if __name__ == "__main__":
    print("알라딘 베스트셀러 스크래핑을 시작합니다...")
    result = scrape_aladin_bestsellers()

    if result:
        print("\n=== 스크래핑 결과 ===")
        for book in result:
            print(f"\n{book['rank']}위: {book['title']}")
            print(f"저자: {book['author']}")
            print(f"출판사: {book['publisher']}")
            print(f"판매지수: {book['sales_point']}")
            if "price" in book and book["price"]:
                print(f"가격: {book['price']}")
            if "discount_price" in book and book["discount_price"]:
                print(f"할인가: {book['discount_price']}")
            if "discount_rate" in book and book["discount_rate"]:
                print(f"할인율: {book['discount_rate']}")
            if "mileage" in book and book["mileage"]:
                print(f"마일리지: {book['mileage']}")
    else:
        print("스크래핑에 실패했습니다.")
