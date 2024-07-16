class Vector:
    def __init__(self, x=0, y=0, z=0):
        if isinstance(x, str):
            values = x.split()
            if len(values) < 3:
                values += ['0'] * (3 - len(values))
            self.x, self.y, self.z = [self._parse_value(v) for v in values[:3]]
        else:
            self.x = self._parse_value(x) if isinstance( x, ( float, int ) ) else 0
            self.y = self._parse_value(y) if isinstance( y, ( float, int ) ) else 0
            self.z = self._parse_value(z) if isinstance( z, ( float, int ) ) else 0

    def _parse_value(self, value):
        value = float(value)
        if value.is_integer() or value == int(value):
            return int(value)
        return value

    def __str__(self):
        _y = str(self.y).split('.')[0] if str(self.y).endswith( '.0' ) else self.y
        _z = str(self.z).split('.')[0] if str(self.z).endswith( '.0' ) else self.z
        _x = str(self.x).split('.')[0] if str(self.x).endswith( '.0' ) else self.x
        return f'{_x} {_y} {_z}'

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __repr__(self):
        return f"Vector( {self.x}, {self.y}, {self.z} )"
