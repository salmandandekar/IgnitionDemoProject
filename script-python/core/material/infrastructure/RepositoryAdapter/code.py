from adapters.persistence.DatabaseAdapter import code as db
from common.exceptions.RepositoryException import code as rex

def save(material, tx=None):
    try:
        sql = "INSERT INTO Materials (Id, Name, Code) VALUES (?, ?, ?)"
        return db.execute(sql, [material.material_id, material.name, material.code], tx=tx)
    except Exception as ex:
        raise rex.RepositoryException("Save failed: %s" % str(ex))

def get_by_id(material_id):
    try:
        row = db.query_one("SELECT Id, Name, Code FROM Materials WHERE Id=?", [material_id])
        if not row:
            return None
        # Row may be dict-like; unify
        try:
            rid = row.get("Id", row[0])
            rname = row.get("Name", row[1])
            rcode = row.get("Code", row[2])
        except Exception:
            rid, rname, rcode = row[0], row[1], row[2]
        return {"id": str(rid), "name": rname, "code": rcode}
    except Exception as ex:
        raise rex.RepositoryException("Get failed: %s" % str(ex))
