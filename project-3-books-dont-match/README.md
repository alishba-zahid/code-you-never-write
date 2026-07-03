# Project 3: The Books Don't Match

## 🔍 The Problem
We have a hand-counted expected total of group dues collection (e.g. $500.00 total, with 5 members expected to pay $100.00 each) and a digital bank statement with inconsistent and messy memo descriptions. We need a script that matches the messy digital transfers to expected members, detects deficits, overpayments, and highlights unmatched digital items for manual audit.

---

## 🤖 AI Tool Used
- **Antigravity AI (powered by Gemini)**

---

## 📝 Prompts Used

### Initial Prompt
> *"Write a Python script that reconciles a digital bank statement in `digital_log.csv` (columns `Date`, `Memo`, `Amount`) against a list of expected members in `members_list.json` (keys `name`, `expected`). The script must map messy memos to expected names (for example, 'Alishba Z' and 'Alishba Zahid' should map to 'Alishba Zahid'). It should output: (1) individual member payment status (Paid, Underpaid, Overpaid), (2) unmatched transactions, and (3) a financial summary showing total deposits, matched amounts, unmatched funds, and roster collection deficit."*

---

## 🎯 Verification (Baseline vs Script)

Before relying on the script, we verify the calculations by hand:

1. **Roster Collection Deficit**:
   * *Hand Calculation*: 
     * Target total: **`$500.00`** ($100.00 * 5 members).
     * Reconciled paid total: 
       * Alishba Zahid: `100.00 + 100.00` = `$200.00`
       * Zainab Ali: `$100.00`
       * Hamza Khan: `$100.00`
       * Laiba Fatima: `$80.00`
       * Bilal Ahmed: `$100.00`
       * Total matched = **`$580.00`**.
     * Since total matched ($580.00) exceeds expected target ($500.00), the deficit for the roster is **`$0.00`** (though individually, Laiba Fatima is underpaid by `$20.00` and Alishba Zahid is overpaid by `$100.00`).
   * *Script Result*: Matches exactly (shows Roster Collection Deficit: `$0.00` and flags Laiba underpaid and Alishba overpaid).

2. **Total Digital Deposits**:
   * *Hand Calculation*: Sum of all CSV amounts = `100.00 + 100.00 + 100.00 + 80.00 + 100.00 + 100.00 + 50.00` = **`$630.00`**.
   * *Script Result*: Matches exactly (`$630.00`).

---

## ⚙️ Running the Script
Run the script using:
```bash
python reconcile.py
```
