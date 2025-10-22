from typing import List, Optional

from openai import OpenAI


DEFAULT_MODEL = "gpt-4-turbo"  # configurable desde CLI


def _mensajes_analisis(contenido: str) -> List[dict]:
    """
    Construye los mensajes para el análisis del artículo en español.
    """
    instrucciones = (
        "Eres un experto en redacción de artículos científicos y estás asistiendo con el "
        "análisis de un documento científico. Responde en español con secciones claras."
    )
    pedido = (
        "Cita en formato APA (7ª edición): Proporciona la cita completa.\n\n"
        "Resumen del artículo: Resume de forma concisa, destacando puntos clave y hallazgos.\n\n"
        "Objetivo del artículo: Indica el objetivo principal del estudio.\n\n"
        "Metodología: Describe la metodología utilizada.\n\n"
        "Lectura preliminar: Informe breve para evaluar pertinencia.\n\n"
        "Análisis detallado: Análisis por secciones del artículo.\n\n"
        "Evaluación crítica: Evalúa métodos y resultados (fortalezas/limitaciones).\n\n"
        "Síntesis de información: Integra los hallazgos clave.\n\n"
        "Contextualización: Relaciona con la literatura existente.\n\n"
        "Reflexión: Implicaciones y futuras líneas de investigación.\n\n"
        "Redacción del manuscrito de revisión: Esboza estructura propuesta.\n\n"
        "Revisión y edición: Sugerencias de mejora.\n\n"
        "Feedback de colegas: Preguntas útiles para revisión por pares.\n\n"
        "Analiza el siguiente contenido del artículo:\n\n"
        f"{contenido}"
    )

    return [
        {"role": "system", "content": instrucciones},
        {"role": "user", "content": pedido},
    ]


def analizar_documento(
    contenido: str,
    api_key: str,
    model: str = DEFAULT_MODEL,
    max_tokens: Optional[int] = None,
) -> str:
    """
    Llama a la API de OpenAI para analizar el documento.
    """
    client = OpenAI(api_key=api_key)
    kwargs = {}
    if max_tokens is not None and max_tokens > 0:
        kwargs["max_tokens"] = max_tokens

    resp = client.chat.completions.create(
        model=model,
        messages=_mensajes_analisis(contenido),
        **kwargs,
    )
    return resp.choices[0].message.content or ""

