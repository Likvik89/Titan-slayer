

class collisionbox():
    def __init__(self, area_type, size, position_x, position_y):
        self.area_type = area_type
        self.size = size
        self.x = position_x
        self.y = position_y
        self.vx = 0 #The velocity in the x-axis
        self.vy = 0 #The velocity in the y-axis



class players(collisionbox):
    def __init__(self, area_type, size, position_x, position_y):
        super().__init__(area_type, size, position_x, position_y)
