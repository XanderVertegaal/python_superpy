import csv
from datetime import date, timedelta
from random import randint
from utilities.time_manipulation import get_today, set_today
from utilities.inventory import write_to_stock

from rich.console import Console
from rich.table import Table
from rich import print


def show_report(date: date = get_today()):
    try:
        with open(f"./reports/{date}.csv", newline="", mode="r") as f:
            products = list(csv.DictReader(f))
    except FileNotFoundError:
        print(
            "\n [red]Warning:[/red]: no report exists for this day. Try buying or selling some items from our shop first (if it is open today) or create a random report with [italic purple]'fabricate_report'[/italic purple].\n"
        )
        return

    console = Console()

    print('\n')
    table = Table(
        show_header=True,
        header_style="bold",
        title=f"Report for {date}"
    )
    table.add_column("Id", style="dim")
    table.add_column("Product name")
    table.add_column("Amount", justify='right')
    table.add_column("Department")
    table.add_column('Buying price', justify='right')
    table.add_column("Selling price", justify="right")
    table.add_column("Status")

    status_dict = {
        'bought': 'cyan',
        'sold': 'green',
        'expired': 'magenta'
    }

    for product in products:

        table.add_row(
            product["id"],
            product["product name"],
            product["amount"],
            product["department"],
            product['buying price'],
            product["selling price"],
            f"[{status_dict[product['status']]}]{product['status']}[/{status_dict[product['status']]}]"
        )

    console.print(table, justify='center')
    print('\n')


def write_to_report(
    product: dict,
    status: str,
    amount: int = 1,
    date: date = get_today()
):
    try:
        with open(f"./reports/{date}.csv", mode="r", newline="") as f:
            existing_contents = list(csv.DictReader(f))
    except FileNotFoundError:
        existing_contents = []

    fieldnames = [
                "id",
                "product id",
                "product name",
                "amount",
                "department",
                "buying price",
                "selling price",
                "status",
            ]
    with open(f"./reports/{date}.csv", mode="w", newline="") as g:
        csv_writer = csv.DictWriter(
            g,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )
        existing = next(
            (
                item
                for item in existing_contents
                if item["product name"] == product["product name"]
                and round(float(item["buying price"]), 2)
                == round(float(product["buying price"]), 2)
                and item["selling price"] == product["selling price"]
                and item["status"] == status
            ),
            None,
        )

        if existing is None:
            product["status"] = status
            product["amount"] = amount
            existing_contents.append(product)
        else:
            existing["amount"] = int(existing["amount"]) + int(amount)

        existing_contents = sorted(
            existing_contents,
            key=lambda x: x["department"]
        )
        g.seek(0)
        g.truncate(0)
        id = 1
        csv_writer.writeheader()
        for item in existing_contents:
            item["id"] = id
            item['buying price'] = "{:.2f}".format(float(item['buying price']))
            csv_writer.writerow(item)
            id += 1


def fabricate_report(amount: int = 50, date: str = get_today()):
    with open("./products.csv", newline="", mode="r") as f:
        products = list(csv.DictReader(f))

    new_stock = []
    for i in range(0, amount):
        random_product = randint(0, len(products) - 1)
        random_status = randint(0, 2)
        statuses = ["sold", "expired", "bought"]
        new_item = products[random_product]
        new_item["status"] = statuses[random_status]
        new_item["selling price"] = "{:.2f}".format(
            round(1.1 * float(new_item["buying price"]), 2)
        )
        new_stock.append(new_item)
    new_stock = sorted(new_stock, key=lambda x: x["department"])

    with open(f"./reports/{date}.csv", newline="", mode="w") as g:
        fieldnames = [
            "id",
            "product id",
            "product name",
            "amount",
            "department",
            "buying price",
            "selling price",
            "status",
        ]
        csv_writer = csv.DictWriter(
            g,
            fieldnames=fieldnames,
            extrasaction="ignore"
        )

        g.seek(0)
        csv_writer.writeheader()
        id = 1
        seen_products = []
        for item in new_stock:
            item["amount"] = str(new_stock.count(item))
            item["id"] = str(id)
            if item not in seen_products:
                csv_writer.writerow(item)
                seen_products.append(item)
                id += 1
        g.truncate()

    if date == get_today():
        print(f" [yellow]Notification:[/yellow] Today's report has been refilled with [cyan]{len(new_stock)}[/cyan] new items.")
    else:
        print(
            f" [yellow]Notification:[/yellow] The report of [cyan]{date}[/cyan] has been refilled with [cyan]{len(new_stock)}[/cyan] new items."
        )


def end_day(override_inv: bool = False, override_rep: bool = False):
    today = get_today()

    try:
        with open(f"./inventories/{today}.csv", newline="", mode="r") as f:
            new_stock = [
                x for x in list(csv.DictReader(f)) if x["expiry date"] != today
            ]
            f.seek(0)
            new_expired = [
                x for x in list(csv.DictReader(f)) if x["expiry date"] == today
            ]
    except FileNotFoundError:
        print(
            "\n [red]Warning:[/red] Sorry, no inventory exists for today. Check the [italic]/inventories/[/italic] directory or create a random inventory with [italic purple]restock[/italic purple].\n"
        )
        return

    try:
        with open(f"./reports/{today}.csv", newline="", mode="r") as g:
            existing_expired = [
                i for i in list(csv.DictReader(g)) if i["status"] == "expired"
            ]
            if len(existing_expired) > 0 and override_rep is False:
                print(
                    "\n [red]Warning:[/red] today's report already contains expired items, suggesting that the report has already been finalised. If you want to add the expired items from the report anyway, call this function with [italic purple]--override_report[/italic purple] / [italic purple]-or[/italic purple].\n"
                )
                return
    except FileNotFoundError:
        print("\n [yellow]Notification:[/yellow] No report is found for today.")
        existing_expired = []

    total_expired = new_expired + existing_expired
    tomorrow = date.fromisoformat(get_today()) + timedelta(days=1)

    try:
        with open(f"./inventories/{tomorrow}.csv", newline="", mode="r") as h:
            tomorrows_stock = [i for i in list(csv.DictReader(h))]
            if len(tomorrows_stock) > 0 and override_inv is False:
                print(
                    "\n [red]Warning:[/red] an existing inventory has already been detected for tomorrow, which suggests that the day has been finalised in the past. If you wish to overwrite this with today's remaining stock, call this function with [italic purple]--override_inventory[/italic purple] / [italic purple]-oi[/italic purple]\n."
                )
                return
    except FileNotFoundError:
        print("\n [yellow]Notification:[/yellow] no inventory is found for tomorrow. One will be created.")
        tomorrows_stock = []

    print("\n [yellow]Notification:[/yellow] adding expired items to report.")
    for item in total_expired:
        write_to_report(
            product=item, status="expired", amount=item["amount"], date=today
        )

    print("\n [yellow]Notification:[/yellow] writing tomorrow's inventory.")
    new_stock = new_stock + tomorrows_stock
    write_to_stock(new_stock=new_stock, date=tomorrow)

    set_today(new_date=(date.fromisoformat(get_today()) + timedelta(days=1)))

    get_today(show=True)
