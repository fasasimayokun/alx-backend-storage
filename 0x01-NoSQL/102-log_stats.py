#!/usr/bin/env python3
"""a script for Log stats - new version """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx = client.logs.nginx
    total_count = nginx.count_documents({})
    get_count = nginx.count_documents({"method": "GET"})
    post_count = nginx.count_documents({"method": "POST"})
    put_count = nginx.count_documents({"method": "PUT"})
    patch_count = nginx.count_documents({"method": "PATCH"})
    delete_count = nginx.count_documents({"method": "DELETE"})
    status_get_count = nginx.count_documents({"method": "GET", "path": "/status"})
    all_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    all_method_counts = [get_count, post_count, put_count, patch_count, delete_count]
    print("{} logs".format(total_count))
    print("Methods:")
    for nm in range(len(all_methods)):
        print("\tmethod {0}: {1}".format(all_methods[nm], all_method_counts[nm]))
    print("{} status check".format(status_get_count))
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(nginx.aggregate(pipeline))
    print("IPs:")
    for i_p in top_ips:
        print("\t{0}: {1}".format(i_p.get("_id"), i_p.get("count")))
