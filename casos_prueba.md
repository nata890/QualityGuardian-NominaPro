ID: CP-01
 Descripción: Verificar que se calcule correctamente el recargo diurno del 25%.
Datos de entrada
salario_base = 2.000.000
horas_diurnas_extra = 10
horas_nocturnas_extra = 0
Resultado esperado
Valor hora calculado correctamente.
Cada hora extra diurna debe pagarse con un 25% adicional.
No deben existir recargos nocturnos.


ID: CP-02
 Descripción: Verificar que se calcule correctamente el recargo nocturno del 75%.
Datos de entrada
salario_base = 2.000.000
horas_diurnas_extra = 0
horas_nocturnas_extra = 8
Resultado esperado
Cada hora extra nocturna debe pagarse con un 75% adicional.
No deben existir recargos diurnos.

ID: CP-03
 Descripción: Verificar el cálculo simultáneo de horas diurnas y nocturnas.
Datos de entrada
salario_base = 3.000.000
horas_diurnas_extra = 5
horas_nocturnas_extra = 4
Resultado esperado
Las horas diurnas deben liquidarse con recargo del 25%.
Las horas nocturnas deben liquidarse con recargo del 75%.
El total devengado debe incluir ambos recargos.

ID: CP-04
 Descripción: Verificar que las deducciones se calculen sobre el total devengado.
Datos de entrada
salario_base = 2.500.000
horas_diurnas_extra = 5
horas_nocturnas_extra = 2
Resultado esperado
El total devengado debe incluir salario + extras.
Salud y pensión deben calcularse sobre ese total.
Las deducciones no deben calcularse únicamente sobre el salario base.

ID: CP-05
 Descripción: Verificar que el auxilio de transporte se otorgue cuando el salario base sea menor o igual a $2.600.000.
Datos de entrada
salario_base = 2.600.000
horas_diurnas_extra = 0
horas_nocturnas_extra = 0
Resultado esperado
El empleado debe recibir auxilio de transporte.

ID: CP-06
 Descripción: Verificar que el auxilio no se otorgue cuando el salario base supere $2.600.000.
Datos de entrada
salario_base = 2.600.001
horas_diurnas_extra = 0
horas_nocturnas_extra = 0
Resultado esperado
El empleado no debe recibir auxilio de transporte.

ID: CP-07
 Descripción: Verificar que se lance una excepción cuando el salario sea inferior al SMMLV.
Datos de entrada
salario_base = 500.000
horas_diurnas_extra = 0
horas_nocturnas_extra = 0
Resultado esperado
Debe lanzarse un ValueError..
El mensaje debe indicar que el salario es inferior al SMMLV.

ID: CP-08
 Descripción: Verificar validación de horas extra diurnas negativas.
Datos de entrada
salario_base = 2.000.000
horas_diurnas_extra = -3
horas_nocturnas_extra = 0
Resultado esperado
Debe lanzarse un ValueError.
El mensaje debe indicar que las horas no pueden ser negativas.

ID: CP-09
 Descripción: Verificar validación de horas extra nocturnas negativas.
Datos de entrada
salario_base = 2.000.000
horas_diurnas_extra = 0
horas_nocturnas_extra = -2
Resultado esperado
Debe lanzarse un ValueError.
El mensaje debe indicar que las horas no pueden ser negativas.

ID: CP-10
 Descripción: Verificar un cálculo completo de nómina con extras, deducciones y auxilio.
Datos de entrada
salario_base = 2.400.000
horas_diurnas_extra = 6
horas_nocturnas_extra = 3
Resultado esperado
Deben calcularse correctamente:
Recargos diurnos.
Recargos nocturnos.
Total devengado.
Deducciones de salud y pensión.
Auxilio de transporte.
El resultado final debe ser consistente con todas las reglas R1–R4.










Escenarios Gherkins 

Feature: Cálculo de nómina con horas extras, deducciones y auxilio de transporte

Scenario: CP-01 Verificar cálculo del recargo diurno del 25%
Given un salario base de 2000000
And 10 horas extra diurnas
And 0 horas extra nocturnas
When se calcula la nómina
Then el valor de la hora debe calcularse correctamente
And cada hora extra diurna debe incluir un recargo del 25%
And no deben existir recargos nocturnos

Scenario: CP-02 Verificar cálculo del recargo nocturno del 75%
Given un salario base de 2000000
And 0 horas extra diurnas
And 8 horas extra nocturnas
When se calcula la nómina
Then cada hora extra nocturna debe incluir un recargo del 75%
And no deben existir recargos diurnos

Scenario: CP-03 Verificar cálculo simultáneo de horas diurnas y nocturnas
Given un salario base de 3000000
And 5 horas extra diurnas
And 4 horas extra nocturnas
When se calcula la nómina
Then las horas extra diurnas deben liquidarse con un recargo del 25%
And las horas extra nocturnas deben liquidarse con un recargo del 75%
And el total devengado debe incluir ambos recargos

Scenario: CP-04 Verificar cálculo de deducciones sobre el total devengado
Given un salario base de 2500000
And 5 horas extra diurnas
And 2 horas extra nocturnas
When se calcula la nómina
Then el total devengado debe incluir salario base y horas extras
And la salud debe calcularse sobre el total devengado
And la pensión debe calcularse sobre el total devengado
And las deducciones no deben calcularse únicamente sobre el salario base

Scenario: CP-05 Verificar otorgamiento de auxilio de transporte
Given un salario base de 2600000
And 0 horas extra diurnas
And 0 horas extra nocturnas
When se calcula la nómina
Then el empleado debe recibir auxilio de transporte

Scenario: CP-06 Verificar que no se otorgue auxilio de transporte
Given un salario base de 2600001
And 0 horas extra diurnas
And 0 horas extra nocturnas
When se calcula la nómina
Then el empleado no debe recibir auxilio de transporte

Scenario: CP-07 Verificar excepción por salario inferior al SMMLV
Given un salario base de 500000
And 0 horas extra diurnas
And 0 horas extra nocturnas
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que el salario es inferior al SMMLV

Scenario: CP-08 Verificar validación de horas extra diurnas negativas
Given un salario base de 2000000
And -3 horas extra diurnas
And 0 horas extra nocturnas
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que las horas no pueden ser negativas

Scenario: CP-09 Verificar validación de horas extra nocturnas negativas
Given un salario base de 2000000
And 0 horas extra diurnas
And -2 horas extra nocturnas
When se intenta calcular la nómina
Then debe lanzarse un ValueError
And el mensaje debe indicar que las horas no pueden ser negativas

Scenario: CP-10 Verificar cálculo completo de nómina
Given un salario base de 2400000
And 6 horas extra diurnas
And 3 horas extra nocturnas
When se calcula la nómina
Then deben calcularse correctamente los recargos diurnos
And deben calcularse correctamente los recargos nocturnos
And debe calcularse correctamente el total devengado
And deben calcularse correctamente las deducciones de salud y pensión
And el empleado debe recibir auxilio de transporte
And el resultado final debe ser consistente con las reglas R1 a R4 






REGLAS DE NEGOCIO

R1 & R2

Calcular recargos diurnos (25%) y nocturnos (75%) sobre el valor de la hora.

R3

Calcular deducciones de Salud y Pensión sobre el total devengado (salario + extras).

R4

Asignar Auxilio de Transporte solo si el salario_base es menor o igual a $2.600.000.

R5 (Validaciones)

Lanzar ValueError con mensajes descriptivos si el salario es inferior al SMMLV o si las horas son negativas.
