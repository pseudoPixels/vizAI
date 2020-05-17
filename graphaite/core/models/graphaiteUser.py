from flaskext.couchdb import (
    Document,
    TextField,
    FloatField,
    DictField,
    Mapping,
    ListField,
    IntegerField,
)
from flask_login import UserMixin


class GraphaiteUserModel(UserMixin, Document):
    doc_type = "graphaite_user"

    email = TextField()  ## unique email address of the user
    password = TextField()  ## hashed user password

    def get_id(self):
        return str(self.email)


if __name__ == "__main__":
    pass
