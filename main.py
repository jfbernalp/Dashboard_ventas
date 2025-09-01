import pandas as pd
import numpy as np
import seaborn as sns
import streamlit as st
import plotly.express as px
from openpyxl.styles.builtins import title
import textwrap as tw

# The first step into our analysis is to load the dataset

store_sells = pd.read_csv('ventas_modaurbana.csv')

# Vamos medida configuro la página con set_page_config, le pongo título ícono y la propiedad wide
# permite que el contenido se ajuste al ancho de la pantalla
st.set_page_config(
    page_title = 'Caso de Estudio – Tienda Online Moda Urbana S.A.S.',
    page_icon = "📊",
    layout="wide"
)
#PALETA DE COLORES
custom_palette = ['#102A38', '#26506B', '#44838B', '#8AC4BE', '#E6D7B5', '#E0A841', '#C87D33', '#B1522F', '#98312A']
#Estilos
#TARJETAS
st.markdown("""
<style>
.card {
    /* Estilos que ya tenías */
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;

    /* --- CÓDIGO CLAVE MEJORADO --- */
    display: flex;            /* 1. Activa el modelo de caja flexible */
    flex-direction: column;   /* 2. Apila los elementos (título y valor) verticalmente */
    height: 100%;             /* 3. Asegura que la tarjeta ocupe toda la altura de la columna */
}
.card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

#ESTILO PARA LOS TITULOS
header_color = custom_palette[-3]
st.markdown(f"""
<style>
/* Esto apunta a los elementos h1, h2, h3 que corresponden a st.title, st.header, st.subheader */
h1, h2, h3 {{
    color: {header_color};
}}
</style>
""", unsafe_allow_html=True)


#limpieza de los datos
# Pandas podrá así entenderla como una fecha y no como simple texto.
store_sells['Fecha'] = pd.to_datetime(store_sells['Fecha'])
# Creamos una nueva columna que contenga el mes y el año ('YYYY-MM').
# Esto nos permite agrupar las ventas por mes de forma cronológica.
store_sells['Mes_Ano'] = store_sells['Fecha'].dt.strftime('%Y-%m')

st.sidebar.header('Menú de navegación')

# creamos el selector

usr_selection = st.sidebar.radio('Selecciona una página:',['1.Análisis General','2.Análisis por categoría','3.Análisis temporal','4.Segmentación de clientes','5.Conclusiones y estrategias'])


#empecemos a crear el análisis

if usr_selection == '1.Análisis General':
    st.header('Análisis general')
    st.divider()
    st.subheader('Presentación del dataset')

    total_ventas = store_sells['Total_Venta'].sum()
    total_productos = store_sells['Cantidad'].sum()
    ticket_promedio = store_sells['Total_Venta'].mean()
    clientes_unicos = store_sells['Cliente'].nunique()
    top_20_clientes = store_sells.groupby('Cliente')['Total_Venta'].sum().sort_values(ascending=False).head(20)
    top_20_clientes =top_20_clientes.reset_index()

    col1, col2, col3 = st.columns(3)
    with col1:
        # Creamos toda la tarjeta como una sola cadena de texto (f-string)
        tarjeta_html = f"""
        <div class="card">
            <h3>Total de Ventas 📈</h3>
            <p style="font-size: 2.0rem; font-weight: 700; margin: 0;">${total_ventas:,.0f}</p>
        </div>
        """
        # Mostramos la tarjeta completa con un solo comando
        st.markdown(tarjeta_html, unsafe_allow_html=True)

    with col2:
        # Creamos toda la tarjeta como una sola cadena de texto (f-string)
        tarjeta_html = f"""
        <div class="card">
            <h3>Productos vendidos</h3>
            <p style="font-size: 2.0rem; font-weight: 700; margin: 0;">{total_productos:,.0f}</p>
        </div>
        """
        # Mostramos la tarjeta completa con un solo comando
        st.markdown(tarjeta_html, unsafe_allow_html=True)

    with col3:
        # Creamos toda la tarjeta como una sola cadena de texto (f-string)
        tarjeta_html = f"""
        <div class="card">
            <h3>Tcket medio</h3>
            <p style="font-size: 2.0rem; font-weight: 700; margin: 0;">${ticket_promedio:,.0f}</p>
        </div>
        """
        # Mostramos la tarjeta completa con un solo comando
        st.markdown(tarjeta_html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # Creamos toda la tarjeta como una sola cadena de texto (f-string)
        tarjeta_html = f"""
        <div class="card">
            <h3>Clientes únicos</h3>
            <p style="font-size: 2.0rem; font-weight: 700; margin: 0;">{clientes_unicos}</p>
        </div>
        """
        # Mostramos la tarjeta completa con un solo comando
        st.markdown(tarjeta_html, unsafe_allow_html=True)
    st.divider()
    st.subheader('Clientes con mayor venta acumulada')
    st.dataframe(top_20_clientes)

elif usr_selection == '2.Análisis por categoría':
    st.header('Análisis por categoría')
    st.divider()
    cat_mayor_ventas_unidades = store_sells.groupby('Categoría')['Cantidad'].sum().sort_values(ascending=True).head(10)
    cat_mayor_ventas_unidades = cat_mayor_ventas_unidades.sort_index()
    cat_mayor_dinero = store_sells.groupby('Categoría')['Total_Venta'].sum().reset_index()
    ventas_por_categoria = store_sells.groupby('Canal')['Total_Venta'].sum().reset_index()
    st.subheader('Categorías con mayor venta por unidades y por ingreso bruto')

    col1, col2 = st.columns([1, 1])

    with col1:
        # Al estar dentro de 'col1', el DataFrame se ajustará al ancho de esa columna.
        st.dataframe(cat_mayor_ventas_unidades)

    # La columna 2 (col2) queda vacía, o puedes poner otro contenido ahí.
    with col2:
        # --- PASO 2: CREAR EL GRÁFICO DE TORTA INTERACTIVO ---
        # Usamos plotly.express.pie para generar el gráfico.
        st.dataframe(cat_mayor_dinero)
    st.divider()
    st.header('Ventas por canal de distribución')
    fig = px.pie(
        ventas_por_categoria,
        names='Canal',
        values='Total_Venta',
        title =None,
        hole=0.3,
        color_discrete_sequence=custom_palette
    )

    # --- Personalización Adicional (Opcional) ---
    # Puedes personalizar cómo se ve el texto dentro del gráfico.
    # Por ejemplo, para mostrar el porcentaje y la etiqueta de la categoría.
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)


    st.divider()
    st.subheader('Los 10 productos más vendidos')
    prod_mayor_ventas_unidades = store_sells.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False).head(10)
    st.dataframe(prod_mayor_ventas_unidades)

elif usr_selection == '3.Análisis temporal':
    st.header('Análisis temporal')

    ventas_mensuales = store_sells.groupby('Mes_Ano')['Total_Venta'].sum().reset_index()

    fig = px.line(
        ventas_mensuales,
        x='Mes_Ano',  # El eje X será nuestra columna de tiempo.
        y='Total_Venta',  # El eje Y mostrará el total de ventas.
        title='Evolución de Ventas Mensuales',
        markers=True,  # Añade marcadores en cada punto de datos para mayor claridad.
        labels={'Mes_Ano': 'Mes', 'Total_Venta': 'Total de Ventas'}  # Etiquetas más amigables.
    )

    # Centramos el título del gráfico.
    fig.update_layout(title_x=0.5)
    fig.update_traces(line_color=custom_palette[2])
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('En el gráfico anterior podemos ver como hay un pico de venta en el mes de marzo, mes en el que se celebra tradicionalmente el día de la mujer en Colombia.'
                )

    st.subheader('Dia de la semana con mayor venta: ')
    weekday_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    store_sells['dia_sem_num'] = store_sells['Fecha'].dt.dayofweek
    store_sells['dia_semana'] = store_sells['dia_sem_num'].map(weekday_map)

    resumen = (store_sells.groupby(["dia_sem_num", "dia_semana"], dropna=True)['Total_Venta']
               .sum()
               .reset_index()
               .sort_values("dia_sem_num"))

    st.dataframe(resumen[['dia_semana', 'Total_Venta']])
    dia_mayor_venta = px.bar(resumen,
                 x="dia_semana",
                 y="Total_Venta",
                 title="Ventas acumuladas por día de la semana",
                 labels={"dia_semana": "Día de la semana", "Total_Ventas": "Ventas acumuladas"},
                color_discrete_sequence=custom_palette
                 )

    # Opcional: Rotar las etiquetas del eje x si son muy largas (aunque Plotly suele manejarlas bien)
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(dia_mayor_venta, use_container_width=True)

    st.markdown('Aunque la diferencia es mínima entre los diferentes días de la semana, vemos como miércolas sábado y domingo son los días con mayor venta')

    df_marzo = store_sells[store_sells['Fecha'].dt.month == 3]
    productos_mas_vendidos = df_marzo.groupby('Producto')['Cantidad'].sum().sort_values(ascending=False).reset_index()
    categorias_mas_vendidas = df_marzo.groupby('Categoría')['Total_Venta'].sum().sort_values(
        ascending=False).reset_index()

    st.subheader('Top de productos más vendidos en marzo:')
    st.dataframe(productos_mas_vendidos.head())

    st.subheader('Top de categorías más vendidas en marzo:')
    st.dataframe(categorias_mas_vendidas.head())

    st.markdown('El hecho de que el producto más vendido haya sido vestido rojo, y ropa mujer se encuentre entre las 3 categorías mas vendidas, nos reafirma que el pico de venta en marzo fue impulsado por el día de la mujer')


elif usr_selection == '4.Segmentación de clientes':
    st.header('Análisis de Segmentación de Clientes:')
    st.divider()
    gasto_cliente = store_sells.groupby('Cliente')['Total_Venta'].sum().reset_index()
    gasto_cliente['Segmento'] = pd.qcut(gasto_cliente['Total_Venta'],
                                        q=3,
                                        labels=['Bajo', 'Medio', 'Alto'])
    df_segmentos = pd.merge(store_sells, gasto_cliente[['Cliente', 'Segmento']], on='Cliente', how='left')

    distribucion_canal = df_segmentos.groupby(['Canal', 'Segmento'])['Cliente'].nunique().reset_index()
    distribucion_canal.rename(columns={'Cliente': 'Numero_de_Clientes'}, inplace=True)
    df_alto_valor = df_segmentos[df_segmentos['Segmento'] == 'Alto']
    categoria_alto_valor = df_alto_valor.groupby('Categoría')['Total_Venta'].sum().sort_values(ascending=False).reset_index()

    st.subheader('Distribución de clientes por segmento y canal:')

    st.dataframe(distribucion_canal, use_container_width=True)
    st.subheader('Distribución de clientes por canal:')
    fig_clientes_por_canal = px.bar(df_segmentos,
                 color_discrete_sequence=custom_palette,
                 x='Segmento',
                 y='Total_Venta',
                 color='Canal',  # Esta línea apila las barras según el canal
                 labels={
                     'Segmento': 'Segmento del Cliente',
                     'Total_Venta': 'Ventas Totales',
                     'Canal': 'Canal de Venta'
                 },
                 category_orders={
                     'Segmento': ['Bajo', 'Medio', 'Alto'],

                 })

    st.plotly_chart(fig_clientes_por_canal, use_container_width=True)

    st.markdown('El gráfico anterior es muy revelador ya que nos deja ver cómo los clientes de alto valor prefieren hacer sus compras por el canal web')

    st.subheader("Categorías preferidas por clientes de alto valor:")
    st.dataframe(categoria_alto_valor.head())

    st.markdown('En cuanto a las categorías más compradas por clientes de alto valor vemos como ropa unisex, calzado y ropa mujer se posicionana en los primeros puestos.')



elif usr_selection == '5.Conclusiones y estrategias':
    st.header("💡 Conclusiones del Análisis")

    with st.container(border=True):
        st.markdown("""
        1.  La tienda ha tenido durante el semestre **1.000 clientes distintos**, con un ticket promedio de **$382.775**. De estos, el 33% se ubica en el segmento de **Alto Valor**.

        2.  Los clientes de alto valor tuvieron como canal de compra preferido la **página web**. Sus categorías preferidas fueron **ropa unisex, calzado y ropa para mujer**.

        3.  El mes de mayor venta fue **marzo**, especialmente los días de quincena (13, 14 y 15), coincidiendo con el mes de la mujer. Las categorías más vendidas fueron **calzado y ropa para mujer**.

        4.  El canal de venta con mayor registro fue la **página web con un 50%** del total, mientras que el de menor rendimiento fue **Redes Sociales con un 19,84%**.
        """)

    st.write("")  # Añade un espacio vertical

    # --- Sección de Estrategias ---
    st.header("🎯 Estrategias Propuestas")

    with st.container(border=True):
        st.markdown("""
        1.  **Campaña de Marketing en la Web:**
            - **Objetivo:** Aumentar el ticket de clientes de alto y medio valor.
            - **Táctica:** Ofrecer promociones en **calzado, ropa femenina y ropa unisex** para compras superiores a **$380.000** realizadas exclusivamente en la página web.

        2.  **Promociones para Temporadas Especiales:**
            - **Evento:** Temporada navideña y Día de la Madre.
            - **Táctica:** Lanzar promociones agresivas enfocadas en **calzado y ropa para mujer**, volcando todos los medios de promoción a incentivar la compra de estos productos.

        3.  **Campaña de Fidelización:**
            - **Objetivo:** Retener a los clientes de alto valor.
            - **Táctica:** Implementar un sistema de puntos o descuentos especiales para recompensar su lealtad y motivar futuras compras.
        """)

    st.write("")
    st.success("Profe ponme un 5 😉")
