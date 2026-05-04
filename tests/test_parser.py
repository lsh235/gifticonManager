from app.parser import parse_dates


def test_parse_dates_multiple_formats():
    text = """
    유효기간: 2026년 5월 4일
    사용기한 2026/05/05
    만료일 26.05.06
    """
    got = parse_dates(text)
    assert "2026-05-04" in got
    assert "2026-05-05" in got
    assert "2026-05-06" in got


def test_parse_dates_invalid_filtered():
    text = "2026.02.31"
    got = parse_dates(text)
    assert got == []
