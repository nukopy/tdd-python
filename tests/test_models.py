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
        dic_model = {"id": 3, "name": "mymodel"}
        model = MyModel.from_dict(dic_model)

        assert isinstance(model, MyModel)
        assert model.id == 3
        assert model.name == "mymodel"

    def test_to_dict(self):
        pass
