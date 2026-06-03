import streamlit as st
import math

st.set_page_config(layout="wide")

st.title("💼 Calculadora Avanzada de Comisiones")

# -------------------------
# FUNCIONES
# -------------------------

def fmt_num(v):
    return f"{v:,.2f}" if math.isfinite(v) else "N/A"

# -------------------------
# INPUT
# -------------------------

rows = []

for i in range(3):
    cols = st.columns(4)
    
    nombre = cols[0].text_input(f"Nombre {i+1}", f"Variable {i+1}", key=f"n{i}")
    meta = cols[1].number_input(f"Meta {i+1}", 0.0, key=f"m{i}")
    cumpl = cols[2].number_input(f"Cumplimiento {i+1}", 0.0, key=f"c{i}")
    monto = cols[3].number_input(f"Monto {i+1}", 0.0, key=f"mo{i}")
    
    rows.append({
        "nombre": nombre,
        "meta": meta,
        "cumplimiento": cumpl,
        "monto": monto
    })

# -------------------------
# PROCESO
# -------------------------

st.markdown("### 📊 Simulación")

for row in rows:
    
    if row["meta"] == 0:
        continue
    
    meta = row["meta"]
    cumpl = row["cumplimiento"]
    
    ratio = cumpl / meta
    pct = ratio * 100
    
    needed = meta * 0.9
    projected = cumpl + 10
    projected_pct = (projected / meta) * 100
    
    gap = max(0, needed - cumpl)
    
    will_commission = projected >= needed
    
    # colores
    bar_actual = min(100, pct)
    bar_projected = min(100, projected_pct)
    
    bar_color = "#22c55e" if will_commission else "#f87171"
    bar_proj_color = "#bbf7d0" if will_commission else "#fecaca"

    st.markdown(f"### {row['nombre']}")

    # ✅ BARRA CORREGIDA
    st.markdown(f"""
    <div style="position:relative;height:10px;background:#f1f5f9;border-radius:9999px;overflow:hidden;margin-bottom:0.3rem;">
        <div style="position:absolute;left:0;width:{bar_projected:.1f}%;background:{bar_proj_color};height:100%;"></div>
        <div style="position:absolute;left:0;width:{bar_actual:.1f}%;background:{bar_color};height:100%;"></div>
        <div style="position:absolute;left:90%;width:2px;background:#ea580c;height:100%;"></div>
    </div>

    <div style="display:flex;justify-content:space-between;font-size:0.8rem;">
        <span>Actual: <b>{pct:.2f}%</b></span>
        <span style="color:#ea580c;">90% mínimo</span>
        <span>Proyección: <b>{projected_pct:.2f}%</b></span>
    </div>
    """, unsafe_allow_html=True)

    # ✅ CARDS CORREGIDOS
    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:10px;">

        <div style="background:#f8fafc;padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Ritmo actual</div>
            <div style="font-weight:bold;">{fmt_num(cumpl)}</div>
        </div>

        <div style="background:#f8fafc;padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Proyección</div>
            <div style="font-weight:bold;color:{'#15803d' if will_commission else '#b91c1c'};">
                {fmt_num(projected)}
            </div>
        </div>

        <div style="background:{'#f0fdf4' if will_commission else '#fff1f2'};padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">
                {'Excedente' if will_commission else 'Faltante'}
            </div>
            <div style="font-weight:bold;color:{'#15803d' if will_commission else '#b91c1c'};">
                {fmt_num(projected - needed if will_commission else gap)}
            </div>
        </div>

        <div style="background:{'#f8fafc' if will_commission else '#fff7ed'};padding:10px;border-radius:6px;">
            <div style="font-size:0.7rem;color:#64748b;">Ritmo necesario</div>
            <div style="font-weight:bold;color:{'#94a3b8' if will_commission else '#ea580c'};">
                {"En ritmo" if will_commission else fmt_num(gap)}
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)
``