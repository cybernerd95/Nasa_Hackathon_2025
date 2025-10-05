import joblib
import numpy as np

# Load your model
model = joblib.load("shark_rf_model.joblib")

# Random Forest has many trees
for i, tree in enumerate(model.estimators_):
    print(f"\nTree {i}:")
    feature = tree.tree_.feature
    threshold = tree.tree_.threshold
    n_nodes = tree.tree_.node_count
    for node in range(n_nodes):
        if feature[node] != -2:  # -2 means leaf node
            print(f" Node {node}: feature={feature[node]}, threshold={threshold[node]}")
