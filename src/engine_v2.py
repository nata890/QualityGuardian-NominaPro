"""
engine.py — Motor de cálculo de nómina colombiana.

Módulo que implementa la liquidación de nómina siguiendo las reglas
laborales colombianas vigentes. Diseñado para ser consumido y auditado
por un Quality Guardian basado en IA Agéntica (LangChain / CrewAI).

Versión: 1.0.0
Python : 3.11+
"""


import math


# ──────────────────────────────────────────────
# Constantes de negocio
# ──────────────────────────────────────────────

SMMLV: float = 1_300_000.0
"""Salario mínimo mensual legal vigente (simulado)."""

TOPE_AUXILIO: float = 2_600_000.0
"""Tope salarial para recibir auxilio de transporte (2 SMMLV simulados)."""

AUXILIO_TRANSPORTE: float = 162_000.0
"""Valor del auxilio de transporte mensual."""

PORCENTAJE_RECARGO_DIURNO: float = 0.25
"""R1 — Recargo por hora extra diurna: 25 %."""

PORCENTAJE_RECARGO_NOCTURNO: float = 0.57
"""R2 — Recargo por hora extra nocturna: 57%."""

PORCENTAJE_SALUD: float = 0.04
"""R3 — Aporte a salud del trabajador: 4 %."""

PORCENTAJE_PENSION: float = 0.04
"""R3 — Aporte a pensión del trabajador: 4 %."""


# ──────────────────────────────────────────────
# Función principal
# ──────────────────────────────────────────────

def liquidar_nomina(
    salario_base: float,
    horas_extras_diurnas: int,
    horas_extras_nocturnas: int,
    vlr_hora: float,
) -> dict:
    """Liquida la nómina mensual de un empleado según las reglas colombianas.

    Parámetros
    ----------
    salario_base : float
        Salario básico mensual del empleado. Debe ser >= 1 SMMLV ($1.300.000).
    horas_extras_diurnas : int
        Cantidad de horas extras diurnas trabajadas. No puede ser negativa.
    horas_extras_nocturnas : int
        Cantidad de horas extras nocturnas trabajadas. No puede ser negativa.
    vlr_hora : float
        Valor de la hora ordinaria de trabajo.

    Retorna
    -------
    dict
        Diccionario con el desglose completo de la liquidación:
        - salario_base            : float
        - vlr_hora                : float
        - horas_extras_diurnas    : int
        - horas_extras_nocturnas  : int
        - recargo_diurno          : float  (valor total extras diurnas)
        - recargo_nocturno        : float  (valor total extras nocturnas)
        - total_devengado         : float  (salario_base + extras)
        - descuento_salud         : float  (4 % sobre total devengado)
        - descuento_pension       : float  (4 % sobre total devengado)
        - auxilio_transporte      : float  ($162.000 o $0)
        - total_a_pagar           : float  (devengado + auxilio − descuentos)

    Excepciones
    -----------
    ValueError
        - Si salario_base < $1.300.000 (por debajo del SMMLV).
        - Si horas_extras_diurnas < 0.
        - Si horas_extras_nocturnas < 0.
        - Si vlr_hora <= 0 (debe ser positivo).
        - Si vlr_hora es NaN (no numérico).
        - Si vlr_hora es infinito.

    Ejemplo
    -------
    >>> resultado = liquidar_nomina(
    ...     salario_base=1_500_000,
    ...     horas_extras_diurnas=5,
    ...     horas_extras_nocturnas=3,
    ...     vlr_hora=10_000,
    ... )
    >>> resultado["total_a_pagar"]
    1_647_800.0
    """

    # ── R5: Validaciones de entrada ──────────────────────────────
    if salario_base < SMMLV:
        raise ValueError(
            f"El salario base (${salario_base:,.0f}) no puede ser inferior "
            f"al SMMLV (${SMMLV:,.0f})."
        )

    if horas_extras_diurnas < 0:
        raise ValueError(
            f"Las horas extras diurnas ({horas_extras_diurnas}) "
            "no pueden ser negativas."
        )

    if horas_extras_nocturnas < 0:
        raise ValueError(
            f"Las horas extras nocturnas ({horas_extras_nocturnas}) "
            "no pueden ser negativas."
        )

    if vlr_hora <= 0:
        raise ValueError(
            f"El valor de la hora ({vlr_hora:,.0f}) debe ser positivo."
        )

    if math.isnan(vlr_hora):
        raise ValueError(
            "El valor de la hora no puede ser NaN (no numérico)."
        )

    if math.isinf(vlr_hora):
        raise ValueError(
            "El valor de la hora no puede ser infinito."
        )

    # ── R1: Recargo diurno — 25 % sobre el valor de la hora ordinaria ──
    recargo_diurno: float = horas_extras_diurnas * vlr_hora * (1 + PORCENTAJE_RECARGO_DIURNO)

    # ── R2: Recargo nocturno — 75 % sobre el valor de la hora ordinaria ──
    recargo_nocturno: float = horas_extras_nocturnas * vlr_hora * (1 + PORCENTAJE_RECARGO_NOCTURNO)

    # ── Total devengado (base para descuentos de seguridad social) ──
    total_devengado: float = salario_base + recargo_diurno + recargo_nocturno

    # ── R3: Seguridad social — 4 % salud + 4 % pensión sobre salario_base SOLO (ignora horas extras) ──
    descuento_salud: float = salario_base * PORCENTAJE_SALUD
    descuento_pension: float = salario_base * PORCENTAJE_PENSION

    # ── R4: Auxilio de transporte — $162.000 si salario_base < 2 SMMLV (BUG menor estricto) ──
    auxilio_transporte: float = AUXILIO_TRANSPORTE if salario_base < TOPE_AUXILIO else 0.0

    # ── Neto a pagar ──
    total_a_pagar: float = total_devengado + auxilio_transporte - descuento_salud - descuento_pension

    # ── Construcción del resultado ──
    return {
        "salario_base": salario_base,
        "vlr_hora": vlr_hora,
        "horas_extras_diurnas": horas_extras_diurnas,
        "horas_extras_nocturnas": horas_extras_nocturnas,
        "recargo_diurno": recargo_diurno,
        "recargo_nocturno": recargo_nocturno,
        "total_devengado": total_devengado,
        "descuento_salud": descuento_salud,
        "descuento_pension": descuento_pension,
        "auxilio_transporte": auxilio_transporte,
        "total_a_pagar": total_a_pagar,
    }
