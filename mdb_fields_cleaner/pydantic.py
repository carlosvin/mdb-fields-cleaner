from typing import Type
from pydantic import BaseModel
from pymongo.results import UpdateResult
from mdb_fields_cleaner import Cleaner, ModelBasedCleaner


class PydanticCleaner(ModelBasedCleaner, Cleaner):
    """
    Helper to easily remove any field that is not declared in the pydantic base model from a collection
    """

    def clean_fields_not_in_model(
        self, collection_name: str, class_or_instance: Type[BaseModel] | BaseModel
    ) -> UpdateResult:
        """
        Remove any field from a collection that is not a field declared in the pydantic base model
        :collection_name: Name of the collection to clean up the fields
        :cls: Pydantic BaseModel class with the fields that we want to keep in the collection
        """
        return super().clean(
            collection_name, keep_fields=[key for key in class_or_instance.model_fields]
        )
