import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
import os
import streamlit as st

st.write("Current working directory:", os.getcwd())
st.write("Files in current directory:", os.listdir('.'))

# Check inside 'app' folder (adjust if needed)
if os.path.exists('app'):
    st.write("Files in 'app':", os.listdir('app'))
    if os.path.exists('app/model'):
        st.write("Files in 'app/model':", os.listdir('app/model'))
else:
    st.write("'app' folder not found")

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
    rmse = mse ** 0.5
    st.write(f"Root Mean Squared Error on validation data: **{rmse:.2f}**")


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
