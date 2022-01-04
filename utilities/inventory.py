import csv

from utilities.store_properties import get_today
from utilities.utilities import get_expiry_date
from random import randint
from datetime import date

from rich.console import Console
from rich.table import Table
from rich import print


def show_inventory(date: date = get_today()):
    try:
        with open(f"./inventories/{date}.csv", newline="", mode="r") as f:
            products = list(csv.DictReader(f))
    except FileNotFoundError:
        print(
            "\n [red]Warning:[/red] No inventory data exists for this day. Try restocking the store using [italic purple]'restock'[/italic purple].\n"
        )
        return

    console = Console()

    print("\n")
    table = Table(show_header=True, header_style="bold", title=f"Inventory for {date}")
    table.add_column("Id", style="dim")
    table.add_column("Product name")
    table.add_column("Amount", justify="right")
    table.add_column("Department")
    table.add_column("Selling price", justify="right")
    table.add_column("Expiry date")

    for product in products:
        table.add_row(
            product["id"],
            product["product name"],
            product["amount"],
            product["department"],
            product["selling price"],
            ("[red]" + product["expiry date"] + "[/red]")
            if product["expiry date"] == get_today()
            else product["expiry date"],
        )

    console.print(table, justify="center")
    print("\n")


def write_to_stock(new_stock: list[dict], date: str | None):
    if date is None:
        write_date = get_today()
    else:
        write_date = date
    new_stock = sorted(new_stock, key=lambda x: x["department"])
    with open(f"./inventories/{write_date}.csv", mode="w", newline="") as g:
        fieldnames = [
            "id",
            "product id",
            "product name",
            "amount",
            "department",
            "buying price",
            "selling price",
            "expiry date",
        ]
        csv_writer = csv.DictWriter(g, fieldnames=fieldnames, extrasaction="ignore")

        g.seek(0)
        csv_writer.writeheader()
        id = 1
        seen_products = []
        for item in new_stock:
            item["id"] = str(id)
            if item not in seen_products:
                csv_writer.writerow(item)
                seen_products.append(item)
                id += 1
        g.truncate()


def restock(amount: int = 50, date: str = get_today()):
    date = get_today() if date is None else date
    with open("./products.csv", newline="", mode="r") as f:
        products = list(csv.DictReader(f))

    new_stock = []
    for i in range(0, amount):
        random_index = randint(0, len(products) - 1)
        new_stock.append(products[random_index])

    for item in new_stock:
        item["expiry date"] = str(get_expiry_date(int(item["shelf-life"])))
        item["amount"] = str(new_stock.count(item))

        # The store increases the price with 10% on every item.
        item["selling price"] = "{:.2f}".format(
            round(float(item["buying price"]) * float(1.10), 2)
        )

    write_to_stock(new_stock=new_stock, date=date)
    if date == get_today():
        print(
            f"\n [yellow]Notification:[/yellow] today's inventory has been refilled with [cyan]{len(new_stock)}[/cyan] new items.\n"
        )
    else:
        print(
            f"\n [yellow]Notification:[/yellow] the inventory of [cyan]{date}[/cyan] has been refilled with [cyan]{len(new_stock)}[/cyan] new items.\n"
        )
