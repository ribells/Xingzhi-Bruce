import requests
import os
import json
import torch
import ml_collections
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    RobertaTokenizer,
    get_linear_schedule_with_warmup,
    set_seed,
    AutoConfig,
    RobertaForSequenceClassification,
)
import spacy

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")
nlp = spacy.load("en_core_web_sm")

# Setting up the model hyperparameters
def model_config():
    cfg_dictionary = {
        "data_path": "data.csv",
        "model_path": "/kaggle/working/bert_model.h5",
        "model_type": "transformer",

        "test_size": 0.1,
        "validation_size":0.2,
        "train_batch_size": 32,
        "eval_batch_size": 32,

        "epochs": 1,
        "adam_epsilon": 1e-8,
        "lr": 3e-5,
        "num_warmup_steps": 10,

        "max_length": 128,
        "random_seed": 42,
        "num_labels": 3,
        "model_checkpoint":"roberta-base",
    }
    cfg = ml_collections.FrozenConfigDict(cfg_dictionary)

    return cfg
cfg = model_config()

# Gets model
model = AutoModelForSequenceClassification.from_pretrained(
    cfg.model_checkpoint, num_labels=cfg.num_labels,
)

# Prepares tokenizer
tokenizer = AutoTokenizer.from_pretrained(cfg.model_checkpoint,use_fast=True)
state_dict = torch.load("model")
model.load_state_dict(state_dict)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print(json.dumps(response.json()))


def set_rules(delete):
    # You can adjust the rules if needed
    sample_rules = [
        {"value": "stock", "tag": "market"},
    ]
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print(json.dumps(response.json()))

def make_prediction(input):
    # Gets prediction from input
    inputs = tokenizer(input, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs).logits
    predicted_class_id = outputs.argmax(dim=-1).item()

    prediction = model.config.id2label[predicted_class_id]

    doc = nlp(input)
    nouns = [chunk.text for chunk in doc.noun_chunks]
    tickers = []

    for noun in nouns:
        if noun[0] == "$":
            tickers.append(noun)

    if len(tickers) != 0:
        if (prediction == "LABEL_0"):
            print(tickers, "SHORT")
        elif (prediction == "LABEL_2"):
            print(tickers, "LONG")


def get_stream(set):
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            make_prediction(json_response["data"]["text"])

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set)


if __name__ == "__main__":
    main()
