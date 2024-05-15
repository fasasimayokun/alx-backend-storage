#!/usr/bin/env python3
"""a sript for Top students tasks"""


def top_students(mongo_collection):
    """a func that returns all students sorted by average score"""
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "topics": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        { "$sort": { "averageScore": -1 } }
    ]
    return mongo_collection.aggregate(pipeline)
