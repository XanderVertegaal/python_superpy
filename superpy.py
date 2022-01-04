# Imports
import argparse
from datetime import date, timedelta
from utilities.store_properties import check_manager, show_products
from utilities.time_manipulation import get_today, set_today
from utilities.buying_selling import buy_product, sell_product
from utilities.inventory import restock, show_inventory
from utilities.report import show_report, fabricate_report, end_day
from utilities.revenue import calculate_revenue

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
def main():

    parser = argparse.ArgumentParser(
        prog="superpy",
        description="Welcome to Superpy! Use this programme to keep track of shop inventories, sales and revenue reports.\n")
    subparsers = parser.add_subparsers(dest='cmd')

    # General store properties
    subparsers.add_parser(
        'manager',
        help="Shows today's manager."
    )
    subparsers.add_parser(
        'products',
        help="Displays a list of items that the store will buy and sell."
    )

    # Time getting / setting
    subparsers.add_parser('today', help="Shows the current date.")

    parser_set_today = subparsers.add_parser(
        'set_today',
        help=("Sets the current date to a supplied date.\
            If no date is provided, the system's current date is taken."))
    parser_set_today.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        type=str,
    )
    parser_set_today.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_set_today.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_set_today.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_set_today.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_set_today.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )

    # Buying and selling
    parser_buy_item = subparsers.add_parser(
        'buy',
        help="The store buys an item.\
            Optional parameters: quantity (default = 1),\
            price (default = buying price) and date (default = today)."
    )
    parser_buy_item.add_argument(
        'product',
        help="Product name (required)."
    )
    parser_buy_item.add_argument(
        '--quantity', '-q',
        help="Quantity (default = 1)",
        default=1,
        type=int
    )
    parser_buy_item.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        default=get_today(),
        type=str
    )
    parser_buy_item.add_argument(
        '--price', '-p',
        help="Proposed price for each individual item\
            (default = buying price per item).",
        type=float
    )

    parser_sell_item = subparsers.add_parser(
        'sell',
        help="The store sells an item to a customer.\
            Optional parameters: quantity (default = 1),\
            price (default = selling price) and date (default = today)."
    )
    parser_sell_item.add_argument(
        'product',
        help="Product name (required)."
    )
    parser_sell_item.add_argument(
        '--quantity', '-q',
        help="Quantity (default = 1).",
        default=1,
        type=int
    )
    parser_sell_item.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        default=get_today(),
        type=str
    )
    parser_sell_item.add_argument(
        '--price', '-p',
        help="Proposed price for each individual item\
            (default = selling price per item).",
        type=float
    )

    # Inventory
    parser_show_inventory = subparsers.add_parser(
        'show_inventory',
        help="Displays the shop inventory for a specified date\
            (YYYY-MM-DD, default = today)."
    )
    parser_show_inventory.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        default=get_today(),
        type=str,
    )
    parser_show_inventory.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_show_inventory.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_show_inventory.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_show_inventory.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_show_inventory.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )

    parser_restock = subparsers.add_parser(
        'restock',
        help="Resets the shop inventory with a specified number (default = 50)\
            of items on a specified date (default = today)."
    )
    parser_restock.add_argument(
        '--quantity', '-q',
        help="Quantity (default = 50).",
        default=50,
        type=int
    )
    parser_restock.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        type=str,
    )
    parser_restock.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_restock.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_restock.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_restock.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_restock.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )

    # Report
    parser_show_report = subparsers.add_parser(
        'show_report',
        help="Displays the report with bought/sold/expired items\
            for the specified date, if available.\
            If no date is provided, today's report is shown."
    )
    parser_show_report.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        type=str,
        default=get_today()
    )
    parser_show_report.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_show_report.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_show_report.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_show_report.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_show_report.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )

    parser_fabricate = subparsers.add_parser(
        'fabricate_report',
        help="Creates a report with a specified number (default: 50)\
            of expired, bought and sold items on a specified date\
            (default: today). (Please don't tell the tax agency about this!)"
    )
    parser_fabricate.add_argument(
        '--quantity', '-q',
        help="Quantity (default = 50).",
        default=50,
        type=int
    )
    parser_fabricate.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        default=get_today(),
        type=str
    )
    parser_fabricate.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_fabricate.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_fabricate.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_fabricate.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_fabricate.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )

    parser_end_day = subparsers.add_parser(
        'end_day',
        help="Ends the day by adding expired items to the report and creating\
            a new inventory for the next day with the remaining items.\
            If a report with expired items or an inventory for the next day\
            already exists, Superpy will send out a warning. Add the flags\
            --override_report and/or --override_inventory to change\
            this behaviour."
    )
    parser_end_day.add_argument(
        '--override_report', '-or',
        help="Adds expired products to the report even if it already contains\
            expired items.",
        action="store_true",
        default=False
    )
    parser_end_day.add_argument(
        '--override_inventory', '-oi',
        help="Overrides an existing inventory for the next day.",
        action="store_true",
        default=False
    )

    # Revenue
    parser_calculate_revenue = subparsers.add_parser(
        'revenue',
        help="Calculate revenue, expenses and profits based on the report\
            on the specified date (default = today)."
    )
    parser_calculate_revenue.add_argument(
        '--date', '-d',
        help="Date (YYYY-MM-DD, default = today).",
        type=str,
        default=get_today()
    )
    parser_calculate_revenue.add_argument(
        '--today', '-td',
        help="Today.",
        action="store_true",
        default=False
    )
    parser_calculate_revenue.add_argument(
        '--yesterday', '-y',
        help="Yesterday.",
        action="store_true",
        default=False
    )
    parser_calculate_revenue.add_argument(
        '--tomorrow', '-tm',
        help="Tomorrow.",
        action="store_true",
        default=False
    )
    parser_calculate_revenue.add_argument(
        '--last_week', '-lw',
        help="Last week.",
        action="store_true",
        default=False
    )
    parser_calculate_revenue.add_argument(
        '--next_week', '-nw',
        help="Next week.",
        action="store_true",
        default=False
    )
    parser_calculate_revenue.add_argument(
        '--period', '-p',
        help="Amount of days up to and including the present day to be\
            included in the report (default = 1).",
        type=int,
        default=1
    )

    # Argument interpretation and action dispatches
    args = parser.parse_args()

    match args.cmd:
        case 'today':
            get_today(show=True)
        case 'set_today':
            if args.today:
                set_today(new_date=get_today())
            elif args.yesterday:
                set_today(new_date=(date.fromisoformat(get_today())
                                    - timedelta(days=1)))
            elif args.tomorrow:
                set_today(new_date=(date.fromisoformat(get_today())
                                    + timedelta(days=1)))
            elif args.next_week:
                set_today(new_date=(date.fromisoformat(get_today())
                                    + timedelta(days=7)))
            elif args.last_week:
                set_today(new_date=(date.fromisoformat(get_today())
                                    - timedelta(days=7)))
            else:
                set_today(new_date=args.date)
            get_today(show=True)
        case 'manager':
            check_manager(show=True)
        case 'products':
            show_products()
        case 'show_inventory':
            if args.today:
                show_inventory(date=get_today())
            elif args.yesterday:
                show_inventory(
                    date=(date.fromisoformat(get_today()) - timedelta(days=1))
                )
            elif args.tomorrow:
                show_inventory(
                    date=(date.fromisoformat(get_today()) + timedelta(days=1))
                )
            elif args.next_week:
                show_inventory(
                    date=(date.fromisoformat(get_today()) + timedelta(days=7))
                )
            elif args.last_week:
                show_inventory(
                    date=(date.fromisoformat(get_today()) - timedelta(days=7))
                )
            else:
                show_inventory(date=args.date)
        case 'restock':
            if args.today:
                restock(amount=args.quantity, date=get_today())
            elif args.yesterday:
                restock(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) - timedelta(days=1))
                )
            elif args.tomorrow:
                restock(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) + timedelta(days=1))
                )
            elif args.next_week:
                restock(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) + timedelta(days=7))
                )
            elif args.last_week:
                restock(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) - timedelta(days=7))
                )
            else:
                restock(amount=args.quantity, date=args.date)
        case 'fabricate_report':
            if args.today:
                fabricate_report(
                    amount=args.quantity,
                    date=get_today()
                )
            elif args.yesterday:
                fabricate_report(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) - timedelta(days=1))
                )
            elif args.tomorrow:
                fabricate_report(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) + timedelta(days=1))
                )
            elif args.next_week:
                fabricate_report(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) + timedelta(days=7))
                    )
            elif args.last_week:
                fabricate_report(
                    amount=args.quantity,
                    date=(date.fromisoformat(get_today()) - timedelta(days=7))
                )
            else:
                fabricate_report(amount=args.quantity, date=args.date)
        case 'show_report':
            if args.today:
                show_report(date=get_today())
            elif args.yesterday:
                show_report(
                    date=(date.fromisoformat(get_today()) - timedelta(days=1))
                )
            elif args.tomorrow:
                show_report(
                    date=(date.fromisoformat(get_today()) + timedelta(days=1))
                )
            elif args.next_week:
                show_report(
                    date=(date.fromisoformat(get_today()) + timedelta(days=7))
                )
            elif args.last_week:
                show_report(
                    date=(date.fromisoformat(get_today()) - timedelta(days=7))
                )
            else:
                show_report(date=args.date)
        case 'buy':
            buy_product(
                product_name=args.product,
                quantity=args.quantity,
                date=args.date,
                price=args.price
            )
        case 'sell':
            sell_product(
                product_name=args.product,
                quantity=args.quantity,
                date=args.date,
                price=args.price
            )
        case 'revenue':
            if args.today:
                calculate_revenue(rev_date=get_today())
            elif args.yesterday:
                calculate_revenue(
                    rev_date=str(
                        date.fromisoformat(get_today()) - timedelta(days=1)
                    ), period=args.period
                )
            elif args.tomorrow:
                calculate_revenue(
                    rev_date=str(
                        date.fromisoformat(get_today()) + timedelta(days=1)
                    ), period=args.period
                )
            elif args.next_week:
                calculate_revenue(
                    rev_date=str(
                        date.fromisoformat(get_today()) + timedelta(days=7)
                    ), period=args.period
                )
            elif args.last_week:
                calculate_revenue(
                    rev_date=str(
                        date.fromisoformat(get_today()) - timedelta(days=7)
                    ), period=args.period
                )
            else:
                calculate_revenue(rev_date=args.date, period=args.period)
        case 'end_day':
            end_day(
                override_inv=args.override_inventory,
                override_rep=args.override_report
            )


if __name__ == "__main__":
    main()
