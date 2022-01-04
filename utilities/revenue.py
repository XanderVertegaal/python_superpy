import csv
from datetime import date, timedelta
from utilities.time_manipulation import get_today
from rich import align, print
from rich.table import Table
from rich.console import Console
from rich.panel import Panel


def calculate_revenue(rev_date: str = get_today(), period: int = 1):
    dates = [(date.fromisoformat(rev_date) - timedelta(days=x))
             for x in reversed(range(0, period))]

    agg_revenue = []
    agg_expenses = []
    agg_profits = []

    console = Console()

    for ind_date in dates:
        bought = []
        sold = []
        expired = []

        try:
            with open(f'./reports/{ind_date}.csv', mode="r", newline='') as f:
                contents = list(csv.DictReader(f))
                for item in contents:
                    match item['status']:
                        case 'sold':
                            sold.append(item)
                        case 'expired':
                            expired.append(item)
                        case 'bought':
                            bought.append(item)
        except FileNotFoundError:
            print(f"\n [yellow]Notification:[/yellow] no report for {ind_date} found.\n")
            continue

        
        bought = sorted(bought, key=lambda x: x['department'])
        sold = sorted(sold, key=lambda x: x['department'])
        expired = sorted(expired, key=lambda x: x['department'])

        if len(bought) == 0:
            print(f'\n [yellow]Notification:[/yellow] no items were bought from the store on {ind_date}.')
        else:
            print('\n')
            id_bought = 1
            table_bought = Table(
                show_header=True,
                header_style="bold",
                title=f"Items bought on {ind_date}"
            )
            table_bought.add_column("Id", style="dim")
            table_bought.add_column("Product name"),
            table_bought.add_column("Amount", justify="right")
            table_bought.add_column("Department")
            table_bought.add_column("Buying price", justify="right")
            table_bought.add_column("Selling price", justify="right")
            
            for item in bought:
                table_bought.add_row(
                    str(id_bought),
                    item['product name'],
                    item['amount'],
                    item['department'],
                    f"[cyan]{item['buying price']}[/cyan]",
                    item['selling price']
                )
                id_bought += 1

            console.print(table_bought, justify='center')

        if len(sold) == 0:
            print(f'\n [yellow]Notification:[/yellow] no items were sold from the store on {ind_date}.')
        else:
            print('\n')
            id_sold = 1
            table_sold = Table(
                show_header=True,
                header_style="bold",
                title=f"Items sold on {ind_date}"
            )
            table_sold.add_column("Id", style="dim")
            table_sold.add_column("Product name"),
            table_sold.add_column("Amount", justify="right")
            table_sold.add_column("Department")
            table_sold.add_column("Buying price", justify="right")
            table_sold.add_column("Selling price", justify="right")
            
            for item in sold:
                table_sold.add_row(
                    str(id_sold),
                    item['product name'],
                    item['amount'],
                    item['department'],
                    item['buying price'],
                    f"[green]{item['selling price']}[/green]"
                )
                id_sold += 1

            console.print(table_sold, justify='center')

        if len(expired) == 0:
            print(f'\n [yellow]Notification:[/yellow] no items reached their expiration date on {ind_date}.')
        else:
            print('\n')
            id_expired = 1
            table_expired = Table(
                show_header=True,
                header_style="bold",
                title=f"Items expired on {ind_date}"
            )
            table_expired.add_column("Id", style="dim")
            table_expired.add_column("Product name"),
            table_expired.add_column("Amount", justify="right")
            table_expired.add_column("Department")
            table_expired.add_column("Buying price", justify="right")
            table_expired.add_column("Selling price", justify="right")
            
            for item in expired:
                table_expired.add_row(
                    str(id_expired),
                    item['product name'],
                    item['amount'],
                    item['department'],
                    item['buying price'],
                    item['selling price']
                )
                id_expired += 1

            console.print(table_expired, justify='center')
            print('\n')

        revenue = sum([float(x['selling price']) for x in sold])
        expenses = sum([float(x['buying price']) for x in bought])
        profits = revenue - expenses

        # Output to file
        with open(f'./summaries/{ind_date}.csv', mode="w", newline="") as g:
            fieldnames = [
                "date",
                "revenue",
                "expenses",
                "profits"
            ]
            csv_writer = csv.DictWriter(g, fieldnames=fieldnames, extrasaction="ignore")
            csv_writer.writeheader()
            csv_writer.writerow({
                'date': str(ind_date),
                'revenue': "{:.2f}".format(revenue),
                'expenses': "{:.2f}".format(expenses),
                'profits': "{:.2f}".format(profits)
            })
            

        # Output to console
        table_day = Table(show_header=False)
        table_day.add_row(
            "[bold]Total revenue:[bold]",
            "{:.2f}".format(revenue)
        )
        table_day.add_row(
            "[bold]Total expenses:[/bold]",
            "{:.2f}".format(expenses)
        )
        table_day.add_row(
            "[bold]Total profits:[/bold]",
            "{:.2f}".format(profits)
        )

        print(align.Align(Panel(
            renderable=table_day,
            title=f"Overview of [cyan]{ind_date}[/cyan]",
            expand=False,
        ), align='center'))

        agg_revenue.append(revenue)
        agg_expenses.append(expenses)
        agg_profits.append(profits)

    if period > 1:
        total_revenue = sum(agg_revenue)
        total_expenses = sum(agg_expenses)
        total_profits = sum(agg_profits)


        table_period = Table(show_header=False)
        table_period.add_row(
            "[bold]Total revenue:[bold]",
            "{:.2f}".format(total_revenue)
        )
        table_period.add_row(
            "[bold]Total expenses:[/bold]",
            "{:.2f}".format(total_expenses)
        )
        table_period.add_row(
            "[bold]Total profits:[/bold]",
            "{:.2f}".format(total_profits)
        )
        
        print('\n')
        print(align.Align(Panel(
            renderable=table_period,
            title=f"Period [cyan]{dates[0]} - {dates[-1]}[/cyan]",
            expand=False,
        ), align='center'))
        