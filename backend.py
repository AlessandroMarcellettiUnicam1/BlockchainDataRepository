from flask import Flask, jsonify, request
from pymongo import MongoClient
from collections import Counter

# Connessione a MongoDB
client = MongoClient("mongodb://localhost:27017/contracts") 
db = client["Contracts"]
collectionOcel = db["logs_Ocel_2_0"]


app = Flask(__name__)

@app.route('/collections', methods=['GET'])
def collections():
    return db.list_collection_names()

@app.route('/informations', methods=['GET'])
def informations():

    contract_type = request.args.get("contract_type", default="default_value", type=str)
    
    collection = db[contract_type]
    data = list(collection.find({}))

    # Mappatura delle colonne da rinominare
    rename_map = {
        "txHash": "Transaction Hash",
        "sender": "From",
        "activity": "Activity",
        "blockNumber": "Block Number",
    }
    
    # Rinomina le chiavi dei dizionari
    for record in data:
        for old_name, new_name in rename_map.items():
            if old_name in record:
                record[new_name] = record.pop(old_name)

        if "_id" in record:
            del record["_id"] 

    return jsonify(data)

@app.route('/details_input', methods = ['GET'])
def details_input():

    contract_type = request.args.get("contract_type", default="default_value", type=str)
    
    collection = db[contract_type]
    data = list(collection.find({}, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "inputs": 1, "_id": 0}))

    inputs_list = [
        {"Transaction Hash": doc.get("txHash", ""),
         "Block Number": doc.get("blockNumber", ""),
         "From": doc.get("sender", ""),
         "Activity": doc.get("activity", ""), 
         "Id": obj["inputId"], "Name": obj["inputName"], 
         "Type": obj["type"], "Value": obj["inputValue"]}
        for doc in data if "inputs" in doc
        for obj in doc["inputs"]
    ]  

    return jsonify(inputs_list)


@app.route('/details_storageState', methods = ['GET'])
def details_storageState():

    contract_type = request.args.get("contract_type", default="default_value", type=str)
    
    collection = db[contract_type]
    data = list(collection.find({}, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "storageState": 1, "_id": 0}))

    #inputs_list = [doc["inputs"] for doc in data if "inputs" in doc]

    storageState_list = [
        {"Transaction Hash": doc.get("txHash", ""),
         "Block Number": doc.get("blockNumber", ""),
         "From": doc.get("sender", ""),
         "Activity": doc.get("activity", ""), 
         "Id": obj["variableId"], "Name": obj["variableName"], 
         "Type": obj["type"], "Value": obj["variableValue"], 
         "RawValue": obj["variableRawValue"]}
        for doc in data if "storageState" in doc
        for obj in doc["storageState"]
    ]

    return jsonify(storageState_list)

@app.route('/details_events', methods = ['GET'])
def details_events():

    contract_type = request.args.get("contract_type", default="default_value", type=str)
    activities = request.args.get("activities", default= None, type=str)
    
    collection = db[contract_type]

    if activities == "approve,transfer,transferFrom":
        query = {"activity": {"$in": ["transferFrom", "approve", "transfer"]}}

        data = list(collection.find(query, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "events": 1, "_id": 0}))

        events_list = [
            {"Transaction Hash": doc.get("txHash", ""),
             "Block Number": doc.get("blockNumber", ""),
             "Sender": doc.get("sender", ""),
             "Activity": doc.get("activity", ""), 
             "Id": obj["eventId"], 
             "Name": obj["eventName"], 
             "From": obj.get("eventValues", []).get("owner" if obj["eventName"] == "Approval" else "from", ""), 
             "To": obj.get("eventValues", []).get("spender" if obj["eventName"] == "Approval" else "to", ""), 
             "Value": obj.get("eventValues", []).get("value", "")}
            for doc in data if "events" in doc
            for obj in doc["events"]
        ]
    elif activities == "safeTransferFrom":
        query = {"activity": {"$in": ["safeTransferFrom"]}}

        data = list(collection.find(query, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "events": 1, "_id": 0}))

        events_list = [
            {"Transaction Hash": doc.get("txHash", ""),
             "Block Number": doc.get("blockNumber", ""),
             "Sender": doc.get("sender", ""),
             "Activity": doc.get("activity", ""),
             "Id": obj["eventId"], "Name": obj["eventName"], 
             "From": obj.get("eventValues", []).get("owner" if obj["eventName"] == "Approval" else "from", ""), 
             "To": obj.get("eventValues", []).get("spender" if obj["eventName"] == "Approval" else "to", ""), 
             "Token Id": obj.get("eventValues", []).get("tokenId", "")}
            for doc in data if "events" in doc
            for obj in doc["events"]
        ]
    elif activities == "setApprovalForAll":
        query = {"activity": {"$in": ["setApprovalForAll"]}}

        data = list(collection.find(query, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "events": 1, "_id": 0}))

        events_list = [
            {"Transaction Hash": doc.get("txHash", ""),
             "Block Number": doc.get("blockNumber", ""),
             "Sender": doc.get("sender", ""),
             "Activity": doc.get("activity", ""),
             "Id": obj["eventId"], 
             "Name": obj["eventName"], "Owner": obj.get("eventValues", []).get("owner", ""), 
             "Operator": obj.get("eventValues", []).get("operator", ""), 
             "Approved": obj.get("eventValues", []).get("approved", "")}
            for doc in data if "events" in doc
            for obj in doc["events"]
        ]
    elif activities == "sendFrom":
        query = {"activity": {"$in": ["sendFrom"]}}

        data = list(collection.find(query, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "events": 1, "_id": 0}))

        events_list = [
            {"Transaction Hash": doc.get("txHash", ""),
             "Block Number": doc.get("blockNumber", ""),
             "Sender": doc.get("sender", ""),
             "Activity": doc.get("activity", ""),
             "Id": obj["eventId"], 
             "Name": obj["eventName"], 
             "ChainID": obj.get("eventValues", {}).get("_dstChainId", ""), 
             "From": obj.get("eventValues", {}).get("_from" if obj["eventName"] == "SendToChain" else "from", ""), 
             "To": obj.get("eventValues", {}).get("_toAddress" if obj["eventName"] == "SendToChain" else "from", ""), 
             "Amount": obj.get("eventValues", {}).get("_amount", "")}
            for doc in data if "events" in doc
            for obj in doc["events"]
        ]
    else:
        query = {"activity": {"$in": ["transferOwnership"]}}

        data = list(collection.find(query, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "events": 1, "_id": 0}))

        events_list = [
            {"Transaction Hash": doc.get("txHash", ""),
             "Block Number": doc.get("blockNumber", ""),
             "Sender": doc.get("sender", ""),
             "Activity": doc.get("activity", ""),
             "Id": obj["eventId"], "Name": obj["eventName"], 
             "Previuous Owner": obj.get("eventValues", []).get("previousOwner", ""), 
             "New Owner": obj.get("eventValues", []).get("newOwner", "")}
            for doc in data if "events" in doc
            for obj in doc["events"]
        ]
    return jsonify(events_list)


@app.route('/details_internalTxs', methods = ['GET'])
def details_internalTxs():

    contract_type = request.args.get("contract_type", default="default_value", type=str)
    
    collection = db[contract_type]
    data = list(collection.find({}, {"txHash": 1, "blockNumber": 1, "sender": 1, "activity": 1, "internalTxs": 1, "_id": 0}))

    internalTxs_list = [
        {"Transaction Hash": doc.get("txHash", ""),
         "Block Number": doc.get("blockNumber", ""),
         "From": doc.get("sender", ""),
         "Activity": doc.get("activity", ""), 
         "Id": obj["callId"], 
         "Type": obj["callType"], 
         "To": obj["to"]}
        for doc in data if "internalTxs" in doc
        for obj in doc["internalTxs"]
    ]

    return jsonify(internalTxs_list)


@app.route('/ocel_Events_count', methods = ['GET'])
def events_count():

    data_ocel = collectionOcel.find({}, {"eventTypes.name": 1, "_id": 0})
    
    # Estrarre i nomi degli eventi e formattarli in dizionari
    event_names = []
    for doc in data_ocel:
        if "eventTypes" in doc:
            for event in doc["eventTypes"]:
                 event_names.append(event["name"])

    event_type_counter = Counter()

    data_ocel_events = collectionOcel.find({}, {"events.type": 1, "_id": 0})

    for doc in data_ocel_events:
        for event in doc["events"]:
            event_type = event.get("type") 
            if event_type in event_names: 
                event_type_counter[event_type] += 1
    
    event_counts = [{"Event Type": event_type, "Occurency": count} for event_type, count in event_type_counter.items()]

    return jsonify(event_counts)


@app.route('/ocel_Object_count', methods=['GET'])
def ocelInformationsObjects():
    data_ocel = list(collectionOcel.find({}, {"objectTypes.name": 1, "_id": 0}))

    object_names = []
    for doc in data_ocel:
        if "objectTypes" in doc:
            for object in doc["objectTypes"]:
                 object_names.append(object["name"])
    
    object_type_counter = Counter()

    data_ocel_objects = collectionOcel.find({}, {"objects": 1, "_id": 0})

    for doc in data_ocel_objects:
        for object in doc["objects"]:
            object_type = object.get("type")  
            if object_type in object_names:  
                object_type_counter[object_type] += 1
    
    object_counts = [{"Object Type": object_type, "Occurency": count} for object_type, count in object_type_counter.items()]

    return jsonify(object_counts)


@app.route('/ocel_Event_relations')
def event_relations():
    
    data_ocel = collectionOcel.find({}, {"events": 1, "_id": 0})
    relationships_count = Counter()

    for doc in data_ocel:
        if "events" in doc:
            for event in doc["events"]:
                event_type = event.get("type", "")

                for relation in event.get("relationships", []):  
                    relation_type = relation.get("qualifier", "")

                    if event_type and relation_type:  # Evitiamo valori vuoti
                        relationships_count[(event_type, relation_type)] += 1

    relations = [
        {"Event": event_type, "Relationship": relation_type, "Occurency": count} for (event_type, relation_type), count in relationships_count.items()
    ]

    return jsonify(relations)

@app.route('/ocel_Object_relations')
def object_relations():

    data_ocel = collectionOcel.find({}, {"objects": 1, "_id": 0})
    relationships_count = Counter()

    for doc in data_ocel:
        if "objects" in doc:
            for object in doc["objects"]:
                object_type = object.get("type", "")

                for relation in object.get("relationships", []):  
                    relation_type = relation.get("qualifier", "")

                    if object_type and relation_type:  # Evitiamo valori vuoti
                        relationships_count[(object_type, relation_type)] += 1

    relations = [
        {"Object": object_type, "Relationship": relation_type, "Occurency": count} for (object_type, relation_type), count in relationships_count.items()
    ]

    return jsonify(relations)

@app.route('/ocel_analisiTemporale_events')
def analisiTemporale_events():
    data_ocel = collectionOcel.find({}, {"events": 1, "_id":0})

    events = []

    for document in data_ocel:
        if "events" in document:
            for event in document["events"]:
                timestamp = event.get("time")
                event_type = event.get("type")
                
                if timestamp and event_type:
                    events.append({
                        "Day": timestamp,
                        "Activity": event_type
                    })

    return jsonify(events)
    

if __name__ == '__main__':
    app.run(debug=True)
