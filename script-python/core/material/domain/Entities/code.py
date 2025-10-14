# Material Aggregate Root
class Material(object):
    def __init__(self, material_id, name, code):
        if not material_id or not name or not code:
            raise ValueError("Material fields must be provided")
        self.material_id = str(material_id)
        self.name = name
        self.code = code

    def rename(self, new_name):
        if not new_name:
            raise ValueError("Name cannot be empty")
        self.name = new_name
        return True
