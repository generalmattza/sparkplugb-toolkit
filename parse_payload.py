import pandas as pd
import json


from payload_structure import dataset_payload


if __name__ == "__main__":
    # Extract columns and rows from the payload
    columns = dataset_payload["metrics"][0]["value"]["columns"]
    rows = dataset_payload["metrics"][0]["value"]["rows"]

    data = []
    for row in rows:
        data.append(row["elements"])

    # Create the DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Display the DataFrame
    print(df)
