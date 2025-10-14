class MaterialRepositoryPort(object):
    def save(self, material, tx=None): 
        raise Exception("Override")

    def get_by_id(self, material_id): 
        raise Exception("Override")
