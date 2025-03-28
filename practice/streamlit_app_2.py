import streamlit as st
from streamlit_shap import st_shap
import shap
from sklearn.model_selection import train_test_split
import xgboost
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    return shap.datasets.adult()

@st.cache_resource
def load_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
    d_train = xgboost.DMatrix(X_train, label=y_train)
    d_test = xgboost.DMatrix(X_test, label=y_test)
    params = {
        "eta": 0.01,
        "objective": "binary:logistic",
        "subsample": 0.5,
        "base_score": np.mean(y_train),
        "eval_metric": "logloss",
        "n_jobs": -1,
    }
    model = xgboost.train(params, d_train, 10, evals=[(d_test, "test")], verbose_eval=100, early_stopping_rounds=20)
    return model

st.title("`streamlit-shap` for displaying SHAP plots in a Streamlit app")

with st.expander('About the app'):
    st.markdown('''[`streamlit-shap`](https://github.com/snehankekre/streamlit-shap) is a Streamlit component that provides a wrapper to display [SHAP](https://github.com/slundberg/shap) plots in [Streamlit](https://streamlit.io/).''')

st.header('Input data')
X, y = load_data()
X_display, y_display = shap.datasets.adult(display=True)

with st.expander('About the data'):
    st.write('Adult census data is used as the example dataset.')
with st.expander('X'):
    st.dataframe(X)
with st.expander('y'):
    st.dataframe(y)

st.header('SHAP output')

# Train XGBoost model
model = load_model(X, y)

# Compute SHAP values
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)

# Initialize SHAP JavaScript for visualization
shap.initjs()

with st.expander('Waterfall plot'):
    st_shap(shap.plots.waterfall(shap.Explanation(values=shap_values[0], base_values=explainer.expected_value, data=X.iloc[0])), height=300)

with st.expander('Beeswarm plot'):
    st_shap(shap.plots.beeswarm(shap.Explanation(values=shap_values, base_values=explainer.expected_value, data=X)), height=300)

with st.expander('Force plot'):
    st.subheader('First data instance')
    st_shap(shap.force_plot(explainer.expected_value, shap_values[0, :], X_display.iloc[0, :]), height=200, width=1000)
    
    st.subheader('First thousand data instances')
    fig, ax = plt.subplots(figsize=(12, 4))
    shap.force_plot(explainer.expected_value, shap_values[:1000, :], X_display.iloc[:1000, :], matplotlib=True, show=False)
    st.pyplot(fig)