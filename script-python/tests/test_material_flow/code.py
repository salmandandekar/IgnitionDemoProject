import sys, os
# Inject mock 'system' module for tests
from types import ModuleType
mock = ModuleType("system")
from mock_system import code as ms
mock.db = ms.db
mock.util = ms.util
sys.modules["system"] = mock
sys.modules["system.db"] = mock.db.__class__  # not exact, but enough to avoid import error
sys.modules["system.util"] = mock.util.__class__

# Update path for project libs
proj = "/mnt/data/MES_Project/script-libraries/MES_Project"
if proj not in sys.path:
    sys.path.insert(0, proj)

# Import controller and run a basic flow
from core.material.presentation import MaterialController as ctrl

def run():
    ctrl.create("M-1", "Bolt", "B-001")   # create
    res = ctrl.get("M-1")                 # query (will be None in mock DB)
    return {"create": "ok", "get": res}

if __name__ == "__main__":
    print(run())
