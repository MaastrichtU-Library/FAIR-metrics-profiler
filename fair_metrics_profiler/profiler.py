import requests
import pandas as pd
import re

BASE_API_URL = "https://api.fair-enough.semanticscience.org/evaluations"

def fetch_fair_evaluation(doi_url):
    """
    Fetches the FAIR evaluation for a given DOI URL using the FAIR API.
    """
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "subject": doi_url,
        "collection": "fair-enough-metadata"
    }
    
    response = requests.post(BASE_API_URL, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        return None

def process_evaluation_data(data_sample):
    """
    Processes the evaluation data for a given DOI and returns the results as a dictionary.
    """
    attributes = [
    "https://w3id.org/fair-enough/metrics/tests/f1-metadata-identifier-persistent",
    "https://w3id.org/fair-enough/metrics/tests/f1-metadata-identifier-unique",
    "https://w3id.org/fair-enough/metrics/tests/a1-metadata-authorization",
    "https://w3id.org/fair-enough/metrics/tests/a1-metadata-protocol",
    "https://w3id.org/fair-enough/metrics/tests/f2-structured-metadata",
    "https://w3id.org/fair-enough/metrics/tests/f1-data-identifier-persistent",
    "https://w3id.org/fair-enough/metrics/tests/f3-metadata-identifier-in-metadata",
    "https://w3id.org/fair-enough/metrics/tests/i3-metadata-contains-outward-links",
    "https://w3id.org/fair-enough/metrics/tests/r1-includes-license",
    "https://w3id.org/fair-enough/metrics/tests/f2-grounded-metadata",
    "https://w3id.org/fair-enough/metrics/tests/a1-data-protocol",
    "https://w3id.org/fair-enough/metrics/tests/a1-data-authorization",
    "https://w3id.org/fair-enough/metrics/tests/a2-metadata-persistent",
    "https://w3id.org/fair-enough/metrics/tests/f3-data-identifier-in-metadata",
    "https://w3id.org/fair-enough/metrics/tests/i1-data-knowledge-representation-structured",
    "https://w3id.org/fair-enough/metrics/tests/i1-metadata-knowledge-representation-structured",
    "https://w3id.org/fair-enough/metrics/tests/f4-searchable",
    "https://w3id.org/fair-enough/metrics/tests/i1-data-knowledge-representation-semantic",
    "https://w3id.org/fair-enough/metrics/tests/i2-fair-vocabularies-known",
    "https://w3id.org/fair-enough/metrics/tests/i1-metadata-knowledge-representation-semantic",
    "https://w3id.org/fair-enough/metrics/tests/r1-includes-standard-license",
    "https://w3id.org/fair-enough/metrics/tests/i2-fair-vocabularies-resolve"
    ]

    rows = []

    for attribute in attributes:
        metric_results = data_sample["contains"].get(attribute, [])
        if not metric_results:
            continue

        metric_result = metric_results[0]
        value = metric_result.get("http://semanticscience.org/resource/SIO_000300", [{}])[0].get("@value", None)
        comment = metric_result.get("http://schema.org/comment", [{}])[0].get("@value", None)
        if comment:
            matches = re.findall(r"(INFO|SUCCESS|FAILURE): \[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\] .+", comment)
            if matches:
                comment = matches[-1]

        rows.append({
            "_id": data_sample["_id"],
            "subject": data_sample["subject"],
            "created_at": data_sample["created_at"],
            "name": data_sample["name"],
            "fair_metric": attribute.split("/")[-1],
            "value": value,
            "comment": comment
        })

    return rows

def evaluate_doi_list_from_csv(csv_file_path):
    """
    Takes in a CSV file path containing a list of DOIs, evaluates each DOI using the FAIR enough API, and returns a DataFrame.
    """
    doi_list = pd.read_csv(csv_file_path)["DOI"].tolist()
    all_rows = []

    for doi in doi_list:
        data_sample = fetch_fair_evaluation(doi)
        if data_sample:
            rows = process_evaluation_data(data_sample)
            all_rows.extend(rows)

    return pd.DataFrame(all_rows)

def save_to_excel(df, output_file="FAIR_metrics_report.xls"):
    """
    Saves the given DataFrame to an Excel file.
    """
    df.to_excel(output_file)
