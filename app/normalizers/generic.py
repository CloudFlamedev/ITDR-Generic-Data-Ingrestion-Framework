def normalize_data(record, source):

    if not isinstance(record, dict):
        raise ValueError("Each record must be a dictionary")

    return {
        "source": source,
        "raw_data": record
    }