import os
import shutil
import hashlib
import sys

def get_file_hash(filepath):
    """Calculate MD5 hash of a file to accurately identify duplicate contents."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()
    except Exception as e:
        print(f"  Error hashing {filepath}: {e}")
        return None

def analyze_directory(target_dir, size_threshold_mb=10.0):
    size_threshold_bytes = size_threshold_mb * 1024 * 1024
    
    analysis = {
        'duplicates': [], # List of file paths to remove
        'large_files': [], # List of (path, size_mb)
        'moves': [] # List of (src, dest_folder)
    }
    
    seen_hashes = {}
    
    # We only scan the top-level files in the messy folder to keep it simple and clean
    for item in os.listdir(target_dir):
        item_path = os.path.join(target_dir, item)
        if os.path.isdir(item_path):
            continue # Skip subdirectories (like output folders we create)
            
        # File Size check
        size_bytes = os.path.getsize(item_path)
        size_mb = size_bytes / (1024 * 1024)
        if size_bytes > size_threshold_bytes:
            analysis['large_files'].append((item_path, size_mb))
            
        # Hash check for duplicates
        file_hash = get_file_hash(item_path)
        if file_hash:
            if file_hash in seen_hashes:
                analysis['duplicates'].append((item_path, seen_hashes[file_hash]))
            else:
                seen_hashes[file_hash] = item_path
                
                # If not a duplicate, categorize it for moves
                ext = os.path.splitext(item)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif']:
                    dest_folder = 'Images'
                elif ext in ['.pdf', '.doc', '.docx', '.txt', '.xlsx']:
                    dest_folder = 'Documents'
                elif ext in ['.zip', '.tar', '.gz', '.rar']:
                    dest_folder = 'Archives'
                else:
                    dest_folder = 'Others'
                analysis['moves'].append((item_path, dest_folder))
                
    return analysis

def execute_plan(target_dir, analysis):
    # Create subdirectories
    for folder in ['Images', 'Documents', 'Archives', 'Others', 'Duplicates_Backup']:
        os.makedirs(os.path.join(target_dir, folder), exist_ok=True)
        
    # 1. Handle Duplicates (Move to Duplicates_Backup for safety instead of deleting)
    for duplicate_path, original_path in analysis['duplicates']:
        filename = os.path.basename(duplicate_path)
        dest = os.path.join(target_dir, 'Duplicates_Backup', filename)
        shutil.move(duplicate_path, dest)
        print(f"  Moved duplicate: {filename} -> Duplicates_Backup/")

    # 2. Handle Moves
    for src_path, folder in analysis['moves']:
        filename = os.path.basename(src_path)
        dest = os.path.join(target_dir, folder, filename)
        shutil.move(src_path, dest)
        print(f"  Moved file: {filename} -> {folder}/")

def main():
    target_dir = './mock_mess_backup'
    # We use a lower size threshold of 100 bytes for our dummy files so we can test the threshold flag easily!
    size_threshold_mb = 0.0001 # ~100 bytes
    
    print("=" * 60)
    print("SAFE FILE ORGANIZER & CLEANUP SUITE")
    print("=" * 60)
    
    if not os.path.exists(target_dir):
        print(f"Error: Target directory '{target_dir}' does not exist.")
        print("Please run this script from the project folder containing 'mock_mess_backup'.")
        return

    print(f"Scanning target directory: {os.path.abspath(target_dir)}")
    print(f"Large file size threshold set to: {size_threshold_mb * 1024 * 1024:.0f} bytes (~100B) for testing.")
    print("Analyzing files...\n")
    
    analysis = analyze_directory(target_dir, size_threshold_mb)
    
    # Present Dry-Run Report
    print("--- [DRY RUN PLAN] ---")
    print(f"1. Large Files Flagged (>{size_threshold_mb * 1024 * 1024:.0f} bytes):")
    if analysis['large_files']:
        for path, size in analysis['large_files']:
            print(f"  * [LARGE]: {os.path.basename(path)} ({size * 1024 * 1024:.1f} bytes)")
    else:
        print("  None.")
        
    print(f"\n2. Duplicate Files Detected (to be moved to Duplicates_Backup/):")
    if analysis['duplicates']:
        for duplicate_path, original_path in analysis['duplicates']:
            print(f"  * [DUPLICATE]: {os.path.basename(duplicate_path)} (matches original: {os.path.basename(original_path)})")
    else:
        print("  None.")
        
    print(f"\n3. File Reorganization Moves:")
    if analysis['moves']:
        for src_path, folder in analysis['moves']:
            print(f"  * [MOVE]: {os.path.basename(src_path)} -> {folder}/")
    else:
        print("  None.")
    print("----------------------\n")
    
    if not analysis['duplicates'] and not analysis['moves']:
        print("No actions to perform. Directory is already clean.")
        return

    # Interactive Safety Check
    try:
        confirm = input("WARNING: Would you like to execute the above plan? This will reorganize files. (y/n): ").strip().lower()
    except Exception:
        # Fallback if running in a non-interactive shell (like standard output testing)
        print("Non-interactive mode detected. Exiting. Set confirm to 'y' to force.")
        return

    if confirm == 'y':
        print("\nExecuting operations...")
        execute_plan(target_dir, analysis)
        print("\nReorganization complete. Your files are now sorted safely.")
    else:
        print("\nOperations cancelled. No files were modified.")
    print("=" * 60)

if __name__ == "__main__":
    main()
