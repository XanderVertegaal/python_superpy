from datetime import date, timedelta


def get_expiry_date(shelf_life: int) -> date:
    with open("./today.txt", mode="r") as f:
        today = date.fromisoformat(f.read())

    expiry_date = today + timedelta(days=shelf_life)
    return expiry_date
