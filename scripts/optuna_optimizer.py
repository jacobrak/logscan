import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.train_test_spliting import prepare_data

X_train, X_test, y_train, y_test = prepare_data() 
assert len(X_train) != 0, "X_train size is 0, Error during optimization"
assert len(y_train) != 0, "y_train size is 0, Error during optimization"

def objective(trial):
    params = {
        "n_estimators": trial.suggest_int("n_estimators", 50, 300),  
        "max_depth": trial.suggest_int("max_depth", 2, 20),
        "min_samples_split": trial.suggest_int("min_samples_split", 2, 10),
        "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
        "max_features": trial.suggest_categorical("max_features", ["sqrt", "log2"]),
    }

    model = RandomForestRegressor(**params, random_state=42, n_jobs=-1)

    score = cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv=3)
    return -score.mean()

def study_():
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50) 
    best_params = study.best_params

    with open("best_params.json", "w") as w:
        json.dump(best_params, w)

if __name__ == "__main__":
    print("Hello World")