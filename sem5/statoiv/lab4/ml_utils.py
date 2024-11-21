import numpy as np
import pandas as pd


def train_test_split(df: pd.DataFrame, test_size: float = 0.2, random_state: int | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    if random_state:
        np.random.seed(random_state)

    indices = df.index.to_list()
    np.random.shuffle(indices)
    
    split_index = int(len(indices) * (1 - test_size))
    train_indices = indices[:split_index]
    test_indices = indices[split_index:]
    
    train_df: pd.DataFrame = df.loc[train_indices].reset_index(drop=True)
    test_df: pd.DataFrame = df.loc[test_indices].reset_index(drop=True)
    
    return train_df, test_df
