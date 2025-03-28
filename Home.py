import streamlit as st

# ========== Page Setup ==========
st.set_page_config(
    page_title="Cloud Roasters | Home",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== Styling ==========
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #C8b49c;
    }

    [data-testid="collapsedControl"] {
        display: none;
    }

    .home-container {
        max-width: 800px;
        margin: 0 auto;
        background-color: #000000;
        color: white;
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }

    .home-container h1 {
        font-size: 2.8rem;
        margin-bottom: 0.75rem;
    }

    .home-container p {
        font-size: 1.2rem;
        margin-bottom: 3rem;  /* Space added between text and buttons */
    }

    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }

    .nav-button {
        padding: 1.2rem 2.5rem;
        font-size: 1.3rem;
        font-weight: 600;
        border-radius: 10px;
        background-color: #000000;
        color: white;
        border: 2px solid white;
        cursor: pointer;
        transition: background-color 0.3s ease, transform 0.2s ease;
    }

    .nav-button:hover {
        background-color: #333333;
        transform: translateY(-2px);
    }

    /* Space between logo and home container */
    .stImage {
        margin-bottom: 2rem;
    }

    a {
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# ========== Logo ==========
st.image("logo.png", use_container_width=True)

# ========== Welcome Block ==========
with st.container():
    st.markdown("""
        <div class="home-container">
            <h1>Welcome to Cloud Roasters</h1>
            <p>
                Your roasting intelligence hub. Use the tools below to submit roasting batch data or explore insights with our coffee-savvy assistant.
            </p>
            <div class="nav-buttons">
                <a href="Roasting_Report_Form" target="_self">
                    <button class="nav-button">Roasting Report Form</button>
                </a>
                <a href="Cloud_Roasters_Assistant" target="_self">
                    <button class="nav-button">Cloud Roasters Assistant</button>
                </a>
            </div>
        </div>
    """, unsafe_allow_html=True)
