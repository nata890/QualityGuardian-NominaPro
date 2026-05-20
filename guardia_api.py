"""
guardia_api.py — Cliente OpenRouter para el Guardian Agent.

Configura y expone un cliente de inferencia remota vía OpenRouter API.
La clave de API se carga exclusivamente desde variable de entorno
OPENROUTER_API_KEY (no hardcodeada).
"""

import os
import json
import time
from typing import Optional

import requests

OPENROUTER_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "baidu/cobuddy"
TIMEOUT_SECONDS = 30
MAX_RETRIES = 2


def get_api_key() -> str:
    """Retorna la clave OPENROUTER_API_KEY desde el entorno."""
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise EnvironmentError(
            "OPENROUTER_API_KEY no está definida. "
            "Cárgala en tu .env o expórtala como variable de entorno."
        )
    return key


def inferir(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Envía un prompt al modelo baidu/cobuddy vía OpenRouter y retorna
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
        "HTTP-Referer": "https://github.com/QualityGuardian-NominaPro",
    }

    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 2048,
        "temperature": 0.2,
    }

    last_error: Optional[Exception] = None
    for attempt in range(1 + MAX_RETRIES):
        try:
            response = requests.post(
                OPENROUTER_ENDPOINT,
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

        except requests.exceptions.TimeError:
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
                f"Error HTTP {status} de OpenRouter: {response.text}"
            ) from e

        except requests.exceptions.RequestException as e:
            last_error = RuntimeError(
                f"Error de conexión con OpenRouter (intento {attempt + 1}): {e}"
            )
            time.sleep(2 ** attempt)
            continue

    raise RuntimeError(
        f"No se pudo completar la inferencia tras {1 + MAX_RETRIES} intentos."
    ) from last_error


def ping() -> bool:
    """Verifica conectividad básica con la API de OpenRouter."""
    try:
        _ = inferir("Responde únicamente 'OK'.")
        return True
    except Exception:
        return False
