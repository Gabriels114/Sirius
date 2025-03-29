import pandas as pd
from PIL import Image
import google.generativeai as genai

# Configura tu clave de API de Gemini (reemplaza con tu clave real)
genai.configure(api_key="AIzaSyAf9WKK2FWpmBX4fd7C6o4Ycjs0M5pFCU0")

def generar_descripcion(frame_number, df, image_path):
    """Genera una descripción textual para un frame específico a partir del CSV."""
    detecciones_frame = df[df['frame'] == frame_number]
    descripcion = f"Frame {frame_number}: Posible incidente detectado.\n"
    if not detecciones_frame.empty:
        for index, row in detecciones_frame.iterrows():
            tipo = row['tipo']  # 'objeto general' o 'incendio'
            confianza = row['confianza']
            x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
            area = row['area']
            tiempo = row['tiempo']

            if tipo == 'incendio':
                descripcion += f"  - {tiempo} Fuego/Humo detectado con confianza {confianza:.2f}. Area: {area:.2f}\n"
            else:
                descripcion += f"  - {tiempo} Objeto {tipo} detectado con confianza {confianza:.2f}. Area: {area:.2f}\n"

        # agregar imagen
        img = Image.open(image_path)

        return descripcion, img  # imagen PIL

    return None, None


def generar_prompt(descripcion, imagen):
    """Crea el prompt para Gemini."""

    prompt = f"""
    Analiza la siguiente imagen y descripción de un incidente captado por un dron.

    Descripción:
    {descripcion}

    Imagen: (adjunta la imagen)

    Tu tarea es:

    1.  Generar un reporte formal y conciso del incidente.
    2.  Clasificar la gravedad del incidente como "Baja", "Media" o "Alta".  Considera la presencia de fuego/humo, la proximidad a estructuras/personas, y la extensión del área afectada.
    3.  Sugerir qué equipo de respuesta (Bomberos, Policía, Ambulancia, etc.) debe ser enviado al lugar, y justifica tu recomendación.

    Responde en formato de reporte formal, incluyendo la clasificación de gravedad y la sugerencia de equipo.
    """
    return prompt



def obtener_respuesta_gemini(prompt, image):
    """Obtiene la respuesta de Gemini a partir del prompt y la imagen."""
    model = genai.GenerativeModel('gemini-1.5-pro-latest') # Reemplaza con el modelo multimodal correcto

    # Preparar el contenido para el modelo multimodal
    contents = [prompt, image]  # Imagen debe ser un objeto PIL Image

    response = model.generate_content(contents)
    return response.text

# Ejemplo de uso:
prompt = generar_prompt(descripcion, image)
respuesta = obtener_respuesta_gemini(prompt, image)
print(respuesta)


# Ejemplo de uso:
df = pd.read_csv('reporte_deteccion_combinada.csv')
frame_ejemplo = 150  # Selecciona un frame con detección
descripcion, image = generar_descripcion(frame_ejemplo, df,
                                         'frame_150.jpg')  # Asegúrate de guardar los frames relevantes como imágenes.
if descripcion:
    print(descripcion)