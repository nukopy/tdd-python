class MyModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, dict_mymodel):
        return cls(dict_mymodel)

    def to_dict(self):
        return self.to_dict()


class TestMyModel:
    def test_from_dict(self):
        pass

    def test_to_dict(self):
        pass
