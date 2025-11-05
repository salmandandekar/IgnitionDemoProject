import os
import sys
from types import ModuleType

# Mock Ignition system module for unit testing
mock = ModuleType("system")
mock.db = ModuleType("db")
mock.dataset = ModuleType("dataset")

# Provide minimal stubs used by repository/view code
mock.db.runPrepQuery = lambda *args, **kwargs: []
mock.dataset.toDataSet = lambda headers, rows: {"headers": headers, "rows": rows}
mock.util = ModuleType("util")
class _Logger(object):
    def info(self, *a, **k):
        pass

    def warn(self, *a, **k):
        pass

    def error(self, *a, **k):
        pass


mock.util.getLogger = lambda name: _Logger()

sys.modules["system"] = mock
sys.modules["system.db"] = mock.db
sys.modules["system.dataset"] = mock.dataset
sys.modules["system.util"] = mock.util

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from core.material.presentation.MaterialController import code as MaterialControllerModule
from core.material.presentation.MaterialView import code as MaterialViewModule


def run():
    controller = MaterialControllerModule.MaterialController(user_id="tester")
    materials = controller.get_materials()
    dataset = MaterialViewModule.get_materialData("tester")
    export_ds = MaterialViewModule.export_materials("tester")
    return {
        "materials": materials,
        "dataset": dataset,
        "export": export_ds,
    }


if __name__ == "__main__":
    print(run())
