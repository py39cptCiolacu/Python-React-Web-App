from back.revision import repository
from back.revision.schema import RevisionSchema
from back.utils.utils import json_response
from typing import List


class RevisionController:
    def __init__(self, db, window=None):
        self.db = db
        self.window = window

    @json_response(List[RevisionSchema])
    def get_all_revisions(self):
        return repository.get_revisions(self.db)

    def create_revision(self, data):
        if data["name"] == "error":
            raise Exception("error")
        repository.create_revision(self.db, data["name"])
