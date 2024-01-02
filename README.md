
# MongoDB fields Cleaner

[![PyPI Version](https://img.shields.io/pypi/v/mdb-fields-cleaner)](https://pypi.org/project/mdb-fields-cleaner/) [![codecov](https://codecov.io/gh/carlosvin/mdb-fields-cleaner/graph/badge.svg?token=JHJFLRX2ED)](https://codecov.io/gh/carlosvin/mdb-fields-cleaner)

It simplifies the process of cleaning up old deprecated fields in a MongoDB database.

This will help you to easily remove obsolete/unused fields in your MongoDB collections so that you can save space in your DB.

## How to use it

It is as simple as [getting a pymongo.MongoClient](https://pymongo.readthedocs.io/en/stable/tutorial.html#making-a-connection-with-mongoclient) and pass it to the Cleaner constructor.

Once we have the Cleaner object instance, we just need to call the clean method with the collection name and the field names we want to keep ([unset](https://www.mongodb.com/docs/manual/reference/operator/update/unset/)), the fields not in this collection will be removed. This call will return an [UpdateResult object](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult).

```python
from mdb_fields_cleaner import Cleaner

client = MongoClient()
cleaner = Cleaner(client)

results: UpdateResult = cleaner.clean(collection.name, ["make", "model"])
print(f"{results.modified_count} modified documents")
```

## Development flow

1. Create a branch and a pull request.
1. Label the pull request with the correct semver label: patch, minor, major.
1. Get the PR approved and merged.

At this point the package should be published in Pypi.org registry.
