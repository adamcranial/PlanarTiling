class TriangleA:

    def init(self,x1,y1,x2,y2,x3,y3):





def rotatePolygon(polygon, degrees):
    """ Rotate polygon the given angle about its center. """
    theta = radians(degrees)  # Convert angle to radians
    cosang, sinang = cos(theta), sin(theta)

    points = polygon.getPoints()
    # find center point of Polygon to use as pivot
    n = len(points)
    cx = sum(p.getX() for p in points) / n
    cy = sum(p.getY() for p in points) / n

    new_points = []
    for p in points:
        x, y = p.getX(), p.getY()
        tx, ty = x-cx, y-cy
        new_x = ( tx*cosang + ty*sinang) + cx
        new_y = (-tx*sinang + ty*cosang) + cy
        new_points.append(Point(new_x, new_y))

    rotated_ploygon = polygon.clone()  # clone to get current attributes
    rotated_ploygon.points = new_points
    return rotated_ploygon