import streamlit as st
import pandas as pd
import numpy as np
from time import time

st.title("First test Streamlit Application!")

st.subheader('Input CSV')
uploaded_file = st.file_uploader("Choose a file")

with st.expander('About this app'):
    st.write('You can now display the progress of your calculations in a Streamlit app with the `st.progress` command.')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader('DataFrame')
    st.write(df)
    st.subheader('Descriptive Statistics')
    st.write(df.describe())
else:
    st.info('☝️ Upload a CSV file')

with st.sidebar:
    st.header("About app")
    st.write("Table of contents")
    st.radio("Select one:", [1, 2, 3, 4])

st.header('This is a header with a divider')
st.divider()

st.markdown("This is created using st.markdown")

# Chat Message Example
with st.chat_message("user"):
    st.write("Test Chat Application")
    st.line_chart(np.random.randn(30, 3))

# Chat Input
st.chat_input("Say something")

st.subheader("x2 Column Header")
col1, col2 = st.columns(2)

with col1:
    x = st.slider("Choose an x value", 1, 10)
with col2:
    st.write("The value of :red[***x***] is", x)

st.subheader("Area Chart Header")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.area_chart(chart_data)

st.button("Click me")

st.subheader('Datetime slider')

st.header('st.selectbox')

option = st.selectbox(
    'What is your favorite color?',
    ('Blue', 'Red', 'Green', 'Black')
)

st.write('Your favorite color is ', option)

st.title('Customizing the theme of Streamlit apps')

st.write('Contents of the `.streamlit/config.toml` file of this app')

st.code("""
[theme]
primaryColor="#F39C12"
backgroundColor="#2E86C1"
secondaryBackgroundColor="#AED6F1"
textColor="#FFFFFF"
font="monospace"
""")

number = st.sidebar.slider('Select a number:', 0, 10, 5)
st.write('Selected number from slider widget is:', number)

a0 = time()
st.subheader('Using st.cache_data')

@st.cache_data
def load_data_a():
    df = pd.DataFrame(
        np.random.rand(2000000, 5),
        columns=['a', 'b', 'c', 'd', 'e']
    )
    return df

st.write(load_data_a())
a1 = time()
st.info(a1-a0)

# Not using cache
b0 = time()
st.subheader('Not using cache')

def load_data_b():
    df = pd.DataFrame(
        np.random.rand(2000000, 5),
        columns=['a', 'b', 'c', 'd', 'e']
    )
    return df

st.write(load_data_b())
b1 = time()
st.info(b1-b0)
