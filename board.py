from field import Field
import random

'''
The Board is basically a Graph with extra information.
Fields are vertices.

- self.fields is a key:value store of vertices (locs) and their fields.
- self.graph is a key:value store of vertices and edges (legal moves)

get_field(loc) to get a relevant field for a location.

'''

class Board:

    def __init__(self, difficulty="beginner", mode="classic"):
        # Sides is the amount of edges each vertex has.

        self.difficulty = difficulty
        self.mode = mode

        sides = {
            "classic": 4,
            "hexagon": 6
        }
        # Edges are the number of sides
        self.edges = sides[mode]

        # Gets settings for chosen difficulty level
        settings = {
            # (squares-x, squares-y, number of bombs)
              "test": (4, 4, 0)
            , "beginner": (8, 10, 10)
            , "intermediate": (13, 16, 40)
            , "expert": (16, 30, 9)
        }
        settings = settings[difficulty]

        # Create the Board of Fields
        self.r = settings[0]
        self.c = settings[1]
        self.__total_mines = settings[2]

        # Build k:v store of loc:field objects
        self.fields = {}
        for row in range(self.r):
            for col in range(self.c):
                self.fields[(row, col)] = Field()

        # Buid k:v store of vertex:edges (loc, legal moves)
        self.graph = self.__build_graph_dictionary()


        # Lay the number of mines from the difficulty settings
        self.lay_mines(self.__total_mines)
        self.count_mines()

    def get_total_number_of_mines(self):
        return self.__total_mines

    def get_board(self):
        '''
        Returns the entire board state for the GUI
        :return:
        '''
        board = []
        for row in range(self.r):
            for col in range(self.c):
                f = self.get_field((row, col))
                if f.revealed is False:
                    if f.flag:
                        board.append("f")
                    else:
                        board.append(False)
                else:
                    board.append(f.value)
        return board


    def __build_graph_dictionary(self):
        '''
        Loops through each loc/field pair in self.fields
        and builds a graph dictionary with vertices and edges
        :return: Dictionary of vertexes and their edges
        '''
        # Get number of edges
        edges = self.edges

        # list of legal moves depends on how many edges a vertex has
        legal_moves = {
            4: [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
            "6_even": [(-1, -1), (-1, 0), (0, 1), (1, 0), (1, -1), (0, -1)],
            "6_odd": [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (0, -1)]
        }

        graph_dict = {}

        # For each vertex
        for vertex_r, vertex_c in self.fields:
            # For each legal move

            # Sort out which legal_moves list to grab
            if self.edges is 6:
                if vertex_r % 2:
                    # Grab the odd list
                    moves = "6_odd"
                else:
                    moves = "6_even"
            elif self.edges is 4:
                moves = 4

            graph_dict[(vertex_r, vertex_c)] = []
            for edge_r, edge_c in legal_moves[moves]:
                # Add the new absolute location of another vertex
                e = (vertex_r + edge_r, vertex_c + edge_c)
                # Guard: Check that loc is not out of bounds
                if not self.get_field(e):
                    continue
                # And add it to the list of edges for the original vertex
                graph_dict[(vertex_r, vertex_c)].append(e)
        return graph_dict

    def get_field(self, loc):
        '''
        Ensures that the Field exists
        :param loc:
        :return: False if none. Field object if it exists.
        '''
        try:
            return self.fields[loc]
        except KeyError:
            # print(f"Field out of bounds at {loc}.")
            return
        except TypeError:
            print(f"Pass one loc to get_field, not multiple: {loc}.")
            return

    def get_value(self, loc):
        return self.get_field(loc).value


    def lay_mines(self, qty):
        '''
        Lays the mines on the graph
        :return:
        '''

        # Guard: Check that qty is above 0
        if qty <= 1:
            return False

        # Lambda for generating a random location
        def rand_loc(): return (random.randint(0, self.r - 1), random.randint(0, self.c - 1))

        while qty is not 0:
            # Get a random field
            field = self.get_field(rand_loc())

            # Try and lay a mine there
            if not field.is_mined:
                field.set_mine()
                # If successful, reduce qty of mines to lay by one
                qty-=1

    def count_mines(self):
        '''
        Counts the mines on the board, and sets vertexes
        :return:
        '''
        for vertex in self.graph:
            edges = self.graph[vertex]
            for e in edges:
                if self.get_field(e).is_mined:
                    self.get_field(vertex).increment()

    def reveal(self, loc):
        '''
        Reveal a field.
        Will reveal multiple if the field has no nearby mines.
        :param loc:
        :return: List of locs to reveal, and their values
        '''

        # ## Field user clicked
        # Get the field object
        field = self.get_field(loc)
        if field is False:
            return

        # This queue is for the 0-fill
        queue = [loc]

        # ## Other fields
        while queue:
            # Get the field object, using queue.pop
            _loc = queue.pop()

            field = self.get_field(_loc)

            # Guard: Check that the Field exists
            if field is False:
                continue

            # Guard: Only operate on covered tiles
            if field.revealed:
                continue

            # Reveal the field
            field.reveal()

            # Guard: Only continue searching if this field contains a 0.
            if field.value is not 0:
                continue

            # Find adjacent vertices
            adjacent_locations = self.graph[_loc]
            # Add them if they have no nearby mines.
            for vertex in adjacent_locations:
                queue.append(vertex)

        # Return the board if successful
        return self.get_board()

    def flag(self, loc):
        '''
        Flags or unflags a field
        :param loc:
        :return:
        '''

        # Get the field object
        field = self.get_field(loc)
        if field is False:
            return

        # Toggle the flag
        if field.flag:
            field.set_flag(False)
        else:
            field.set_flag(True)

        # Return the board
        return self.get_board()
