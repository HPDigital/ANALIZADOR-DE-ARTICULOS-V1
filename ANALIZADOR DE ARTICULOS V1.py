"""
Compatibilidad con el script original.

Ahora el proyecto expone una CLI:
    python -m src.analizador.cli RUTA_AL_PDF --output output.txt

Este archivo invoca la CLI con valores por defecto si se ejecuta directamente.
"""

from src.analizador.cli import main as cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())

