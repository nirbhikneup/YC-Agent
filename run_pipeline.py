import os
import subprocess
import sys

SCRIPTS = [
    "scraper/yc_scraper.py",
    "scraper/hn_scraper.py",
    "link_companies.py"
]

def run_script(script):
    print(f"\n=== Running {script} ===")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        print(f"Error running {script}")
        sys.exit(result.returncode)

if __name__ == "__main__":
    print("Starting YC Agent Pipeline...")
    for script in SCRIPTS:
        run_script(script)
    print("\nPipeline complete!")
    print("Results: yc_agent.db and contacts.csv updated.")
