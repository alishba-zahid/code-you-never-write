# Project 1: Money Detective

## 🔍 The Problem
We want to audit personal transaction logs to identify duplicate charges, recurring subscription bills (which are often easy to forget), and track month-over-month total spending. The rules for what counts as a duplicate or recurring subscription are personal, so custom code is used instead of third-party budgeting applications.

---

## 🤖 AI Tool Used
- **Antigravity AI (powered by Gemini)**

---

## 📝 Prompts Used

### Initial Prompt
> *"Write a Python script that reads a `transactions.csv` file with columns `Date`, `Description`, and `Amount`. The script should parse this file and do three things: (1) calculate the total spending for each month, (2) identify duplicate charges (same date, description, and amount), and (3) detect recurring monthly charges or potential subscriptions (same description and amount appearing across multiple months). Outlines must be clear and readable."*

---

## 🎯 Verification (Baseline vs Script)

Before relying on the script, we verify the output against two hand-calculated figures:

1. **July 2026 Total Spend**: 
   * *Hand Calculation*: `$15.49` (Netflix) + `$6.75` (Starbucks) + `$120.00` (Grocery) + `$45.00` (AWS) + `$50.00` (Gym) + `$85.00` (Restaurant) + `$85.00` (Duplicate Restaurant) + `$10.00` (GitHub Copilot) = **`$417.24`**.
   * *Script Result*: Matches exactly (`$417.24`).

2. **Flagged Duplicate Count**:
   * *Hand Verification*: 
     * `2026-06-05, Uber Ride, -$22.50` (2 entries)
     * `2026-07-22, Restaurant Lahore, -$85.00` (2 entries)
     * Total duplicate events: **`2`**.
   * *Script Result*: Matches exactly (flags the duplicate Uber Ride and Restaurant Lahore transactions).

---

## ⚙️ Running the Script
Run the script using:
```bash
python money_detective.py
```
