def collide(obj1, obj2):
    offset_x = obj2.x_pos - obj1.x_pos
    offset_y = obj2.y_pos - obj1.y_pos
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

