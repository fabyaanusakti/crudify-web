from datetime import datetime
def parse_date(date_str):
    if not date_str:
        return None
    try:
        # indonesian time format
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    except ValueError:
        try:
            # ISO time format
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None