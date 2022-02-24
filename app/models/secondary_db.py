"""

"""
from .database import db, ma


#  ---------- Models ---------- #
class TableB(db.Model):

    """
    CREATE TABLE IF NOT EXISTS
        schema.tableb
        (
            id Serial PRIMARY KEY,
            name varchar(50) UNIQUE,
            data JSON,
            is_operational Boolean
        )
            WITH (
        OIDS=FALSE
        )
    ;
    """

    __bind_key__ = 'DB2'

    __tablename__ = 'tableb'
    __table_args__ = {
        "schema": "schema",
        "extend_existing": True
    }

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    data = db.Column(db.JSON)
    is_operational = db.Column(db.Boolean)


#  ---------- Schemas ---------- #
class TableBSchema(ma.Schema):

    class Meta(object):
        fields = (
            'id',
            'name',
            'data',
            'is_operational'
        )
