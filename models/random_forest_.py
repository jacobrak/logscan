from sklearn.ensemble import RandomForestRegressor
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.dataset_creation import prepare_data

X_train, X_test, y_train, y_test = prepare_data()

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
    
    return model_best

if __name__ == "__main__":
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, root_mean_squared_error
    model = RandomForestRegressor_model(X_train, y_train, best_parms)

    y_pred = model.predict(X_test)

    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"MSE:  {mean_squared_error(y_test, y_pred):.2f}")
    print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2f}")
    print(f"R²:   {r2_score(y_test, y_pred):.2f}")