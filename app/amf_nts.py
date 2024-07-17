from transformers import AutoTokenizer, pipeline
from amf_fast_inference import model

def filter_xaif(xaif_data):
    filtered_xaif = xaif_data.copy()
    l_ya_edges = []
    l_ya_speaker = []

    if "nodes" in xaif_data["AIF"]:
        for node in xaif_data["AIF"]["nodes"]:
            if node['type'] == 'L' or node['type'] == 'YA':
                l_ya_speaker.append(node)

    if "edges" in xaif_data["AIF"]:
        for edge in xaif_data["AIF"]["edges"]:
            if edge:
                l_ya_edges.append(edge)
            
    # Remove the timestamp, scheme, and schemeID keys and their values from the nodes
    for node in l_ya_speaker:
        node.pop("timestamp", None)
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

def input(filtered):
    list1 = []
    
    # Check for fromID keys in edges that match nodeID keys in nodes with type L
    for edge in filtered["AIF"]["edges"]:
        for node in filtered["AIF"]["nodes"]:
            if node["nodeID"] == edge["fromID"] and node["type"] == "L":
                list1.append(node["text"])

    return list1

def get_predicted_values(inputs, pipe):
    # Instantiate an empty list to store the predicted values
    predicted_values = []

    for text in inputs:
        prediction = pipe(text)
        predicted_values.append(prediction[0]['label'])  # Extract the label

    return predicted_values

def mind(comma, intentions):
    # Update the values of the text key in the nodes with the predicted values
    ya_nodes = [node for node in comma["AIF"]["nodes"] if node["type"] == "YA"]
    for node, intention in zip(ya_nodes, intentions):
        node["text"] = intention  # Update the text value with the predicted value

    return comma

def generate_predictions_amf_nts(input_xaif_data):
    comma = filter_xaif(input_xaif_data)
    filtered = (filter_nodes(comma))
    # Load BERT model and tokenizer
    model_path = 'Godfrey2712/amf_illoc_force_intent_recognition'

    # Load the tokenizer and model from the Hugging Face repository
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    loader = model.ModelLoader(model_path)
    pruned_model = loader.load_model()   

    # Initialize the pipeline with the loaded model and tokenizer
    pipe = pipeline('text-classification', model=pruned_model, tokenizer=tokenizer)

    # Call the input function
    locutions = input(filtered)
    inputs = locutions

    predicted_values = get_predicted_values(inputs, pipe)

    predictions = mind(comma, predicted_values)

    return predictions
