<h2 align='center'>Superpy</h2>
<h3 align='center'> A Python supermarket</h3>

### **Introduction**

Superpy is a tool that manages the stock of items in your shop, keeps track of all transactions and provides an overview of revenue, expenses and profits, fully written in Python and beautified with the help of Rich. This short guide will teach you how to manipulate and consult your supermarket data.

All positional and optional arguments are entered after `python superpy.py`.

A good way to initialise Superpy is to start with:

```
python superpy.py set_today
python superpy.py restock
```

This resets Superpy's notion of today to the current system date and creates a new inventory with random items. These commands and others are explained below.

<br />

### **Time manipulation**

- `today`: shows the date and day currently set as _today_.
- `set_today (--date / -d <date>)`: sets _today_ to be the supplied date (in YYYY-MM-DD format). If no date is provided, _today_ is set to the user's current system date.

    <br />

  **Optional arguments:**

  In addition to setting the date _absolutely_ using `--date` / `-d`, the date can be set _relatively_ using the following optional arguments:

  - `--today`, `-td`: set's _today_'s date to today (no effect in combination with `set_today`).
  - `--tomorrow`, `-tm`: increases _today_'s date by one day.
  - `--next_week`, `-nw`: increases _today_'s date by one week.
  - `--yesterday`, `-y`: decreases _today_'s date by one day.
  - `--last_week`, `-lw`: decreases _today_'s date by one week.

    <br />

  **Examples:**

  Set _today_ to May 8th, 2022:

  ```
  python superpy.py --date 2022-05-08
  ```

  Advance the current _today_ date by 7 days:

  ```
  python superpy.py -nw
  ```

<br />

### **Products**

The supermarket only sells a certain number of items, but more can be made available by adding them in CSV format to `products.csv`.

- `products`: provides an overview of all available items: their names, respective departments, their buying price and their shelf life (in days).

<br />

### **Buying and selling**

Superpy does not only keep track of bought and sold items but also checks whether purchases are allowed to take place. Superpy will give out a warning if a sale cannot continue.

- `buy <product name>`: records that the store bought an item from a customer.
- `sell <product name>`: records that the store sold an item to a customer.

    <br />

  **Optional arguments:**

  Both commands take the following optional arguments:

  - `--price`, `-p`: specify the item price that the customers offers or requests. Customers are allowed to haggle. It is up to the supermarket manager to decide whether the transaction is allowed or not. By default, the buying price or the selling price (= 1.10 \* the buying price) are used.
  - `--date`, `-d`: specifies the (absolute) date (format: YYYY-MM-DD) when the purchase was proposed. If no date is provided, _today_'s date is used.
  - `--quantity`, `-q`: specifies the amount of goods purchased or sold. If the customer wants to buy more goods than are available in _today_'s inventory, Superpy will give a warning. If no quantity is provided, it is set to 1 by default.

    <br />

  **Examples:**

  A customer wants to sell 2 oranges _today_ for 1.10 each.

  ```
  python superpy.py buy 'orange' -q 2 -p 1.10
  ```

  A customer wants to buy one kale on December 12th for the selling price.

  ```
  python superpy.py sell `kale` -d 2021-12-12
  ```

<br />

### **Managers**

The supermarket is closed on Sunday. On every other day, there is a different manager who oversees all transactions. To see who is working _today_, use the following command.

- `manager`: displays _today_'s supermarket manager.

The following managers are currently employed at the supermarket.

- **Phyllis (Monday)** is sweet and allows the customer to buy items at 95% of their selling price, and sell at 105% of their buying price.
- **Andy (Tuesday)** is a maniac and will not allow any transactions in 40% of cases. Simply try again.
- **Angela (Wednesday)** will not buy or sell any alcohol, as she thinks drinking is bad.
- **Oscar (Thursday)** does everything by the books. If more or less money is offered than either the buying price or the selling price, he will refuse.
- **Kevin (Friday)** will buy cookies at any price. He will not sell them, though.
- **Michael (Saturday)** runs the store as a real manager would. He will gladly buy and sell items if the customer undercuts the buying price or offers more than the standard selling price.

<br />

### **Inventory**

A list of items currently on sale in the supermarket can be consulted and manipulated using the following commands.

- `show_inventory`: shows the inventory. If no date is provided, _today_'s date is used.

- `restock`: fills the inventory of a set date with a set number of random items. If no quantity is provided, the inventory will be restocked with 50 items. Any existing inventories are overwritten.

    <br />

  **Optional arguments**

  - `--quantity`, `-q`: Restocks the inventory with a set amount of items.
  - `--date`, `-d`: the date of `show_inventory` and `restock` can be set by providing a specific date (YYYY-MM-DD).
  - For relative dates, use the arguments listed under [**Time manipulation**](#time-manipulation) above.

    <br />

  **Examples**

  Show the inventory on December 17th, 2021.

  ```
  python superpy.py show_inventory --date 2021-12-17
  ```

  Restock _today_'s inventory with 50 items.

  ```
  python superpy.py restock
  ```

  Restock last week's inventory with 200 items.

  ```
  python superpy.py restock -q 200 -lw
  ```

<br />

### **Report**

A report is a daily overview of all transactions (buying/selling) and is used to calculate the supermarket's revenue and profits. At the end of the day, items that have expired are also added to the report. The following commands are used to view and create reports.

- `show_report`: shows the report of an arbitrary date. If no date is provided, _today_'s report is shown.

- `fabricate_report`: creates a report for a set date and fills it with a set number of random items (with random statuses, i.e. _bought_, _sold_ or _expired_). If no quantity is provided, the report is filled with 50 items.

- `end_day`: ends the current working day by:

  1. adding all expiring items to the report;
  2. creating a new inventory on the next day with all remaining items;
  3. advancing time one day to the next day.

  By default, Superpy will not end the day and give out a warning message if the day already appears to have been closed off and/or if an inventory for the next day already exists. This behaviour can be overridden.

    <br />

  **Optional arguments**

  - `--quantity`, `-q`: use with `fabricate_report` with a set amount of items.
  - `--date`, `-d`: the date of `show_report` and `fabricate_report` can be set by providing a specific date (YYYY-MM-DD).
  - For relative dates, use the arguments listed under [**Time manipulation**](#time-manipulation) above.
  - `--override_inventory`, `-oi`: replaces an existing inventory for the next day with a new one containing all non-expired items in _today_'s inventory.
  - `--override_report`, `-or`: replaces an existing report for _today_ with a new one to which items that expired _today_ have been added.

    <br />

  **Examples**

  Show yesterday's report.

  ```
  python superpy.py show_report --yesterday
  ```

  Create a report with 150 items for November 11th, 1992.

  ```
  python superpy.py fabricate_report -q 150 -d 1992-11-11
  ```

  End the day, overwrite tomorrow's existing inventory.

  ```
  python superpy.py end_day -oi
  ```

<br />

### **Revenue**

An overview of revenue, expenses and profits for individual days and periods can be created by using the following command. The results are printed to the console and written per day to a csv file.

- `revenue`: displays a report for a set date (default: _today_) and time period (default: single day) up to and including the set date.

    <br />

  **Optional arguments:**

  - `--date`, `-d`: the date for the report can be set by providing a specific date (YYYY-MM-DD).
  - For relative dates, use the arguments listed under [**Time manipulation**](#time-manipulation) above.
  - `--period`, `-p`: specify the period (number of days) in the past you want to include in the overview.

    <br />

  **Examples**

  Create a revenue overview for _today_.

  ```
  python superpy.py revenue
  ```

  Create a revenue overview for yesterday and the week before.

  ```
  python superpy.py revenue --yesterday --period 7
  ```

  Create a revenue overview for both Christmas days in 2021.

  ```
  python superpy.py revenue -d 2021-12-26 -p 2
  ```
