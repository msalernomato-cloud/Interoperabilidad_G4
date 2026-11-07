try:
    from fhir.resources.R4B.condition import Condition
except ImportError:
    from fhir.resources.condition import Condition


def make_concept(system, code, display):
    """Arma un CodeableConcept (código de una terminología + texto legible)."""
    return {
        "coding": [{"system": system, "code": code, "display": display}],
        "text": display
    }


# Crear el recurso FHIR Condition asociado a un paciente (Actividad 3.c - Grupo 4)
# Se arma como diccionario porque Condition tiene un campo obligatorio (subject)
# y no se puede crear vacío como el Patient.
def create_condition_resource(patient_id, snomed_code, snomed_display,
                              onset_date=None, recorded_date=None, note=None):
    data = {
        "resourceType": "Condition",

        # Estado clínico: active | recurrence | relapse | inactive | remission | resolved
        "clinicalStatus": make_concept(
            "http://terminology.hl7.org/CodeSystem/condition-clinical", "active", "Active"),

        # Estado de verificación: unconfirmed | provisional | differential | confirmed | refuted
        "verificationStatus": make_concept(
            "http://terminology.hl7.org/CodeSystem/condition-ver-status", "confirmed", "Confirmed"),

        # Categoría: problem-list-item | encounter-diagnosis
        "category": [make_concept(
            "http://terminology.hl7.org/CodeSystem/condition-category",
            "problem-list-item", "Problem List Item")],

        # Gravedad (SNOMED CT): 255604002 leve, 6736007 moderada, 24484000 severa
        "severity": make_concept("http://snomed.info/sct", "6736007", "Moderate"),

        # Qué condición es (SNOMED CT)
        "code": make_concept("http://snomed.info/sct", snomed_code, snomed_display),

        # A quién le pasa: referencia al Patient (campo obligatorio)
        "subject": {"reference": f"Patient/{patient_id}"},
    }

    # Cuándo comenzó y cuándo se registró
    if onset_date:
        data["onsetDateTime"] = onset_date
    if recorded_date:
        data["recordedDate"] = recorded_date

    # Observaciones en texto libre
    if note:
        data["note"] = [{"text": note}]

    return Condition(**data)  # fhir.resources valida la estructura contra el estándar
