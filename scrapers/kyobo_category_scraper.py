import requests
import json
import time
import os
import sys


def scrape_kyobo_category_bestsellers(category_name: str, clst_code: str):
    books = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json",
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
        "Referer": "https://product.kyobobook.co.kr/",
        "Origin": "https://product.kyobobook.co.kr",
    }

    url = "https://product.kyobobook.co.kr/api/gw/best/best-seller/online"
    params = {
        "page": 1,
        "per": 20,
        "saleCmdtDvsnCode": "KOR",
        "saleCmdtClstCode": clst_code,
        "isEvent": "false",
        "isPackage": "false",
        "isMDPicked": "false",
        "saleCmdtDsplDvsnCode": "KOR",
        "period": "002",
        "dsplDvsnCode": "001",
        "dsplTrgtDvsnCode": "004",
    }

    try:
        print(f"📦 교보문고 '{category_name}' 베스트셀러 수집 시작...")
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("data") and "bestSeller" in data["data"]:
            bestseller_list = data["data"]["bestSeller"]

            for book in bestseller_list:
                try:
                    release_date = book.get("rlseDate", "")
                    if release_date and len(release_date) == 8:
                        year = release_date[:4]
                        month = release_date[4:6]
                        formatted_date = f"{year}년 {month}월"
                    else:
                        formatted_date = "정보 없음"

                    book_info = {
                        "img": f"https://contents.kyobobook.co.kr/sih/fit-in/100x151/pdt/{book.get('cmdtCode', '')}.jpg",
                        "title": book.get("cmdtName", "제목 없음"),
                        "author": book.get("chrcName", "저자 정보 없음"),
                        "publisher": book.get("pbcmName", "출판사 정보 없음"),
                        "price": str(int(book.get("price", 0))),
                        "release_date": formatted_date,
                        "rank": book.get("prstRnkn", 0),
                        "category": book.get("saleCmdtClstName", "분류 없음"),
                        "discount_rate": book.get("dscnRate", 0),
                        "rating": book.get("buyRevwRvgr", 0.0),
                        "review_count": book.get("buyRevwNumc", 0),
                        "book_link": f"https://product.kyobobook.co.kr/detail/{book.get('saleCmdtid', '')}",
                    }

                    books.append(book_info)
                    print(f"📚 수집 완료: {book_info['rank']}위 - {book_info['title']}")
                    time.sleep(0.1)  # 과도한 요청 방지

                except Exception as e:
                    print(f"⚠️ 개별 도서 처리 중 오류: {e}")
                    continue

            print(f"\n✅ 총 {len(books)}권 수집 완료")

        else:
            print(f"❌ API 응답 오류: 데이터가 없습니다")

    except requests.exceptions.RequestException as e:
        print(f"❌ 네트워크 오류: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
    except Exception as e:
        print(f"❌ 예외 발생: {e}")

    try:
        # 프로젝트 루트 기준 경로 설정
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data_dir = os.path.join(project_root, f"{category_name}_data")
        os.makedirs(data_dir, exist_ok=True)
        filename = os.path.join(data_dir, f"kyobo_{category_name}.json")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f"📁 저장 완료: {filename}")
    except Exception as e:
        print(f"❌ 파일 저장 중 오류: {e}")

    return books


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python kyobo_category_scraper.py [category_name] [clst_code]")
        print("예시:  python kyobo_category_scraper.py handicraft 1103")
        sys.exit(1)

    category_name = sys.argv[1]
    clst_code = sys.argv[2]

    scrape_kyobo_category_bestsellers(category_name, clst_code)
