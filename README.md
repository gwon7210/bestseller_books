# 온라인 서점 베스트셀러 스크래퍼

Yes24와 교보문고의 베스트셀러 정보를 수집하는 파이썬 스크립트입니다.

## 기능

### Yes24 스크래퍼 (`scrape_yes24.py`)
- Yes24의 주간 베스트셀러 상위 5개의 도서 정보를 수집
- 수집 정보: 이미지 URL, 제목, 저자, 출판사, 가격, 출간일, 판매지수
- 수집된 정보는 `yes24_weekly_bestsellers.json` 파일로 저장

### 교보문고 스크래퍼 (`scrape_kyobo.py`)
- 교보문고의 베스트셀러 상위 5개의 도서 정보를 수집
- 수집 정보: 이미지 URL, 제목, 저자, 출판사, 가격, 출간일
- 수집된 정보는 `kyobo_bestsellers.json` 파일로 저장

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 사용 방법

Yes24 스크래퍼 실행:
```bash
python scrape_yes24.py
```

교보문고 스크래퍼 실행:
```bash
python scrape_kyobo.py
```

## 주의사항

- 웹사이트의 구조가 변경될 경우 스크립트가 정상적으로 동작하지 않을 수 있습니다
- 스크래핑 시 서버에 부하를 주지 않도록 주의해주세요# bestseller_books
