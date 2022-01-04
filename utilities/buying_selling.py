import csv
from random import randint
from utilities.store_properties import check_manager
from utilities.report import write_to_report
from utilities.time_manipulation import get_today
from utilities.inventory import write_to_stock
from datetime import datetime
from utilities.utilities import get_expiry_date
from rich import print


def buy_product(
    product_name: str,
    quantity: int = 1,
    date: str = get_today(),
    price: float = None
):
    with open("./products.csv", newline="", mode="r") as f:
        products = list(csv.DictReader(f))

        item = next(
            (item for item in products
                if item["product name"] == product_name), None,
        )

    if item is None:
        print("\n [red]Warning:[/red] this product is currently not sold in our store. Check our product list for an overview of items we can accept (command: [italic blue]products[/italic blue]).\n")
        return

    try:
        with open(f"./inventories/{date}.csv", mode="r+", newline="") as g:
            products = list(csv.DictReader(g))
    except:
        with open(f"./inventories/{date}.csv", mode="w", newline="") as h:
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
            csv_writer = csv.DictWriter(h, fieldnames=fieldnames, extrasaction="ignore")
            h.seek(0)
            csv_writer.writeheader()
        products = []

    if price is None:
            price = item['buying price']

    if is_purchase_successful(product_name, price, 'buy', date) is False:
        print('\n [red]Warning:[/red] this product cannot be bought right now. Please try again later.\n')
        return

    selling_price = "{:.2f}".format(
        round(1.10 * float(item["buying price"]), 2)
    )

    existing = list(
        filter(
            lambda x: x["product name"] == item["product name"]

            and x["expiry date"]
            == str(get_expiry_date(int(item["shelf-life"])))

            and "{:.2f}".format(float(x["buying price"]))
            == "{:.2f}".format(float(price)),
            products,
        )
    )

    sold_item = {
        "product id": item["product id"],
        "product name": item["product name"],
        "amount": quantity,
        "department": item["department"],
        "buying price": "{:.2f}".format(round((float(price)), 2)),
        "selling price": selling_price,
        "expiry date": get_expiry_date(int(item["shelf-life"])),
    }

    if len(existing) == 0:
        products.append(sold_item)
    else:
        existing[0]["amount"] = str(int(existing[0]["amount"]) + quantity)

    total_price = "{:.2f}".format(quantity * round((float(price)), 2))
    print(
        f'\n [yellow]Notification:[/yellow] the store bought [cyan]{quantity}[/cyan]x [magenta]{item["product name"]}[/magenta] for a total of [cyan]{total_price}[/cyan].\n'
    )

    write_to_stock(
        new_stock=products,
        date=date
    )
    write_to_report(
        product=sold_item,
        status='bought',
        amount=quantity,
        date=date
    )


def sell_product(
    product_name: str,
    quantity: int = 1,
    date: str = get_today(),
    price: float = None
):
    try:
        with open(f"./inventories/{date}.csv", newline="", mode="r") as f:
            products = list(csv.DictReader(f))
    except:
        print('\n [red]Warning:[/red] no inventory found for today. Create a new one using [italic blue]restock[/italic blue] or by ending the previous day.\n')
        return

    stock = list(filter(lambda x: x["product name"] == product_name, products))

    if len(stock) == 0:
        print("\n [red]Warning:[/red] this product is out of stock today. Please try again tomorrow.\n")
        return

    # If the customers has not specified a buying price,
    # the shop takes the selling price as a default.
    if price is None:
        price = min([float(item['selling price']) for item in stock])

    total_amount = sum([int(x["amount"]) for x in stock])
    if total_amount < quantity:
        print(f"\n [red]Warning:[/red] the store only has [cyan]{total_amount}[/cyan] of these in stock. Please try again with a lower quantity.\n")
        return

    if is_purchase_successful(product_name, price, 'sell', date) is False:
        print('\n [red]Warning:[/red] the manager has refused your offer.\n')
        return

    # The shop sells products that expire soon first
    stock = sorted(stock, key=lambda x: x["expiry date"])
    sold = []
    total_price = 0
    total_quantity = 0
    for item in stock:
        item['selling price'] = price
        if int(item["amount"]) > quantity:
            item["amount"] = int(item["amount"]) - quantity
            sold.append({**item, "amount": quantity})
            total_price += quantity * float(item["selling price"])
            total_quantity += quantity
            write_to_report(
                product=item,
                status='sold',
                amount=quantity,
                date=date
            )
            break
        elif int(item["amount"]) == quantity:
            products.remove(item)
            sold.append(item)
            total_price += quantity * float(item["selling price"])
            total_quantity += quantity
            write_to_report(
                product=item,
                status='sold',
                amount=quantity,
                date=date
            )
            break
        else:
            quantity = quantity - int(item["amount"])
            products.remove(item)
            sold.append(item)
            total_price += quantity * float(item["selling price"])
            total_quantity += quantity
            write_to_report(
                product=item,
                status='sold',
                amount=quantity,
                date=date
            )

    print(
        f'\n [yellow]Notification:[/yellow] the store sold [cyan]{quantity}[/cyan]x [magenta]{stock[0]["product name"]}[/magenta] for a total of [cyan]{"{:.2f}".format(round(total_price, 2))}[/cyan].\n'
    )
    write_to_stock(products, date)


def is_purchase_successful(
    product_name: str,
    price: float,
    action_type: str,
    date: str
) -> bool:
    try:
        date_object = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print("\n [red]Warning:[/red] you have entered an invalid date. Please try again using the YYYY-MM-DD format.")
        return False

    day = date_object.strftime('%A')
    if day == 'Sunday':
        print("\n [yellow]Notification:[/yellow] the store is closed on [cyan]Sunday[/cyan]. Please try again tomorrow.\n")
        return False

    manager = check_manager(date)

    with open('products.csv', mode="r") as g:
        products = csv.DictReader(g)
        product = next(
            (item for item in products
                if item['product name'] == product_name), None
        )
        buying_price = float(product['buying price'])
        selling_price = round(float(1.10 * buying_price), 2)
        price = float(price)

    print(f"\n Today's supermarket manager is [bright_yellow]{manager['name']}[/bright_yellow].")
    print(f" Requested product: [magenta]{product_name}[/magenta].")
    print(f' Buying price: [cyan]{round(buying_price, 2)}[/cyan].')
    print(f' Selling price: [cyan]{round(selling_price, 2)}[/cyan].')
    print(f' The customer offers: [cyan]{price}[/cyan].')

    match manager['name']:
        case 'Phyllis':
            phyllis_special_price = 1.05 * buying_price
            if action_type == 'sell':
                if price < phyllis_special_price:
                    print('\n [yellow]Notification:[/yellow] the customer is offering too little money, even for [bright_yellow]Phyllis[/bright_yellow].')
                    return False
                elif phyllis_special_price < price < selling_price:
                    print('\n [yellow]Notification:[/yellow] [bright_yellow]Phyllis[/bright_yellow] is making an exception just for the customer.')
                return True
            else:
                if price > phyllis_special_price:
                    print('\n [yellow]Notification:[/yellow] the customer is asking too much money, even for [bright_yellow]Phyllis[/bright_yellow].')
                    return False
                elif price > phyllis_special_price > buying_price:
                    print('\n [yellow]Notification:[/yellow] [bright_yellow]Phyllis[/bright_yellow] is making a special exception just for the customer.')
                return True
        case 'Andy':
            andy_random = randint(1, 10)
            if andy_random >= 5:
                print('\n [yellow]Notification:[/yellow] [bright_yellow]Andy[/bright_yellow] randomly decides to go ahead with the sale!')
                return True
            else:
                print('\n [yellow]Notification:[/yellow] [bright_yellow]Andy[/bright_yellow] has decided he does not like your face and refuses. (Try again.)')
                return False
        case 'Angela':
            if product_name in ['white wine', 'red wine', 'heineken']:
                print("\n [yellow]Notification:[/yellow] [bright_yellow]Angela[/bright_yellow] does not like alcohol and will not buy/sell this product.")
                return False
            else:
                if action_type == 'sell' and price >= selling_price:
                    return True
                if action_type == 'buy' and price <= buying_price:
                    return True
            return False
        case 'Oscar':
            if action_type == 'sell' and price != selling_price:
                print('\n [yellow]Notification:[/yellow] [bright_yellow]Oscar[/bright_yellow] does not accept anything more/less than the set selling price.')
                return False
            if action_type == 'buy' and price != buying_price:
                print('\n [yellow]Notification:[/yellow] [bright_yellow]Oscar[/bright_yellow] will not give anything more/less than the set buying price.')
                return False
            return True

        case 'Kevin':
            if product_name == 'cookie':
                if action_type == 'buy':
                    print('\n [yellow]Notification:[/yellow] [bright_yellow]Kevin[/bright_yellow] will always buy cookies!')
                    return True
                if action_type == 'sell':
                    print('\n [yellow]Notification:[/yellow] [bright_yellow]Kevin[/bright_yellow] is reluctant to let go\
                        of his precious cookies.')
                    return False
            else:
                if action_type == 'sell' and price >= selling_price:
                    return True
                if action_type == 'buy' and price <= buying_price:
                    return True
                return False

        case 'Michael':
            if action_type == 'sell' and price >= selling_price:
                return True
            if action_type == 'buy' and price <= buying_price:
                return True
            return False
