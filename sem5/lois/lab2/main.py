from solver import solve_system, get_valid_results
from parser import parse
from formater import format_system_result, format_final_result
import os


def main() -> None:
    folder_path = "tests"
    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        
        x_name, y, z = parse(file_path)
        print("-"*30, x_name, "-"*30)
        print(y)
        print()
        print(z)
        print()
        
        res_rows = solve_system(y, z)
        print(format_system_result(res_rows))

        res = get_valid_results(res_rows)

        print("Final result:\n", format_final_result(res))
        print("\n\n")
    
    
main()
