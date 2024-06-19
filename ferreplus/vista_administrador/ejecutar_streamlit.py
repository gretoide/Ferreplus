import streamlit as st

# Función principal
def main():
    st.title("Estadísticas de FerrePlus")

    # Sección de intercambios y montos
    col1, col2 = st.columns(2)

    with col1:
        st.header("Intercambios")

        with st.expander("Más intercambios por categoría"):
            st.write("Gráfico de intercambios por categoría")
            # Aquí iría tu gráfico, por ejemplo:
            # st.bar_chart(datos_categoria)
        
        with st.expander("Más intercambios por fecha y hora"):
            st.write("Gráfico de intercambios por fecha y hora")
            # Aquí iría tu gráfico, por ejemplo:
            # st.line_chart(datos_fecha_hora)
        
        with st.expander("Más intercambios por sucursal"):
            st.write("Gráfico de intercambios por sucursal")
            # Aquí iría tu gráfico, por ejemplo:
            # st.bar_chart(datos_sucursal)

    with col2:
        st.header("Ganancias")

        with st.expander("Mayores montos por sucursal"):
            st.write("Gráfico de montos por sucursal")
            # Aquí iría tu gráfico, por ejemplo:
            # st.bar_chart(montos_sucursal)
        
        with st.expander("Mayores montos por fecha"):
            st.write("Gráfico de montos por fecha")
            # Aquí iría tu gráfico, por ejemplo:
            # st.line_chart(montos_fecha)
        
        with st.expander("Mayores montos por categoría"):
            st.write("Gráfico de montos por categoría")
            # Aquí iría tu gráfico, por ejemplo:
            # st.bar_chart(montos_categoria)

if __name__ == "__main__":
    main()
