import pandas as pd
from typing import Union


def parse(file_path: str) -> Union[str, pd.DataFrame, pd.DataFrame]:
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    name = lines[0]

    blocks = []
    current_block = []

    for line in lines[1:]:
        if line.strip() == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(line)

    if current_block:
        blocks.append(current_block)

    df1 = pd.DataFrame([row.split() for row in blocks[0][1:]], columns=blocks[0][0].split())
    df2 = pd.DataFrame([row.split() for row in blocks[1][1:]], columns=blocks[1][0].split())

    df1 = df1.astype(float)
    df2 = df2.astype(float)
    
    return name, df1, df2
