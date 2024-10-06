import os
import subprocess

MAX_DEPTH = 3

APPS_DIR  = os.path.dirname(os.path.abspath(__file__))

print(MAX_DEPTH, APPS_DIR )

# Git diff command to check staged changes
def get_staged_files():
    try:
        result = subprocess.run(['git', 'diff', '--cached', '--name-status'], stdout=subprocess.PIPE, text=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Error running git diff: {e}")
        return []


# Function to check if a file is within max folder depth
def is_within_depth(file_path):
    depth = len(file_path.split(os.sep)) - len(APPS_DIR.split(os.sep))
    return depth <= MAX_DEPTH

# Function to detect new .py files
def detect_new_modules():
    staged_files = get_staged_files()
    new_modules = []
    for file_status in staged_files:
        status, file_path = file_status.split("\t")
        print(status,file_path)
        # Check only added (A) or renamed (R) files
        if status in ["A", "R"] and file_path.endswith(".py"):
            # Ensure the file is within the apps directory and within the depth limit
            if is_within_depth(file_path):
                new_modules.append(file_path)
    return new_modules

def main():
    new_modules = detect_new_modules()

    if new_modules:
        print("Detected newly added Python modules:")
        for module in new_modules:
            print(f" - {module}")
        print("Please verify the module addition before committing.")
        exit(1)  # Exit with non-zero status to prevent commit
    else:
        print("No new modules detected.")
        exit(0)  # Exit with zero status to allow commit

if __name__ == "__main__":
    main()