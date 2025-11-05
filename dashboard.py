import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuración de la página ---
st.set_page_config(
    page_title="Dashboard de Ventas de Amazon 2025",
    page_icon="🛒",
    layout="wide"
)

# --- Título del Dashboard ---
st.title("🛒 Dashboard de Ventas de Amazon 2025")

# --- Función para cargar datos (con caché para mejorar rendimiento) ---
@st.cache_data
def load_data(filepath):
    """
    Carga y procesa los datos del archivo CSV.
    """
    try:
        df = pd.read_csv(filepath)
        
        # --- Procesamiento de Datos ---
        # Convertir 'Date' a formato datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extraer mes y año para agrupación
        df['YearMonth'] = df['Date'].dt.to_period('M').astype(str)

        # --- CAMBIO ---
        # Ya NO filtramos por 'Delivered' aquí.
        # Devolvemos el dataframe completo.
        return df
    
    except FileNotFoundError:
        st.error(f"Error: No se pudo encontrar el archivo de datos en la ruta: {filepath}")
        return None
    except Exception as e:
        st.error(f"Error al cargar o procesar los datos: {e}")
        return None

# --- Cargar Datos ---
# df_base contendrá TODOS los datos, sin filtrar
df_base = load_data("amazon_sales_2025_INR.csv")

# --- INICIO DEL CAMBIO SOLICITADO (FILTRO EN SIDEBAR) ---
st.sidebar.header("Filtros del Dashboard")

filtro_estado = st.sidebar.selectbox(
    "Seleccionar Estado de Entrega:",
    options=['General', 'Delivered', 'Pending', 'Returned'],
    index=0 # 'General' será la opción por defecto
)

# Crear el dataframe 'df' dinámicamente basado en el filtro
if df_base is not None:
    if filtro_estado == 'General':
        df = df_base.copy()
    else:
        df = df_base[df_base['Delivery_Status'] == filtro_estado].copy()
else:
    df = None # Si la carga falló, df sigue siendo None
# --- FIN DEL CAMBIO SOLICITADO ---


# --- El resto del script AHORA usa el 'df' dinámico ---
if df is not None:
    
    # --- 1. Métricas Superiores (Requisito 2) ---
    st.header(f"Métricas Principales ({filtro_estado})")

    # --- CAMBIO MÉTRICAS ---
    # Añadimos un chequeo por si el df filtrado está vacío
    if not df.empty:
        num_meses = df['YearMonth'].nunique()
        
        if num_meses > 0:
            total_sales = df['Total_Sales_INR'].sum()
            promedio_ventas_mensuales = total_sales / num_meses
        else:
            promedio_ventas_mensuales = 0
        
        promedio_rating = df['Review_Rating'].mean()

    else:
        # Si el df está vacío (ej. filtro 'Pending' no tiene datos)
        promedio_ventas_mensuales = 0.0
        promedio_rating = 0.0
    # --- FIN CAMBIO MÉTRICAS ---

    # Presentar métricas en columnas
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Promedio de Ventas Mensuales (INR)",
            value=f"{promedio_ventas_mensuales:,.2f}"
        )
    with col2:
        st.metric(
            label="Promedio General de Calificación (Rating)",
            value=f"{promedio_rating:.2f} ★"
        )

    st.markdown("---") # Separador visual

    # --- 2. Visualizaciones Principales (Requisito 3 - Adaptado) ---
    st.header("Visualizaciones Principales")
    
    
    # Gráfico 1: Ventas Totales por Categoría de Producto
    st.subheader("Ventas Totales por Categoría de Producto")
    sales_by_category = df.groupby('Product_Category')['Total_Sales_INR'].sum().sort_values(ascending=False)
    fig_bar_category = px.bar(
        sales_by_category,
        x=sales_by_category.index,
        y='Total_Sales_INR',
        title="Ventas Totales por Categoría",
        labels={'Total_Sales_INR': 'Ventas Totales (INR)', 'Product_Category': 'Categoría'},
        template="plotly_white"
    )
    st.plotly_chart(fig_bar_category, use_container_width=True)

    # Dos columnas para los siguientes gráficos
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        # Gráfico 2: Ventas Totales por Método de Pago
        st.subheader("Ventas por Método de Pago")
        sales_by_payment = df.groupby('Payment_Method')['Total_Sales_INR'].sum().sort_values(ascending=False)
        fig_pie_payment = px.pie(
            sales_by_payment,
            names=sales_by_payment.index,
            values='Total_Sales_INR',
            title="Distribución de Ventas por Método de Pago",
            hole=0.3
        )
        st.plotly_chart(fig_pie_payment, use_container_width=True)

    with fig_col2:
        # Gráfico 3: Evolución de las Ventas Mensuales
        st.subheader("Evolución de Ventas Mensuales")
        sales_by_month = df.groupby('YearMonth')['Total_Sales_INR'].sum().reset_index()
        
        fig_line_sales = px.line(
            sales_by_month,
            x='YearMonth',
            y='Total_Sales_INR',
            title="Ventas Totales a lo largo del Tiempo",
            labels={'YearMonth': 'Mes', 'Total_Sales_INR': 'Ventas Totales (INR)'},
            markers=True # Añadir marcadores para ver los puntos de datos
        )
        
        # Añadir la línea de promedio mensual
        if promedio_ventas_mensuales > 0: # Solo mostrar la línea si hay datos
            fig_line_sales.add_hline(
                y=promedio_ventas_mensuales, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"Promedio Mensual ({promedio_ventas_mensuales:,.2f})",
                annotation_position="bottom right"
            )

        fig_line_sales.update_xaxes(tickangle=45)
        st.plotly_chart(fig_line_sales, use_container_width=True)

    st.markdown("---") # Separador visual

    # --- 3. Listado de Productos (Requisito 4) ---
    st.header("Ranking de Productos por Ventas")
    
    product_sales = df.groupby('Product_Name')['Total_Sales_INR'].sum()
    product_sales_sorted = product_sales.sort_values(ascending=False).reset_index()
    product_sales_sorted.columns = ['Nombre del Producto', 'Ventas Totales (INR)']
    product_sales_sorted['Ventas Totales (INR)'] = product_sales_sorted['Ventas Totales (INR)'].map('{:,.2f}'.format)
    
    st.dataframe(
        product_sales_sorted,
        use_container_width=True,
        hide_index=True
    )

else:
    st.error("No se pudieron cargar los datos. El dashboard no puede mostrarse.")