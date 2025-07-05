import requests
import json
import os
from datetime import datetime

# 여성 취미

# 오늘 연도와 달 구하기
now = datetime.now()
year = now.year
month = now.month

# 1. week 리스트 조회 (첫 번째 시도)
week_url = f"https://www.ypbooks.co.kr/back_shop/base_shop/api/v1/best-seller/bestsellerDateList?year={year}&month={month}"
print(f"week_url: {week_url}")

week_response = requests.get(week_url)
week_data = week_response.json()

# 2. 가장 큰 week 값 찾기
week_list = week_data.get("data", [])
if not week_list:
    # 한 번만 month 값을 -1 해서 다시 시도
    month -= 1
    if month == 0:
        month = 12
        year -= 1
    
    week_url = f"https://www.ypbooks.co.kr/back_shop/base_shop/api/v1/best-seller/bestsellerDateList?year={year}&month={month}"
    print(f"재시도 week_url: {week_url}")
    
    week_response = requests.get(week_url)
    week_data = week_response.json()
    
    week_list = week_data.get("data", [])
    if not week_list:
        raise Exception("해당 월의 week 정보를 찾을 수 없습니다.")
max_week = max(item["week"] for item in week_list)

# 3. 책 리스트 API 호출
url = f"https://www.ypbooks.co.kr/back_shop/base_shop/api/v1/best-seller/bestCd/1/10?year={year}&month={month}&week={max_week}&searchDiv=W&outOfStock=y&categoryIdKey=&categoryBestCd=A006"
response = requests.get(url)
data = response.json()

# 책 리스트 추출
data_list = data.get("data", {}).get("dataList", [])

books = []

for item in data_list:
    book_info = item.get("bookProductInfo", {})
    item_id = item.get("productCd")  # 예: 202410035877967910
    book_link = f"https://www.ypbooks.co.kr/books/{item_id}" if item_id else None
    books.append(
        {
            "title": book_info.get("bookTitle"),
            "image": f"https://cdn.ypbooks.co.kr{book_info.get('bookImgPath')}/{book_info.get('bookImgName')}",
            "author": book_info.get("sapWriterName"),
            "publisher": book_info.get("pubCompanyName"),
            "book_link": book_link,
        }
    )

# economics_data 폴더에 저장
data_dir = "../economics_data"
os.makedirs(data_dir, exist_ok=True)
filename = os.path.join(data_dir, "ypbooks_economics.json")
with open(filename, "w", encoding="utf-8") as f:
    json.dump(books, f, ensure_ascii=False, indent=2)

print(f"✅ JSON 저장 완료: {filename}")
