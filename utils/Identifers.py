class Identifier:
    identifier_table = {}

    def __init__(self):
        pass

    @staticmethod
    def get_id(key):
        id = Identifier.identifier_table.get(key, 0)
        Identifier.identifier_table[key] = id + 1

        return id