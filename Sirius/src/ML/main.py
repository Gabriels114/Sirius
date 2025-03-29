# main.py (versión adaptada)

import pandas as pd
import os

from Sirius_ML.src.ML.detection.detector import run_detection
from Sirius_ML.src.ML.gemini_integration.gemini_utils import (
    generar_descripcion,
    generar_prompt,
    obtener_respuesta_gemini
)
import google.generativeai as genai

genai.configure(api_key="AIzaSyAf9WKK2FWpmBX4fd7C6o4Ycjs0M5pFCU0")

def main():
    # -------------------------------------------------------------------------
    # 1) Ejecuta la detección con YOLO
    # -------------------------------------------------------------------------
    video_entrada = 'inputs/puente.MP4'
    modelo_general_path = 'models/yolov8n.pt'
    modelo_fuego_path   = 'models/last20.pt'

    csv_path = run_detection(
        video_entrada=video_entrada,
        modelo_general_path=modelo_general_path,
        modelo_fuego_path=modelo_fuego_path,
        output_base_folder='outputs',
        conf_general=0.35,
        conf_fuego=0.2
    )

    # -------------------------------------------------------------------------
    # 2) Generar reporte de Gemini para un frame específico
    # -------------------------------------------------------------------------
    # En este ejemplo, escogemos el frame 150, pero podrías usar frame_most_fire_id
    frame_ejemplo      = 150
    output_folder      = os.path.dirname(csv_path)  # Carpeta donde está el CSV
    image_ejemplo_path = os.path.join(output_folder, "frame_most_fire.jpg")

    df = pd.read_csv(csv_path)

    descripcion, pil_image = generar_descripcion(frame_ejemplo, df, image_ejemplo_path)
    if not descripcion:
        print(f"[INFO] No se encontraron detecciones en el frame {frame_ejemplo}.")
        return

    prompt_text = generar_prompt(descripcion)

    # Obtenemos respuesta de Gemini (puedes cambiar el modelo_name si deseas)
    respuesta = obtener_respuesta_gemini(
        prompt_text,
        pil_image,
        model_name="gemini-2.0-flash"
    )

    print("\n[REPORTE DE GEMINI]\n", respuesta)

    # -------------------------------------------------------------------------
    # 3) Guardar el reporte en un .txt en la misma carpeta de CSV/frames
    # -------------------------------------------------------------------------
    report_txt_path = os.path.join(output_folder, "gemini_report.txt")
    with open(report_txt_path, "w", encoding="utf-8") as f:
        f.write(respuesta)

    print(f"[INFO] Reporte de Gemini guardado en: {report_txt_path}")


if __name__ == "__main__":
    main()
