"""
guardian_client.py — Orquestador que ingiere el oráculo y genera
test_engine.py con Pytest vía OpenRouter API.

Flujo:
  1. Lee casos_prueba.md
  2. Envía cada escenario Gherkin al modelo baidu/cobuddy
  3. Genera funciones test_* en test_engine.py
"""

import os
import re
import sys
import ast
from pathlib import Path

from dotenv import load_dotenv

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

load_dotenv()

from src.guardia_api import inferir


# Ruta al último output crudo de la LLM (si existe)
LLM_RAW_PATH: str | None = None

ORACULO_PATH = "casos_prueba.md"
OUTPUT_PATH = ".planning/fix-all-audit-issues/test_engine.py"
VEREDICTO_PATH = ".planning/fix-all-audit-issues/veredicto.json"
JUNIT_PATH = ".planning/fix-all-audit-issues/reporte_junit.xml"

SYSTEM_PROMPT = """
Eres un generador de pruebas Pytest para el motor de nómina colombiano.
Conviertes cada escenario Gherkin (Dado/Cuando/Entonces) de casos_prueba.md
en una función test_* válida que importa liquidar_nomina desde engine.py.

Reglas:
- Cada escenario produce UNA función test_ separada.
- Usa assert para verificar el resultado esperado.
- Los valores monetarios deben coincidir exactamente con los del escenario.
- Incluye docstring en cada test citando el ID del escenario.
- No uses clases. Solo funciones con prefijo test_.
"""


def leer_oraculo() -> str:
    """Retorna el contenido completo de casos_prueba.md."""
    with open(ORACULO_PATH, "r", encoding="utf-8") as f:
        return f.read()


def generate_test_engine_from_llm(oraculo: str) -> str:
    """Usa el modelo para generar test_engine.py."""
    prompt = (
        f"A continuación está el oráculo de pruebas:\n\n{oraculo}\n\n"
        "Genera el contenido COMPLETO de test_engine.py con todas las funciones test_*.\n"
        "Incluye el import de engine.py al inicio.\n"
        "Usa números exactos según los escenarios."
    )
    try:
        result = inferir(prompt, system_prompt=SYSTEM_PROMPT)
        return result
    except Exception as e:
        import traceback

        tb = traceback.format_exc()
        # Mostrar al usuario el error recibido de la llamada a la API
        print(f"[WARN] Falló inferencia para generación: {e}")
        print("[WARN] Stacktrace:\n", tb)
        print("[WARN] Usando generación por plantilla (fallback).")
        # Devolver la información del error como 'raw' para que el caller lo registre
        return f"LLM_EXCEPTION:\n{e}\n{tb}"


def _strip_code_fences(code: str) -> str:
    """Remueve fences ``` y encabezados como ```python de la salida de la LLM."""
    if not code:
        return ""
    # Eliminar cualquier fence ```...``` (líneas que comienzan con ``` o ```python)
    code = re.sub(r"(?m)^\s*```.*$\n?", "", code, flags=re.IGNORECASE)
    # Quitar cualquier leftover de backticks
    code = code.replace("```", "")
    return code.strip()


def _is_valid_python(code: str) -> bool:
    """Valida sintaxis de Python intentando parsear con ast.

    Retorna True si `ast.parse` no lanza excepción.
    """
    try:
        ast.parse(code)
        return True
    except Exception:
        return False


def _normalize_imports(code: str) -> str:
    """Ajusta imports comunes que la LLM puede generar a los imports correctos del proyecto.

    Ejemplos:
    - from engine import ...  -> from src.engine import ...
    - import engine          -> from src import engine as engine
    """
    if not code:
        return code
    # from engine import X -> from src.engine import X
    code = re.sub(r"(?m)^\s*from\s+engine\s+import\s+", "from src.engine import ", code)
    # import engine -> import src.engine as engine
    code = re.sub(r"(?m)^\s*import\s+engine\s*$", "import src.engine as engine", code)
    return code


def generate_test_engine_fallback(oraculo: str) -> str:
    """Generador por plantilla directa — convierte Gherkin a Pytest."""
    lines = oraculo.split("\n")
    tests = []
    current_id = "unknown"
    current_desc = ""
    dado = ""
    cuando = ""
    entonces = ""

    for line in lines:
        m_id = re.match(r"^### Escenario\s+(\S+):\s*(.*)", line)
        if m_id:
            if current_id != "unknown" and dado:
                tests.append((current_id, current_desc, dado, cuando, entonces))
            current_id = m_id.group(1)
            current_desc = m_id.group(2).strip()
            dado = ""
            cuando = ""
            entonces = ""
            continue

        m_dado = re.match(r"^- \*\*Dado\*\*\s+(.*)", line)
        if m_dado:
            dado = m_dado.group(1)
            continue

        m_cuando = re.match(r"^- \*\*Cuando\*\*\s+(.*)", line)
        if m_cuando:
            cuando = m_cuando.group(1)
            continue

        m_entonces = re.match(r"^- \*\*Entonces\*\*\s+(.*)", line)
        if m_entonces:
            entonces = m_entonces.group(1)
            continue

    if current_id != "unknown" and dado:
        tests.append((current_id, current_desc, dado, cuando, entonces))

    if not tests:
        tests = [
            ("R1-Nominal", "Cálculo de horas extras diurnas", "", "", ""),
            ("R1-Cero", "Sin horas diurnas", "", "", ""),
            ("R2-Nominal", "Cálculo de horas extras nocturnas", "", "", ""),
            ("R2-Cero", "Sin horas nocturnas", "", "", ""),
            ("R3-Nominal", "Cálculo de descuentos", "", "", ""),
            ("R3-Sin-Extras", "Descuentos sobre salario base", "", "", ""),
            ("R4-Aplica", "Salario dentro del tope", "", "", ""),
            ("R4-En-El-Tope", "Salario exactamente en el límite", "", "", ""),
            ("R4-No-Aplica", "Salario sobre el tope", "", "", ""),
            ("R5-Salario-Invalido", "Salario menor al SMMLV", "", "", ""),
            ("R5-Horas-Negativas", "Horas extras negativas", "", "", ""),
        ]

    engine = []
    engine.append('"""')
    engine.append("test_engine.py — Pruebas Pytest generadas desde el oráculo.")
    engine.append("")
    engine.append("Generado automáticamente por guardian_client.py")
    engine.append('"""')
    engine.append("")
    engine.append("from src.engine import liquidar_nomina")
    engine.append("")

    for tid, tdesc, tdado, tcuando, tentonces in tests:
        safe_name = tid.replace("-", "_").replace(" ", "_")
        engine.append("")
        engine.append(f"def test_{safe_name}():")
        engine.append(f'    """{tid}: {tdesc}"""')

        if "R1" in tid and "Cero" not in tid:
            engine.append('    result = liquidar_nomina(')
            engine.append('        salario_base=1_500_000,')
            engine.append('        horas_extras_diurnas=5,')
            engine.append('        horas_extras_nocturnas=0,')
            engine.append('        vlr_hora=10_000,')
            engine.append('    )')
            engine.append('    assert result["recargo_diurno"] == 62_500.0')
        elif "R1" in tid and "Cero" in tid:
            engine.append('    result = liquidar_nomina(1_500_000, 0, 0, 10_000)')
            engine.append('    assert result["recargo_diurno"] == 0.0')
        elif "R2" in tid and "Cero" not in tid:
            engine.append('    result = liquidar_nomina(')
            engine.append('        salario_base=2_000_000,')
            engine.append('        horas_extras_diurnas=0,')
            engine.append('        horas_extras_nocturnas=3,')
            engine.append('        vlr_hora=12_000,')
            engine.append('    )')
            engine.append('    assert result["recargo_nocturno"] == 63_000.0')
        elif "R2" in tid and "Cero" in tid:
            engine.append('    result = liquidar_nomina(2_000_000, 5, 0, 12_000)')
            engine.append('    assert result["recargo_nocturno"] == 0.0')
        elif "R3" in tid and "Nominal" in tid:
            engine.append('    result = liquidar_nomina(1_500_000, 5, 3, 10_000)')
            engine.append('    assert result["descuento_salud"] == 64_600.0')
            engine.append('    assert result["descuento_pension"] == 64_600.0')
        elif "R3" in tid and "Sin" in tid:
            engine.append('    result = liquidar_nomina(1_500_000, 0, 0, 10_000)')
            engine.append('    assert result["descuento_salud"] == 60_000.0')
            engine.append('    assert result["descuento_pension"] == 60_000.0')
        elif "R4" in tid and "Aplica" in tid:
            engine.append('    result = liquidar_nomina(1_500_000, 0, 0, 10_000)')
            engine.append('    assert result["auxilio_transporte"] == 162_000.0')
        elif "R4" in tid and "Tope" in tid:
            engine.append('    result = liquidar_nomina(2_600_000, 0, 0, 10_000)')
            engine.append('    assert result["auxilio_transporte"] == 162_000.0')
        elif "R4" in tid and "No-Aplica" in tid:
            engine.append('    result = liquidar_nomina(3_000_000, 0, 0, 10_000)')
            engine.append('    assert result["auxilio_transporte"] == 0.0')
        elif "R5" in tid and "Salario" in tid:
            engine.append('    import pytest')
            engine.append('    with pytest.raises(ValueError):')
            engine.append('        liquidar_nomina(1_000_000, 0, 0, 10_000)')
        elif "R5" in tid and "Horas" in tid:
            engine.append('    import pytest')
            engine.append('    with pytest.raises(ValueError):')
            engine.append('        liquidar_nomina(1_500_000, -2, 0, 10_000)')
            engine.append('    with pytest.raises(ValueError):')
            engine.append('        liquidar_nomina(1_500_000, 0, -1, 10_000)')
        else:
            engine.append('    pass  # placeholder — escenario no mapeado')

        engine.append("")

    return "\n".join(engine)


def generar_veredicto(resultados: dict) -> dict:
    """Genera la estructura de veredicto.json según el protocolo definido en AGENTS.md."""
    import time
    return {
        "escenarios": [
            {
                "id": tid,
                "descripcion": f"Test {tid}",
                "resultado": "PASS" if ok else "FAIL",
                "duracion_ms": 0,
            }
            for tid, ok in resultados.items()
        ],
        "resumen": {
            "total": len(resultados),
            "pasaron": sum(1 for v in resultados.values() if v),
            "fallaron": sum(1 for v in resultados.values() if not v),
            "cobertura": "N/A",
        },
        "metadata": {
            "modelo": "baidu/cobuddy:free",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "oraculo": "casos_prueba.md",
            "duracion_total_ms": 0,
            "llm_raw_path": LLM_RAW_PATH,
        },
    }


def guardar_veredicto(veredicto: dict, path: str = VEREDICTO_PATH):
    """Escribe el veredicto JSON a disco."""
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump(veredicto, f, indent=2, ensure_ascii=False)
    print(f"[guardian] → {path} escrito ({veredicto['resumen']['total']} escenarios)")


def compilar():
    """Lee el oráculo, genera test_engine.py y lo guarda."""
    Path(".planning/fix-all-audit-issues").mkdir(parents=True, exist_ok=True)
    if not os.path.exists(ORACULO_PATH):
        print(f"[WARN] Oráculo {ORACULO_PATH} no encontrado — usando fallback por plantilla.")
        oraculo = ""
        codigo = generate_test_engine_fallback(oraculo)
    else:
        print(f"[guardian] Leyendo oráculo: {ORACULO_PATH}")
        oraculo = leer_oraculo()
        print(oraculo)
        print("[guardian] Generando test_engine.py...")
        # Permitir forzar fallback mediante variable de entorno
        force_fallback = os.getenv("FORCE_FALLBACK", "0") in ("1", "true", "True")
        if force_fallback:
            print("[guardian] FORCE_FALLBACK activado — usando generación por plantilla.")
            codigo = generate_test_engine_fallback(oraculo)
        else:
            codigo = generate_test_engine_from_llm(oraculo) or ""
            # Guardar salida cruda de la LLM para auditoría
            import time
            global LLM_RAW_PATH
            ts = int(time.time())
            raw_dir = Path("artifacts")
            raw_dir.mkdir(exist_ok=True)
            raw_path = raw_dir / f"llm_output_{ts}.txt"
            with open(raw_path, "w", encoding="utf-8") as rf:
                rf.write(codigo)
            LLM_RAW_PATH = str(raw_path)

            # Limpiar fences comunes devueltos por LLMs y validar sintaxis
            codigo = _strip_code_fences(codigo)
            codigo = _normalize_imports(codigo)
            if not codigo.strip() or not _is_valid_python(codigo):
                print("[guardian] Salida LLM inválida o vacía — registrando raw output y usando fallback por plantilla.")
                print(f"[guardian] Raw LLM output guardado en: {LLM_RAW_PATH}")
                codigo = generate_test_engine_fallback(oraculo)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(codigo)

    tests = codigo.count("def test_")
    print(f"[guardian] → {OUTPUT_PATH} generado con {tests} funciones test_*.")
    return tests


def ejecutar_y_veredicto():
    """Genera tests, los ejecuta y emite veredicto.json."""
    n = compilar()
    print(f"\n[guardian] Ejecutando {n} tests...")
    import subprocess
    import xml.etree.ElementTree as ET
    import re

    junit_path = JUNIT_PATH
    result = subprocess.run(
        ["python", "-m", "pytest", OUTPUT_PATH, "-v", "--tb=short",
         "--junitxml=" + junit_path, "--cov=src.engine", "--cov-report=term"],
        capture_output=True, text=True,
    )
    print(result.stdout)

    # Parsear duraciones desde JUnit XML
    escenarios = []
    total = 0
    pasaron = 0
    fallaron = 0
    try:
        tree = ET.parse(junit_path)
        root = tree.getroot()
        testsuite = root[0] if len(root) > 0 else root
        total = int(testsuite.get("tests", 0))
        fallaron = int(testsuite.get("failures", 0)) + int(testsuite.get("errors", 0))
        pasaron = total - fallaron
        for tc in testsuite.findall(".//testcase"):
            tid = tc.get("name", "unknown")
            failure = tc.find("failure")
            duracion_ms = max(int(float(tc.get("time", 0)) * 1000), 1)
            escenarios.append({
                "id": tid,
                "descripcion": f"Test {tid}",
                "resultado": "FAIL" if failure is not None else "PASS",
                "duracion_ms": duracion_ms,
                "error": failure.text if failure is not None else None,
            })
    except Exception as e:
        print(f"[WARN] No se pudo parsear JUnit XML: {e}")
        resultados = {}
        lineas = result.stdout.strip().split("\n")
        for line in lineas:
            if "PASSED" in line:
                tid = line.split("::")[-1].split()[0]
                resultados[tid] = True
                pasaron += 1
            elif "FAILED" in line:
                tid = line.split("::")[-1].split()[0]
                resultados[tid] = False
                fallaron += 1
            if "collected" in line:
                m = re.search(r"collected (\d+)", line)
                if m:
                    total = int(m.group(1))
        escenarios = [
            {
                "id": tid,
                "descripcion": f"Test {tid}",
                "resultado": "PASS" if ok else "FAIL",
                "duracion_ms": 1,
            }
            for tid, ok in resultados.items()
        ]

    # Extraer cobertura del output de pytest-cov
    cobertura = "0.0%"
    for line in result.stdout.split("\n") + result.stderr.split("\n"):
        m = re.search(r"TOTAL\s+.*?(\d+\.?\d*)%", line)
        if m:
            pct = float(m.group(1))
            cobertura = f"{pct:.1f}%"
            break

    veredicto = {
        "escenarios": escenarios,
        "resumen": {
            "total": total,
            "pasaron": pasaron,
            "fallaron": fallaron,
            "cobertura": cobertura,
        },
        "metadata": {
            "modelo": "baidu/cobuddy:free",
            "timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
            "oraculo": "casos_prueba.md",
            "duracion_total_ms": sum(e["duracion_ms"] for e in escenarios),
            "llm_raw_path": LLM_RAW_PATH,
        },
    }
    guardar_veredicto(veredicto)
    print(f"\n[guardian] Pipeline completo: {pasaron}/{total} tests OK, {fallaron} fallaron, cobertura={cobertura}")
    return veredicto


if __name__ == "__main__":
    v = ejecutar_y_veredicto()
