"""
guardia_api.py — Cliente OpenCode Zen para el Guardian Agent.

Configura y expone un cliente de inferencia remota vía OpenCode Zen API
(endpoint compatible con OpenAI). La clave de API se carga exclusivamente
desde variable de entorno OPENCODE_ZEN_API_KEY (no hardcodeada).
"""

import os
import json
import time
from typing import Optional

from dotenv import load_dotenv
import requests

load_dotenv()

OPENCODE_ZEN_ENDPOINT = "https://opencode.ai/zen/go/v1/chat/completions"
OPENCODE_ZEN_MODEL = "deepseek-v4-flash"
TIMEOUT_SECONDS = 120
MAX_RETRIES = 2


def get_api_key() -> str:
    """Retorna la clave OPENCODE_ZEN_API_KEY desde el entorno."""
    key = os.getenv("OPENCODE_ZEN_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENCODE_ZEN_API_KEY no está definida. "
            "Cárgala en tu .env o expórtala como variable de entorno."
        )
    return key


def inferir(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Envía un prompt al modelo deepseek-v4-flash vía OpenCode Zen y retorna
    la respuesta de texto.

    Maneja timeouts, rate limits y errores HTTP 4xx/5xx con
    reintentos y backoff exponencial.
    """
    api_key = get_api_key()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": OPENCODE_ZEN_MODEL,
        "messages": messages,
        "max_tokens": 6144,
    }

    last_error: Optional[Exception] = None
    for attempt in range(1 + MAX_RETRIES):
        try:
            response = requests.post(
                OPENCODE_ZEN_ENDPOINT,
                headers=headers,
                json=payload,
                timeout=TIMEOUT_SECONDS,
            )

            if response.status_code == 429:
                wait = min(2 ** (attempt + 1), 30)
                time.sleep(wait)
                continue

            response.raise_for_status()

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.Timeout:
            wait = min(2 ** (attempt + 1), 30)
            time.sleep(wait)
            last_error = TimeoutError(
                f"Timeout tras {TIMEOUT_SECONDS}s (intento {attempt + 1})"
            )
            continue

        except requests.exceptions.HTTPError as e:
            status = response.status_code
            if status >= 500 and attempt < MAX_RETRIES:
                wait = min(2 ** (attempt + 1), 30)
                time.sleep(wait)
                last_error = e
                continue
            raise RuntimeError(
                f"Error HTTP {status} de OpenCode Zen: {response.text}"
            ) from e

        except requests.exceptions.RequestException as e:
            last_error = RuntimeError(
                f"Error de conexión con OpenCode Zen (intento {attempt + 1}): {e}"
            )
            time.sleep(2 ** attempt)
            continue

    raise RuntimeError(
        f"No se pudo completar la inferencia tras {1 + MAX_RETRIES} intentos."
    ) from last_error


def ping() -> bool:
    """Verifica conectividad básica con la API de OpenCode Zen."""
    try:
        _ = inferir("Responde únicamente 'OK'.")
        return True
    except Exception:
        return False
