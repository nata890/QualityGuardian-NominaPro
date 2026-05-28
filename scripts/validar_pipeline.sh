#!/usr/bin/env bash
# ============================================================================
# validar_pipeline.sh — Orquestador de validación del pipeline Nómina Pro
#
# Ejecuta en secuencia:
#   1. Verificación de entorno y dependencias
#   2. Tests Pytest (engine.py vía test_engine.py)
#   3. Validación de conectividad OpenRouter (guardia_api.py)
#   4. Generación de test_engine.py desde oráculo (guardian_client.py)
#   5. Emisión de veredicto.json
#   6. Reporte final
#
# Uso: bash validar_pipeline.sh
# ============================================================================

set -euo pipefail

ROJO='\033[0;31m'
VERDE='\033[0;32m'
AMARILLO='\033[1;33m'
AZUL='\033[0;34m'
SIN_COLOR='\033[0m'

PASOS_TOTALES=6
PASO_ACTUAL=0

ORACULO="casos_prueba.md"
ENGINE="src/engine.py"
GUARDIA_API="src/guardia_api.py"
GUARDIAN_CLIENT="src/guardian_client.py"
TEST_FILE="tests/test_engine.py"
VEREDICTO="veredicto.json"

# ── Funciones auxiliares ────────────────────────────────────────────────

ok()    { echo -e "  ${VERDE}✔${SIN_COLOR} $1"; }
fail()  { echo -e "  ${ROJO}✖${SIN_COLOR} $1"; }
warn()  { echo -e "  ${AMARILLO}⚠${SIN_COLOR} $1"; }
info()  { echo -e "  ${AZUL}→${SIN_COLOR} $1"; }
paso()  { PASO_ACTUAL=$((PASO_ACTUAL + 1)); echo -e "\n${AZUL}[$PASO_ACTUAL/$PASOS_TOTALES]${SIN_COLOR} $1"; }

verificar_archivo() {
    if [[ -f "$1" ]]; then
        ok "Archivo encontrado: $1 ($(wc -l < "$1") líneas)"
        return 0
    else
        fail "Archivo NO encontrado: $1"
        return 1
    fi
}

verificar_dependencia() {
    if command -v "$1" &>/dev/null; then
        ok "Dependencia: $1 ($($1 --version 2>&1 | head -1))"
    else
        fail "Dependencia faltante: $1"
        EXIT_CODE=1
    fi
}

# ── Contador de errores ──────────────────────────────────────────────────
EXIT_CODE=0

# ============================================================================
# PASO 1: Verificación de entorno
# ============================================================================
paso "Verificación de entorno y dependencias"

verificar_archivo "$ENGINE"
verificar_archivo "$GUARDIA_API"
verificar_archivo "$GUARDIAN_CLIENT"
verificar_archivo "$TEST_FILE"

if [[ -f "$ORACULO" ]]; then
    ok "Oráculo encontrado: $ORACULO ($(wc -l < "$ORACULO") líneas)"
    ORACULO_EXISTE=true
else
    warn "Oráculo ($ORACULO) no encontrado — será creado por Miguel (US-NOM02)"
    ORACULO_EXISTE=false
fi

verificar_dependencia python3
verificar_dependencia pytest

info "Verificando paquetes Python..."
if python3 -c "import requests, json, os, time" 2>/dev/null; then
    ok "Paquetes Python básicos: requests, json, os, time"
else
    fail "Faltan paquetes Python: requests"
    EXIT_CODE=1
fi

# Cargar API key desde .env si existe
if [[ -f .env ]]; then
    export OPENROUTER_API_KEY="${OPENROUTER_API_KEY:-$(grep OPENROUTER_API_KEY .env | cut -d= -f2)}"
    ok "OPENROUTER_API_KEY cargada desde .env"
else
    if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
        warn "OPENROUTER_API_KEY no definida — pruebas de conectividad se omitirán"
    else
        ok "OPENROUTER_API_KEY presente en entorno"
    fi
fi

# ============================================================================
# PASO 2: Tests Pytest sobre engine.py
# ============================================================================
paso "Ejecución de tests Pytest sobre $ENGINE"

if pytest "$TEST_FILE" -v --tb=short --no-header 2>&1; then
    ok "Todos los tests Pytest PASARON"
else
    fail "Uno o más tests FALLARON (revisar arriba)"
    EXIT_CODE=1
fi

# ============================================================================
# PASO 3: Validación de conectividad OpenRouter
# ============================================================================
paso "Validación de conectividad OpenRouter"

if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
    info "Ejecutando ping a modelo $(python3 -c "from src.guardia_api import OPENROUTER_MODEL; print(OPENROUTER_MODEL)")..."
    if python3 -c "
import os, time
os.environ['OPENROUTER_API_KEY'] = os.environ.get('OPENROUTER_API_KEY', '')
from src.guardia_api import ping, OPENROUTER_MODEL, OPENROUTER_ENDPOINT
start = time.time()
ok = ping()
elapsed = (time.time() - start) * 1000
if ok:
    print(f'OK: {OPENROUTER_ENDPOINT} | modelo={OPENROUTER_MODEL} | latencia={elapsed:.0f}ms')
    if elapsed > 2000:
        print(f'ALERTA: Latencia elevada ({elapsed:.0f}ms > 2000ms)')
else:
    print(f'FALLO: Sin respuesta de {OPENROUTER_ENDPOINT}')
    exit(1)
" 2>&1; then
        ok "Conectividad OpenRouter validada"
    else
        fail "Conectividad OpenRouter FALLÓ"
        EXIT_CODE=1
    fi
else
    warn "OPENROUTER_API_KEY no disponible — omitiendo validación de conectividad"
fi

# ============================================================================
# PASO 4: Generación de test_engine.py desde oráculo
# ============================================================================
paso "Regeneración de $TEST_FILE desde oráculo"

if [[ "$ORACULO_EXISTE" == true ]]; then
    if python3 "$GUARDIAN_CLIENT" 2>&1; then
        ok "$TEST_FILE generado correctamente"
    else
        fail "Falló generación de $TEST_FILE"
        EXIT_CODE=1
    fi
else
    warn "Oráculo no disponible — usando $TEST_FILE existente (pre-generado)"
    info "Para regenerar: Miguel debe crear $ORACULO primero (US-NOM02)"
fi

# ============================================================================
# PASO 5: Emisión de veredicto.json (desde pytest independiente)
# ============================================================================
paso "Emisión de veredicto.json"

if python3 -m pytest "$TEST_FILE" --junitxml=reporte_junit.xml -q --tb=short 2>&1; then
    ok "Tests ejecutados correctamente"
fi

if python3 -c "
import json, xml.etree.ElementTree as ET, time

tree = ET.parse('reporte_junit.xml')
root = tree.getroot()
ts = root[0] if len(root) > 0 else root
total = int(ts.get('tests', 0))
fallaron = int(ts.get('failures', 0)) + int(ts.get('errors', 0))
pasaron = total - fallaron

escenarios = []
for tc in ts.findall('.//testcase') if ts.tag == 'testsuite' else ts.iter('testcase'):
    name = tc.get('name', 'unknown')
    failure = tc.find('failure')
    escenarios.append({
        'id': name,
        'descripcion': tc.get('classname', ''),
        'resultado': 'FAIL' if failure is not None else 'PASS',
        'duracion_ms': int(float(tc.get('time', 0)) * 1000),
    })

conteo_escenarios = len(escenarios)
with open('$VEREDICTO', 'w') as f:
    json.dump({
        'escenarios': escenarios,
        'resumen': {
            'total': total,
            'pasaron': pasaron,
            'fallaron': fallaron,
            'cobertura': 'N/A',
        },
        'metadata': {
            'modelo': 'deepseek/deepseek-v4-flash:free',
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'oraculo': 'casos_prueba.md',
            'duracion_total_ms': 0,
        },
    }, f, indent=2, ensure_ascii=False)

print(f'Resumen: {pasaron}/{total} tests OK ({pasaron/total*100:.0f}% si total>0)')
" 2>&1; then
    if [[ -f "$VEREDICTO" ]]; then
        ok "Veredicto generado: $VEREDICTO ($(wc -c < "$VEREDICTO") bytes)"
        python3 -c "
import json
with open('$VEREDICTO') as f:
    v = json.load(f)
r = v['resumen']
print(f'  Total: {r[\"total\"]} | Pasaron: {r[\"pasaron\"]} | Fallaron: {r[\"fallaron\"]}')
print(f'  Modelo: {v[\"metadata\"][\"modelo\"]}')
"
    fi
else
    fail "Falló emisión de veredicto"
    EXIT_CODE=1
fi

# ============================================================================
# PASO 6: Reporte final
# ============================================================================
paso "Reporte final del pipeline"

echo ""
echo "=================== RESUMEN DEL PIPELINE ==================="
echo ""
echo "  src/engine.py         : $(wc -l < src/engine.py) líneas — lógica R1-R5"
echo "  src/guardia_api.py    : $(wc -l < src/guardia_api.py) líneas — cliente OpenRouter"
echo "  src/guardian_client.py: $(wc -l < src/guardian_client.py) líneas — orquestador"
echo "  tests/test_engine.py  : $(wc -l < tests/test_engine.py) líneas — $(grep -c 'def test_' tests/test_engine.py) tests"
echo "  scripts/validar_conexion.py: $(wc -l < scripts/validar_conexion.py) líneas — script diagnóstico"
echo "  veredicto.json    : $( [[ -f veredicto.json ]] && echo '✓ generado' || echo '✖ ausente' )"
echo ""

if [[ $EXIT_CODE -eq 0 ]]; then
    echo -e "  ${VERDE}ESTADO: PIPELINE COMPLETO — TODAS LAS VALIDACIONES PASARON${SIN_COLOR}"
else
    echo -e "  ${ROJO}ESTADO: PIPELINE CON ERRORES — Revisar reportes arriba${SIN_COLOR}"
fi

echo ""
echo "============================================================="
exit $EXIT_CODE
