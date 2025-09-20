import sys
import subprocess

# Get batch from command-line arguments, default to Summer 2024
batch = "Summer 2024"
if len(sys.argv) > 1:
    batch = sys.argv[1]

print(f"Starting YC Agent Pipeline for batch: {batch}\n")

# Scripts to run
SCRIPTS = [
    "scraper/yc_scraper.py",
    "scraper/hn_scraper.py",
    "link_companies.py"
]

def run_script(script, batch):
    print(f"\n=== Running {script} ===")
    subprocess.run([sys.executable, script, batch])

# Run each script
for script in SCRIPTS:
    run_script(script, batch)

print("\nPipeline complete!")
print("Results: yc_agent.db and contacts.csv updated.")
