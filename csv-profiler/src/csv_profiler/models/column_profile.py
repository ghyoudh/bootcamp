class columnProfile:
    def __init__(self, name: str, inferred_type: str, total: int, missing: int, unique: int):
        self.name = name
        self.inferred_type = inferred_type
        self.total = total
        self.missing = missing
        self.unique = unique
    
    @property
    def missing_pct(self) -> float:
        return 0.0 if self.total == 0 else 100.0 * self.missing / self.total

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "inferred_type": self.inferred_type,
            "total": self.total,
            "missing": self.missing,
            "unique": self.unique,
            "missing_pct": self.missing_pct,
        }
    def __repr__(self):
        return f"columnProfile(name: '{self.name}', inferred_type: '{self.inferred_type}', total: {self.total}, missing: {self.missing}, unique: {self.unique})"

col1 = columnProfile(name="name", inferred_type="string", total=100, missing=0, unique=95)
col2 = columnProfile(name="age", inferred_type="int", total=100, missing=5, unique=20)
