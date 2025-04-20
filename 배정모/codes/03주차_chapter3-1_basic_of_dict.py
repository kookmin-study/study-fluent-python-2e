import _collections_abc
import os 
path = _collections_abc.__file__
os.system(f"grep -A 20 'class Mapping' {path}")

ex = """I’m going to study hard and become a high-level Python developer""".split(' ')
myDict = {word : len(word)**2 for word in ex if len(word) > 3 }
print(myDict)

print({**{'a' : 1, 'b' : 2,'c' : 3},'a':77 , 'b':45})
# print(dict(x=1,y=1,x=3))  # SyntaxError: keyword argument repeated: x
# print(dict(x=1,y=1,**{'x':3})) # TypeError: dict() got multiple values for keyword argument 'x'

class MyDict(dict):
    def __or__(self, other):    # __or__ method overloading 필요함. MyDict 로 Wrapping 안하면, 자료형이 dict 따라감
        result = super().__or__(other)
        return MyDict(result)

dict1 = MyDict(x=1,y=22,**{'z':333,'w':4444})
dict2 = dict(x=4,y=33,**{'z':222,'w':1111})
merged_dict1 = dict1|dict2
merged_dict2 = dict2|dict1
print(merged_dict1, merged_dict2)  # {'x': 4, 'y': 33, 'z': 222, 'w': 1111} {'x': 1, 'y': 22, 'z': 333, 'w': 4444}
print(type(merged_dict1),type(merged_dict2))    # <class '__main__.MyDict'> <class 'dict'>


