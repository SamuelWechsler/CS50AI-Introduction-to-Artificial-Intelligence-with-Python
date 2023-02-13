import sys
import numpy as np

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.crossword.variables:
            for word in self.domains[variable].copy():
                # if length not equal to goal
                if len(word) != variable.length:
                    # remove word from domain of variable
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # get overlap of variable x and y
        i, j = self.crossword.overlaps[x, y]

        for value_x in self.domains[x].copy():
            # check if there's any value_y in domain of Y such that binary constraint is true
            consistent = any([value_x[i] == value_y[j] for value_y in self.domains[y]])

            if not consistent:
                self.domains[x].remove(value_x)
                revised = True
        
        return revised

    def initial_arcs(self):
        """
        This method returns a list of all intitial arcs by checking which
        variable have overlaps.
        """
        arcs = []
        for x in self.crossword.variables:
            for y in self.crossword.variables:
                # check if x equlas y
                if x == y:
                    continue

                # if variable x and y have overlap
                if self.crossword.overlaps[x, y] is not None:
                    arcs.append((x, y))
        return arcs
        

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs or self.initial_arcs()

        # loop while queue is not empty
        while len(queue) != 0:
            x, y = queue.pop()

            # if x and y are arc-consistent
            if self.revise(x, y):

                # check if x has any values left in its domain 
                if len(self.domains[x]) == 0:
                    return False
                
                # add x with all it's neighbors (except y) back into queue
                for z in self.crossword.neighbors(x):
                    if z != y:
                        queue.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in assignment.keys():
            if assignment[variable] is None:
                return False
        return True

    def match_neighbors(self, x, assignment):
        """
        This method returns True if any variable in the assignment that overlaps with x
        has the same letter in the 'overlapping' coordinate, otherwise returns False.
        """
        for variable in assignment.keys():
            # check if variable overlaps with x
            if variable in self.crossword.neighbors(x):
                # get overlaping coordinates of x and variable
                i, j = self.crossword.overlaps[x, variable]

                # check if overlapping region is identical
                match = assignment[x][i] == assignment[variable][j]

                if not match:
                    return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # list of all previous words to check if the next word is distinct
        previous = []

        for variable in assignment.keys():
            # check if variable is distinct
            distinct = variable not in previous
            previous.append(variable)

            # check if word has correct length
            length = variable.length == len(assignment[variable])


            # check if word matches neighbors
            match = self.match_neighbors(variable, assignment)

            # if any of the conditions isn't met
            if not(distinct and length and match):
                return False
        
        return True
    
    def least_constraining(self, word, var, assignment):
        """
        Returns and integer of how many interferences a constraints a
        given word of a variable has on its neighbors.
        """
        n = 0

        # check that variable isn't already assigned
        if var in assignment.keys():
            return n
        
        for neighbor in self.crossword.neighbors(var):
            # get the overlap
            i, j = self.crossword.overlaps[var, neighbor]

            for value in self.domains[neighbor]:
                if word[i] != value[j]:
                    n += 1

        return n


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = list(self.domains[var])
        
        # define key function
        least_constraining = lambda word: self.least_constraining(word, var, assignment)

        # sort list according to asceding least_constraining key
        values.sort(key=least_constraining)

        return values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # get list of unassigned variables
        unassigned = [
            var for var in self.crossword.variables if var not in assignment.keys()
        ]

        # sort list according to number of remaining values in domain
        unassigned.sort(key=lambda var:len(self.domains[var]), reverse=True)

        # remove all variables that don't have minimal amounts of words in their
        # domain
        unassigned = [
            var for var in unassigned if (len(self.domains[var])) == len(self.domains[unassigned[-1]])
        ]
        
        # if there's more of one element left in the list
        if len(unassigned) > 1:
            # next heuristic: maximize degree
            unassigned.sort(key=lambda var:len(self.crossword.neighbors(var)))

        if len(unassigned) >= 1:
            return unassigned[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        var = self.select_unassigned_variable(assignment)
        if var is None:
            return assignment
        
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                return self.backtrack(new_assignment)
        return 

    
def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
