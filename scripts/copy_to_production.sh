#!/usr/bin/env bash
# copy_to_production.sh — Mueve artifacts DRAFT de .planning/ a paths de producción.
# Uso: bash scripts/copy_to_production.sh
# Requiere aprobación humana antes de ejecutar.

set -euo pipefail

PLANNING_DIR=".planning/fix-all-audit-issues"

if [ ! -d "$PLANNING_DIR" ]; then
    echo "[ERROR] Directorio $PLANNING_DIR no existe."
    exit 1
fi

echo "[copy_to_production] Moviendo artifacts de $PLANNING_DIR a producción..."

if [ -f "$PLANNING_DIR/test_engine.py" ]; then
    cp "$PLANNING_DIR/test_engine.py" tests/test_engine.py
    echo "  ✓ tests/test_engine.py"
fi

if [ -f "$PLANNING_DIR/veredicto.json" ]; then
    cp "$PLANNING_DIR/veredicto.json" veredicto.json
    echo "  ✓ veredicto.json"
fi

if [ -f "$PLANNING_DIR/reporte_junit.xml" ]; then
    cp "$PLANNING_DIR/reporte_junit.xml" reporte_junit.xml
    echo "  ✓ reporte_junit.xml"
fi

echo "[copy_to_production] Completo."
