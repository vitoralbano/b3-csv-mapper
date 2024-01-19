import argparse
from pathlib import Path
from b3 import b3mapper

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

target_dir = Path(args.path)

if not target_dir.exists():
    print("The target dir doesn't exist")
    raise SystemExit(1)


b3 = b3mapper.B3Mapper()

for entry in target_dir.iterdir():
    if entry.is_file():
        b3.parse_earnings(entry)
        