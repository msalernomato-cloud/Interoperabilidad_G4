import requests
from patient import create_patient_resource


# Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource,resource_type):
    url = f"https://hapi.fhir.org/baseR4/{resource_type}"
    headers = {"Content-Type": "application/fhir+json"}
    # fhir.resources 8 (pydantic 2) usa model_dump_json; las versiones anteriores, json()
    if hasattr(resource, "model_dump_json"):
        resource_json = resource.model_dump_json(exclude_none=True)
    else:
        resource_json = resource.json()

    response = requests.post(url, headers=headers, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")
        
        # Devolver el ID del recurso creado
        return response.json()['id']
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar el recurso por ID 
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"https://hapi.fhir.org/baseR4/{resource_type}/{resource_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        resource = response.json()
        print(resource)
        return resource
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar pacientes por documento (Actividad 3.b)
def search_patient_by_dni(dni, system="http://www.renaper.gob.ar/dni"):
    url = "https://hapi.fhir.org/baseR4/Patient"
    # Búsqueda FHIR por identifier con el formato sistema|valor
    params = {"identifier": f"{system}|{dni}"}
    headers = {"Accept": "application/fhir+json", "Cache-Control": "no-cache"}
    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        bundle = response.json()  # una búsqueda devuelve un Bundle de tipo "searchset"
        patients = [entry["resource"] for entry in bundle.get("entry", [])]
        print(f"Pacientes encontrados con DNI {dni}: {len(patients)}")
        for p in patients:
            name = p.get("name", [{}])[0]
            print(f"- ID {p['id']}: {' '.join(name.get('given', []))} {name.get('family', '')}")
        return patients
    else:
        print(f"Error en la búsqueda: {response.status_code}")
        print(response.json())
        return []

# Buscar las condiciones de un paciente (para verificar el vínculo Patient-Condition)
def search_conditions_by_patient(patient_id):
    url = "https://hapi.fhir.org/baseR4/Condition"
    params = {"subject": f"Patient/{patient_id}"}
    headers = {"Accept": "application/fhir+json", "Cache-Control": "no-cache"}
    response = requests.get(url, params=params, headers=headers)
    bundle = response.json()
    conditions = [entry["resource"] for entry in bundle.get("entry", [])]
    print(f"Condiciones registradas para Patient/{patient_id}: {len(conditions)}")
    return conditions

