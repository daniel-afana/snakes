
from collections import deque
from random import randint
from point import GPoint

class GStruct:
    pass

DIRECTIONS          = GStruct()
DIRECTIONS.DOWN     = GPoint(x=0, y=1)
DIRECTIONS.UP       = GPoint(x=0, y=-1)
DIRECTIONS.LEFT     = GPoint(x=-1, y=0)
DIRECTIONS.RIGHT    = GPoint(x=1, y=0)

class GSnake(object):
    apple = GPoint(x=0,y=0)

    @classmethod
    def generate_apple(cls):
        apple = GPoint(x=randint(0, 50), y=randint(0,50))
        cls.apple = apple

    

    """docstring for GSnake"""
    def __init__(self, body=deque(), max_x=50, max_y=50):
        super(GSnake, self).__init__()
        self._current_direction = DIRECTIONS.DOWN
        self._previous_direction = DIRECTIONS.DOWN
        self._body = body
        self._bite_self = False
        
        self._max_x = max_x
        self._max_y = max_y


    @property
    def head(self):
        return self._body[0]

    @property
    def hit_border(self):
        a = 0 <= self.head.x < self._max_x
        b = 0 <= self.head.y < self._max_y

        return not(a and b)
    

    def MakeStep(self):
        head = self._body[0]
        new_head = head + self._current_direction
        if new_head in self._body:
            self._bite_self = True
        if new_head == GSnake.apple:
            GSnake.generate_apple()
            self._body.appendleft(new_head)
        self._body.appendleft(new_head)
        self._body.pop()
        self._previous_direction = self._current_direction


    def bite_somebody(self, snakes):
        for s in snakes:
            if self.head in s._body:
                return True
            
        
        
    def ChangeDirection(self, new_direction=DIRECTIONS.UP):
        dd = self._previous_direction + new_direction
        if dd.x == 0 and dd.y == 0:
            pass
        else:
            self._current_direction = new_direction


    def GetAsDict(self):
        res = {"body": []}
        for point in self._body:
            res["body"].append({"x": point.x, "y": point.y})
        return res


