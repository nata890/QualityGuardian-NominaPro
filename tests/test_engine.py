"""
test_engine.py — Pruebas Pytest generadas desde el oráculo.

Generado automáticamente por guardian_client.py
"""

from src.engine import liquidar_nomina


def test_R1_Nominal():
    """R1-Nominal: Cálculo de horas extras diurnas"""
    result = liquidar_nomina(
        salario_base=1_500_000,
        horas_extras_diurnas=5,
        horas_extras_nocturnas=0,
        vlr_hora=10_000,
    )
    assert result["recargo_diurno"] == 62_500.0


def test_R1_Cero():
    """R1-Cero: Sin horas diurnas"""
    result = liquidar_nomina(1_500_000, 0, 0, 10_000)
    assert result["recargo_diurno"] == 0.0


def test_R2_Nominal():
    """R2-Nominal: Cálculo de horas extras nocturnas"""
    result = liquidar_nomina(
        salario_base=2_000_000,
        horas_extras_diurnas=0,
        horas_extras_nocturnas=3,
        vlr_hora=12_000,
    )
    assert result["recargo_nocturno"] == 63_000.0


def test_R2_Cero():
    """R2-Cero: Sin horas nocturnas"""
    result = liquidar_nomina(2_000_000, 5, 0, 12_000)
    assert result["recargo_nocturno"] == 0.0


def test_R3_Nominal():
    """R3-Nominal: Cálculo de descuentos"""
    result = liquidar_nomina(1_500_000, 5, 3, 10_000)
    assert result["descuento_salud"] == 64_600.0
    assert result["descuento_pension"] == 64_600.0


def test_R3_Sin_Extras():
    """R3-Sin-Extras: Descuentos sobre salario base"""
    result = liquidar_nomina(1_500_000, 0, 0, 10_000)
    assert result["descuento_salud"] == 60_000.0
    assert result["descuento_pension"] == 60_000.0


def test_R4_Aplica():
    """R4-Aplica: Salario dentro del tope"""
    result = liquidar_nomina(1_500_000, 0, 0, 10_000)
    assert result["auxilio_transporte"] == 162_000.0


def test_R4_En_El_Tope():
    """R4-En-El-Tope: Salario exactamente en el límite"""
    result = liquidar_nomina(2_600_000, 0, 0, 10_000)
    assert result["auxilio_transporte"] == 162_000.0


def test_R4_No_Aplica():
    """R4-No-Aplica: Salario sobre el tope"""
    result = liquidar_nomina(3_000_000, 0, 0, 10_000)
    assert result["auxilio_transporte"] == 0.0


def test_R5_Salario_Invalido():
    """R5-Salario-Invalido: Salario menor al SMMLV"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_000_000, 0, 0, 10_000)


def test_R5_Horas_Negativas():
    """R5-Horas-Negativas: Horas extras negativas"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, -2, 0, 10_000)
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, -1, 10_000)


def test_R5_VlrHora_Cero():
    """R5-VlrHora-Cero: Valor de hora en cero lanza ValueError"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, 0, 0)


def test_R5_VlrHora_Negativa():
    """R5-VlrHora-Negativa: Valor de hora negativo lanza ValueError"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, 0, -5_000)


def test_R5_VlrHora_NaN():
    """R5-VlrHora-NaN: Valor de hora NaN lanza ValueError"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, 0, float('nan'))


def test_R5_VlrHora_Infinito():
    """R5-VlrHora-Infinito: Valor de hora infinito lanza ValueError"""
    import pytest
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, 0, float('inf'))
    with pytest.raises(ValueError):
        liquidar_nomina(1_500_000, 0, 0, float('-inf'))
