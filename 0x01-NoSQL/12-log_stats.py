#!/usr/bin/env python3
'''Python script that provides some stats about
Nginx logs stored in MongoDB:'''
from pymongo import MongoClient


def get_nginx_log_stats():
    """Fetch and display stats about Nginx logs in MongoDB."""
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']  # Database name
    collection = db['nginx']  # Collection name

    # Total number of documents
    total_logs = collection.count_documents({})

    # Count of methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
        {"method": method}) for method in methods}

    # Count of GET requests with path /status
    get_status_count = collection.count_documents(
            {"method": "GET", "path": "/status"})

    # Output the stats
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\t{method_counts[method]} {method}")
    print(f"\t{get_status_count} GET /status")


if __name__ == "__main__":
    get_nginx_log_stats()
