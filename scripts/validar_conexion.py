"""
validar_conexion.py — Valida conectividad, latencia y manejo de errores
contra OpenRouter API (modelo baidu/cobuddy).

Uso: python validar_conexion.py
"""

import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

load_dotenv()

from src.guardia_api import ping, inferir, OPENROUTER_ENDPOINT, OPENROUTER_MODEL


def test_ping():
    """Valida conectividad básica."""
    ok = ping()
    status = "✓ CONECTADO" if ok else "✖ SIN RESPUESTA"
    print(f"[PING]    {status} — {OPENROUTER_ENDPOINT}")


def test_inferencia():
    """Valida inferencia mínima con latencia."""
    try:
        start = time.time()
        resp = inferir("Responde exactamente: 'OK'")
        elapsed = (time.time() - start) * 1000
        print(f"[INFERIR] ✓ Respuesta recibida en {elapsed:.0f} ms")
        if resp:
            print(f"           Contenido: {resp[:100]}")
    except Exception as e:
        print(f"[INFERIR] ✖ Error: {e}")


def test_api_key_no_hardcode():
    """Verifica que la clave NO esté hardcodeada en el código."""
    with open(Path(__file__).resolve().parent.parent / "src" / "guardia_api.py") as f:
        content = f.read()
    if "sk-or-v1" in content and "# Ejemplo" not in content:
        print("[SEGURID] ✖ API KEY hardcodeada en guardia_api.py")
    else:
        print("[SEGURID] ✓ No hay API KEY hardcodeada en código")
    print(f"           Endpoint: {OPENROUTER_ENDPOINT}")
    print(f"           Modelo:   {OPENROUTER_MODEL}")


if __name__ == "__main__":
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        print("[ERROR]   OPENROUTER_API_KEY no está definida.")
        print("          Cárgala con: export OPENROUTER_API_KEY=sk-...")
        sys.exit(1)

    print(f"== Validación OpenRouter (modelo: {OPENROUTER_MODEL}) ==\n")
    test_api_key_no_hardcode()
    test_ping()
    test_inferencia()
    print("\n== Validación completa. ==")
