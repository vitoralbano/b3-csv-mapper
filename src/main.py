import argparse
from pathlib import Path
from lib.b3 import b3mapper

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

target_dir = Path(args.path)

if not target_dir.exists():
    print("The target dir doesn't exist")
    raise SystemExit(1)


b3 = b3mapper.B3Mapper()

def build_output(entry):
    size = entry.stat().st_size
    name = entry.name
    print(f"{file} - {size:>6d}")

for entry in target_dir.iterdir():
    if entry.is_file():
        b3.parse_earnings(entry)
        