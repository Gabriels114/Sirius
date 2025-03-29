# Código mejorado para detección combinada usando YOLOv8 (objetos generales + fuego)

import cv2
import pandas as pd
from ultralytics import YOLO

# Carga modelo general (coches, personas, etc.)
modelo_general = YOLO('models/yolov8n.pt')

# Carga modelo especializado en fuego
modelo_fuego = YOLO('models/kedy-50.pt')

# Video original del dron
video_path = "videos/insendio.mp4"
cap = cv2.VideoCapture(video_path)

# Información del video
fps = cap.get(cv2.CAP_PROP_FPS)

# DataFrame para reporte
reporte = []
frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1
    tiempo_actual = frame_id / fps
    minutos, segundos = divmod(tiempo_actual, 60)
    tiempo_formateado = f"{int(minutos)}:{int(segundos):02d}"

    # Detección general (coches, personas, etc.)
    resultados_general = modelo_general.predict(frame, conf=0.3)

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

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Detección especializada (fuego)
    resultados_fuego = modelo_fuego.predict(frame, conf=0.3)

    for result in resultados_fuego:
        for box in result.boxes:
            cls = int(box.cls[0])
            label = modelo_fuego.names[cls]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            area = (x2 - x1) * (y2 - y1)

            reporte.append({
                "Frame": frame_id,
                "Tiempo": tiempo_formateado,
                "Tipo": "Fuego",
                "Etiqueta": label,
                "Confianza": round(conf, 2),
                "Area": area,
                "Coordenadas": (x1, y1, x2, y2)
            })

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Mostrar frame procesado
    cv2.imshow("Detección Combinada - Objetos y Fuego", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Exportar reporte a CSV
df_reporte = pd.DataFrame(reporte)
df_reporte.to_csv("reporte_deteccion_combinada.csv", index=False)
print("Reporte generado exitosamente: reporte_deteccion_combinada.csv")