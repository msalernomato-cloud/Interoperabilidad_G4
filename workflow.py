from patient import create_patient_resource
from condition import create_condition_resource
from base import (send_resource_to_hapi_fhir, get_resource_from_hapi_fhir,
                  search_patient_by_dni, search_conditions_by_patient)

if __name__ == "__main__":
    # Parámetros del paciente
    family_name = "Gómez"
    given_name = "Lucía"
    birth_date = "1998-03-21"
    gender = "female"
    phone = "+5491155554444"
    dni = "40947123"  

    # ---- 3.a Crear y leer el paciente con DNI ----
    print("\n===== 3.a Crear y leer Patient =====")
    patient = create_patient_resource(family_name, given_name, birth_date, gender, phone, dni)
    patient_id = send_resource_to_hapi_fhir(patient, 'Patient')
    if patient_id:
        get_resource_from_hapi_fhir(patient_id, 'Patient')

    # ---- 3.b Buscar el paciente por DNI ----
    print("\n===== 3.b Buscar Patient por DNI =====")
    search_patient_by_dni(dni)

    # ---- 3.c Crear y leer una Condition para el paciente (Grupo 4) ----
    print("\n===== 3.c Crear y leer Condition =====")
    if patient_id:
        condition = create_condition_resource(
            patient_id=patient_id,
            snomed_code="38341003",
            snomed_display="Hypertensive disorder, systemic arterial (disorder)",
            onset_date="2025-08-10",
            recorded_date="2025-08-15",
            note="Diagnosticada en control clínico. Inicia tratamiento con enalapril."
        )
        condition_id = send_resource_to_hapi_fhir(condition, 'Condition')
        if condition_id:
            get_resource_from_hapi_fhir(condition_id, 'Condition')
            search_conditions_by_patient(patient_id)
