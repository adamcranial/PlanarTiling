psi = 2

class TileA:
    """
    A class representing a Robinson triangle and the rhombus formed from it.

    """

    def __init__(self, x, y,size ):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size = x, y, size

    def path(self):
            """
            Return the SVG polygon points specifier for the polygon formed
            by this tile and its mirror image joined along their bases.
            """

            return '<polygon points=\"{},{} {},{} {},{} {},{} {},{} {},{}\" style=\"fill:yellow; stroke:black; stroke-width:1\"/>'.format(self.x,self.y,
                                                                                                                                          self.x,self.y+self.size,
                                                                                                                                          self.x+self.size, self.y+self.size,
                                                                                                                                          self.x + (self.size/2),self.y+(self.size/2),
                                                                                                                                          self.x + (self.size/2),self.y)

    def inflate(self):
        x = self.x * psi
        y = self.y * psi

        return [TileA(x, y+self.size, self.size),
                TileD(x, y, self.size),
                TileA(x+(self.size/2),y+(self.size/2),self.size),
                TileB(x+self.size, y+self.size, self.size)
                ]

class TileB:
    """
    A class representing a Robinson triangle and the rhombus formed from it.

    """

    def __init__(self, x, y, size):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size = x, y, size

    def path(self):
        """
        Return the SVG polygon points specifier for the polygon formed
        by this tile and its mirror image joined along their bases.
        """

        return '<polygon points=\"{},{} {},{} {},{} {},{} {},{} {},{}\" style=\"fill:red; stroke:black; stroke-width:1\"/>'.format(
            self.x, self.y + self.size,
            self.x + self.size, self.y + self.size,
            self.x + self.size, self.y,
            self.x + (self.size / 2), self.y,
            self.x + (self.size / 2), self.y + (self.size / 2),
            self.x, self.y + (self.size/2))


    def inflate(self):
        x = self.x * psi
        y = self.y * psi
        return [TileB(x+self.size, y+self.size, self.size),
                TileA(x, y+self.size, self.size),
                TileB(x + (self.size / 2), y + (self.size / 2), self.size),
                TileC(x+self.size, y, self.size)]

class TileC:
    """
    A class representing a Robinson triangle and the rhombus formed from it.

    """

    def __init__(self, x, y, size):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size = x, y, size

    def path(self):
        """
        Return the SVG polygon points specifier for the polygon formed
        by this tile and its mirror image joined along their bases.
        """

        return '<polygon points=\"{},{} {},{} {},{} {},{} {},{} {},{}\" style=\"fill:chartreuse; stroke:black; stroke-width:1\"/>'.format(
            self.x, self.y,
            self.x, self.y + (self.size / 2),
            self.x + (self.size / 2), self.y + (self.size / 2),
            self.x + (self.size/2) , self.y + (self.size ),
            self.x + self.size, self.y + self.size,
            self.x+self.size, self.y


        )


    def inflate(self):
        x = self.x * psi
        y = self.y * psi
        return [TileD(x, y, self.size),
                TileC(x+self.size, y, self.size),
                TileC(x + (self.size / 2), y + (self.size / 2), self.size),
                TileB(x+self.size, y+self.size, self.size)
                ]


class TileD:
    """
    A class representing a Robinson triangle and the rhombus formed from it.

    """

    def __init__(self, x, y, size):
        """
        Initialize the triangle with the ordered vertices. A and C are the
        vertices at the equal base angles; B is at the vertex angle.

        """
        self.x, self.y, self.size = x, y, size

    def path(self):
        """
        Return the SVG polygon points specifier for the polygon formed
        by this tile and its mirror image joined along their bases.
        """

        return '<polygon points=\"{},{} {},{} {},{} {},{} {},{} {},{}\" style=\"fill:cyan; stroke:black; stroke-width:1\"/>'.format(
            self.x, self.y,
            self.x, self.y + (self.size),
            self.x + (self.size / 2), self.y + (self.size),
            self.x + (self.size / 2), self.y + (self.size / 2),
            self.x + self.size, self.y + (self.size/2),
            self.x+self.size, self.y


        )


    def inflate(self):
        x = self.x*psi
        y = self.y*psi
        return [TileD(x, y, self.size),
                TileC(x+self.size, y, self.size),
                TileD(x + (self.size / 2), y + (self.size / 2), self.size),
                TileA(x, y+self.size, self.size)
                ]



class Chair:

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
        svg = [#'<html>', '<link href="cartesian.css" rel="stylesheet" type="text/css"/>',
               '<svg  viewBox="0 0 1500 1500" width="100%" height="100%" '
               ' preserveAspectRatio="xMidYMid meet" version="1.1"'
               ' baseProfile="full" xmlns="http://www.w3.org/2000/svg"><g>'
                ]

        for e in self.elements:
            svg.append(e.path())
        svg.append('</g>\n</svg>')
        #svg.append('\n</html>')
        return '\n'.join(svg)


    def write_svg(self, filename):
        """ Make and write the SVG for the tiling to filename. """
        svg = self.make_svg()
        print(svg)
        with open(filename, 'w') as fo:
            fo.write(svg)


ch = Chair()


#ch.set_initial_tiles([TileD(0,0,10)])
inflations=6
ch.set_initial_tiles([TileB(0,0,10),
                      TileA(10,0,10),
                      TileC(0,10,10),
                      TileD(10,10,10)])

for i in range(inflations):
    ch.inflate()
    ch.write_svg("chairtile" + str(i) + ".svg")




