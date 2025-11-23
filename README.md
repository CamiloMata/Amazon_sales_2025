🛒 Dashboard de Ventas de Amazon 2025
Este proyecto es un dashboard interactivo construido con Streamlit para visualizar y analizar un conjunto de datos ficticio de ventas de Amazon del año 2025. La aplicación permite a los usuarios filtrar los datos y explorar métricas clave, tendencias de ventas y rendimiento de productos.

👁️Vista Previa

![demo del dashboard](viewsales.gif)

🚀 Características Principales
Métricas Dinámicas: Muestra el promedio de ventas mensuales y la calificación (rating) promedio general.

Filtro Interactivo en Sidebar: Permite filtrar todo el dashboard por el estado de entrega (Delivered, Pending, Returned o General).

Visualizaciones Interactivas (con Plotly):

Ventas por Categoría: Un gráfico de barras que muestra las ventas totales (INR) por categoría de producto.

Ventas por Método de Pago: Un gráfico de pastel (donut) que muestra la distribución de las ventas según el método de pago.

Evolución de Ventas Mensuales: Un gráfico de líneas que muestra la tendencia de las ventas a lo largo del tiempo, con una línea que marca el promedio mensual.

Ranking de Productos: Una tabla de datos (dataframe) que muestra los productos ordenados por sus ventas totales de mayor a menor.

Carga de Datos Optimizada: Utiliza @st.cache_data de Streamlit para cargar el set de datos una sola vez y mejorar el rendimiento.

🛠️ Requisitos e Instalación
Para ejecutar este dashboard localmente, necesitarás Python 3.7+ y las siguientes librerías:

streamlit

pandas

plotly

Puedes instalar todas las dependencias ejecutando:

Bash

pip install streamlit pandas plotly
📂 Archivo de Datos
Este script está diseñado para funcionar con un archivo CSV llamado amazon_sales_2025_INR.csv.

Asegúrate de que este archivo se encuentre en el mismo directorio que el script dashboard.py. El archivo CSV debe contener (al menos) las siguientes columnas:

Date (para análisis de series temporales)

Delivery_Status (para el filtro)

Total_Sales_INR (para métricas y gráficos)

Review_Rating (para métricas)

Product_Category (para gráficos)

Payment_Method (para gráficos)

Product_Name (para el ranking)

🏃 Cómo Ejecutar el Dashboard
Asegúrate de tener todas las librerías instaladas (pip install ...).

Coloca tu archivo amazon_sales_2025_INR.csv en la misma carpeta que dashboard.py.

Abre tu terminal o línea de comandos.

Navega hasta el directorio del proyecto.

Ejecuta el siguiente comando:

Bash

streamlit run dashboard.py
Streamlit iniciará un servidor web local y abrirá automáticamente el dashboard en tu navegador predeterminado.




