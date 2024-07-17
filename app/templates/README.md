

# Default Intent Recognition using Roberta-large

This service, part of the Argument Mining Framework (AMF), classifies illocutionary forces in locutions as either Agreeing, Arguing, Asserting, Assertive Questioning, Challenging, Default Illocuting, Disagreeing, Pure Questioning, Restating, Rhetorical Questioning. It leverages a pre-trained LLM fine-tuned on the QT30, US2016, MM123, and MM2012 dataset. It can be integrated into the argument mining pipeline alongside other AMF components for further analysis and processing.

## Table of Contents
- [Brief Overview of the Architecture/Method](#brief-overview-of-the-architecturemethod)
- [Endpoints](#endpoints)
  - [/bert-te](#bert-te)
- [Input and Output Formats](#input-and-output-formats)
  - [Input Format](#input-format)
  - [Output Format](#output-format)
- [Installation](#installation)
  - [Requirements for Installation](#requirements-for-installation)
  - [Installation Setup](#installation-setup)
    - [Using Docker Container](#using-docker-container)
    - [From Source Without Docker](#from-source-without-docker)
- [Usage](#usage)
  - [Using Programming Interface](#using-programming-interface)
  - [Using cURL](#using-curl)
  - [Using Web Interface](#using-web-interface)

## Brief Overview of the Architecture/Method
This application leverages a pruned and quantized BART model, fine-tuned on the MNLI dataset, to perform textual entailment in text-classification task settings. By pruning and quantizing the model, we achieve faster inference times without significantly compromising accuracy. The system maps entailment relations to support relations and contradiction relations to conflicts, for constructing argument structures. This approach ensures the model remains lightweight and suitable for real-time applications within AMF.

- **Dataset**: [Link to datasets](#)
- **Model ID**: [facebook/bart-large-mnli](https://huggingface.co/facebook/bart-large-mnli)
- **Repository**: [GitHub repository](https://github.com/arg-tech/bert-te)
- **Paper**: [Link to published paper](https://arxiv.org/abs/1909.00161)

### Endpoints

#### /bert-te

**Details**
- **URL**: `bert-te.amfws.arg.tech/bert-te`
- **Methods**: `GET`, `POST`

**GET Method**
- **Input**: No parameters
- **Output**: Returns information about the service and its usage.

**POST Method**
- **Input**: Expects a file upload (`file` parameter) in the xAIF format.
- **Output**: The route processes the uploaded file, identifies argument relations between I-nodes, updates the xAIF with these relations, and returns the updated xAIF as a JSON file.



## Input and Output Formats
### Input Format
- **JSON File**: The input must be in xAIF format. For details on the xAIF JSON format, refer to [xAIF format details](https://wiki.arg.tech/books/amf/page/xaif). xAIF json can be viewed as a dictionary containing list of nodes, edges, locutions, among others. 
- Argument units and their relations are represented as nodes. Both argument units and argument relations are classified by their type. 
  - **Argument Units**: Propositions are specified as type "I" nodes, while locution nodes are specified as type "L".
  - **Argument Relations**: Support relations are denoted as "RA" and attack relations as "CA".
- The relations between the nodes (argument units and relations) are presented as edges.
In the following example, the xAIF involves L nodes, I nodes, YA nodes (relation nodes connecting the L nodes with the I nodes).  The nodes indicating the argument relations between the I nodes are missing.

- **Example**: 
```python
{
  "AIF": {
    "descriptorfulfillments": null,
    "edges": [
      {
        "edgeID": 0,
        "fromID": 0,
        "toID": 4
      },
      {
        "edgeID": 1,
        "fromID": 4,
        "toID": 3
      },
      {
        "edgeID": 2,
        "fromID": 1,
        "toID": 6
      },
      {
        "edgeID": 3,
        "fromID": 6,
        "toID": 5
      },
      {
        "edgeID": 4,
        "fromID": 2,
        "toID": 8
      },
      {
        "edgeID": 5,
        "fromID": 8,
        "toID": 7
      }
    ],
    "locutions": [
      {
        "nodeID": 0,
        "personID": 0
      },
      {
        "nodeID": 1,
        "personID": 1
      },
      {
        "nodeID": 2,
        "personID": 2
      }
    ],
    "nodes": [
      {
        "nodeID": 0,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "L"
      },
      {
        "nodeID": 1,
        "text": "the SNP has disagreements.",
        "type": "L"
      },
      {
        "nodeID": 2,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "L"
      },
      {
        "nodeID": 3,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "I"
      },
      {
        "nodeID": 4,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 5,
        "text": "the SNP has disagreements.",
        "type": "I"
      },
      {
        "nodeID": 6,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 7,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "I"
      },
      {
        "nodeID": 8,
        "text": "Default Illocuting",
        "type": "YA"
      }
    ],
    "participants": [
      {
        "firstname": "Speaker",
        "participantID": 0,
        "surname": "1"
      },
      {
        "firstname": "Speaker",
        "participantID": 1,
        "surname": "2"
      }
    ],
    "schemefulfillments": null
  },
  "dialog": true,
  "ova": [],
  "text": {
    "txt": " Speaker 1 <span class=\"highlighted\" id=\"0\">disagreements between party members are entirely to be expected.</span>.<br><br> Speaker 2 <span class=\"highlighted\" id=\"1\">the SNP has disagreements.</span>.<br><br> Speaker 1 <span class=\"highlighted\" id=\"2\">it's not uncommon for there to be disagreements between party members. </span>.<br><br>"
  }
}
```



### Output Format
The inferred argument structure is returned in the xAIF format, including the argument relation nodes and their connecting edges, while preserving other information in a monotonic fashion. As demonstrated in the following example, the service identifies 1 "RA" node (nodeID 9) between "I" node 3 and 7.
- Example xAIF Output:

```python
{
  "AIF": {
    "descriptorfulfillments": null,
    "edges": [
      {
        "edgeID": 0,
        "fromID": 0,
        "toID": 4
      },
      {
        "edgeID": 1,
        "fromID": 4,
        "toID": 3
      },
      {
        "edgeID": 2,
        "fromID": 1,
        "toID": 6
      },
      {
        "edgeID": 3,
        "fromID": 6,
        "toID": 5
      },
      {
        "edgeID": 4,
        "fromID": 2,
        "toID": 8
      },
      {
        "edgeID": 5,
        "fromID": 8,
        "toID": 7
      },
      {
        "edgeID": 6,
        "fromID": 3,
        "toID": 9
      },
      {
        "edgeID": 7,
        "fromID": 9,
        "toID": 7
      }
    ],
    "locutions": [
      {
        "nodeID": 0,
        "personID": 0
      },
      {
        "nodeID": 1,
        "personID": 1
      },
      {
        "nodeID": 2,
        "personID": 2
      }
    ],
    "nodes": [
      {
        "nodeID": 0,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "L"
      },
      {
        "nodeID": 1,
        "text": "the SNP has disagreements.",
        "type": "L"
      },
      {
        "nodeID": 2,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "L"
      },
      {
        "nodeID": 3,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "I"
      },
      {
        "nodeID": 4,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 5,
        "text": "the SNP has disagreements.",
        "type": "I"
      },
      {
        "nodeID": 6,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 7,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "I"
      },
      {
        "nodeID": 8,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 9,
        "text": "Default Inference",
        "type": "RA"
      }
    ],
    "participants": [
      {
        "firstname": "Speaker",
        "participantID": 0,
        "surname": "1"
      },
      {
        "firstname": "Speaker",
        "participantID": 1,
        "surname": "2"
      }
    ],
    "schemefulfillments": null
  },
  "dialog": true,
  "ova": [],
  "text": {
    "txt": " Speaker 1 <span class=\"highlighted\" id=\"0\">disagreements between party members are entirely to be expected.</span>.<br><br> Speaker 2 <span class=\"highlighted\" id=\"1\">the SNP has disagreements.</span>.<br><br> Speaker 1 <span class=\"highlighted\" id=\"2\">it's not uncommon for there to be disagreements between party members. </span>.<br><br>"
  }
}
```


## Installation
### Requirements for Installation
- torch
- numpy
- transformers
- xaif_eval==0.0.9
- amf-fast-inference==0.0.3
- markdown2

### Installation Setup
#### Using Docker Container


1. **Clone the Repository:**
   ```sh
   git clone https://github.com/arg-tech/bert-te.git
   ```

2. **Navigate to the Project Root Directory:**
   ```sh
   cd bert-te
   ```

3. **Make Required Changes:**
   - Edit the `Dockerfile`, `main.py`, and `docker-compose.yml` files to specify the container name, port number, and other settings as needed.

4. **Build and Run the Docker Container:**
   ```sh
   docker-compose up
   ```

#### From Source Without Docker

If you prefer to install without Docker:

1. **Install Dependencies:**
   - Ensure Python and necessary libraries are installed.

2. **Configure and Run:**
   - Configure the environment variables and settings in `main.py`.
   - Run the application using Python:
     ```sh
     python main.py
     ```

## Usage

### Using Programming Interface
#### Example Python Code Snippet

```python
import requests
import json

url = 'http://your-server-url/bert-te'
input_file_path = 'example_xAIF.json'

with open(input_file_path, 'r', encoding='utf-8') as file:

    files = {'file': (input_file_path, file, 'application/json')}

response = requests.post(url, files=files)

if response.status_code == 200:

    output_file_path = 'output_xAIF.json'

    with open(output_file_path, 'w', encoding='utf-8') as output_file:

        json.dump(response.json(), output_file, ensure_ascii=False, indent=4)

    print(f'Response saved to {output_file_path}')

else:

    print(f'Failed to make a POST request. Status code: {response.status_code}')

    print(response.text)

```

### Using cURL

- **Example Request**:

```bash
curl -X POST \
  -F "file=@example_xAIF.json" \
  http://your-server-url/bert-te
```

### Using Web Interface

The service can also be used to create a pipeline on our n8n interface. 
The service can also be used to create a pipeline on our n8n interface. 

1. **Create an HTTP node**
2. **Configure the node** 
   - Specify the URL of the service
   - Include the parameter (`file`)


<div style="text-align:center;">
    <img src="img/n8n_screnshot.jpeg" alt="Image Description" width="40%">
</div>
