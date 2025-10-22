import os
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
except Exception:  # dotenv es opcional, pero recomendado
    load_dotenv = None  # type: ignore


def load_env(env_path: Optional[str] = None) -> None:
    """
    Carga variables de entorno desde un archivo .env si está disponible.
    """
    if load_dotenv is None:
        return
    # Busca .env en el cwd o ruta provista
    if env_path:
        load_dotenv(dotenv_path=env_path, override=False)
        return
    # Busca .env en el cwd
    cwd_env = Path.cwd() / ".env"
    if cwd_env.exists():
        load_dotenv(dotenv_path=str(cwd_env), override=False)


def get_openai_api_key() -> Optional[str]:
    """Obtiene la API key desde OPENAI_API_KEY si existe."""
    return os.getenv("OPENAI_API_KEY")

