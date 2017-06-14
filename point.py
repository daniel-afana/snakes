
class GPoint(object):
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y


    def __add__(self, point):
        new_x = self.x + point.x
        new_y = self.y + point.y
        return GPoint(x=new_x, y=new_y)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y


    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
    