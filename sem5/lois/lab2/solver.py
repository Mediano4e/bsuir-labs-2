from sympy import Interval, symbols, Eq, solve, solveset, EmptySet, FiniteSet
import pandas as pd
from typing import Dict, List
from parser import parse
import itertools
from functools import reduce
from formater import format_system_result, format_final_result



def solve_equation(y: float, z: float) -> FiniteSet:
    equation_str = f"x + {y} - {z} - 1"
    x = symbols("x")
    equation = Eq(eval(equation_str), 0)
    solution = solve(equation, x)
    if (solution[0] < 0) or (solution[0] > 1):
        return EmptySet
    else:
        return FiniteSet(solution[0])
    

def solve_inequality(y: float, z: float) -> Interval | FiniteSet:
    inequality_str = f"x + {y} - 1 <= {z}"
    x = symbols("x")
    inequality = eval(inequality_str)
    domain = Interval(0, 1, left_open=False, right_open=False)
    solution = solveset(inequality, x, domain=domain)
    return solution


def solve_row_combination(row: pd.Series, z: float, target_y: str | None = None) ->  Dict | None:
    res = {}
    for pos, (idx, y) in enumerate(row.items()):
        x_name = f'x{pos + 1}'
        if idx == target_y:
            new_res = solve_equation(y, z)
            if new_res is EmptySet:
                return None
        else: 
            new_res = solve_inequality (y, z)
            
        res[x_name] = new_res
    return res


def solve_full_row(row: pd.Series, z: float) -> List:
    y_names = list(row.index)
    row_res = []
    if z != 0:
        processed_y = set()
        for y_name in y_names:
            if row.loc[y_name] in processed_y:
                continue
            if new_res := solve_row_combination(row, z, y_name):
                row_res.append(new_res)
            processed_y.add(row.loc[y_name])
    else:
        if new_res := solve_row_combination(row, z):
            row_res.append(new_res)
    return row_res


def solve_system(y_vals: pd.DataFrame, z_vals: pd.DataFrame):
    row_results = []
    for index, row in y_vals.iterrows():
        z = z_vals.loc[index, "z"]
        new_res = solve_full_row(row, z)
        row_results.append(new_res)
    return row_results


def is_subset_dict(dict1: Dict, dict2: Dict) -> bool:
    for key in dict1:
        if not dict1[key].is_subset(dict2[key]):
            return False
    return True


def remove_subsets(row_results: List) -> List:
    result = []
    for i, dict1 in enumerate(row_results):
        is_subset = False
        for j, dict2 in enumerate(row_results):
            if i != j and is_subset_dict(dict1, dict2):
                is_subset = True
                break
        if not is_subset:
            result.append(dict1)
    return result
    

def get_valid_results(row_results: List) -> List | None:
    result = []

    for combination in itertools.product(*row_results):
        if not combination:
            continue
        
        keys = combination[0].keys()
        intersection_dict = {}
        
        for key in keys:
            values = [d[key] for d in combination]

            intersection = reduce(lambda a, b: a.intersection(b), values)
            intersection_dict[key] = intersection
        
        if not any(val is EmptySet for val in intersection_dict.values()):
            result.append(intersection_dict)
    
    return remove_subsets(result)
