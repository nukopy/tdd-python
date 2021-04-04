class MyModel:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, dict_mymodel):
        return cls(**dict_mymodel)

    def to_dict(self):
        return self.__dict__


class TestMyModel:
    def test_from_dict(self):
        dict_mymodel = {"id": 3, "name": "mymodel"}
        model = MyModel.from_dict(dict_mymodel)

        assert isinstance(model, MyModel)
        assert model.id == 3
        assert model.name == "mymodel"

    def test_to_dict(self):
        model = MyModel(id=3, name="mymodel")
        dict_mymodel = model.to_dict()

        assert dict_mymodel["id"] == 3
        assert dict_mymodel["name"] == "mymodel"
