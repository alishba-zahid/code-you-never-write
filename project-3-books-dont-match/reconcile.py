import csv
import json
from collections import defaultdict

def load_members(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def load_digital_log(filename):
    records = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'date': row['Date'].strip(),
                'memo': row['Memo'].strip(),
                'amount': float(row['Amount'].strip())
            })
    return records

def match_member(memo, members):
    # Custom mapping rules based on personal knowledge:
    # "Alishba Z" -> Alishba Zahid
    # "Zainab" -> Zainab Ali
    # "Hamza K. dues" -> Hamza Khan
    # "Laiba F" -> Laiba Fatima
    # "B. Ahmed" -> Bilal Ahmed
    
    memo_lower = memo.lower()
    for m in members:
        name = m['name']
        name_lower = name.lower()
        parts = name_lower.split()
        
        # Rule 1: Check full name match
        if name_lower in memo_lower:
            return name
        # Rule 2: Check first name match
        if parts[0] in memo_lower:
            return name
        # Rule 3: Check initials and last name (e.g. B. Ahmed)
        if len(parts) > 1:
            initial = parts[0][0]
            last_name = parts[1]
            if f"{initial}. {last_name}" in memo_lower or f"{initial} {last_name}" in memo_lower:
                return name
    return None

def main():
    members_file = 'members_list.json'
    digital_file = 'digital_log.csv'
    
    print("=" * 60)
    print("LEDGER RECONCILIATION ENGINE")
    print("=" * 60)

    try:
        members = load_members(members_file)
        digital_log = load_digital_log(digital_file)
    except Exception as e:
        print(f"Error loading inputs: {e}")
        return

    # Total expected
    expected_total = sum(m['expected'] for m in members)
    print(f"Hand-Counted Target Total: ${expected_total:.2f} (5 Members @ $100.00 each)\n")

    # Reconciliation state
    payments_by_member = defaultdict(float)
    unmatched_records = []
    
    # Process digital deposits
    for r in digital_log:
        matched_name = match_member(r['memo'], members)
        if matched_name:
            payments_by_member[matched_name] += r['amount']
        else:
            unmatched_records.append(r)

    # Output member status
    print("[1] Roster Payment Status:")
    for m in members:
        name = m['name']
        expected = m['expected']
        paid = payments_by_member.get(name, 0.0)
        diff = paid - expected
        
        if diff == 0:
            status = "PAID (Reconciled)"
        elif diff < 0:
            status = f"UNDERPAID (Deficit of ${abs(diff):.2f})"
        else:
            status = f"OVERPAID (Surplus of ${diff:.2f})"
            
        print(f"  * {name} | Expected: ${expected:.2f} | Paid: ${paid:.2f} | {status}")
    print()

    # Output unmatched records
    print("[2] Unmatched Digital Transactions (Action Required):")
    if unmatched_records:
        for u in unmatched_records:
            print(f"  [UNMATCHED] Date: {u['date']} | Memo: '{u['memo']}' | Amount: ${u['amount']:.2f}")
    else:
        print("  None.")
    print()

    # Summary
    reconciled_paid_total = sum(payments_by_member.values())
    unmatched_total = sum(u['amount'] for u in unmatched_records)
    total_digital = reconciled_paid_total + unmatched_total

    print("[3] Financial Summary:")
    print(f"  * Total Digital Deposits: ${total_digital:.2f}")
    print(f"  * Reconciled Roster Total: ${reconciled_paid_total:.2f}")
    print(f"  * Unmatched Funds: ${unmatched_total:.2f}")
    print(f"  * Roster Collection Deficit: ${max(0.0, expected_total - reconciled_paid_total):.2f}")
    print("=" * 60)

if __name__ == "__main__":
    main()
