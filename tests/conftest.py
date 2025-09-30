import sys
from pathlib import Path

# Добавляем корень репозитория в PYTHONPATH, чтобы можно было импортировать пакет.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
