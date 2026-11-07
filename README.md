# TP6 Interoperabilidad – Grupo 4 (Condition)

16.22 Informática Médica – ITBA. Basado en el repo de la cátedra [FHIR-basics](https://github.com/euberrino/FHIR-basics).

Servidor: HAPI FHIR público R4 (`https://hapi.fhir.org/baseR4`).

## Patient
Creación del recurso paciente con algunos parámetros, incluido el DNI como `identifier` (Actividad 3.a).

## Condition
Creación del recurso Condition (problema de salud o diagnóstico) asociado a un paciente, codificado con SNOMED CT (Actividad 3.c).

## Base
Lectura y escritura de recursos en el servidor público de HAPI FHIR, búsqueda de pacientes por DNI (Actividad 3.b) y búsqueda de las condiciones de un paciente.

## Workflow
Desde acá se corre el código: `python workflow.py`
