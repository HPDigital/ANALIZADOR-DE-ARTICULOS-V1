import argparse
import sys
from pathlib import Path

from .config import load_env, get_openai_api_key
from .pdf_reader import leer_pdf, truncar_texto
from .analyzer import analizar_documento, DEFAULT_MODEL


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="analizador-articulos",
        description="Analiza un artículo científico en PDF usando OpenAI.",
    )
    p.add_argument("pdf", type=str, help="Ruta al archivo PDF a analizar")
    p.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Modelo de OpenAI a usar (por defecto: {DEFAULT_MODEL})",
    )
    p.add_argument(
        "--max-chars",
        type=int,
        default=30000,
        help="Máximo de caracteres a enviar al modelo (truncado seguro)",
    )
    p.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Límite de tokens de salida (opcional)",
    )
    p.add_argument(
        "--output",
        type=str,
        default=None,
        help="Archivo de salida para guardar el análisis (opcional)",
    )
    p.add_argument(
        "--env",
        type=str,
        default=None,
        help="Ruta al archivo .env (opcional)",
    )
    return p


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    parser = build_parser()
    args = parser.parse_args(argv)

    # Carga variables de entorno (.env)
    load_env(args.env)
    api_key = get_openai_api_key()
    if not api_key:
        parser.error(
            "No se encontró OPENAI_API_KEY. Define la variable de entorno o usa un archivo .env"
        )

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        parser.error(f"No existe el archivo: {pdf_path}")

    # Lee y trunca el texto si es necesario
    texto = leer_pdf(str(pdf_path))
    texto = truncar_texto(texto, args.max_chars)

    # Llamada al modelo
    try:
        analisis = analizar_documento(
            contenido=texto, api_key=api_key, model=args.model, max_tokens=args.max_tokens
        )
    except Exception as e:
        parser.error(f"Error al invocar OpenAI: {e}")
        return 2

    # Salida
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(analisis, encoding="utf-8")
        print(f"✔ Análisis guardado en: {out_path}")
    else:
        print(analisis)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

