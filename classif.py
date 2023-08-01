import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
import csv
import os


def classify_lines_to_topic(csv_file, topic_keyword, threshold=0.5):
    # Read the CSV file into a pandas DataFrame with no header
    df = pd.read_csv(csv_file, header=None)

    # Get the list of lines from the DataFrame
    lines_list = df[0].tolist()

    # Load BERT tokenizer and model for sequence classification
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

    # Tokenize the topic keyword and get its ID
    topic_tokens = tokenizer(
        topic_keyword, return_tensors="pt", truncation=True, padding=True
    )
    topic_input_ids = topic_tokens.input_ids
    topic_attention_mask = topic_tokens.attention_mask

    # Prepare inputs for sequence classification (binary classification)
    inputs = tokenizer(
        lines_list,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=256,
        add_special_tokens=True,
    )

    # Set the topic keyword ID and attention mask for classification
    inputs["input_ids"][:, 0 : topic_input_ids.shape[1]] = topic_input_ids
    inputs["attention_mask"][:, 0 : topic_input_ids.shape[1]] = topic_attention_mask

    # Perform the classification
    with torch.no_grad():
        outputs = model(**inputs)

    # Get the predicted probabilities for the positive class
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)[:, 1]

    # Check if the probability of belonging to the topic is greater than the threshold
    is_topic = probabilities >= threshold

    return is_topic


def append_keywords_to_csv(csv_file, new_csv_file, lines_list, is_topic_list):
    # Append the keywords that belong to the topic to the new CSV file
    mode = "a" if os.path.exists(new_csv_file) else "w"
    with open(new_csv_file, mode, newline="") as new_file:
        writer = csv.writer(new_file)
        for line, is_topic in zip(lines_list, is_topic_list):
            if is_topic:
                writer.writerow([line])


if __name__ == "__main__":
    # Replace 'keywords.csv' with the path to your CSV file
    csv_file = "./navigations.csv"
    new_csv_file = "./keywords_topic.csv"
    topic_keyword = "espionnage"
    probability_threshold = 0.5

    # Classify each line to the topic
    lines_list = pd.read_csv(csv_file, header=None)[0].tolist()
    is_topic_list = classify_lines_to_topic(
        csv_file, topic_keyword, probability_threshold
    )
    for line, is_topic in zip(
        pd.read_csv(csv_file, header=None)[0].tolist(), is_topic_list
    ):
        if is_topic:
            print(f"Line: '{line}' belongs to the topic.")
        else:
            print(f"Line: '{line}' does not belong to the topic.")

    # Append keywords that belong to the topic to the new CSV file
    append_keywords_to_csv(csv_file, new_csv_file, lines_list, is_topic_list)
