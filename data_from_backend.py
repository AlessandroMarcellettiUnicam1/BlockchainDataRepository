import requests

def all_collections_name():
    url = "http://127.0.0.1:5000/collections" # URL dell'endpoint Flask
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []

def fetch_all_data(contract_type):

    url = f"http://127.0.0.1:5000/informations?contract_type={contract_type}"  
    response = requests.get(url)  
    
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []
    
    expanded_data = []

    for record in data:
        # Mantenere i dati di base non complessi
        base_data = {
            "Activity": record.get("Activity", ""),
            "Block Number": record.get("Block Number", ""),
            "From": record.get("From", ""),
            "Transaction Hash": record.get("Transaction Hash", ""),
            "contractAddress": record.get("contractAddress", ""),
            "gasUsed": record.get("gasUsed", ""),
            "timestamp": record.get("timestamp", ""),
        }
    
        expanded_data.append(base_data)
    
    return expanded_data

def fetch_details_input(contract_type):

    url = f"http://127.0.0.1:5000/details_input?contract_type={contract_type}"  
    response = requests.get(url) 
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []


def fetch_details_storageState(contract_type):

    url = f"http://127.0.0.1:5000/details_storageState?contract_type={contract_type}" 
    response = requests.get(url) 
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []


def fetch_details_internalTxs(contract_type):

    url = f"http://127.0.0.1:5000/details_internalTxs?contract_type={contract_type}" 
    response = requests.get(url)  
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []


def fetch_details_events(contract_type, activities):

    url = f"http://127.0.0.1:5000/details_events?contract_type={contract_type}&activities={activities}" 
    response = requests.get(url)  
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []


def fetch_ocel_data_event():
    url = "http://127.0.0.1:5000/ocel_Events_count" 
    response = requests.get(url) 

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []
    
def fetch_ocel_data_object():
    url = "http://127.0.0.1:5000/ocel_Object_count"  
    response = requests.get(url)  

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []

def fetch_ocel_event_relationships():
    url = "http://127.0.0.1:5000/ocel_Event_relations" 
    response = requests.get(url)  

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []
    
def fetch_ocel_object_relationships():
    url = "http://127.0.0.1:5000/ocel_Object_relations" 
    response = requests.get(url)  

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []

def fetch_ocel_time_events():
    url = "http://127.0.0.1:5000/ocel_analisiTemporale_events" 
    response = requests.get(url) 

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Errore nel recupero dei dati: {response.status_code}")
        return []
