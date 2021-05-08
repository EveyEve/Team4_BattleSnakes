import heapq

class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0

    def __lt__(self, other):
        return self.g < other.g


class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None
        self.walls = None
        self.others_walls = None
        self.weights = None

    def init_grid(self, width, height, walls, others_walls, start):
        """Prepare grid cells, walls.
        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        self.walls = walls
        self.others_walls = others_walls
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.weights = []
        
        for cell in self.cells:
          self.weights.append(self.close_to_wall(cell))

    def close_to_wall(self, cell):
      #change weight depending on how close or far it is from wall 
      # need to know where heads are to avoid those more than walls
      distanceToAllWalls = 0
      for wall in self.walls:
        if wall != self.start:
          dist = abs(cell.x - wall[0]) + abs(cell.y - wall[1])
          distanceToAllWalls = distanceToAllWalls + dist*dist

      for block in self.get_adjacent_cells(cell):
        if not block.reachable:
          distanceToAllWalls = distanceToAllWalls - 1
        if (block.x, block.y) in self.walls:
           distanceToAllWalls = distanceToAllWalls - 2
      if distanceToAllWalls <= 0:
        distanceToAllWalls = 0.01
      return self.grid_height/(distanceToAllWalls)

    def get_cell(self, x, y):
        """Returns a cell from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_adjacent_walls(self, wall):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if wall[0] < self.grid_width-1:
            cells.append(self.get_cell(wall[0]+1, wall[1]))
        if wall[1] > 0:
            cells.append(self.get_cell(wall[0], wall[1]-1))
        if wall[0] > 0:
            cells.append(self.get_cell(wall[0]-1, wall[1]))
        if wall[1] < self.grid_height-1:
            cells.append(self.get_cell(wall[0], wall[1]+1))
        return cells

    def get_path(self, endX, endY):
        endCell = self.get_cell(endX, endY)
        if endCell.g > 100:
          adj_cells = self.get_adjacent_cells(endCell)
          endCell = adj_cells[0]
          for block in adj_cells:
            if endCell.g > block.g:
              endCell = block

        path = [(endCell.x, endCell.y)]
        while endCell.parent is not self.start:
            endCell = endCell.parent
            if endCell is None:
              return None, None
            path.append((endCell.x, endCell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path, endCell.g

    def update_cell(self, adj, cell):
        """Update adjacent cell.
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + self.weights[adj.x * self.grid_height + adj.y]
        adj.parent = cell

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.g, self.start))
        while len(self.opened):
            # pop cell from heap queue
            g, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.g, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + self.weights[adj_cell.x * self.grid_height + adj_cell.y]:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.g, adj_cell))