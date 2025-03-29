# detection/detector.py

import os
import cv2
import pandas as pd
from ultralytics import YOLO

def run_detection(video_entrada: str,
                  modelo_general_path: str,
                  modelo_fuego_path: str,
                  output_base_folder: str = 'outputs',
                  conf_general: float = 0.35,
                  conf_fuego: float = 0.35) -> str:
    """
    Ejecuta la detección tanto general como de fuego/humo en el video de entrada.
    Guarda el video de salida, el CSV de reporte y los frames relevantes.

    :param video_entrada: Ruta al video a procesar.
    :param modelo_general_path: Ruta al modelo YOLO (objetos generales).
    :param modelo_fuego_path: Ruta al modelo YOLO (fuego/humo).
    :param output_base_folder: Carpeta base donde se guardarán las salidas.
    :param conf_general: Umbral de confianza para detección general.
    :param conf_fuego: Umbral de confianza para detección especializada (fuego/humo).
    :return: La ruta del CSV generado.
    """

    video_basename = os.path.basename(video_entrada)
    video_name, ext = os.path.splitext(video_basename)

    # Carpeta de salida específica para este video
    output_folder = os.path.join(output_base_folder, f'{video_name}_outputs')
    os.makedirs(output_folder, exist_ok=True)

    video_salida = os.path.join(output_folder, f'{video_name}_output.mp4')
    csv_path = os.path.join(output_folder, f'{video_name}_output.csv')

    print("[INFO] Cargando modelos...")
    modelo_general = YOLO(modelo_general_path)
    modelo_fuego = YOLO(modelo_fuego_path)

    cap = cv2.VideoCapture(video_entrada)
    if not cap.isOpened():
        raise ValueError(f"[ERROR] No se pudo abrir el video {video_entrada}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Definimos 3 fotogramas fijos (aprox. 1/4, 1/2, 3/4 del total)
    frame_1 = total_frames // 4
    frame_2 = total_frames // 2
    frame_3 = (3 * total_frames) // 4

    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter(video_salida, fourcc, fps, (width, height))

    reporte = []
    frame_id = 0

    # Variables para el fotograma con más fuegos
    max_fire_detections = 0
    frame_most_fire = None
    frame_most_fire_id = -1


    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_id += 1
        tiempo_actual_seg = frame_id / fps
        minutos, segundos = divmod(tiempo_actual_seg, 60)
        tiempo_formateado = f"{int(minutos)}:{int(segundos):02d}"

        # Contador de fuegos en este frame
        fire_count = 0


        resultados_general = modelo_general.predict(frame, conf=conf_general)
        for result in resultados_general:
            for box in result.boxes:
                cls = int(box.cls[0])
                label = modelo_general.names[cls]
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)

                reporte.append({
                    "Frame": frame_id,
                    "Tiempo": tiempo_formateado,
                    "Tipo": "Objeto",
                    "Etiqueta": label,
                    "Confianza": round(conf, 2),
                    "Area": area,
                    "Coordenadas": (x1, y1, x2, y2)
                })

                # Dibuja en el frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


        resultados_fuego = modelo_fuego.predict(frame, conf=conf_fuego)
        for result in resultados_fuego:
            for box in result.boxes:
                cls = int(box.cls[0])
                label = modelo_fuego.names[cls]
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                area = (x2 - x1) * (y2 - y1)

                if label.lower() == "fire":
                    tipo = "Fuego"
                    color = (0, 0, 255)  # rojo
                    fire_count += 1
                elif label.lower() == "smoke":
                    tipo = "Humo"
                    color = (255, 0, 0)  # azul
                else:
                    tipo = "Desconocido"
                    color = (255, 255, 255)

                reporte.append({
                    "Frame": frame_id,
                    "Tiempo": tiempo_formateado,
                    "Tipo": tipo,
                    "Etiqueta": label,
                    "Confianza": round(conf, 2),
                    "Area": area,
                    "Coordenadas": (x1, y1, x2, y2)
                })

                # Dibuja en el frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # 2.3 Revisamos si este frame tuvo más fuego que el récord anterior
        if fire_count > max_fire_detections:
            max_fire_detections = fire_count
            frame_most_fire = frame.copy()
            frame_most_fire_id = frame_id

        # Guardamos el frame en el video de salida
        out.write(frame)

        # Guardamos los 3 fotogramas fijos (dibujados) si coincide con frame_1, frame_2 o frame_3
        if frame_id == frame_1:
            cv2.imwrite(os.path.join(output_folder, "frame_1.jpg"), frame)
        elif frame_id == frame_2:
            cv2.imwrite(os.path.join(output_folder, "frame_2.jpg"), frame)
        elif frame_id == frame_3:
            cv2.imwrite(os.path.join(output_folder, "frame_3.jpg"), frame)

        # Mostramos el frame en pantalla (opcional)
        cv2.imshow("Detección Combinada - Objetos, Humo y Fuego", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()


    df_reporte = pd.DataFrame(reporte)
    df_reporte.to_csv(csv_path, index=False)

    if frame_most_fire is not None:
        max_fire_path = os.path.join(output_folder, "frame_most_fire.jpg")
        cv2.imwrite(max_fire_path, frame_most_fire)
        print(f"[INFO] Frame con mayor número de fuegos: {frame_most_fire_id}")
        print(f"[INFO] Imagen guardada en: {max_fire_path}")

    print(f"[INFO] Reporte generado exitosamente: {csv_path}")
    print("[INFO] Video de salida guardado como:", video_salida)
    print(f"[INFO] Se guardaron frames relevantes en '{output_folder}'")

    # Devolvemos la ruta del CSV para que luego puedas usarlo en Gemini
    return csv_path
