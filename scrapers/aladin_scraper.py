import requests
from bs4 import BeautifulSoup
import json
import os
import re
import sys


def fetch_page(url, headers):
    try:
        print(f"🌐 [요청 시작] {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print("✅ [응답 수신 완료]")
        response.raise_for_status()
        response.encoding = "utf-8"
        return response.text
    except requests.RequestException as e:
        print(f"❌ 페이지 요청 중 오류 발생: {e}")
        return None


def extract_price_info(item):
    price_info = {}
    for li in item.find_all("li"):
        if "원" not in li.get_text():
            continue

        spans = li.find_all("span")
        if spans and not spans[0].get("class"):
            price_info["original_price"] = spans[0].get_text(strip=True) + "원"

        discount_span = li.find("span", class_="ss_p2")
        if discount_span and discount_span.find("em"):
            price_info["discount_price"] = discount_span.find("em").get_text(strip=True)

        for s in li.find_all("span", class_="ss_p"):
            txt = s.get_text(strip=True)
            if "%" in txt:
                price_info["discount_rate"] = txt
            elif txt.replace(",", "").isdigit():
                price_info["mileage"] = txt + "원"
        break

    return price_info


def extract_book_info(item, rank):
    try:
        title_tag = item.find("a", class_="bo3")
        title = title_tag.get_text(strip=True) if title_tag else ""
        book_link = title_tag["href"] if title_tag else ""
        if book_link and not book_link.startswith("http"):
            book_link = "https://www.aladin.co.kr" + book_link

        authors, translators, publisher, publish_date = [], [], "", ""
        for li in item.find_all("li"):
            li_text = li.get_text()
            for a in li.find_all("a"):
                href = a.get("href", "")
                name = a.get_text(strip=True)
                if "AuthorSearch" in href:
                    if "(지은이)" in li_text:
                        authors.append(name)
                    elif "(옮긴이)" in li_text:
                        translators.append(name)
                elif "PublisherSearch" in href:
                    publisher = name
            date_match = re.search(r"(\d{4}년\s*\d{1,2}월)", li_text)
            if date_match:
                publish_date = date_match.group(1)

        price_info = extract_price_info(item)

        return {
            "rank": rank,
            "title": title,
            "author": ", ".join(authors),
            "publisher": publisher,
            "release_date": publish_date,
            "category": (
                item.find("span", class_="tit_category").get_text(strip=True)
                if item.find("span", class_="tit_category")
                else ""
            ),
            "sales_point": (
                item.find("span", class_="sales_point").get_text(strip=True)
                if item.find("span", class_="sales_point")
                else ""
            ),
            "img": (
                item.find("img", class_="front_cover")["src"]
                if item.find("img", class_="front_cover")
                else ""
            ),
            "book_link": book_link,
            "price": price_info.get("original_price"),
            "discount_price": price_info.get("discount_price"),
            "discount_rate": price_info.get("discount_rate"),
            "mileage": price_info.get("mileage"),
        }

    except Exception as e:
        print(f"{rank}위 도서 정보 추출 오류: {e}")
        return None


def scrape_aladin(category_name, category_id):
    url = f"https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID={category_id}"
    headers = {"User-Agent": "Mozilla/5.0"}

    print(f"\n🔍 [스크래핑 시작] {category_name} (CID={category_id})")
    html = fetch_page(url, headers)

    if not html:
        print("⚠️ HTML 응답 없음. 종료.")
        return

    print("📦 [HTML 파싱 시작]")
    soup = BeautifulSoup(html, "html.parser")

    print("📚 [도서 목록 추출]")
    items = soup.find_all("div", class_="ss_book_box")[:10]
    print(f"✅ 도서 {len(items)}권 감지됨")

    books = []
    for idx, item in enumerate(items, start=1):
        print(f"🔎 [{idx}위] 도서 정보 추출 중...")
        book_info = extract_book_info(item, idx)
        if book_info:
            books.append(book_info)
        else:
            print(f"⚠️ [{idx}위] 도서 추출 실패")

    # 프로젝트 루트 기준으로 저장 디렉토리 설정
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(project_root, f"{category_name}_data")
    os.makedirs(data_dir, exist_ok=True)
    output_file = os.path.join(data_dir, f"aladin_{category_name}.json")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

    print(f"✅ {category_name} 저장 완료: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python aladin_scraper.py [category_name] [category_id]")
        print("예시:  python aladin_scraper.py economics 170")
        sys.exit(1)

    category_name = sys.argv[1]
    category_id = sys.argv[2]
    scrape_aladin(category_name, category_id)
