from flaskext.couchdb import (
    Document,
    TextField,
    FloatField,
    DictField,
    Mapping,
    ListField,
    IntegerField,
)


class GraphaiteUserModel(Document):
    doc_type = "graphaite_user"

    email = TextField()  ## unique email address of the user
    password = TextField()  ## hashed user password


if __name__ == "__main__":
    pass
