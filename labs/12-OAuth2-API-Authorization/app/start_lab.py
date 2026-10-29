"""Create an isolated Python environment, install pinned dependencies, start the lab."""
from pathlib import Path
import subprocess
import sys
import venv
root = Path(__file__).resolve().parent
folder = root / '.venv'
python = folder / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
try:
    if not python.exists():
        print('Creating the local Python environment...', flush=True)
        venv.EnvBuilder(with_pip=True).create(folder)
    marker = folder / '.requirements-installed'
    requirements = (root / 'requirements.txt').read_text()
    if not marker.exists() or marker.read_text() != requirements:
        subprocess.run([str(python), '-m', 'pip', 'install', '-r', str(root / 'requirements.txt')], check=True)
        marker.write_text(requirements)
    subprocess.run([str(python), str(root / 'server.py')], check=True, cwd=root)
except (OSError, subprocess.CalledProcessError) as e:
    print('Lab could not start. Check Python 3.11 or newer, internet access, and the message above.')
    sys.exit(1)
except KeyboardInterrupt:
    pass
