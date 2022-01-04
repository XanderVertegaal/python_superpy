import csv
from datetime import datetime

from utilities.time_manipulation import get_today
from rich import print
from rich.console import Console
from rich.table import Table


def check_manager(date: str = get_today(), show: bool = False):
    date_object = datetime.strptime(date, "%Y-%m-%d")
    day = date_object.strftime('%A')
    with open('employees.csv', mode="r") as f:
        employees = csv.DictReader(f)
        manager = next(
            (
                item for item in employees if item["day"] == day
            ), None
        )

    if show is True and manager is None:
        print(f'\n [yellow]Notification:[/yellow] the shop is closed on [blue]Sunday[/blue], so there is no manager on duty today. Try again tomorrow.\n')
    elif show is True:
        print(f"\n  [yellow]Notification:[/yellow] today's manager is [bright_yellow]{manager['name']}[/bright_yellow].\n")

    return manager


def show_products():
    try:
        with open('./products.csv', newline='', mode='r') as f:
            products = list(csv.DictReader(f))
    except FileNotFoundError:
        print('\n [red]Warning:[/red] list of products cannot be found. Check if [italic]products.csv[/italic] exists.\n')
        return

    console = Console()

    print('\n')
    table = Table(
        show_header=True,
        header_style='bold',
        title=f"Product overview"
    )
    table.add_column("Id", style="dim")
    table.add_column("Product name")
    table.add_column("Department")
    table.add_column("Buying price", justify="right")
    table.add_column("shelf-life")

    id = 1
    for product in products:
        table.add_row(
            str(id),
            product['product name'],
            product['department'],
            product['buying price'],
            product['shelf-life']
        )
        id += 1

    console.print(table, justify='center')
    print('\n')
    