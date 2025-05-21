import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error, mean_absolute_error, root_mean_squared_error, r2_score
import os
import streamlit as st

# --- Load saved artifacts ---
@st.cache_data
def load_model():
    return joblib.load('models/random_forest_model.joblib')

@st.cache_data
def load_data():
    # Replace with your data path
    return pd.read_csv('data/processed_data.csv')

# --- Feature importance plotting ---
def plot_feature_importance(model, feature_names):
    importances = model.feature_importances_
    fi_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    fig, ax = plt.subplots()
    sns.barplot(data=fi_df, x='importance', y='feature', ax=ax)
    ax.set_title("Feature Importance")
    st.pyplot(fig)

# Main App 
def main():
    st.title("ML Project Dashboard")
    
    st.header("Model Metrics")
    model = load_model()

    data = load_data()
    X = data.drop(["response_time"], axis=1)
    y_true = data['response_time']

    y_pred = model.predict(X)
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    RMSE = root_mean_squared_error(y_true, y_pred)
    R = r2_score(y_true, y_pred)

    st.write(f"RMSE: **{RMSE:.2f}**")
    st.write(f"MSE: **{mse:.2f}**")
    st.write(f"MAE: **{mae:.2f}**")
    st.write(f"R²: **{R:.2f}**")

    st.header("Feature Importance")
    plot_feature_importance(model, X.columns)


    st.header("Make a Prediction")
    st.write("Upload a CSV file with features to get predictions.")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        preds = model.predict(new_data)
        st.write("Predictions:")
        st.write(preds)

if __name__ == "__main__":
    main()
