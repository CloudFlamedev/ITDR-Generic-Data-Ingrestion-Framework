import json
import csv
import xml.etree.ElementTree as ET
import io


def parse_json(file_content: bytes) -> list:
    data = json.loads(file_content.decode("utf-8"))

    if isinstance(data, dict):
        return [data]

    return data


def parse_csv(file_content: bytes) -> list:
    text = file_content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))

    return list(reader)


def parse_xml(file_content: bytes) -> list:
    root = ET.fromstring(file_content)

    records = []

    for item in root:
        record = {}

        for child in item:
            record[child.tag] = child.text

        records.append(record)

    return records