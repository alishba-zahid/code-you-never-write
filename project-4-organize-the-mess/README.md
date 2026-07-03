# Project 4: Organize the Mess (The Files You Forgot)

## 🔍 The Problem
Most computers accumulate massive digital clutter (downloads, temp files, duplicate photos, screenshots). Standard file cleaner programs can be invasive and unsafe. We need a script to safely scan a folder, locate exact duplicate files (using content hashes), flag files exceeding a size threshold, and group remaining files into subdirectories by category.

---

## 🛡️ Safety-First Design Checklist
To make sure no files are lost or damaged:
1. **Target Backup Copy**: The script is run only on a duplicated folder (`mock_mess_backup`) rather than the original messy source.
2. **Dry Run Plan**: The script must first scan the target folder and print a detailed proposal of all moves and duplicates.
3. **Interactive Gate**: No changes are executed until the user explicitly reviews the dry-run proposal and inputs `y` (yes) at the terminal.
4. **Safety Instead of Deletion**: Flagged duplicates are moved to a `Duplicates_Backup/` subfolder instead of being permanently deleted.

---

## 🤖 AI Tool Used
- **Antigravity AI (powered by Gemini)**

---

## 📝 Prompts Used

### Initial Prompt
> *"Write a Python script that organizes files in a directory safely. The script should: (1) check files for duplicate contents using MD5 hashes, (2) identify files larger than a specific threshold, and (3) group files into folders by extension (Images, Documents, Archives, Others). Crucially, the script must be safe: it must output a full dry-run plan listing every proposed file move and duplicate, and pause for interactive user approval ('y/n') before executing any file operations. Instead of deleting duplicates, move them to a 'Duplicates_Backup' folder."*

---

## 🎯 Verification (Baseline vs Script)

Before execution, we verify the dry-run plan on our test folder:

1. **Duplicate Detection Verification**:
   * *Roster of files*: `photo1.png` and `photo2.png` have the identical content `"ABCD"`.
   * *Script Result*: Matches exactly (flags `photo2.png` as a duplicate of `photo1.png`).

2. **Large File Flag Verification**:
   * *Threshold set*: `0.0001 MB` (~100 bytes).
   * *Target file*: `large_presentation.pdf` is `436 bytes`.
   * *Script Result*: Matches exactly (flags `large_presentation.pdf` as a large file, while skipping smaller files).

3. **Categorization Verification**:
   * `document.txt` -> `Documents/`
   * `photo1.png` -> `Images/`
   * `archive.zip` -> `Archives/`
   * `large_presentation.pdf` -> `Documents/` (since `.pdf` is mapped to Documents)
   * `photo2.png` -> `Duplicates_Backup/` (as duplicate)
   * *Script Result*: Matches exactly.

---

## ⚙️ Running the Script
Run the script using:
```bash
python organizer.py
```
