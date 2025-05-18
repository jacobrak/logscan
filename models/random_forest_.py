from sklearn.ensemble import RandomForestRegressor
import json
 
with open("models/best_params.json", "r") as infile:
    best_parms = json.load(infile)


def RandomForestRegressor_model(X_train, y_train, params):
    """
    Train a RandomForestRegressor with optimized hyperparameters.

    Parameters:
    - X_train: pd.DataFrame or np.array
    - y_train: pd.Series or np.array

    Returns:
    - Trained RandomForestRegressor model
    """
    assert len(best_parms) != 0
    assert len(X_train) != 0 
    assert len(y_train) != 0
    model_best = RandomForestRegressor(**params)
    model_best.fit(X_train, y_train)

if __name__ == "__main__":
    model = RandomForestRegressor_model(X_train, y_train, best_params)