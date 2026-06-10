"""
Calculadora Avanzada de Comisiones — Laureate
Herramienta financiera para equipos de ventas
"""

import streamlit as st
from dataclasses import dataclass
from typing import Literal
from datetime import date
import calendar
import math
import io
import csv

# ─────────────────────────────────────────────
# ESTILOS — paleta naranja profesional
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Calculadora de Comisiones",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    /* Fondo gris muy claro */
    .stApp { background-color: #f8fafc; }

    /* Botón principal naranja */
    .stButton > button[kind="primary"] {
        background-color: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 0.55rem 2rem !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #c2410c !important;
    }

    /* Botón secundario */
    .stButton > button[kind="secondary"] {
        background-color: transparent !important;
        border: 1.5px solid #fed7aa !important;
        color: #ea580c !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background-color: #fff7ed !important;
    }

    /* Ocultar barra superior de Streamlit */
    #MainMenu, footer, header { visibility: hidden; }

    /* Encabezado */
    .app-title {
        font-size: 2rem;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }
    .app-subtitle {
        color: #64748b;
        font-size: 1.05rem;
        margin-top: 0.15rem;
        margin-bottom: 1.5rem;
    }

    /* Tarjeta genérica */
    .card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid #f1f5f9;
    }

    /* Resultado total (naranja oscuro) */
    .total-card {
        background: #ea580c;
        border-radius: 8px;
        padding: 1.25rem 1.5rem;
        color: white;
        margin-top: 1rem;
    }
    .total-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #fed7aa;
        margin-bottom: 0.2rem;
    }
    .total-value {
        font-size: 1.9rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: white;
    }

    /* Badges */
    .badge-green  { background:#dcfce7; color:#15803d; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:600; }
    .badge-red    { background:#fee2e2; color:#b91c1c; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:600; }
    .badge-amber  { background:#fef3c7; color:#92400e; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:600; }
    .badge-gray   { background:#f1f5f9; color:#64748b; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:600; }
    .badge-orange { background:#fff7ed; color:#ea580c; padding:2px 8px; border-radius:9999px; font-size:0.75rem; font-weight:600; }

    /* Simulador */
    .sim-header {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-radius: 10px 10px 0 0;
        padding: 1rem 1.5rem;
    }
    .sim-title { font-size:1.05rem; font-weight:700; color:#7c2d12; }
    .sim-subtitle { font-size:0.82rem; color:#c2410c; margin-top:2px; text-transform: capitalize; }
    .sim-body {
        background: white;
        border: 1px solid #fed7aa;
        border-top: none;
        border-radius: 0 0 10px 10px;
        padding: 1rem 1.5rem;
    }
    .sim-var-name { font-size:0.9rem; font-weight:700; color:#1e293b; }
    .sim-stat-box {
        background: #f8fafc;
        border-radius: 6px;
        padding: 0.6rem 0.75rem;
        font-size: 0.78rem;
    }
    .sim-stat-label { color:#64748b; margin-bottom:2px; }
    .sim-stat-value { font-weight:700; color:#1e293b; }

    /* Columna de encabezado de tabla */
    .col-header {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #64748b;
        padding-bottom: 0.4rem;
    }

    /* Línea divisora */
    .divider { border-top: 1px solid #f1f5f9; margin: 0.75rem 0; }

    /* Resultado por variable */
    .var-result-row { display:flex; justify-content:space-between; align-items:center; padding: 0.35rem 0; }
    .var-result-name { font-weight:600; color:#334155; font-size:0.9rem; }
    .var-result-amount { font-weight:700; color:#0f172a; font-size:0.9rem; }
    .pct-green { color:#15803d; font-weight:600; font-size:0.8rem; }
    .pct-red   { color:#b91c1c; font-weight:600; font-size:0.8rem; }
    .pct-amber { color:#92400e; font-weight:600; font-size:0.8rem; }
    .pct-gray  { color:#94a3b8; font-weight:600; font-size:0.8rem; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LÓGICA DE NEGOCIO
# ─────────────────────────────────────────────
@dataclass
class VariableResult:
    nombre: str
    monto: float
    meta: float
    cumplimiento_val: float
    porcentaje: float
    resultado: float
    status: Literal["green", "red", "amber", "gray"]
    capped: bool


@dataclass
class CalculationResult:
    variables: list[VariableResult]
    total: float


def calcular_variables(rows: list[dict]) -> CalculationResult:
    """Replica exacta de calculator.ts → calcularVariables()."""
    variables_con_meta = [r for r in rows if r["meta"] > 0]

    # Paso 1: % cumplimiento y tope del 200 %
    computed = []
    for r in rows:
        pct = r["cumplimiento_val"] / r["meta"] if r["meta"] > 0 else 0.0
        capped = False
        if r["meta"] in (1, 2) and pct > 2.0:
            pct = 2.0
            capped = True
        computed.append({**r, "porcentaje": pct, "capped": capped})

    # Paso 2: ¿todas las variables alcanzan el 90 %?
    todas_90 = (
        len(variables_con_meta) > 0
        and all(v["porcentaje"] >= 0.90 for v in computed if v["meta"] > 0)
    )

    # Paso 3: resultado final y tope del 100 % si no todas son ≥ 90 %
    total = 0.0
    final_vars: list[VariableResult] = []

    for v in computed:
        pct_final = v["porcentaje"]
        capped = v["capped"]
        resultado = 0.0
        status: Literal["green", "red", "amber", "gray"] = "gray"

        if v["meta"] == 0:
            resultado = v["monto"]
            status = "gray"
        else:
            if pct_final >= 0.90:
                if len(variables_con_meta) > 1:
                    if pct_final > 1.0 and not todas_90:
                        pct_final = 1.0
                        capped = True
                resultado = v["monto"] * pct_final
                status = "amber" if capped else "green"
            else:
                resultado = 0.0
                status = "red"

        total += resultado
        final_vars.append(VariableResult(
            nombre=v["nombre"],
            monto=v["monto"],
            meta=v["meta"],
            cumplimiento_val=v["cumplimiento_val"],
            porcentaje=pct_final,
            resultado=resultado,
            status=status,
            capped=capped,
        ))

    return CalculationResult(variables=final_vars, total=total)


# ─────────────────────────────────────────────
# SIMULADOR AL CIERRE
# ─────────────────────────────────────────────
@dataclass
class SimRow:
    nombre: str
    has_meta: bool
    days_in_month: int
    days_elapsed: int
    days_remaining: int
    cumplimiento_actual: float
    meta: float
    needed_for_commission: float
    daily_pace_actual: float
    projected: float
    projected_pct: float
    gap: float
    daily_pace_needed: float
    will_commission: bool
    current_pct: float


def simulate(rows: list[dict], ref_date: date | None = None) -> tuple[date, int, int, int, str, list[SimRow]]:
    """Replica de simulator.ts → simulate()."""
    today = ref_date or date.today()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_elapsed = today.day
    days_remaining = days_in_month - today.day

    MONTHS_ES = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
    }
    month_label = f"{MONTHS_ES[today.month]} {today.year}"

    sim_rows: list[SimRow] = []
    for r in rows:
        meta = float(r["meta"] or 0)
        cumpl = float(r["cumplimiento_val"] or 0)

        if meta == 0:
            sim_rows.append(SimRow(
                nombre=r["nombre"], has_meta=False,
                days_in_month=days_in_month, days_elapsed=days_elapsed,
                days_remaining=days_remaining, cumplimiento_actual=cumpl,
                meta=0, needed_for_commission=0, daily_pace_actual=0,
                projected=cumpl, projected_pct=0, gap=0,
                daily_pace_needed=0, will_commission=True, current_pct=0,
            ))
            continue

        needed = meta * 0.90
        pace = cumpl / days_elapsed if days_elapsed > 0 else 0.0
        projected = cumpl + pace * days_remaining
        projected_pct = (projected / meta) * 100
        current_pct = (cumpl / meta) * 100
        gap = max(0.0, needed - cumpl)
        pace_needed = (
            gap / days_remaining if days_remaining > 0
            else (math.inf if gap > 0 else 0.0)
        )
        sim_rows.append(SimRow(
            nombre=r["nombre"], has_meta=True,
            days_in_month=days_in_month, days_elapsed=days_elapsed,
            days_remaining=days_remaining, cumplimiento_actual=cumpl,
            meta=meta, needed_for_commission=needed,
            daily_pace_actual=pace, projected=projected,
            projected_pct=projected_pct, gap=gap,
            daily_pace_needed=pace_needed,
            will_commission=projected >= needed,
            current_pct=current_pct,
        ))

    return today, days_in_month, days_elapsed, days_remaining, month_label, sim_rows


# ─────────────────────────────────────────────
# HELPERS DE FORMATO
# ─────────────────────────────────────────────
def fmt_currency(v: float) -> str:
    return f"${v:,.2f} MXN"


def fmt_pct(v: float) -> str:
    return f"{v * 100:.2f}%"


def fmt_num(v: float, decimals: int = 2) -> str:
    if not math.isfinite(v):
        return "Imposible"
    return f"{v:,.{decimals}f}"


# ─────────────────────────────────────────────
# ESTADO DE SESIÓN
# ─────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None


# ─────────────────────────────────────────────
# ENCABEZADO
# ─────────────────────────────────────────────
st.markdown('<p class="app-title">Calculadora Avanzada de Comisiones</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Herramienta financiera para equipos de ventas — Laureate</p>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# LAYOUT PRINCIPAL
# ─────────────────────────────────────────────
col_form, col_results = st.columns([2, 1], gap="large")

# ── FORMULARIO DE VARIABLES ─────────────────
with col_form:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">Variables de Comisión</div>', unsafe_allow_html=True)

    # Encabezados de columna
    h1, h2, h3, h4, h5 = st.columns([3, 3, 2, 2, 2])
    h1.markdown('<div class="col-header">Nombre</div>', unsafe_allow_html=True)
    h2.markdown('<div class="col-header">Monto ($)</div>', unsafe_allow_html=True)
    h3.markdown('<div class="col-header">Meta</div>', unsafe_allow_html=True)
    h4.markdown('<div class="col-header">Cumplimiento</div>', unsafe_allow_html=True)
    h5.markdown('<div class="col-header">% Cumplim.</div>', unsafe_allow_html=True)

    rows_data: list[dict] = []

    for i in range(6):
        c1, c2, c3, c4, c5 = st.columns([3, 3, 2, 2, 2])
        with c1:
            nombre = st.text_input(
                "Nombre", value=f"Variable {i+1}",
                key=f"nombre_{i}", label_visibility="collapsed"
            )
        with c2:
            monto = st.number_input(
                "Monto", value=0.0, min_value=0.0, step=100.0, format="%.2f",
                key=f"monto_{i}", label_visibility="collapsed"
            )
        with c3:
            meta = st.number_input(
                "Meta", value=0.0, min_value=0.0, step=1.0, format="%.2f",
                key=f"meta_{i}", label_visibility="collapsed"
            )
        with c4:
            cumpl = st.number_input(
                "Cumplimiento", value=0.0, min_value=0.0, step=1.0, format="%.2f",
                key=f"cumpl_{i}", label_visibility="collapsed"
            )
        with c5:
            if meta == 0:
                st.markdown("—")
            else:
                ratio = cumpl / meta
                if meta in (1, 2) and ratio > 2:
                    ratio = 2.0
                pct_val = ratio * 100
                color = "pct-green" if pct_val >= 90 else "pct-red"
                st.markdown(f'<span class="{color}">{pct_val:.2f}%</span>', unsafe_allow_html=True)

        rows_data.append({"nombre": nombre, "monto": monto, "meta": meta, "cumplimiento_val": cumpl})

    st.markdown("")
    if st.button("Calcular Comisiones", type="primary", use_container_width=False):
        st.session_state.result = calcular_variables(rows_data)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PANEL DE RESULTADOS ──────────────────────
with col_results:
    st.markdown('<div class="card" style="padding:0; overflow:hidden;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title" style="padding:1rem 1.5rem; margin:0;">Resultados</div>', unsafe_allow_html=True)

    res: CalculationResult | None = st.session_state.result

    if res is None:
        st.markdown(
            '<div style="padding:3rem 1.5rem; text-align:center; color:#94a3b8;">'
            'Ingresa los datos y presiona "Calcular" para ver los resultados.'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div style="padding:1rem 1.5rem;">', unsafe_allow_html=True)
        for i, v in enumerate(res.variables):
            badge_map = {
                "green": ("badge-green", ""),
                "red":   ("badge-red",   ""),
                "amber": ("badge-amber",  "Tope"),
                "gray":  ("badge-gray",   ""),
            }
            badge_cls, badge_txt = badge_map[v.status]
            pct_str = "N/A" if v.meta == 0 else fmt_pct(v.porcentaje)
            pct_color_cls = {"green":"pct-green","red":"pct-red","amber":"pct-amber","gray":"pct-gray"}[v.status]

            st.markdown(f"""
            <div class="var-result-row">
                <span class="var-result-name">{v.nombre}</span>
                <span class="var-result-amount">{fmt_currency(v.resultado)}</span>
            </div>
            <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:0.5rem;">
                <span style="font-size:0.78rem;color:#64748b;">
                    {'Fijo (Sin meta)' if v.meta == 0 else 'Cumplimiento'}
                </span>
                <span>
                    {'<span class="badge-amber">Tope</span>&nbsp;' if v.capped else ''}
                    <span class="{pct_color_cls}">{pct_str}</span>
                </span>
            </div>
            {'<div class="divider"></div>' if i < len(res.variables) - 1 else ''}
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Total naranja
        st.markdown(f"""
        <div class="total-card">
            <div class="total-label">Total a Pagar</div>
            <div class="total-value">{fmt_currency(res.total)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Botón CSV
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Variable", "% Cumplimiento", "Resultado", "Tope"])
        for v in res.variables:
            writer.writerow([
                v.nombre,
                "N/A" if v.meta == 0 else f"{v.porcentaje*100:.2f}%",
                f"{v.resultado:.2f}",
                "Sí" if v.capped else "No",
            ])
        writer.writerow([])
        writer.writerow(["TOTAL", "", f"{res.total:.2f}", ""])

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
        st.download_button(
            label="Descargar CSV",
            data=csv_buffer.getvalue(),
            file_name="comisiones.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIMULADOR AL CIERRE DE MES
# ─────────────────────────────────────────────
vars_con_meta = [r for r in rows_data if r["meta"] > 0]

if vars_con_meta:
    today, days_in_month, days_elapsed, days_remaining, month_label, sim_rows = simulate(rows_data)
    rows_with_meta = [r for r in sim_rows if r.has_meta]
    on_track = sum(1 for r in rows_with_meta if r.will_commission)
    at_risk   = len(rows_with_meta) - on_track

    badges_html = f'<span class="badge-green">{on_track} en ritmo</span>'
    if at_risk > 0:
        badges_html += f'&nbsp;&nbsp;<span class="badge-red">{at_risk} en riesgo</span>'

    st.markdown(f"""
    <div class="sim-header">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
            <div>
                <div class="sim-title">Simulador al Cierre de Mes</div>
                <div class="sim-subtitle">
                    Día {days_elapsed} de {days_in_month} &middot; {days_remaining} días restantes &middot; {month_label}
                </div>
            </div>
            <div>{badges_html}</div>
        </div>
    </div>
    <div class="sim-body">
    """, unsafe_allow_html=True)

    for idx, row in enumerate(sim_rows):
        if not row.has_meta:
            continue

        status_badge = (
            '<span class="badge-green">Comisiona</span>'
            if row.will_commission else
            '<span class="badge-red">En riesgo</span>'
        )

        # Barra de progreso
        bar_actual    = min(100.0, row.current_pct)
        bar_projected = min(100.0, row.projected_pct)
        bar_color     = "#22c55e" if row.will_commission else "#f87171"
        bar_proj_color= "#bbf7d0" if row.will_commission else "#fecaca"

        # Stat: excedente o faltante
        if row.will_commission:
            stat3_label = "Excedente proyectado"
            stat3_value = f"+{fmt_num(row.projected - row.needed_for_commission)}"
            stat3_color = "#15803d"
            stat3_bg    = "#f0fdf4"
        else:
            stat3_label = "Faltante para comisionar"
            stat3_value = fmt_num(row.gap)
            stat3_color = "#b91c1c"
            stat3_bg    = "#fff1f2"

        # Stat: ritmo necesario
        if row.will_commission:
            stat4_label = "Ritmo necesario / día"
            stat4_value = "En ritmo"
            stat4_color = "#94a3b8"
            stat4_bg    = "#f8fafc"
        else:
            stat4_label = "Ritmo necesario / día"
            stat4_value = fmt_num(row.daily_pace_needed)
            stat4_color = "#ea580c"
            stat4_bg    = "#fff7ed"

        st.markdown(f"""
        {'<div class="divider"></div>' if idx > 0 else ''}
        <div style="margin:1rem 0;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.6rem;">
                <div>
                    <span class="sim-var-name">{row.nombre}</span>
                    <span style="font-size:0.78rem;color:#64748b;margin-left:0.5rem;">
                        Meta: {fmt_num(row.meta)} &middot; Necesita: {fmt_num(row.needed_for_commission)} (90%)
                    </span>
                </div>
                {status_badge}
            </div>

            <!-- Barra de progreso -->
            <div style="position:relative;height:10px;background:#f1f5f9;border-radius:9999px;overflow:hidden;margin-bottom:0.3rem;">
                <div style="position:absolute;left:0;top:0;bottom:0;width:{bar_projected:.1f}%;background:{bar_proj_color};border-radius:9999px;"></div>
                <div style="position:absolute;left:0;top:0;bottom:0;width:{bar_actual:.1f}%;background:{bar_color};border-radius:9999px;"></div>
                <div style="position:absolute;left:90%;top:0;bottom:0;width:2px;background:#ea580c;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:#64748b;margin-bottom:0.8rem;">
                <span>Actual: <strong style="color:#334155;">{row.current_pct:.2f}%</strong></span>
                <span style="color:#ea580c;font-weight:600;">90% mínimo</span>
                <span>Proyección: <strong style="color:{'#15803d' if row.will_commission else '#b91c1c'};">{row.projected_pct:.2f}%</strong></span>
            </div>

            <!-- Estadísticas -->
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;">
                <div class="sim-stat-box">
                    <div class="sim-stat-label">Ritmo actual / día</div>
                    <div class="sim-stat-value">{fmt_num(row.daily_pace_actual) if row.daily_pace_actual > 0 else "—"}</div>
                </div>
                <div class="sim-stat-box">
                    <div class="sim-stat-label">Proyección al cierre</div>
                    <div class="sim-stat-value" style="color:{'#15803d' if row.will_commission else '#b91c1c'};">{fmt_num(row.projected)}</div>
                </div>
                <div class="sim-stat-box" style="background:{stat3_bg};">
                    <div class="sim-stat-label">{stat3_label}</div>
                    <div class="sim-stat-value" style="color:{stat3_color};">{stat3_value}</div>
                </div>
                <div class="sim-stat-box" style="background:{stat4_bg};">
                    <div class="sim-stat-label">{stat4_label}</div>
                    <div class="sim-stat-value" style="color:{stat4_color};">{stat4_value}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)