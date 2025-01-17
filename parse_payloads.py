from pprint import pprint
import pandas as pd
import json


from example_payloads import dataset_payload, timeseries_payload
from sparkplugb_validator.validator import SparkplugBPayload


with open("mixed_payload.json", "r") as f:
    mixed_payload_json_str = f.read()

mixed_payload = json.loads(mixed_payload_json_str)


def display_metrics(payload):
    validated_payload = SparkplugBPayload(**payload)

    for metric in validated_payload.metrics:
        print(metric.name, metric.dataType, metric.value)
        if metric.properties:
            for k, v in zip(metric.properties.keys, metric.properties.values):
                print("  Property:", k, "=", v.value)


def parse_to_df(payload):
    # Extract columns and rows from the payload
    columns = payload["metrics"][0]["value"]["columns"]
    rows = payload["metrics"][0]["value"]["rows"]

    data = []
    for row in rows:
        data.append(row["elements"])

    # Create the DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Display the DataFrame
    print(df)


def parse_dataset_to_df(payload):

    payload = SparkplugBPayload(**payload)
    df = payload.metrics[0].value.to_dataframe()
    print(df)


def validate_payload(payload):
    validated_payload = SparkplugBPayload(**payload)
    print("\nValidated Payload:")
    pprint(validated_payload.model_dump(), width=120, indent=4)


if __name__ == "__main__":
    validate_payload(dataset_payload)
    validate_payload(timeseries_payload)

    print("\nDataFrame:")
    parse_to_df(dataset_payload)

    print("\nDataFrame from DataSet:")
    parse_dataset_to_df(dataset_payload)

    print("\nMixed Payload:")
    display_metrics(mixed_payload)
