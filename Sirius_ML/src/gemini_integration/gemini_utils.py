# gemini_integration/gemini_utils.py

import os
import base64
import pandas as pd
from PIL import Image
from io import BytesIO

# La librería pública 'google.generativeai'
import google.generativeai as genai

# Configura tu API key (o hazlo desde main.py una sola vez)
API_KEY = os.getenv("GEMINI_API_KEY", "TU_API_KEY")
genai.configure(api_key=API_KEY)


def generar_descripcion(frame_number: int, df: pd.DataFrame, image_path: str):
    """
    Dada la información del CSV (detecciones), genera un texto descriptivo
    y retorna (descripcion, imagen_PIL).
    """
    # Filtra las detecciones de ese frame
    detecciones_frame = df[df['Frame'] == frame_number]
    if detecciones_frame.empty:
        return None, None

    descripcion = f"Frame {frame_number}: Posible incidente detectado.\n"
    for _, row in detecciones_frame.iterrows():
        tipo = row['Tipo']  # 'Objeto', 'Fuego', 'Humo', etc.
        etiqueta = row['Etiqueta']
        confianza = row['Confianza']
        coords = row['Coordenadas']  # (x1, y1, x2, y2)
        area = row['Area']
        tiempo = row['Tiempo']

        if tipo.lower() in ['fuego', 'humo']:
            descripcion += (
                f"- {tiempo} {tipo} detectado ({etiqueta}) "
                f"con confianza {confianza:.2f}. Área: {area:.2f}. {coords}\n"
            )
        else:
            descripcion += (
                f"- {tiempo} Objeto '{etiqueta}' con confianza {confianza:.2f}. "
                f"Área: {area:.2f}. {coords}\n"
            )

    # Cargamos la imagen
    pil_image = None
    try:
        pil_image = Image.open(image_path)
    except FileNotFoundError:
        print(f"[ADVERTENCIA] Imagen no encontrada: {image_path}")

    return descripcion, pil_image


def generar_prompt(descripcion: str) -> str:
    """
    Crea un prompt para Gemini a partir de la descripción textual generada.
    """
    prompt = f"""
    Analiza la siguiente descripción de un incidente captado por un dron:

    Descripción:
    {descripcion}

    Tu tarea es:

    1. Generar un reporte formal y conciso del incidente.
    2. Clasificar la gravedad del incidente (Baja, Media o Alta).
    3. Sugerir qué equipo de respuesta (Bomberos, Policía, Ambulancia, etc.)
       debe ser enviado al lugar, justificando la recomendación.

    Responde en un formato de reporte formal, incluyendo la clasificación de gravedad
    y la sugerencia de equipo.
    """
    return prompt.strip()


def obtener_respuesta_gemini(prompt: str, image: Image.Image = None, model_name: str = "gemini-1.5-flash") -> str:
    """
    Envía el prompt (y, opcionalmente, la imagen) al modelo de Gemini para obtener
    un reporte. Retorna el texto de la respuesta.

    Usamos `genai.GenerativeModel(model_name)` y `generate_content(...)`
    tal y como la guía sugiere.
    """
    # 1) Instanciamos el modelo
    model = genai.GenerativeModel(model_name)

    # 2) Creamos la lista de inputs
    #    La guía muestra que podemos pasar ["string", imagen_PIL] o un Content object.
    contents = []
    # Agrega el texto
    contents.append(prompt)

    # Agrega la imagen si existe
    if image is not None:
        contents.append(image)

    # 3) Llamamos a generate_content
    response = model.generate_content(contents)

    # 4) Retornamos la respuesta en texto
    return response.text
