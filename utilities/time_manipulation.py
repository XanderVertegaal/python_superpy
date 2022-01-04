from datetime import date, datetime
from rich import print


def get_today(show: bool = False) -> date:
    with open("./today.txt", mode="r+") as f:
        today = str(f.read())
        date_object = datetime.strptime(today, "%Y-%m-%d")
        day = date_object.strftime('%A')
    print(f"\n [yellow]Notification:[/yellow] today's date is [cyan]{today}[/cyan], which is a [blue]{day}[/blue].\n") if show else None
    return today


def set_today(new_date: str | None = None) -> None:
    if new_date is None:
        new_date = date.today()
        print("\n [yellow]Notification:[/yellow] resetting today to the system's current time.")
    else:
        try:
            valid_date = datetime.strptime(str(new_date), "%Y-%m-%d")
        except:
            print("\n [red]Warning:[/red] the date you entered was not valid. Provide a date in the format YYYY-MM-DD.")
            return
        print(f'\n [yellow]Notification:[/yellow] resetting today to [cyan]{new_date}[/cyan].')

    with open("./today.txt", mode="r+") as f:
        f.seek(0)
        f.write(str(new_date))
        f.truncate()
