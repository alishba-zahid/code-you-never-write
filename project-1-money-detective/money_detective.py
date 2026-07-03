import csv
from collections import defaultdict
from datetime import datetime

def load_transactions(filename):
    transactions = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                'date': row['Date'].strip(),
                'description': row['Description'].strip(),
                'amount': float(row['Amount'].strip())
            })
    return transactions

def analyze_expenditures(transactions):
    monthly_totals = defaultdict(float)
    for t in transactions:
        # Extract YYYY-MM
        month = t['date'][:7]
        monthly_totals[month] += t['amount']
    return monthly_totals

def find_duplicates(transactions):
    # Duplicates: Same date, description, and amount
    seen = {}
    duplicates = []
    for t in transactions:
        key = (t['date'], t['description'], t['amount'])
        if key in seen:
            duplicates.append(t)
        else:
            seen[key] = True
    return duplicates

def find_recurring(transactions):
    # Recurring: Same description and amount occurring in different months
    by_item = defaultdict(set)
    for t in transactions:
        month = t['date'][:7]
        key = (t['description'], t['amount'])
        by_item[key].add(month)
    
    recurring = []
    for key, months in by_item.items():
        if len(months) >= 2:
            recurring.append({
                'description': key[0],
                'amount': key[1],
                'months_active': sorted(list(months))
            })
    return recurring

def main():
    csv_file = 'transactions.csv'
    print("=" * 60)
    print("MONEY DETECTIVE — TRANSACTION HISTORY AUDIT")
    print("=" * 60)
    
    try:
        transactions = load_transactions(csv_file)
        print(f"Loaded {len(transactions)} transaction records successfully.\n")
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
        return

    # 1. Monthly totals
    print("[1] Monthly Expenditures Summaries:")
    totals = analyze_expenditures(transactions)
    for month, total in sorted(totals.items()):
        print(f"  * Month: {month} | Total Expenditure: ${abs(total):.2f}")
    print()

    # 2. Duplicate Check
    print("[2] Flagged Duplicate Charges:")
    duplicates = find_duplicates(transactions)
    if duplicates:
        for d in duplicates:
            print(f"  [ALERT] Duplicate charge detected on {d['date']} | {d['description']} | Amount: ${abs(d['amount']):.2f}")
    else:
        print("  No duplicate charges detected.")
    print()

    # 3. Recurring Charges
    print("[3] Flagged Active Subscriptions / Recurring Charges:")
    recurring = find_recurring(transactions)
    if recurring:
        for r in recurring:
            months_str = ", ".join(r['months_active'])
            print(f"  [SUBSCRIPTION] {r['description']} | Cost: ${abs(r['amount']):.2f} | Seen in: {months_str}")
    else:
        print("  No recurring subscription channels flagged.")
    print("=" * 60)

if __name__ == "__main__":
    main()
