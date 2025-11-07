import pandas as pd
import os
from datetime import datetime
import sys

DATA_FILE = "expenses.csv"
COLUMNS = ["date", "category", "amount", "note"]

def init_datafile():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_FILE, index=False)
        print("✅ Created a new expenses.csv file.")
    else:
        print("✅ expenses.csv file already exists.")

def add_expense():
    date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if date_str == "":
        date = datetime.now().date()
    else:
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print("❌ Invalid date format.")
            return

    category = input("Enter category (e.g., Food, Transport, etc.): ").strip()
    if category == "":
        print("❌ Category cannot be empty.")
        return

    try:
        amount = float(input("Enter amount: ").strip())
    except ValueError:
        print("❌ Invalid amount.")
        return

    note = input("Add a short note (optional): ").strip()

    df = pd.read_csv(DATA_FILE)
    new_row = {"date": date.isoformat(), "category": category, "amount": amount, "note": note}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    print("✅ Expense added successfully!")

def view_expenses(limit=None):
    if not os.path.exists(DATA_FILE):
        print("No data file found. Add an expense first.")
        return

    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    if df.empty:
        print("No expenses recorded yet.")
        return

    df_sorted = df.sort_values("date", ascending=False)
    if limit is not None:
        df_sorted = df_sorted.head(limit)

    df_display = df_sorted.copy()
    df_display["amount"] = df_display["amount"].map(lambda x: f"{float(x):,.2f}")
    print("\n--- Expenses ---")
    print(df_display.to_string(index=False, columns=COLUMNS))
    print("----------------\n")

def summary_by_category():
    """Show total and count per category and overall total. Also shows current-month breakdown."""
    if not os.path.exists(DATA_FILE):
        print("No data file found. Add some expenses first.")
        return

    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    if df.empty:
        print("No expenses recorded yet.")
        return

    # Overall summary
    by_cat = df.groupby("category", as_index=False)["amount"].agg(total="sum", count="count")
    by_cat = by_cat.sort_values("total", ascending=False)
    by_cat["total"] = by_cat["total"].map(lambda x: f"{float(x):,.2f}")

    print("\n--- Expense Summary (All time) ---")
    print(by_cat.to_string(index=False))
    overall_total = df["amount"].sum()
    print(f"\nTotal spent (all time): {overall_total:,.2f}")

    # Current month summary
    now = datetime.now()
    df["date"] = pd.to_datetime(df["date"])
    cm = df[(df["date"].dt.year == now.year) & (df["date"].dt.month == now.month)]
    if not cm.empty:
        cm_by_cat = cm.groupby("category", as_index=False)["amount"].agg(total="sum", count="count")
        cm_by_cat = cm_by_cat.sort_values("total", ascending=False)
        cm_by_cat["total"] = cm_by_cat["total"].map(lambda x: f"{float(x):,.2f}")
        print(f"\n--- This month: {now.strftime('%B %Y')} ---")
        print(cm_by_cat.to_string(index=False))
        print(f"\nTotal spent (this month): {cm['amount'].sum():,.2f}")
    else:
        print(f"\nNo expenses recorded for {now.strftime('%B %Y')} yet.")
    print("----------------\n")

def menu():
    while True:
        print("""
==== Expense Tracker ====
1. Add expense
2. View recent expenses (10)
3. View all expenses
4. Summary by category
0. Exit
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses(limit=10)
        elif choice == "3":
            view_expenses(limit=None)
        elif choice == "4":
            summary_by_category()
        elif choice == "0":
            print("Bye 👋")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    try:
        init_datafile()
        menu()
    except KeyboardInterrupt:
        print("\nInterrupted — exiting.")
        sys.exit(0)
