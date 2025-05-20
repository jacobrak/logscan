from sklearn.ensemble import RandomForestRegressor
import json
from joblib import dump
from scripts.train_test_spliting import prepare_data

X_train, X_test, y_train, y_test = prepare_data()

with open("models/best_params.json", "r") as infile:
    best_parms = json.load(infile)

def RandomForestRegressor_model(X_train=X_train, y_train=y_train, params=best_parms):
    """
    Train a RandomForestRegressor with optimized hyperparameters.

    Parameters:
    - X_train: pd.DataFrame or np.array
    - y_train: pd.Series or np.array

    Returns:
    - Trained RandomForestRegressor model
    """
    assert len(best_parms) != 0, "best_parms is empty"
    assert len(X_train) != 0, "X_train size is 0, Error during optimization"
    assert len(y_train) != 0, "y_train size is 0, Error during optimization"
    model_best = RandomForestRegressor(**params, random_state=42)
    model_best.fit(X_train, y_train)
    
    return model_best

def model_to_file():
    model = RandomForestRegressor_model(X_train, y_train, best_parms)
    dump(model, 'models/random_forest_model.joblib')

if __name__ == "__main__":
    model_to_file()
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, root_mean_squared_error
    model = RandomForestRegressor_model(X_train, y_train, best_parms)

    y_pred = model.predict(X_test)

    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.2f}")
    print(f"MSE:  {mean_squared_error(y_test, y_pred):.2f}")
    print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2f}")
    print(f"R²:   {r2_score(y_test, y_pred):.2f}")