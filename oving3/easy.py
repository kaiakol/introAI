import copy
from itertools import product as prod

class CSP:
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.constraints = {}

    def add_variable(self, name: str, domain: list):
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a: list, b: list) -> list[tuple]:
        return prod(a, b)

    def get_all_arcs(self) -> list[tuple]:
        return [(i, j) for i in self.constraints for j in self.constraints[i]]

    def get_all_neighboring_arcs(self, var: str) -> list[tuple]:
        return [(i, var) for i in self.constraints[var]]

    def add_constraint(self, i: str, j: str, constraint_function: callable):
        if j not in self.constraints[i]:
            self.constraints[i][j] = constraint_function

    def add_all_different_constraint(self, var_list: list):
        for (i, j) in self.get_all_possible_pairs(var_list, var_list):
            if i != j:
                self.add_constraint(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        assignment = copy.deepcopy(self.domains)
        self.inference(assignment, self.get_all_arcs())
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        if all(len(assignment[var]) == 1 for var in self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in assignment[var]:
            new_assignment = copy.deepcopy(assignment)
            new_assignment[var] = [value]
            if self.inference(new_assignment, self.get_all_neighboring_arcs(var)):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        return None

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [var for var in self.variables if len(assignment[var]) > 1]
        return min(unassigned_vars, key=lambda var: len(assignment[var]))

    def inference(self, assignment, queue):
        while queue:
            i, j = queue.pop(0)
            if self.revise(assignment, i, j):
                if not assignment[i]:
                    return False

                for k in self.get_all_neighboring_arcs(i):
                    if k[0] != j:
                        queue.append(k)

        return True

    def revise(self, assignment, i, j):
        revised = False
        for x in assignment[i]:
            if all(not self.constraints[i][j](x, y) for y in assignment[j]):
                assignment[i].remove(x)
                revised = True
        return revised

def create_sudoku_csp(filename: str) -> CSP:
    csp = CSP()
    board = list(map(lambda x: x.strip(), open(filename, 'rt')))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), list(map(str, range(1, 10))))
            else:
                csp.add_variable('%d-%d' % (row, col), [board[row][col]])

    for row in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for col in range(9)])
    for col in range(9):
        csp.add_all_different_constraint(['%d-%d' % (row, col) for row in range(9)])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    for row in range(9):
        for col in range(9):
            print(solution['%d-%d' % (row, col)][0], end=" ")
            if col == 2 or col == 5:
                print('|', end=" ")
        print("")
        if row == 2 or row == 5:
            print('------+-------+------')

if __name__ == "__main__":
    filename = "easy.txt"  
    sudoku_csp = create_sudoku_csp(filename)
    solution = sudoku_csp.backtracking_search()

    if solution is not None:
        print_sudoku_solution(solution)
    else:
        print("No solution found.")