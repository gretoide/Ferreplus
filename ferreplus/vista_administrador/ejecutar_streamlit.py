import django
import sys
import os
from pathlib import Path
import streamlit as st
from datetime import datetime, date
import matplotlib.pyplot as plt
import numpy as np

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

django.setup()

from vista_usuario.models import Intercambio, Publicacion, Oferta, Sucursal

def main():
    intercambios = Intercambio.objects.exclude(estado='PENDIENTE')

    st.title("Estadísticas de FerrePlus")

    # Sección de intercambios y montos
    col1, col2 = st.columns(2)

    with col1:
        st.header("Intercambios")

        with st.expander("Total de intercambios"):
            st.text(intercambios.count())

        # Gráfico de intercambios por categoría
        with st.expander("Intercambios por categoría"):
            intercambios_por_categoria = {}

            categorias = Publicacion.CATEGORIA_CHOICES
            for categoria, _ in categorias:
                intercambios_cate = intercambios.filter(
                    base__categoria=categoria).count()
                intercambios_por_categoria[categoria] = intercambios_cate

            st.bar_chart(intercambios_por_categoria)

        # Gráfico de intercambios por mes en el último año
        with st.expander("Intercambios en el último año"):
            anio = datetime.now().year
            inter_ultimo_anio = intercambios.filter(fecha_intercambio__year=anio)
            ultimo_anio = {mes: 0 for mes in [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]}

            meses = {
                1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
                5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
                9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
            }

            for inter in inter_ultimo_anio:
                fecha = inter.fecha_intercambio
                ultimo_anio[meses[fecha.month]] += 1

            st.line_chart(ultimo_anio)

        with st.expander("Proporciones de intercambios por estado"):
            cant_por_estado = {"CANCELADO": 0, "CANCELADO_AUSENTE": 0, "REALIZADO": 0}
            for inter in intercambios:
                if inter.estado in cant_por_estado:
                    cant_por_estado[inter.estado] += 1

            cant_final = [cant_por_estado["CANCELADO"], cant_por_estado["CANCELADO_AUSENTE"], cant_por_estado["REALIZADO"]]

            # Validar que todos los valores en cant_final sean válidos y numéricos
            cant_final = [v if isinstance(v, (int, float)) and v >= 0 else 0 for v in cant_final]

            # Asegurarse de que no todos los valores sean cero
            if sum(cant_final) == 0:
                st.warning("No hay datos suficientes para generar el gráfico de pastel.")
            else:
                labels = 'CANCELADO', 'CANCELADO AUSENTE', 'REALIZADO'
                colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
                explode = (0.08, 0.08, 0.08)  # Solo "explota" el primer segmento (A)

                fig, ax = plt.subplots()
                ax.pie(cant_final, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=140)

                ax.axis('equal')
                st.pyplot(fig)
                st.text(f"Realizados: {cant_por_estado['REALIZADO']} Cancelados: {cant_por_estado['CANCELADO']} Cancelados por ausente: {cant_por_estado['CANCELADO_AUSENTE']}")

        # Gráfico de intercambios por sucursal
        with st.expander("Intercambios por sucursal"):
            intercambios_por_sucursal = {}
            for intercambio in intercambios:
                sucursal = intercambio.sucursal.nombre if intercambio.sucursal else "Sin sucursal"
                intercambios_por_sucursal[sucursal] = intercambios_por_sucursal.get(sucursal, 0) + 1

            st.bar_chart(intercambios_por_sucursal)

        with st.expander("Intercambios en el último mes por sucursal"):
            intercambios_por_sucursal = {}
            fecha = datetime.today()
            anio, mes = fecha.year, fecha.month
            inter_ultimo_mes = intercambios.filter(fecha_intercambio__year=anio, fecha_intercambio__month=mes)

            for inter in inter_ultimo_mes:
                sucursal = inter.sucursal.nombre
                intercambios_por_sucursal[sucursal] = intercambios_por_sucursal.get(sucursal, 0) + 1

            st.bar_chart(intercambios_por_sucursal)

    with col2:
        st.header("Ganancias")

        with st.expander("Total de ganancia"):
            total = sum(float(inter.ganancia) for inter in intercambios if inter.ganancia)
            st.text(f"${total:.2f}")
            
        with st.expander("Total por categoría"):
            montos_por_categoria = {}

            for inter in intercambios:
                categoria = inter.base.categoria
                montos_por_categoria[categoria] = montos_por_categoria.get(categoria, 0) + float(inter.ganancia)

            st.bar_chart(montos_por_categoria)

        # Gráfico de ganancias por mes en el último año
        with st.expander("Ganancias en el último año"):
            anio = datetime.now().year
            inter_ultimo_anio = intercambios.filter(fecha_intercambio__year=anio)
            ultimo_anio = {mes: 0 for mes in [
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]}

            for inter in inter_ultimo_anio:
                fecha = inter.fecha_intercambio
                ultimo_anio[meses[fecha.month]] += float(inter.ganancia)

            st.line_chart(ultimo_anio)

        with st.expander("Proporción de ganancia por estado"):
            monto_por_estado = {"CANCELADO": 0, "CANCELADO_AUSENTE": 0, "REALIZADO": 0}
            for inter in intercambios:
                monto_por_estado[inter.estado] += float(inter.ganancia)

            cant_final = [monto_por_estado["CANCELADO"], monto_por_estado["CANCELADO_AUSENTE"], monto_por_estado["REALIZADO"]]

            # Validar que todos los valores en cant_final sean válidos y numéricos
            cant_final = [v if isinstance(v, (int, float)) and v >= 0 else 0 for v in cant_final]

            # Asegurarse de que no todos los valores sean cero
            if sum(cant_final) == 0:
                st.warning("No hay datos suficientes para generar el gráfico de pastel.")
            else:
                labels = 'CANCELADO', 'CANCELADO AUSENTE', 'REALIZADO'
                colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
                explode = (0.08, 0.08, 0.08)  # Solo "explota" el primer segmento (A)

                fig, ax = plt.subplots()
                ax.pie(cant_final, explode=explode, labels=labels, colors=colors,
                       autopct='%1.1f%%', shadow=True, startangle=140)

                ax.axis('equal')
                st.pyplot(fig)
                st.text(f"Realizados: {monto_por_estado['REALIZADO']} Cancelados: {monto_por_estado['CANCELADO']} Cancelados por ausente: {monto_por_estado['CANCELADO_AUSENTE']}")

        with st.expander("Montos por sucursal"):
            montos_por_sucursal = {}

            for inter in intercambios:
                sucursal = inter.sucursal.nombre
                montos_por_sucursal[sucursal] = montos_por_sucursal.get(sucursal, 0) + float(inter.ganancia)

            st.bar_chart(montos_por_sucursal)

        with st.expander("Montos mensuales por sucursal"):
            montos_por_sucursal = {}
            fecha = datetime.today()
            anio, mes = fecha.year, fecha.month
            inter_ultimo_mes = intercambios.filter(fecha_intercambio__year=anio, fecha_intercambio__month=mes)

            for inter in inter_ultimo_mes:
                sucursal = inter.sucursal.nombre
                montos_por_sucursal[sucursal] = montos_por_sucursal.get(sucursal, 0) + float(inter.ganancia)

            st.bar_chart(montos_por_sucursal)

if __name__ == "__main__":
    main()
