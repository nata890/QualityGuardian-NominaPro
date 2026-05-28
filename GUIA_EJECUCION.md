# Guía de Ejecución — QualityGuardian-NominaPro

> Instrucciones paso a paso para ejecutar el proyecto completo desde cero.
> Proyecto COIL — Universidad de Caldas × Universidad Manuela Beltrán

---

## 0. Prerrequisitos

Asegúrate de tener instalados:

| Herramienta | Versión mínima | Verificar |
|---|---|---|
| **Python** | 3.11+ | `python --version` |
| **pip** | 23.0+ | `pip --version` |
| **Docker** | 20.10+ | `docker --version` |
| **Git** | 2.30+ | `git --version` |
| **Bash** | 5.0+ | `bash --version` |

Si no tienes Docker, puedes ejecutar las pruebas localmente (sección 3), pero el pipeline completo requiere Docker para aislamiento.

---

## 1. Clonar el repositorio

```bash
git clone https://github.com/nata890/QualityGuardian-NominaPro.git
cd QualityGuardian-NominaPro
```

---

## 2. Configurar la API Key de OpenCode Zen

El Guardian Agent necesita acceso a OpenCode Zen API para generar pruebas con IA.

### Paso 2.1: Obtener la API Key

Tu API key de OpenCode Zen (`OPENCODE_ZEN_API_KEY`) se obtiene desde el dashboard de OpenCode.

### Paso 2.2: Configurar localmente

Crea un archivo `.env` en la raíz del proyecto:

```bash
cat > .env << 'EOF'
OPENCODE_ZEN_API_KEY=sk-tu-clave-aqui
EOF
```

O exporta la variable directamente:

```bash
export OPENCODE_ZEN_API_KEY="sk-tu-clave-aqui"
```

> **Importante:** El archivo `.env` está en `.gitignore`. Nunca se sube al repositorio.

### Paso 2.3: Verificar que no está hardcodeada

```bash
python scripts/validar_conexion.py
```

Deberías ver:
```
== Validación OpenCode Zen (modelo: deepseek-v4-flash) ==

[SEGURID] ✓ No hay API KEY hardcodeada en código
[PING]    ✓ CONECTADO — https://opencode.ai/zen/go/v1/chat/completions
[INFERIR] ✓ Respuesta recibida en 1234 ms

== Validación completa. ==
```

---

## 3. Instalar dependencias

```bash
pip install -r infra/requirements.txt
```

Esto instala:
- `requests` — comunicación con OpenCode Zen API
- `pytest` — framework de pruebas
- `pytest-cov` — medición de cobertura de código
- `python-dotenv` — carga automática de `.env`

---

## 4. Ejecutar el motor de nómina (prueba rápida)

Puedes probar el motor directamente desde Python:

```bash
python -c "
from src.engine import liquidar_nomina
resultado = liquidar_nomina(
    salario_base=1_500_000,
    horas_extras_diurnas=5,
    horas_extras_nocturnas=3,
    vlr_hora=10_000,
)
for clave, valor in resultado.items():
    print(f'{clave}: {valor:,.2f}')
"
```

Salida esperada:
```
salario_base: 1,500,000.00
vlr_hora: 10,000.00
horas_extras_diurnas: 5
horas_extras_nocturnas: 3
recargo_diurno: 62,500.00
recargo_nocturno: 52,500.00
total_devengado: 1,615,000.00
descuento_salud: 64,600.00
descuento_pension: 64,600.00
auxilio_transporte: 162,000.00
total_a_pagar: 1,647,800.00
```

---

## 5. Ejecutar las pruebas Pytest directamente

### Opción A: Pruebas sin cobertura

```bash
python -m pytest tests/test_engine.py -v --tb=short
```

### Opción B: Pruebas con cobertura (recomendado)

```bash
python -m pytest tests/test_engine.py -v --tb=short --cov=src.engine --cov-report=term
```

Salida esperada (15 pruebas, 100% cobertura):
```
============================= test session starts ==============================
collected 15 items

tests/test_engine.py::test_R1_Nominal PASSED                             [  6%]
tests/test_engine.py::test_R1_Cero PASSED                                [ 13%]
tests/test_engine.py::test_R2_Nominal PASSED                             [ 20%]
tests/test_engine.py::test_R2_Cero PASSED                                [ 26%]
tests/test_engine.py::test_R3_Nominal PASSED                             [ 33%]
tests/test_engine.py::test_R3_Sin_Extras PASSED                          [ 40%]
tests/test_engine.py::test_R4_Aplica PASSED                              [ 46%]
tests/test_engine.py::test_R4_En_El_ToPE PASSED                          [ 53%]
tests/test_engine.py::test_R4_No_Aplica PASSED                           [ 60%]
tests/test_engine.py::test_R5_Salario_Invalido PASSED                    [ 66%]
tests/test_engine.py::test_R5_Horas_Negativas PASSED                     [ 73%]
tests/test_engine.py::test_R5_VlrHora_Cero PASSED                        [ 80%]
tests/test_engine.py::test_R5_VlrHora_Negativa PASSED                    [ 86%]
tests/test_engine.py::test_R5_VlrHora_NaN PASSED                         [ 93%]
tests/test_engine.py::test_R5_VlrHora_Infinito PASSED                    [100%]

================================ tests coverage ================================
Name            Stmts   Miss  Cover
-----------------------------------
src/engine.py      36      0   100%
-----------------------------------
TOTAL              36      0   100%
============================== 15 passed in 0.10s ==============================
```

---

## 6. Ejecutar el Guardian Agent (pipeline completo local)

El Guardian Agent lee el oráculo (`casos_prueba.md`), genera las pruebas, las ejecuta y emite un veredicto:

```bash
python src/guardian_client.py
```

Esto ejecuta el siguiente flujo:

```
1. Lee casos_prueba.md (oráculo)
2. Intenta generar test_engine.py con OpenCode Zen API (modelo deepseek-v4-flash)
   ↓ Si falla la API → usa generación por plantilla (fallback)
3. Guarda test_engine.py en .planning/fix-all-audit-issues/
4. Ejecuta pytest con cobertura y reporte JUnit
5. Parsea resultados (duraciones reales, cobertura)
6. Emite veredicto.json en .planning/fix-all-audit-issues/
```

### Forzar fallback (sin API Key)

Si no quieres usar la API o no tienes conectividad:

```bash
FORCE_FALLBACK=1 python src/guardian_client.py
```

### Archivos generados

| Archivo | Ubicación | Descripción |
|---|---|---|
| `test_engine.py` | `.planning/fix-all-audit-issues/` | Pruebas Pytest generadas |
| `veredicto.json` | `.planning/fix-all-audit-issues/` | Veredicto con PASS/FAIL por escenario |
| `reporte_junit.xml` | `.planning/fix-all-audit-issues/` | Reporte JUnit de pytest |
| `llm_output_*.txt` | `artifacts/` | Output crudo de la LLM (auditoría) |

---

## 7. Mover resultados de DRAFT a producción

Los resultados del Guardian Agent se guardan primero en `.planning/` como DRAFT. Después de revisarlos, muévelos a producción:

```bash
bash scripts/copy_to_production.sh
```

Esto copia:
- `.planning/fix-all-audit-issues/test_engine.py` → `tests/test_engine.py`
- `.planning/fix-all-audit-issues/veredicto.json` → `veredicto.json`
- `.planning/fix-all-audit-issues/reporte_junit.xml` → `reporte_junit.xml`

---

## 8. Ejecutar dentro de Docker (aislamiento total)

### Paso 8.1: Construir la imagen

```bash
docker build -f infra/Dockerfile -t guardian .
```

La imagen es multi-stage:
- **Stage builder**: instala dependencias Python
- **Stage runtime**: imagen mínima con usuario non-root (`guardian`), permisos de solo lectura (`chmod 550`)

### Paso 8.2: Ejecutar el pipeline completo en contenedor

```bash
docker run --name guardian-test --read-only \
  -e OPENCODE_ZEN_API_KEY \
  guardian \
  python src/guardian_client.py
```

### Paso 8.3: Ejecutar solo las pruebas en contenedor

```bash
docker run --name guardian-test --read-only \
  -e OPENCODE_ZEN_API_KEY \
  guardian \
  python -m pytest tests/test_engine.py -v --tb=short \
    --junitxml=/tmp/reporte_junit.xml \
    --cov=src.engine --cov-report=term
```

### Paso 8.4: Extraer resultados del contenedor

```bash
docker cp guardian-test:/tmp/reporte_junit.xml reporte_junit.xml
docker rm guardian-test
```

### Flags de seguridad

| Flag | Propósito |
|---|---|
| `--read-only` | El contenedor no puede escribir en el filesystem |
| `-e OPENCODE_ZEN_API_KEY` | Inyecta la API key sin copiar `.env` a la imagen |
| `--rm` | Elimina el contenedor automáticamente al terminar |
| `USER guardian` | Ejecuta como usuario non-root (definido en Dockerfile) |

---

## 9. CI/CD (GitHub Actions)

El pipeline se ejecuta automáticamente en cada push a `main` o `develop`, y en pull requests a `main`.

### Flujo del CI

```
1. Checkout del repositorio
2. Build Docker image desde infra/Dockerfile
3. Validar conectividad OpenCode Zen (dentro del contenedor)
4. Generar test_engine.py con Guardian Agent (dentro del contenedor)
5. Ejecutar pruebas con docker run --read-only
6. Extraer veredicto.json y reporte_junit.xml con docker cp
7. Generar veredicto.json desde JUnit XML
8. Upload artifacts a GitHub
```

### Configurar GitHub Secrets

1. Ve a tu repositorio → **Settings** → **Secrets and variables** → **Actions**
2. Crea un nuevo secret:
   - **Name:** `OPENCODE_ZEN_API_KEY`
   - **Value:** tu clave de OpenCode Zen

### Verificar ejecución

Ve a **Actions** en GitHub y busca el workflow "Guardian Agent CI". Los artifacts descargables son:
- `veredicto` → `veredicto.json`
- `reporte-junit` → `reporte_junit.xml`

---

## 10. Solución de problemas

### Error: `OPENCODE_ZEN_API_KEY no está definida`

```bash
# Verifica que la variable exista
echo $OPENCODE_ZEN_API_KEY

# Si está vacía, carga el .env
source .env
# O exporta directamente
export OPENCODE_ZEN_API_KEY="sk-tu-clave-aqui"
```

### Error: `ModuleNotFoundError: No module named 'src'`

Ejecuta desde la raíz del proyecto:

```bash
cd /ruta/al/QualityGuardian-NominaPro
python src/guardian_client.py
```

### Error: `docker: permission denied`

```bash
# Agrega tu usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### Error: `pytest-cov: unrecognized arguments`

```bash
pip install --user pytest-cov
```

### Error: Docker build falla con `COPY .env .env`

Este error ya no debería ocurrir (fue corregido). Si aparece, verifica que tu `infra/Dockerfile` NO tenga la línea `COPY .env .env`.

### La LLM no responde o da timeout

- Verifica tu conexión a internet
- Verifica que la API Key sea válida en el dashboard de OpenCode
- Usa `FORCE_FALLBACK=1` para ejecutar sin la API:

```bash
FORCE_FALLBACK=1 python src/guardian_client.py
```

---

## 11. Resumen rápido (comandos en orden)

```bash
# 1. Clonar
git clone https://github.com/nata890/QualityGuardian-NominaPro.git
cd QualityGuardian-NominaPro

# 2. Configurar API Key
echo 'OPENCODE_ZEN_API_KEY=sk-tu-clave' > .env

# 3. Instalar dependencias
pip install -r infra/requirements.txt

# 4. Probar el motor
python -c "from src.engine import liquidar_nomina; print(liquidar_nomina(1500000, 5, 3, 10000))"

# 5. Ejecutar pruebas
python -m pytest tests/test_engine.py -v --cov=src.engine

# 6. Ejecutar Guardian Agent
python src/guardian_client.py

# 7. Mover a producción
bash scripts/copy_to_production.sh

# 8. Docker (alternativa aislada)
docker build -f infra/Dockerfile -t guardian .
docker run --rm --read-only -e OPENCODE_ZEN_API_KEY guardian python -m pytest tests/test_engine.py -v
```
