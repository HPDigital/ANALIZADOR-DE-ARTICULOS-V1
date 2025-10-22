from typing import Optional

import fitz  # PyMuPDF


def leer_pdf(ruta_pdf: str) -> str:
    """
    Extrae texto plano de todas las páginas de un PDF.
    """
    doc = fitz.open(ruta_pdf)
    try:
        partes = []
        for pagina in doc:
            partes.append(pagina.get_text())
        return "\n\n".join(partes)
    finally:
        doc.close()


def truncar_texto(texto: str, max_chars: Optional[int] = None) -> str:
    """
    Trunca el texto a `max_chars` si se indica.
    """
    if max_chars is None or max_chars <= 0:
        return texto
    if len(texto) <= max_chars:
        return texto
    # Añade indicación de truncado al final
    sufijo = "\n\n[Texto truncado para análisis por límite de tamaño]"
    return texto[: max_chars - len(sufijo)] + sufijo

