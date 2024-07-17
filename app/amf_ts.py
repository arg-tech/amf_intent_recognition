import torch
from transformers import BertForSequenceClassification, BertTokenizer
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, timedelta

def filter_xaif(xaif_data):
    filtered_xaif = xaif_data.copy()
    l_ya_edges = []
    l_ya_speaker = []

    if "nodes" in xaif_data["AIF"]:
        for i, node in enumerate(xaif_data["AIF"]["nodes"]):
            if node['type'] == 'L' or node['type'] == 'YA' or node['type'] == 'CA' or node['type'] == 'RA' or node['type'] == 'I' or node['type'] == 'TA':
                # Add progressive timestamp to the node
                timestamp = (datetime(2023, 1, 10, 00, 00, 10) + timedelta(seconds=i)).strftime("%H:%M:%S")
                node['timestamp'] = timestamp
                l_ya_speaker.append(node)

    if "edges" in xaif_data["AIF"]:
        for edge in xaif_data["AIF"]["edges"]:
            if edge:
                l_ya_edges.append(edge)
            
    # Remove the timestamp, scheme, and schemeID keys and their values from the nodes
    for node in l_ya_speaker:
        #node.pop("timestamp", None)
        node.pop("scheme", None)
        node.pop("schemeID", None)

    filtered_xaif["AIF"]["nodes"] = l_ya_speaker
    filtered_xaif["AIF"]["edges"] = l_ya_edges

    return filtered_xaif

def filter_nodes(comma):    
    
    filtered_nodes = []
    for edge in comma["AIF"]["edges"]:
        from_id = edge['fromID']
        to_id = edge['toID']
    
        l_node = next((node for node in comma["AIF"]['nodes'] if node['type'] == 'L' and node['nodeID'] == from_id), None)
        ya_node = next((node for node in comma["AIF"]['nodes'] if node['type'] == 'YA' and node['nodeID'] == to_id), None)
    
        if l_node is not None and ya_node is not None:
            filtered_nodes.append(ya_node)
            filtered_nodes.append(l_node)
            
    comma["AIF"]["nodes"] = filtered_nodes

    return comma

def input (filtered):
    list1 = []
    
    # Check for fromID keys in edges that match nodeID keys in nodes with type L
    for edge in filtered["AIF"]["edges"]:
        for node in filtered["AIF"]["nodes"]:
            if node["nodeID"] == edge["fromID"] and node["type"] == "L":
                list1.append(node["text"])

    return list1

def output (filtered):
    list2 = []

    for edge in filtered["AIF"]["edges"]:
        for node in filtered["AIF"]["nodes"]:
            if node["nodeID"] == edge["toID"] and node["type"] == "YA":
                list2.append(node["text"])

    return list2

# Create a function to make predictions
def predict(intent, tokenizer, model):
    # Tokenize input text
    inputs = tokenizer(intent, padding=True, truncation=True, return_tensors="pt")

    # Get predictions from model
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities
    probs = torch.softmax(outputs.logits, dim=1)

    # Return the predicted class (0 or 1) with the highest probability
    return torch.argmax(probs).item()

def get_predicted_values(inputs, tokenizer, model):
    # Instantiate an empty list to store the predicted values
    predicted_values = []

    # Call the predict function for each input text
    for intent in inputs:
        predicted_value = predict(intent, tokenizer, model)
        predicted_values.append(predicted_value)

    return predicted_values

def mind(comma, intentions):
    # Update the values of the text key in the nodes with the predicted values
    ya_nodes = [node for node in comma["AIF"]["nodes"] if node["type"] == "YA"]
    for node, intention in zip(ya_nodes, intentions):
        node["text"] = intention  # Update the text value with the predicted value

    return comma

def generate_predictions_amf_ts(input_xaif_data):
    comma = filter_xaif(input_xaif_data)
    filtered = (filter_nodes(comma))
    # Load BERT model and tokenizer
    model_path = 'Godfrey2712/amf_ir'
    tokenizer_path = 'Godfrey2712/amf_ir_bert_tokens'
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
    model = BertForSequenceClassification.from_pretrained(model_path)

    # Set model to evaluation mode
    model.eval()

    # Call the input function
    locutions = input (filtered)
    inputs = locutions

    # List with decoded values
    labels = ['Popular Conceding', 'Arguing', 'Directive Questioning', 'Rhetorical Challenging', 'Agreeing', 'Asserting', 'Pure Questioning', 'Assertive Challenging', 'Pure Challenging', 'Ironic Asserting', 'Challenging', 'Disagreeing', 'Conceding', 'Ad verecundiam', 'Offering', 'Order', 'Default Illocuting', 'Assertive Questioning', 'Rhetorical Questioning']
    # Instantiate a LabelEncoder object
    label_encoder = LabelEncoder()

    # Fit the label encoder on the labels
    label_encoder.fit(labels)
    predicted_values = get_predicted_values(inputs, tokenizer, model)

    intentions = label_encoder.inverse_transform(predicted_values)

    predictions = mind(comma, intentions)

    return predictions