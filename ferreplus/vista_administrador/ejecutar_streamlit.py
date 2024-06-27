import sys
import os
from pathlib import Path
import streamlit as st

# Obtén la dirección del directorio actual
current_dir = Path(__file__).resolve().parent
print("Current directory:", current_dir)

# Navega hacia arriba tres niveles para llegar al directorio que contiene 'Ferreplus'
base_dir = current_dir.parent.parent.parent
print("Base directory:", base_dir)

# Añade el directorio 'Ferreplus' al sys.path
ferreplus_dir = base_dir / 'Ferreplus'
sys.path.append(str(ferreplus_dir))
print("Ferreplus directory:", ferreplus_dir)

# Añade el directorio que contiene 'settings.py' al sys.path
settings_dir = ferreplus_dir / 'ferreplus'
sys.path.append(str(settings_dir))
print("Settings directory:", settings_dir)

print("sys.path:", sys.path)
print("Contents of Ferreplus directory:", os.listdir(ferreplus_dir))
print("Contents of settings directory:", os.listdir(settings_dir))

# Configura el entorno de Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from vista_usuario.models import Intercambio, Publicacion, Oferta, Sucursal

def main():
    st.title("Estadísticas de FerrePlus")

    # Sección de intercambios y montos
    col1, col2 = st.columns(2)

    with col1:
        st.header("Intercambios")

        # Gráfico de intercambios por categoría
        with st.expander("Más intercambios por categoría"):
            intercambios_por_categoria = {}

            categorias = Publicacion.CATEGORIA_CHOICES
            for categoria, _ in categorias:
                intercambios = Intercambio.objects.filter(base__categoria=categoria).count()
                intercambios_por_categoria[categoria] = intercambios

            st.bar_chart(intercambios_por_categoria)

        # Gráfico de intercambios por fecha y hora
        with st.expander("Más intercambios por fecha y hora"):
            intercambios_por_fecha_hora = {}

            intercambios = Intercambio.objects.all()
            for intercambio in intercambios:
                fecha_hora = intercambio.fecha_intercambio.strftime('%Y-%m-%d %H:%M')
                if fecha_hora in intercambios_por_fecha_hora:
                    intercambios_por_fecha_hora[fecha_hora] += 1
                else:
                    intercambios_por_fecha_hora[fecha_hora] = 1

            st.line_chart(intercambios_por_fecha_hora)

        # Gráfico de intercambios por sucursal
        with st.expander("Más intercambios por sucursal"):
            intercambios_por_sucursal = {}

            intercambios = Intercambio.objects.all()
            for intercambio in intercambios:
                sucursal = intercambio.sucursal.nombre if intercambio.sucursal else "Sin sucursal"
                if sucursal in intercambios_por_sucursal:
                    intercambios_por_sucursal[sucursal] += 1
                else:
                    intercambios_por_sucursal[sucursal] = 1

            st.bar_chart(intercambios_por_sucursal)

    with col2:
        st.header("Ganancias")

        # Gráfico de montos por sucursal (ejemplo ficticio)
        with st.expander("Mayores montos por sucursal"):
            montos_por_sucursal = {}

            # Aquí podrías hacer una consulta adecuada para calcular los montos por sucursal
            for sucursal in Sucursal.objects.all():
                montos_por_sucursal[sucursal.nombre] = calcular_monto_sucursal(sucursal)

            st.bar_chart(montos_por_sucursal)

        # Gráfico de montos por fecha (ejemplo ficticio)
        with st.expander("Mayores montos por fecha"):
            montos_por_fecha = {}

            # Aquí podrías hacer una consulta adecuada para calcular los montos por fecha
            montos_por_fecha["2023-01-01"] = 5000
            montos_por_fecha["2023-01-02"] = 7000
            montos_por_fecha["2023-01-03"] = 3000

            st.line_chart(montos_por_fecha)

        # Gráfico de montos por categoría (ejemplo ficticio)
        with st.expander("Mayores montos por categoría"):
            montos_por_categoria = {}

            # Aquí podrías hacer una consulta adecuada para calcular los montos por categoría
            for categoria, _ in Publicacion.CATEGORIA_CHOICES:
                montos_por_categoria[categoria] = calcular_monto_categoria(categoria)

            st.bar_chart(montos_por_categoria)

def calcular_monto_sucursal(sucursal):
    # Lógica para calcular montos por sucursal
    return 5000  # Ejemplo ficticio

def calcular_monto_categoria(categoria):
    # Lógica para calcular montos por categoría
    return 3000  # Ejemplo ficticio

if __name__ == "__main__":
    main()
