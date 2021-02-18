import numpy as np
import networkx as nx
import sys
from typing import List 

def read_float(number : str) -> float:
    '''
    Just a helper function to read rational numbers (fractions) into floats, i.e. "1/5" -> 0.2
    '''
    try:
        return float(number)
    except ValueError:
        num, denom = number.split('/')
        return float(num) / float(denom)

def read_upper_traingular_row(row: List[str]) -> List[float]:
    return [read_float(n) for n in row.split(",")]

def read_upper_triangular(s: str) -> List[List[float]]:
    return [read_upper_traingular_row(r) for r in s.split(";")]

def fill_comparison_matrix_from_upper_triangular(upper_triangular: List[List[float]]) -> np.array:
    '''
        Creates a comparison matrix based on the upper triangular part of the matrix, i.e.
        an upper triangular matrix:
        
        0 2 3
        0 0 4
        0 0 0

        we should get a full comparison matrix:

        1    2    3
        1/2  1    4
        1/3  1/4  1
    '''
    size = len(upper_triangular)
    comparison_matrix = np.eye(size, dtype=float)
    for row in range(size):
        comparison_matrix[row] += upper_triangular[row]
    for row in range(1, size):
        for col in range(0, row):
            comparison_matrix[row, col] = 1 / comparison_matrix[col, row]
           
    return comparison_matrix

def read_comparison_matrix(s: str) -> np.array:
    '''
    Just a helper function to read a comparison matrix from upper triangular matrix
    written in a simple format, where "," separates cols and ";" rows, e.g.

    "2,3;4" = [[2,3],[4]] 

    which represents: 

    0 2 3
    0 0 4
    0 0 0 
    '''
    upper_triangular_matrix = read_upper_triangular(s)
    return fill_comparison_matrix_from_upper_triangular(upper_triangular_matrix)

def evm(c: np.array) -> List[float]:
    graph = nx.from_numpy_matrix(c.T, create_using=nx.DiGraph)
    principal_eigenvector = nx.eigenvector_centrality_numpy(graph, weight='weight').values()
    normalized_principal_eigenvector = [v / sum(principal_eigenvector) for v in principal_eigenvector]
    return normalized_principal_eigenvector

if __name__ == "__main__":
    '''
    Reads the upper triangular from the first arg and calculates normalized principal eigenvector
    '''
    comparison_matrix_string = sys.argv[1]
    comparison_matrix = read_comparison_matrix(comparison_matrix_string)
    print(evm(comparison_matrix))