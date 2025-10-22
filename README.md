# ANALIZADOR-DE-ARTÍCULOS-V1

CLI en Python para analizar artículos científicos en PDF con OpenAI.

## Características
- Lectura de PDFs con PyMuPDF
- Análisis vía Chat Completions (OpenAI Python SDK v1)
- Carga de credenciales desde `.env`
- CLI con opciones de modelo, límite de caracteres y salida a archivo

## Requisitos
```bash
pip install -r requirements.txt
```

## Configuración
Crea un archivo `.env` en la raíz del proyecto con tu credencial:
```
OPENAI_API_KEY=TU_API_KEY_AQUI
```

Nunca compartas tus API keys ni las subas al repositorio.

## Uso
Ejecuta desde la raíz del proyecto (CLI):
```bash
python -m src.analizador.cli RUTA_AL_PDF --output salida.txt
```

Opciones útiles:
- `--model`: modelo de OpenAI (por defecto: gpt-4-turbo)
- `--max-chars`: límite de caracteres enviados (por defecto: 30000)
- `--max-tokens`: límite de tokens de salida (opcional)
- `--output`: archivo donde guardar el análisis
- `--env`: ruta a un `.env` alternativo (opcional)

Ejemplo:
```bash
python -m src.analizador.cli ./docs/ejemplo.pdf --output analisis.txt --max-chars 50000
```

También puedes ejecutar el archivo de compatibilidad:
```bash
python "ANALIZADOR DE ARTICULOS V1.py" ./docs/ejemplo.pdf --output analisis.txt
```

### Interfaz Gráfica (Tkinter)
- Ejecutar la GUI:
```bash
python -m src.analizador.gui
```
- Funcionalidades:
  - Seleccionar PDF, configurar modelo y límites.
  - Usar `OPENAI_API_KEY` desde `.env` o introducir la clave manualmente.
  - Ver el resultado en pantalla y guardarlo en archivo.

## Estructura del Proyecto
```
ANALIZADOR-DE-ARTICULOS-V1/
├─ README.md
├─ requirements.txt
├─ ANALIZADOR DE ARTICULOS V1.py   # compatibilidad: reenvía a la CLI
└─ src/
   └─ analizador/
      ├─ __init__.py
      ├─ config.py
      ├─ pdf_reader.py
      ├─ analyzer.py
      ├─ cli.py
      └─ gui.py
```

## Notas
- El análisis puede truncar el texto si supera `--max-chars`.
- La calidad de la cita APA depende del texto disponible en el PDF.

## Licencia
MIT
