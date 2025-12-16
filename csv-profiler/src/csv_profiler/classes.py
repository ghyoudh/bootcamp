class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    @property
    def age(self) -> int:
        return self._age
    @age.setter
    def age(self, value: int) -> None:
        assert 0 <= value <= 120
        self._age = value

    def __repr__(self):
        return f"Person(name: '{self.name}', age: '{self.age}')"
    
    def __eq__(self, value):
        return {self.name, self.age} == {value.name, value.age}
    
p1 = Person("Ghyoudh", 23)
p2 = Person("Ghyoudh", 23)
print(f"{p1} \n{p2}")
print(p1 == p2)