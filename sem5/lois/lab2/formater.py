from typing import List, Dict
from sympy import EmptySet, FiniteSet


def format_sympy_obj(obj) -> str:
    if isinstance(obj, str):
        return obj
    
    if obj is EmptySet:
        return "∅"

    if isinstance(obj, FiniteSet):
        return str(obj)

    left_bracket = "(" if obj.left_open else "["
    right_bracket = ")" if obj.right_open else "]"
    return f"{left_bracket}{float(obj.left):g}, {float(obj.right):g}{right_bracket}"


def format_one_row_result(result: Dict) -> str:
    res_vars = result.keys()
    values = list(map(format_sympy_obj, result.values()))

    if len(res_vars) == 1:
        keys_str = next(iter(res_vars))
    else:
        keys_str = ", ".join(res_vars)
        keys_str = f"<{keys_str}>"

    values_str = " × ".join(map(str, values))

    result = f"{keys_str} ∊ {values_str}"
    return result

    
def format_system_result(system_results: List[List[Dict]]) -> str:
    formated_results = ""
    for i, row_result in enumerate(system_results):
        solution = "Solutions" if len(row_result) > 1 else "Solution"
        formated_results += f"{solution} for line {i + 1}:\n"
        for result in row_result:
            formated_results += "\t" + format_one_row_result(result) + "\n"
        if i != len(system_results) - 1:
            formated_results += "\n"
        
    return formated_results


def reformat_row_keys(result: Dict) -> str:
    keys = list(result.keys())
    if len(keys) == 1:
        return keys[0]
    return "<" + ", ".join(keys) + ">"


def reformat_row_vals(result: Dict) -> str:
    values = result.values()
    if all(isinstance(val, FiniteSet) for val in values):
        str_els = [f"{float(element):g}" for finite_set in values for element in finite_set.args]
        return "<" + ", ".join(str_els) + ">" if len(str_els) > 1 else ", ".join(str_els)
    
    values = list(map(format_sympy_obj, result.values()))
    val_str = " × ".join(map(str, values))
    return f"{val_str}"


def format_final_result(final_results: List[Dict]) -> str:
    if len(final_results) == 0:
        return "No Results"
    if len(final_results) == 1:
        return reformat_row_keys(final_results[0]) + " ∊ " + f"{{{reformat_row_vals(final_results[0])}}}"
    
    vars_str = reformat_row_keys(final_results[0]) + " ∊ "
    
    res_strs = []
    for fin_res in final_results:
        res_str = reformat_row_vals(fin_res)
        res_strs.append(res_str)
    
    return vars_str + "(" + ") ∪ (".join(res_strs) + ")"
    