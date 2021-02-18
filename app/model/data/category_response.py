import json

from app.model.data.category import Category

class CategoryResonse:

    len: int
    categories: []


    def __init__(self, len: int, categories: []):
        self.len = len
        self.categories = categories


    def __del__(self):
        pass


    def __str__(self):
        return f'len={self.len},' + \
               f'categories={self.categories}'


    def toJson(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)


if __name__=='__main__':
    print(__name__)
    categories = CategoryResonse(1, [Category(1, "test", 1)])
    print(categories)
    print(categories.toJson())
