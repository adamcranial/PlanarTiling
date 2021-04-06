import math
import random


#A small tolerance for comparing floats for equality
TOL = 1.e-5
# psi = 1/phi where phi is the Golden ratio, sqrt(5)+1)/2
phi = (math.sqrt(5) +1) / 2
psi = math.sqrt(5)
eig = 1/(math.sqrt(5))
ang = math.degrees(math.asin(eig))

scale = 0.01
print(ang)


def rotatePolygon(polygon, degrees):
    """ Rotate polygon the given angle about its center. """
    theta = math.radians(degrees)  # Convert angle to radians
    cosang, sinang = math.cos(theta), math.sin(theta)

    points = polygon.getPoints()
    # find center point of Polygon to use as pivot
    n = len(points)
    cx = sum(p.getX() for p in points) / n
    cy = sum(p.getY() for p in points) / n

    cx = points[0].getX()
    cy = points[0].getY()

    r_points = []
    for p in points:
        x, y = p.getX(), p.getY()
        tx, ty = x-cx, y-cy
        new_x = ( tx*cosang + ty*sinang) + cx
        new_y = (-tx*sinang + ty*cosang) + cy
        r_points.append(Point(new_x, new_y))
    # ok the rotation shifts the bounding box of the item so shift the damn thing back.
    rotated_polygon = Polygon([])
    rotated_polygon.points = r_points

    # rect = polygon.getRect()
    # r_rect = rotated_polygon.getRect()
    #
    # diff_x = r_rect[0][0] - rect[0][0]
    # diff_y = r_rect[0][1] - rect[0][1]
    # print(diff_x)
    # print(diff_y)
    # rotated_polygon.shift(diff_x,diff_y)

    return rotated_polygon

def rotatePolygon_origin(polygon, degrees,origin_x,origin_y):
    """ Rotate polygon the given angle about its center. """
    theta = math.radians(degrees)  # Convert angle to radians
    cosang, sinang = math.cos(theta), math.sin(theta)

    points = polygon.getPoints()
    # find center point of Polygon to use as pivot
    n = len(points)
    cx = sum(p.getX() for p in points) / n
    cy = sum(p.getY() for p in points) / n

    # if origin_x > 10000:
    #     return polygon
    cx = origin_x
    cy = origin_y

    r_points = []
    for p in points:
        x, y = p.getX(), p.getY()
        tx, ty = x-cx, y-cy
        new_x = ( tx*cosang + ty*sinang) + cx
        new_y = (-tx*sinang + ty*cosang) + cy
        if new_x < -1000:
            print(str(origin_x) + " " +str(x))
        r_points.append(Point(new_x, new_y))
    # ok the rotation shifts the bounding box of the item so shift the damn thing back.
    rotated_polygon = Polygon([])
    rotated_polygon.points = r_points

    # rect = polygon.getRect()
    # r_rect = rotated_polygon.getRect()
    #
    # diff_x = r_rect[0][0] - rect[0][0]
    # diff_y = r_rect[0][1] - rect[0][1]
    # print(diff_x)
    # print(diff_y)
    # rotated_polygon.shift(diff_x,diff_y)

    return rotated_polygon


def mirrorPolygon(polygon):
    """ Rotate polygon the given angle about its center. """
    new_points = []
    points = polygon.getPoints()
    for p in points:
        X = [p.getX(), p.getY()]
        Y = [[1, 0], [0, -1]]
        result = [0,0]
        print(X)
        print(Y)
        # iterate through columns of Y
        for j in range(len(Y[0])):
            # iterate through rows of Y
            for k in range(len(Y)):
                result[j] += X[k] * Y[k][j]
        for r in result:
            print(r)
        new_points.append(Point(result[0], result[1]))

    #rotated_ploygon = polygon.clone()  # clone to get current attributes
    mirror = Polygon([])
    mirror.points = new_points
    return mirror



class Point:

    def __init__(self, x, y):
        self.x, self.y = round(x), round(y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class Polygon:

    def __init__(self, arr ):
        self.points = []

        for item in arr:
            p = Point( item[0],item[1] )
            self.points.append(p)

    def getPoints(self):
        return self.points


    def getRect(self):
        """
        Return a boundary rect for the polygon, intended to move a rotated polygon back into position
        """
        minx, miny, maxx, maxy =10000, 10000, 0, 0
        for p in self.points:
            if p.getX() > maxx:
                maxx = p.getX()
            if p.getY() > maxy:
                maxy = p.getY()
            if p.getX() < minx:
                minx = p.getX()
            if p.getY() < miny:
                miny = p.getY()

        return [[minx, miny], [maxx, maxy]]


    def shift(self, x, y):
        new_points = []
        for p in self.points:
            newp = Point(p.getX()-x, p.getY()-y)
            new_points.append(newp)
        self.points = new_points

    def path(self, scale, colour):
        flatten_list = []
        for p in self.getPoints():
            flatten_list.append(p.getX())
            flatten_list.append(p.getY())
        return '<polygon transform=\'scale('+ str(scale) +' ' + str(scale) +')\' points=\"' + str(flatten_list)[
                                                                   1:-1] + '\" style=\"fill:'+colour+'; stroke:black; stroke-width:10\"/>'
class TileA:
    """
    A class representing a triangle and the rhombus formed from it.

    """

    def __init__(self, x, y, size,rotate,pos):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size, self.rotate = x, y, size, (rotate % 360)
        self.pos=[]
        self.polygon = Polygon([[self.x, self.y],
                    [self.x, round(self.y + self.size)],
                    [round(self.x + self.size * 2), round(self.y)],

        ])

        if self.rotate != 0:
            self.polygon = rotatePolygon(self.polygon,self.rotate)

        for old_pos in pos:
            self.pos.append(old_pos)
        count=1
        for old_pos in reversed(pos):
            if old_pos[2] != 0:
                inf = psi**count
                self.polygon = rotatePolygon_origin(self.polygon, old_pos[2], old_pos[0]*inf, old_pos[1]*inf)
                count=count+1
        self.pos.append([self.x, self.y, self.rotate])
        print(self.pos)

    def path(self):
        """
        Return the SVG polygon points specifier for the polygon formed
        by this tile and its mirror image joined along their bases.
        """
        colour="deepskyblue"

        return self.polygon.path(scale, colour)
        # flatten_list = []
        # for p in self.polygon.getPoints():
        #     flatten_list.append(p.getX())
        #     flatten_list.append(p.getY())
        #
        # return '<polygon transform=\'scale(0.1 0.1)\' points=\"' + str(flatten_list)[1:-1] + '\" style=\"fill:yellow; stroke:black; stroke-width:1\"/>'

    def points(self):
        return self.polygon

    def inflate(self):
        x = self.x * psi
        y = self.y * psi
        pos =self.pos
        return [
             TileB(x,y,self.size,270+ang,pos),
                 TileA(x+(self.size*eig), y+(self.size*eig*2), self.size, ang, pos),
                 TileA(x + (self.size *((2*math.sqrt(5)) - (4/math.sqrt(5)) )), y + (self.size * eig * 2), self.size, 180+ang, pos),
                 TileB(x+self.size*math.sqrt(5), y, self.size,180+ang,pos),
                  TileB(x + self.size * 2*math.sqrt(5), y, self.size, 180 + ang,pos)]


class TileB:
    """
    A class representing a triangle and the rhombus formed from it.

    """

    def __init__(self, x, y, size,rotate,pos):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size, self.rotate = x, y, size, (rotate % 360)
        self.pos =[]
        self.polygon = Polygon([[self.x, self.y],
                    [round(self.x + self.size * 2), round(self.y + self.size)],
                    [round(self.x + self.size * 2), round(self.y)],

        ])

        if self.rotate != 0:
            self.polygon = rotatePolygon(self.polygon,self.rotate)
        for old_pos in pos:
            self.pos.append(old_pos)
        count = 1
        for old_pos in reversed(pos):
            if old_pos[2] != 0:
                inf = psi**count
                self.polygon = rotatePolygon_origin(self.polygon, old_pos[2] , old_pos[0] * inf,
                                                    old_pos[1] * inf)
                count = count + 1
        self.pos.append([self.x, self.y, self.rotate])

        print(self.pos)

    def path(self):
        """
        Return the SVG polygon points specifier for the polygon formed
        by this tile and its mirror image joined along their bases.
        """
      #  print(self.rotate)
        colour="greenyellow"

        return self.polygon.path(scale, colour)
        # flatten_list = []
        # for p in self.polygon.getPoints():
        #     flatten_list.append(p.getX())
        #     flatten_list.append(p.getY())
        #
        # return '<polygon transform=\'scale(0.1 0.1)\' points=\"' + str(flatten_list)[1:-1] + '\" style=\"fill:yellow; stroke:black; stroke-width:1\"/>'

    def points(self):
        return self.polygon

    def inflate(self):
        x = self.x * psi
        y = self.y * psi

        pos=self.pos
        return [TileA(x + (self.size * ((2 * math.sqrt(5)) - (2 / math.sqrt(5)))), y + (self.size * eig * 4), self.size,90-ang,pos),
                TileB(x + (self.size * math.sqrt(5)), y, self.size, 360-ang,pos),
                TileB(x + (self.size * ((2 * math.sqrt(5)) - (2 / math.sqrt(5)))), y + (self.size * eig * 4), self.size,
                      180-ang,pos),
                TileA(x + self.size*(4 / math.sqrt(5)), y +self.size*(2 / math.sqrt(5)), self.size,180-ang,pos),
                TileA(x + self.size*(4 / math.sqrt(5) + math.sqrt(5)),  y +self.size*(2 / math.sqrt(5)), self.size,  180-ang, pos)
                ]

class Pinwheel:
    def __init__(self):
        self.elements = []

    def set_initial_tiles(self, tiles):
        self.elements = tiles


    def inflate(self):
        """ "Inflate" each triangle in the tiling ensemble."""
        new_elements = []
        for element in self.elements:
            new_elements.extend(element.inflate())
        self.elements = new_elements

    def make_svg(self):
        svg = ['<html>', '<link href="cartesian.css" rel="stylesheet" type="text/css"/>',
               '<svg  viewBox="0 0 1000 1000" width="100%" height="100%" '
               ' preserveAspectRatio="xMidYMid meet" version="1.1"'
               ' baseProfile="full" xmlns="http://www.w3.org/2000/svg"><g>'
                ]

        for e in self.elements:
            svg.append(e.path())
        svg.append('</g>\n</svg>')
        svg.append('\n</html>')
        return '\n'.join(svg)


    def write_svg(self, filename):
        """ Make and write the SVG for the tiling to filename. """
        svg = self.make_svg()
        print(svg)
        with open(filename, 'w') as fo:
            fo.write(svg)

ch = Pinwheel()

#ch.set_initial_tiles([TileD(0,0,10)])
inflations=5
size =800

ch.set_initial_tiles([TileA(0,0,size,0,[]),TileA(size*2,size,size,180,[])])
ch.write_svg("pinwheel0.svg")
for i in range(inflations):
    ch.inflate()
    ch.write_svg("pinwheel" + str(i+1) + ".svg")




