# Se usa la versión R4B del estándar porque el servidor HAPI público es R4.
# fhir.resources >= 7 trae R4B en un subpaquete; la 6.x lo trae por defecto.
try:
    from fhir.resources.R4B.patient import Patient
    from fhir.resources.R4B.humanname import HumanName
    from fhir.resources.R4B.contactpoint import ContactPoint
    from fhir.resources.R4B.identifier import Identifier
except ImportError:
    from fhir.resources.patient import Patient
    from fhir.resources.humanname import HumanName
    from fhir.resources.contactpoint import ContactPoint
    from fhir.resources.identifier import Identifier

# Sistema de identificación para el DNI argentino
DNI_SYSTEM = "http://www.renaper.gob.ar/dni"


# Crear el recurso FHIR de paciente con parámetros opcionales
def create_patient_resource(family_name=None, given_name=None, birth_date=None, gender=None, phone=None, dni=None):
    patient = Patient()

    # Agregar el DNI como identifier si está disponible (Actividad 3.a)
    if dni:
        identifier = Identifier()
        identifier.use = "official"
        identifier.system = DNI_SYSTEM
        identifier.value = dni
        patient.identifier = [identifier]

    # Agregar el nombre del paciente si está disponible
    if family_name or given_name:
        name = HumanName()
        if family_name:
            name.family = family_name
        if given_name:
            name.given = [given_name]
        patient.name = [name]

    # Agregar la fecha de nacimiento si está disponible
    if birth_date:
        patient.birthDate = birth_date

    # Agregar el género si está disponible
    if gender:
        patient.gender = gender

    # Agregar información de contacto si está disponible
    if phone:
        contact = ContactPoint()
        contact.system = "phone"
        contact.value = phone
        contact.use = "mobile"
        patient.telecom = [contact]

    return patient
