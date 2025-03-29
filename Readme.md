# SIRIUS

SIRIUS es una plataforma integral para la gestión de drones en la atención inmediata de incidentes urbanos. Utilizando análisis de video en tiempo real y reportes generados con el LLM Gemini, la solución permite responder de manera rápida y precisa ante emergencias, facilitando la toma de decisiones de las autoridades y mejorando la seguridad de la ciudad.

---

## Inspiración

El proyecto nace de la preocupación ante el incremento de emergencias en áreas urbanas como Querétaro, y de la convicción de que muchas situaciones críticas pueden mitigarse mediante respuestas anticipadas y eficientes. Cada integrante del equipo aportó una perspectiva única, impulsando la integración de tecnología avanzada y enfoques innovadores para proteger vidas y reducir riesgos tanto para ciudadanos como para autoridades.

---

## ¿Qué Hace SIRIUS?

- **Gestión de Drones Autónomos:** Despliega drones de forma rápida a la zona del incidente, garantizando una respuesta inmediata.
- **Análisis en Tiempo Real:** Utiliza modelos de visión artificial (como YOLO) para detectar objetos, incendios, humo y otros indicadores críticos en situaciones de emergencia.
- **Generación de Reportes Inteligentes:** Emplea el LLM Gemini para elaborar reportes detallados y precisos, ofreciendo recomendaciones prácticas para una intervención eficaz.
- **Monitoreo y Control:** Proporciona una interfaz intuitiva para visualizar en tiempo real la operación de los drones, definir rutas automáticas y revisar información visual y reportes generados.

> **Nota Operativa:** El análisis y reporte que genera SIRIUS está diseñado para servir como una evaluación preliminar, realizada **antes de enviar recursos humanos a la escena**. Esto permite que las autoridades reciban un informe detallado de la situación, con recomendaciones sobre la magnitud del incidente y las acciones a seguir, optimizando el despliegue de equipos de emergencia y asegurando una respuesta más coordinada y eficiente.

---

## Arquitectura del Proyecto

SIRIUS se compone de tres pilares fundamentales:

1. **Interfaz de Usuario (Front-End):**
   - Desarrollada con **React** y **TypeScript**, la interfaz permite monitorear drones, visualizar rutas y acceder a reportes y datos en tiempo real.
   - Se han incorporado componentes visuales intuitivos para facilitar la interacción y la toma de decisiones.

2. **Módulo de Análisis Inteligente (Back-End y Machine Learning):**
   - Implementado en **Python**, se emplean modelos avanzados como **YOLO** para el procesamiento y análisis de video.
   - La integración con el LLM **Gemini** permite transformar las detecciones en reportes inteligentes, optimizando la interpretación de los datos visuales.
   - Se ha realizado un exhaustivo fine-tuning de los hiperparámetros del modelo para mejorar la precisión y velocidad del análisis, incluso en condiciones de iluminación variable.

3. **Infraestructura de Servidores:**
   - Se cuenta con un **servidor central** que coordina la asignación y monitoreo de drones basándose en parámetros críticos como proximidad, autonomía y disponibilidad.
   - La comunicación se extiende a **subestaciones**, asegurando que cada dron sea gestionado de manera óptima y segura.

---

## Tecnologías Utilizadas

- **Hardware y SDK:**
  - Capa de abstracción modular para manejar comandos de navegación, telemetría y transmisión de video a través de SDKs de DJI o OpenSource.

- **Back-End:**
  - **Python** y **FastAPI** para el desarrollo del servidor central.
  - Integración con bases de datos **MongoDB** para el manejo de información en tiempo real.

- **Machine Learning y Visión Artificial:**
  - Modelos de detección basados en **YOLO** para identificar incidentes específicos.
  - Ajuste y fine-tuning de modelos para lograr detecciones precisas y rápidas.

- **Front-End:**
  - **React** y **TypeScript** para crear una interfaz de usuario moderna y responsiva.
  - Diseño intuitivo que permite monitorear la operación de los drones y visualizar reportes de forma clara.

- **Generación de Reportes:**
  - Uso del LLM **Gemini** para transformar las detecciones en reportes inteligentes y comprensibles.

---

## Desafíos y Soluciones

- **Integración del DJI SDK:**  
  La limitada documentación y los protocolos cerrados del DJI SDK representaron un reto considerable. Se optó por desarrollar una capa de abstracción modular en Python, lo que permitió definir interfaces generales para comandos y adaptarlas a distintos SDKs, garantizando compatibilidad y seguridad en el sistema.

- **Optimización del Modelo YOLO:**  
  Inicialmente, se enfrentaron problemas de velocidad y precisión en el procesamiento en tiempo real. A través de una exhaustiva investigación en literatura académica y ajustes en el tamaño de entrada y hiperparámetros del modelo, se logró mejorar significativamente la eficiencia y exactitud de las detecciones.

- **Comunicación y Seguridad en Tiempo Real:**  
  Asegurar una transmisión de datos robusta y segura entre drones, servidores y la interfaz de usuario fue clave para el éxito del proyecto. Se implementaron protocolos y estrategias de conexión que permitieron una operación coordinada y confiable.

---

## Logros y Aprendizajes

- **Desarrollo Integral en Tiempo Limitado:**  
  Se logró construir una plataforma robusta y escalable durante el Hackathon Troyano 2025, demostrando la capacidad del equipo para innovar bajo presión.

- **Colaboración y Trabajo Multidisciplinario:**  
  La integración de diversas tecnologías y la colaboración entre expertos en hardware, software y machine learning permitieron superar retos técnicos complejos.

- **Mejora Continua y Adaptabilidad:**  
  La experiencia adquirida en la optimización de modelos y la integración de SDKs ha fortalecido la capacidad del equipo para enfrentar futuros desafíos tecnológicos.

---

## Próximos Pasos

- **Integración con Drones Avanzados:**  
  Ampliar la compatibilidad de la plataforma con drones más especializados y de última generación.

- **Pruebas Exhaustivas:**  
  Realizar tests simultáneos con múltiples subestaciones para garantizar la robustez del sistema en entornos reales.

- **Optimización de la Transmisión en Tiempo Real:**  
  Perfeccionar la comunicación y análisis en vivo, buscando reducir latencias y mejorar la precisión de las detecciones.

- **Colaboración con Expertos y Autoridades:**  
  Establecer diálogos con profesionales y organismos competentes para adaptar la plataforma a diversas necesidades y escenarios de emergencia.

---

*SIRIUS aspira a ser una herramienta revolucionaria en la gestión de emergencias, combinando innovación tecnológica con un fuerte impacto social para proteger vidas y mejorar la seguridad en nuestras ciudades.*
