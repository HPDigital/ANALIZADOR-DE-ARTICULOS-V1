"""
ANALIZADOR DE ARTICULOS V1
"""

#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openai import OpenAI
import fitz  # PyMuPDF
# Configuración de la clave de la API de OpenAI

client = OpenAI(api_key="YOUR_API_KEY_HERE")


# Función para leer el contenido del archivo
def extraer_texto_pdf(ruta_pdf):
    # Abrir el documento PDF
    documento = fitz.open(ruta_pdf)

    # Recopilar el texto de cada página
    texto_completo = ""
    for pagina in documento:
        texto_completo += pagina.get_text()

    # Cerrar el documento
    documento.close()
    return texto_completo


# Función para interactuar con ChatGPT y obtener el análisis del documento
def analizar_documento(contenido):
    response = client.chat.completions.create(
        model="gpt-4-turbo",  # Utiliza el modelo más reciente disponible
        messages=[
            {"role": "system", "content": "Eres un experto en redaccion de articulos cientificos y estas asistiendo con un análisis de un documento científico."},
            {"role": "user", "content": f"Hola, ¿podrías ayudarme con el análisis de este artículo científico que adjunto? Necesito lo siguiente: y el articulo en cuation es. {contenido}"},
            {"role": "user", "content": f"""Citación en formato APA versión 7: Por favor, proporciona la citación completa del artículo según las normas APA versión 7.
            \n\nResumen del artículo: Elabora un resumen conciso del contenido del artículo, destacando los puntos clave y los hallazgos principales.
            \n\nObjetivo del artículo: Indica cuál es el objetivo principal del estudio que se discute en el artículo.
            \n\nMetodología utilizada: Indica cual es la metodología que el autor indica que se usa para esta investigación.
            \n\nLectura preliminar:Elabora un informe de la Lectura preliminar para evaluar pertinencia.
            \n\nAnálisi detallado:Elabora un informe del análisis detallado de cada sección del artículo.
            \n\nInform de evaluación:Elabora un informe de la evaluación crítica de métodos y resultados.
            \n\nSintesisi de información:Elabora una síntesis de información encontrada.
            \n\nContextualización:Elabora la contextualización en la literatura existente.
            \n\nReflexion:Elabora la reflexión sobre implicaciones y futuras direcciones.
            \n\nRedaccion: Elabora la redacción del manuscrito de revisión.
            \n\nRevision:Elabora un inform sebre la revisión y edición del manuscrito.
            \n\nFeedbak:Elabora un informaosbre los Feedback de colegas. 
            \n\n{contenido}"""},              
        ],
        #max_tokens=30048
    )
    return response.choices[0].message.content

# Ruta del archivo local (ajustar según sea necesario)
ruta_archivo = r"C:\Users\HP\Downloads\documento.pdf"

# Leer el contenido del documento
contenido = extraer_texto_pdf(ruta_archivo)

# Obtener el análisis del documento
analisis = analizar_documento(contenido)

# Imprimir el análisis
print(analisis)


# In[ ]:






if __name__ == "__main__":
    pass
