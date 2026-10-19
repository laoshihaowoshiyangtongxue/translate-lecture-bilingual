"""Copy this entire skill into a user-selected skills root, without overwriting anything."""
import argparse
from pathlib import Path
import shutil

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--skills-root', required=True, help='Directory containing skill directories')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()
source = Path(__file__).resolve().parents[1]
root = Path(args.skills_root).expanduser().resolve()
destination = root / source.name
if destination == source or source in destination.parents:
    raise ValueError('Destination cannot be inside the source skill')
if destination.exists():
    raise FileExistsError(f'Already exists; not overwritten: {destination}')
if not args.dry_run:
    root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'node_modules', '.venv'))
print(('Would install: ' if args.dry_run else 'Installed: ') + str(destination))
