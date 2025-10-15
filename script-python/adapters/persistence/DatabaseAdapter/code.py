from infrastructure import DatabaseConfig as dbc
from common.exceptions import RepositoryException as rex

def query_one(sql, params=None, tx=None):
    try:
        params = params or []
        try:
            from system.db import runPrepQuery
            rows = runPrepQuery(sql, params, tx) if tx else runPrepQuery(sql, params)
            return rows[0] if rows else None
        except Exception:
            # outside Ignition: simulate empty result
            return None
    except Exception as ex:
        raise rex.RepositoryException("DB query failed: %s" % str(ex))

def execute(sql, params=None, tx=None):
    try:
        params = params or []
        try:
            from system.db import runPrepUpdate
            return runPrepUpdate(sql, params, tx) if tx else runPrepUpdate(sql, params)
        except Exception:
            # outside Ignition: simulate success
            return 1
    except Exception as ex:
        raise rex.RepositoryException("DB execute failed: %s" % str(ex))
