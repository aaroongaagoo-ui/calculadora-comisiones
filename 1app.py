import streamlit as st
import math

st.set_page_config(layout="wide")

st.title("💼 Calculadora Avanzada de Comisiones")

# -------------------------
# FUNCIONES
# -------------------------
def fmt_num(v):
    return f"{v:,.2f}" if math.isfinite(v) else "N/A"

def fmt_pct(v):
    return f"{v:.2f}%"

# -------------------------
# INPUT VARIABLES
# -------------------------

NUM_VARIABLES = 6
rows = []

st.markdown("## 📋 Variables de Comisión")

for i in range(NUM_VARIABLES):
    col1, col2, col3, col4, col5 = st.columns(5)

    nombre = col1.text_input(f"Nombre {i+1}", f"Variable {i+1}", key=f"n{i}")
    meta = col2.number_input(f"Meta {i+1}", min_value=0.0, key=f"m{i}")
    cumplimiento = col3.number_input(f"Cumplimiento {i+1}", min_value=0.0, key=f"c{i}")
    monto = col4.number_input(f"Monto {i+1}", min_value=0.0, key=f"mo{i}")

    if meta > 0:
        pct = (cumplimiento / meta) * 100
        col5.markdown(f"**{fmt_pct(pct)}**")
    else:
        col5.markdown("—")

    rows.append({
        "nombre": nombre,
        "meta": meta,
        "cumplimiento": cumplimiento,
        "monto": monto
    })

# -------------------------
# SIMULADOR
# -------------------------

st.markdown("---")
st.markdown("## 📊 Simulación de desempeño")

for row in rows:

    if row["meta"] == 0:
        continue

    meta = row["meta"]
    cumplimiento = row["cumplimiento"]

    porcentaje = (cumplimiento / meta) * 100

    meta_90 = meta * 0.9

    dias_totales = 30
    dias_transcurridos = 15
    dias_restantes = dias_totales - dias_transcurridos

    ritmo_actual = cumplimiento / dias_transcurridos if dias_transcurridos > 0 else 0
    proyeccion = cumplimiento + (ritmo_actual * dias_restantes)
    proyeccion_pct = (proyeccion / meta) * 100

    gap = max(0, meta_90 - cumplimiento)

    cumplira = proyeccion >= meta_90

    # BARRA
    bar_actual = min(100, porcentaje)
    bar_proy = min(100, proyeccion_pct)

    color_actual = "#22c55e" if cumplira else "#f87171"
    color_proy = "#bbf7d0" if cumplira else "#fecaca"

    st.markdown(f"### {row['nombre']}")

    # ✅ BARRA VISUAL
    st.markdown(f"""
    <div style="position:relative;height:10px;background:#f1f5f9;border-radius:9999px;overflow:hidden;">
        <div style="position:absolute;left:0;width:{bar_proy:.1f}%;background:{color_proy};height:100%;"></div>
        <div style="position:absolute;left:0;width:{bar_actual:.1f}%;background:{color_actual};height:100%;"></div>
        <div style="position:absolute;left:90%;width:2px;background:#ea580c;height:100%;"></div>
    </div>

    <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-top:4px;">
        <span>Actual: <b>{porcentaje:.2f}%</b></span>
        <span style="color:#ea580c;">Meta 90%</span>
        <span>Proyección: <b>{proyeccion_pct:.2f}%</b></span>
    </div>
    """, unsafe_allow_html=True)

    # ✅ TARJETAS
    adicional = (proyeccion - meta_90) if cumplira else gap
    ritmo_necesario = gap / dias_restantes if dias_restantes > 0 else 0

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px;">

        <div style="background:#f8fafc;padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Ritmo actual</div>
            <div style="font-weight:bold;">{fmt_num(ritmo_actual)}</div>
        </div>

        <div style="background:#f8fafc;padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Proyección</div>
            <div style="font-weight:bold;color:{'#15803d' if cumplira else '#b91c1c'};">
                {fmt_num(proyeccion)}
            </div>
        </div>

        <div style="background:{'#f0fdf4' if cumplira else '#fff1f2'};padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">
                {'Excedente proyectado' if cumplira else 'Faltante'}
            </div>
            <div style="font-weight:bold;color:{'#15803d' if cumplira else '#b91c1c'};">
                {fmt_num(adicional)}
            </div>
        </div>

        <div style="background:{'#f8fafc' if cumplira else '#fff7ed'};padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Ritmo necesario</div>
            <div style="font-weight:bold;color:{'#94a3b8' if cumplira else '#ea580c'};">
                {"En ritmo" if cumplira else fmt_num(ritmo_necesario)}
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)
