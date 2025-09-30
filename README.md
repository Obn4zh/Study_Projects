# Study Projects (Cryptography)

Набор учебных реализаций криптографических алгоритмов: RSA, ElGamal, ГОСТ.

> ⚠️ **Дисклеймер:** код предназначен только для обучения и демонстрации идей. Не используйте эти реализации в продакшене.

## Содержимое
- `RSA(Full).py`, `RSA(low).py`, `RSA(ЭП).py`
- `El Gamal.py`
- `ГОСТ28147-89(Full).py`
- `ГОСТ Р 34.10-94.py`
- `rsa.kt` (Kotlin эксперимент)
- `funcs.py` — вспомогательные функции

## Быстрый старт (Python)
```bash
git clone https://github.com/Obn4zh/Study_Projects.git
cd Study_Projects

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

python "RSA(Full).py"
```

## Тесты
```bash
pytest -q
```

## Идеи для развития
- Бенчмарки скорости
- Визуализация шагов алгоритмов (Streamlit/Gradio)
- Сравнение с промышленными библиотеками (`cryptography`, `PyNaCl`) — только как справка

## Лицензия
MIT — см. `LICENSE`.
