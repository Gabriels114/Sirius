# Código completo optimizado para detección combinada (vehículos, personas, fuego) usando YOLOv8

import cv2
import pandas as pd
from ultralytics import YOLO

# Carga el modelo YOLOv8 especializado en detección de incendios (del proyecto del usuario)
modelo_yolo = YOLO(r'G:\Hackaton\Computer-Vision-Term-Project-main\Computer-Vision-Term-Project-main\object_recognition\kedy-50.pt')

# Video original del dron
video_path = "insendio.mp4"
cap = cv2.VideoCapture(video_path)

# DataFrame para reporte
reporte = []
frame_id = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_id += 1

    # Detección combinada con YOLOv8 (vehículos, personas, fuego)
    resultados = modelo_yolo.predict(frame, conf=0.3)

    for result in resultados:
        for box in result.boxes:
            cls = int(box.cls[0])
            label = modelo_yolo.names[cls]
            conf = float(box.conf[0])

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            reporte.append({
                "Frame": frame_id,
                "Etiqueta": label,
                "Confianza": round(conf, 2),
                "Coordenadas": (x1, y1, x2, y2)
            })

            color = (0, 0, 255) if label.lower() in ["fire", "fuego"] else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Mostrar frame procesado
    cv2.imshow("Detección YOLOv8 - Vehículos, Personas, Fuego", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Exportar reporte a CSV
df_reporte = pd.DataFrame(reporte)
df_reporte.to_csv("reporte_incendio_yolo8.csv", index=False)
print("Reporte generado exitosamente: reporte_incendio_yolo8.csv")
