# Oráculo de Pruebas — Nómina Colombiana

> Fuente de verdad contractual para el Guardian Agent.
> Cada escenario incluye `vlr_hora` explícito y formato Gherkin estricto.

---

## Escenarios

### Scenario: CP-01 — Recargo diurno 25%
Given un salario base de 2_000_000
And 10 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el recargo diurno debe ser 125_000.0 (10 * 10_000 * 1.25)
And el recargo nocturno debe ser 0.0
And el total devengado debe ser 2_125_000.0

### Scenario: CP-02 — Recargo nocturno 75%
Given un salario base de 2_000_000
And 0 horas extras diurnas
And 8 horas extras nocturnas
And un valor de hora de 12_000
When se calcula la nómina
Then el recargo nocturno debe ser 168_000.0 (8 * 12_000 * 1.75)
And el recargo diurno debe ser 0.0
And el total devengado debe ser 2_168_000.0

### Scenario: CP-03 — Recargos diurno y nocturno simultáneos
Given un salario base de 3_000_000
And 5 horas extras diurnas
And 4 horas extras nocturnas
And un valor de hora de 15_000
When se calcula la nómina
Then el recargo diurno debe ser 93_750.0 (5 * 15_000 * 1.25)
And el recargo nocturno debe ser 105_000.0 (4 * 15_000 * 1.75)
And el total devengado debe ser 3_198_750.0

### Scenario: CP-04 — Deducciones sobre total devengado
Given un salario base de 2_500_000
And 5 horas extras diurnas
And 2 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el total devengado debe ser 2_597_500.0
And el descuento de salud debe ser 103_900.0 (2_597_500 * 0.04)
And el descuento de pensión debe ser 103_900.0 (2_597_500 * 0.04)
And las deducciones no deben calcularse únicamente sobre el salario base

### Scenario: CP-05 — Auxilio de transporte aplica (salario en el tope)
Given un salario base de 2_600_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el auxilio de transporte debe ser 162_000.0

### Scenario: CP-06 — Auxilio de transporte no aplica (salario sobre el tope)
Given un salario base de 2_600_001
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el auxilio de transporte debe ser 0.0

### Scenario: CP-07 — Salario inferior al SMMLV lanza ValueError
Given un salario base de 500_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que el salario es inferior al SMMLV

### Scenario: CP-08 — Horas extras diurnas negativas lanza ValueError
Given un salario base de 2_000_000
And -3 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que las horas no pueden ser negativas

### Scenario: CP-09 — Horas extras nocturnas negativas lanza ValueError
Given un salario base de 2_000_000
And 0 horas extras diurnas
And -2 horas extras nocturnas
And un valor de hora de 10_000
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que las horas no pueden ser negativas

### Scenario: CP-10 — Cálculo completo de nómina
Given un salario base de 2_400_000
And 6 horas extras diurnas
And 3 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el recargo diurno debe ser 75_000.0 (6 * 10_000 * 1.25)
And el recargo nocturno debe ser 52_500.0 (3 * 10_000 * 1.75)
And el total devengado debe ser 2_527_500.0
And el descuento de salud debe ser 101_100.0
And el descuento de pensión debe ser 101_100.0
And el auxilio de transporte debe ser 162_000.0
And el total a pagar debe ser 2_487_300.0

### Scenario: CP-11 — Horas extras en cero (sin recargos)
Given un salario base de 1_500_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el recargo diurno debe ser 0.0
And el recargo nocturno debe ser 0.0
And el total devengado debe ser igual al salario base (1_500_000.0)

### Scenario: CP-12 — Valor de hora en cero lanza ValueError
Given un salario base de 1_500_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 0
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que el valor de la hora debe ser positivo

### Scenario: CP-13 — Valor de hora negativo lanza ValueError
Given un salario base de 1_500_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de -5_000
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que el valor de la hora debe ser positivo

### Scenario: CP-14 — Salario exactamente en SMMLV (caso límite)
Given un salario base de 1_300_000
And 0 horas extras diurnas
And 0 horas extras nocturnas
And un valor de hora de 10_000
When se calcula la nómina
Then el auxilio de transporte debe ser 162_000.0
And no debe lanzarse ninguna excepción

---

## Reglas de Negocio Cubiertas

| Regla | Descripción | Escenarios |
|---|---|---|
| R1 | Recargo diurno 25% | CP-01, CP-03, CP-04, CP-10 |
| R2 | Recargo nocturno 75% | CP-02, CP-03, CP-04, CP-10 |
| R3 | Deducciones 4% salud + 4% pensión | CP-04, CP-10 |
| R4 | Auxilio transporte si salario ≤ $2.600.000 | CP-05, CP-06, CP-10, CP-14 |
| R5 | Validaciones de entrada | CP-07, CP-08, CP-09, CP-12, CP-13 |
