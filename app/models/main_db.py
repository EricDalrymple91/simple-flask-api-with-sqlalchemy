"""

"""
from .database import db, ma


#  ---------- Models ---------- #
class TableA(db.Model):

    """
    CREATE TABLE IF NOT EXISTS
        schema.tablea
        (
            id Serial PRIMARY KEY,
            name varchar(50) UNIQUE,
            data JSON
        )
            WITH (
        OIDS=FALSE
        )
    ;
    """

    __tablename__ = 'tablea'
    __table_args__ = {
        "schema": "schema"
    }

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    data = db.Column(db.JSON)


#  ---------- Schemas ---------- #
class TableASchema(ma.Schema):

    class Meta(object):
        fields = (
            'id',
            'name',
            'data'
        )
