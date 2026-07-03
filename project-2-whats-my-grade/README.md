# Project 2: What's My Grade, Really

## 🔍 The Problem
School grading applications often only show simple averages, failing to account for complex syllabus grading rules such as category weighting (Quizzes 20%, Assignments 10%, Midterm 30%, Final Exam 40%), dropping the lowest score, or dynamic replacement rules. We need a script to calculate the exact running grade and determine the exact score needed on the Final Exam to secure target grades.

---

## 🤖 AI Tool Used
- **Antigravity AI (powered by Gemini)**

---

## 📝 Prompts Used

### Initial Prompt
> *"Write a Python script that reads a student's scores from `scores.json` and calculates their current running grade and target final exam requirements. The grading policy states: (1) Quizzes are 20% of the total grade, and the lowest quiz score is dropped. (2) Assignments are 10% of the total grade. (3) Midterm is 30% of the total grade. (4) The Final Exam is 40% of the total grade. The script must report: (a) average score per category, (b) current weighted score out of 60 possible points, (c) running grade percentage, and (d) final exam score required to achieve overall targets of 90%, 85%, 80%, and 70%."*

---

## 🎯 Verification (Baseline vs Script)

Before relying on the script, we verify the calculations by hand:

1. **Current Running Grade**:
   * *Quizzes*: `[80, 70, 90, 85]` -> Drop `70` -> `[80, 90, 85]` -> Average = **`85.00%`**.
   * *Assignments*: `[90, 95, 88]` -> Average = **`91.00%`**.
   * *Midterm*: **`85.00%`**.
   * *Weighted points calculation*:
     * Quizzes: `85.00 * 0.20` = **`17.00`**
     * Assignments: `91.00 * 0.10` = **`9.10`**
     * Midterm: `85.00 * 0.30` = **`25.50`**
     * Sum = **`51.60`** out of 60 possible points.
   * *Current Running Grade Percentage*: `51.60 / 0.60` = **`86.00%`**.
   * *Script Result*: Matches exactly (`86.00%`).

2. **Final Exam Target for A (90%)**:
   * *Hand Calculation*: `FinalExam = (90 - 51.60) / 0.40` = `38.40 / 0.40` = **`96.00%`**.
   * *Script Result*: Matches exactly (`96.00%`).

---

## ⚙️ Running the Script
Run the script using:
```bash
python grade_calculator.py
```
