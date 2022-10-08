import os
import math
import itertools

import numpy as np
import matplotlib.pyplot as plt

class Solver:

    def __init__(self, input_list, given_boundary_nodes=True) -> None:
        if given_boundary_nodes:
            self.boundary = input_list
            self.nodes = self._calculate_nodes(self.boundary)
        else:
            function_params = input_list
            self.nodes, self.boundary = self._calculate_nodes_and_boundary(function_params)

    def _calculate_nodes(self, boundary):
        nodes = []

        x_list = [x for x,y in boundary]
        y_list = [y for x,y in boundary]
        
        min_y, max_y = min(y_list), max(y_list)
        
        for y in range(min_y+1, max_y):
            indices = [i for i,y_temp in enumerate(y_list) if y_temp == y]
            x_vals = [x_list[i] for i in indices]
            
            min_x, max_x = min(x_vals), max(x_vals)
            
            inside = False
            for x in range(min_x, max_x + 1):
                if ((x,y) in boundary) & ((x-1, y) in boundary):
                    continue
                elif (x,y) in boundary:
                    inside = not inside
                    continue
                elif inside:
                    nodes.append((x,y))
                    
        return nodes

    def _calculate_nodes_and_boundary(self, function_params):
        """
        function_params = [a, b, c, d, e]
        """
        a, b, c, d, e = function_params
        
        x_max = a + (b * np.sqrt(e))
        x_min = a + (b * -np.sqrt(e))
        x_max, x_min = int(np.ceil(x_max)), int(np.floor(x_min))
        
        y_max = c + (d * np.sqrt(e))
        y_min = c + (d * -np.sqrt(e))
        y_max, y_min = int(np.ceil(y_max)), int(np.floor(y_min))
        
        nodes = []
        for y in range(y_min, y_max+1):
            for x in range(x_min, x_max):
                if ((x-a)/b)**2 + ((y-c)/d)**2 < e:
                    nodes.append((x,y))
        
        boundary = []
        for (x,y) in nodes:
            if ((x+1,y) not in nodes) & ((x+1,y) not in boundary):
                boundary.append((x+1,y))
            if ((x-1,y) not in nodes) & ((x-1,y) not in boundary):
                boundary.append((x-1,y))
            if ((x,y+1) not in nodes) & ((x,y+1) not in boundary):
                boundary.append((x,y+1))
            if ((x,y-1) not in nodes) & ((x,y-1) not in boundary):
                boundary.append((x,y-1))
        
        return nodes, boundary

    def _calculate_transition_matrix(self, nodes, boundaries):
        rows = []
        
        for x,y in nodes:
            row = np.zeros(len(nodes))
            if (x+1, y) not in boundaries:
                index = nodes.index((x+1, y))
                row[index] = 0.25
            if (x-1, y) not in boundaries:
                index = nodes.index((x-1, y))
                row[index] = 0.25
            if (x, y+1) not in boundaries:
                index = nodes.index((x, y+1))
                row[index] = 0.25
            if (x, y-1) not in boundaries:
                index = nodes.index((x, y-1))
                row[index] = 0.25
            rows.append(row)
            
        return np.vstack(rows)

    def expected_number_of_steps(self, starting_node=None):
        if starting_node == None:
            starting_node = (0,0)

        transition_matrix = self._calculate_transition_matrix(self.nodes, self.boundary)
        N = np.identity(transition_matrix.shape[0]) - transition_matrix
        N = np.linalg.inv(N)

        return sum(N[self.nodes.index(starting_node)])

