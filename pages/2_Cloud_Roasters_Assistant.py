import streamlit as st
import snowflake.connector
import pandas as pd
import requests
import re

# ========== Page Setup ==========
st.set_page_config(
    page_title="Cloud Roasters | LLM",
    page_icon="☁️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ========== Custom Styling ==========
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #C8b49c;
    }

    .custom-form-wrapper {
        max-width: 800px;
        margin: 0 auto;
    }

    [data-testid="stForm"] {
        background-color: #000000;
        color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
    }

    textarea {
        background-color: #1c1c1c !important;
        color: white !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        font-size: 16px !important;
    }

    pre {
        max-height: 300px !important;
        overflow-y: auto !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    </style>
""", unsafe_allow_html=True)

# ========== Logo ==========
st.image("logo.png", use_container_width=True)

# ========== Ask Mistral LLM ==========
def ask_llm(question):
    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['mistral']['api_key']}",
            "Content-Type": "application/json"
        }

        prompt = f"""
        You are a helpful assistant for a coffee roasting company.

        If the user asks a question about roasting data (e.g. batch times, weights, roast levels),
        return a single valid Snowflake SQL query using the ROASTING_REPORTS table. Do not explain it.

        If the question is about coffee knowledge (e.g. bean pairings, brewing tips, flavour profiles),
        respond with a natural language answer.

        ROASTING_REPORTS columns:
        BATCH_ID, ROASTERY, ROAST_DATE, BEAN_CODE, ORIGIN, MOISTURE_CONTENT,
        ROAST_LEVEL, ROAST_DURATION_MINS, FIRST_CRACK_TIME_MINS, DEVELOPMENT_TIME_MINS,
        GREEN_BEAN_WEIGHT_KG, ROASTED_WEIGHT_KG, WEIGHT_LOSS, ROAST_NOTES, SUBMISSION_TIMESTAMP.

        If the query filters by ROASTERY, ORIGIN, or BEAN_CODE, use a case-insensitive partial match like:
        ROASTERY ILIKE '%coogee%' instead of ROASTERY = 'Coogee Store'.

        Also, wrap all string values in single quotes.

        Question: {question}
        """

        data = {
            "model": "mistral-small",
            "messages": [
                {"role": "system", "content": "You are a coffee expert and Snowflake SQL expert."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        st.error(f"❌ Mistral API error: {e}")
        return ""

# ========== Snowflake Connection ==========
def connect_to_snowflake():
    try:
        return snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"],
            role=st.secrets["snowflake"]["role"]
        )
    except Exception as e:
        st.error(f"❌ Snowflake connection failed: {e}")
        return None

# ========== Run SQL Query ==========
def run_query(query, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            if not rows:
                st.success("✅ Query executed successfully!")
                st.warning("⚠️ But it returned no results.")
                return pd.DataFrame()
            columns = [desc[0] for desc in cur.description]
            st.success("✅ Query executed successfully!")
            return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        st.error(f"❌ SQL execution error:\n\n{e}")
        return None

# ========== Streamlit UI ==========
st.markdown('<div class="custom-form-wrapper">', unsafe_allow_html=True)

with st.form("llm_roaster_form", clear_on_submit=True):
    st.markdown("<h3 style='text-align: center; color: white;'>Ask About Roasting or Coffee</h3>", unsafe_allow_html=True)

    question = st.text_area(
        "What would you like to know?",
        height=150,
        placeholder="e.g. What goes well with an Ethiopian roast? OR Show me the latest batch from Coogee"
    )

    submitted = st.form_submit_button("Ask")

    if submitted:
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("🧠 Thinking..."):
                response = ask_llm(question)

            # Check if LLM response is SQL
            if re.match(r"(?i)^(SELECT|WITH|INSERT|UPDATE|DELETE)", response.strip()):
                with st.spinner("🔍 Running SQL..."):
                    conn = connect_to_snowflake()
                    if conn:
                        df = run_query(response, conn)
                        if df is not None:
                            st.code(response, language="sql")
                            if not df.empty:
                                st.dataframe(df, use_container_width=True)
            else:
                st.success("✅ Answer from your coffee assistant:")
                st.markdown(response)

st.markdown('</div>', unsafe_allow_html=True)
