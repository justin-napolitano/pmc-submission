from google.cloud import bigtable


def login():
    client = bigtable.Client()
    return client