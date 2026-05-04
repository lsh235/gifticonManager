# Gifticon Manager (Image-based)

이미지 기반 기프티콘을 등록하면 OCR로 문구를 추출하고, 다양한 날짜 형식을 파싱해 저장하는 예제 앱입니다.

## 핵심 기능
- 이미지 업로드
- OCR 텍스트 추출 (`pytesseract`)
- 다중 형식 날짜 파싱 (정규식 + `dateutil` fallback)
- 추출된 텍스트/날짜를 SQLite에 저장

## 실행
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API
### `POST /gifticons`
multipart form-data:
- `image`: 이미지 파일

응답:
- `raw_text`: OCR 전체 문구
- `parsed_dates`: 파싱된 날짜 목록 (ISO 8601)
- `id`: 저장된 기프티콘 id

## 설계 요약
1. OCR 단계: 이미지 전처리(그레이스케일 + threshold) 후 텍스트 추출
2. 날짜 파싱 단계:
   - 한글/숫자 패턴(예: `2026년 5월 4일`, `26.05.04`, `2026/05/04`, `2026-5-4`) 우선 탐지
   - 기간 표기(예: `~ 2026.05.04`)에서도 날짜 토큰 추출
   - 중복 제거 및 현실 범위 검증
   - 보조적으로 `dateutil` fuzzy 파싱
3. 저장 단계: 추출문/원본경로/파싱일자 목록 저장

## 향후 확장
- 브랜드별 템플릿 기반 정확도 향상
- 만료일/발행일 분류 모델 추가
- 모바일 앱/웹 프론트 연동
