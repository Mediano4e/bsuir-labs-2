import numpy as np
import pandas as pd


class ID3DecisionTreeClassifier:
    def __init__(self, max_depth=None, min_samples_split=2, random_state=None):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.tree_ = None

    @staticmethod
    def entropy(y):
        counts = y.value_counts()
        probabilities = counts / len(y)
        return -sum(probabilities * np.log2(probabilities))

    def information_gain(self, df, target_col, feature_col):
        total_entropy = self.entropy(df[target_col])
        values, counts = np.unique(df[feature_col], return_counts=True)
        weighted_entropy = sum(
            (counts[i] / len(df)) * self.entropy(df[df[feature_col] == values[i]][target_col])
            for i in range(len(values))
        )
        return total_entropy - weighted_entropy

    def _build_tree(self, df, target_col, features, depth=0):
        if len(df[target_col].unique()) == 1:
            return df[target_col].iloc[0]
        if not features or (self.max_depth is not None and depth >= self.max_depth):
            return df[target_col].mode()[0]
        if len(df) < self.min_samples_split:
            return df[target_col].mode()[0]
        
        best_feature = max(features, key=lambda f: self.information_gain(df, target_col, f))
        tree = {best_feature: {}}
        
        for value in df[best_feature].unique():
            subset = df[df[best_feature] == value]
            subtree = self._build_tree(
                subset,
                target_col,
                [f for f in features if f != best_feature],
                depth + 1
            )
            tree[best_feature][value] = subtree
        
        return tree

    def fit(self, X, y):
        df = X.copy()
        df['target'] = y
        features = list(X.columns)
        self.tree_ = self._build_tree(df, 'target', features)

    def _predict_row(self, row, tree):
        if not isinstance(tree, dict):
            return tree
        feature = next(iter(tree))
        value = row[feature]
        if value in tree[feature]:
            return self._predict_row(row, tree[feature][value])
        else:
            return None

    def predict(self, X):
        predictions = [self._predict_row(row, self.tree_) for _, row in X.iterrows()]
        return predictions

