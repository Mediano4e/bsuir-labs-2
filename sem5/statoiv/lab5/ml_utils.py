import numpy as np


def rmse_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    squared_errors = (y_true - y_pred) ** 2
    
    mse = np.mean(squared_errors)

    return np.sqrt(mse)


def r2_score(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    y_true_mean = np.mean(y_true)
    
    ss_total = np.sum((y_true - y_true_mean) ** 2)
    
    ss_residual = np.sum((y_true - y_pred) ** 2)
    
    return 1 - (ss_residual / ss_total)
