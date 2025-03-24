import streamlit as st
from datetime import date, datetime
import pytz
import snowflake.connector

def get_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

def initialize_table():
    create_query = """
        CREATE TABLE IF NOT EXISTS ROASTING_REPORTS (
            "BATCH_ID" INTEGER PRIMARY KEY,
            "ROASTERY" VARCHAR(255),
            "ROAST_DATE" DATE,
            "BEAN_CODE" VARCHAR(255),
            "ORIGIN" VARCHAR(255),
            "MOISTURE_CONTENT" NUMBER(5,2),
            "ROAST_LEVEL" VARCHAR(50),
            "ROAST_DURATION_MINS" INTEGER,
            "FIRST_CRACK_TIME_MINS" INTEGER,
            "DEVELOPMENT_TIME_MINS" INTEGER,
            "GREEN_BEAN_WEIGHT_KG" NUMBER(10,2),
            "ROASTED_WEIGHT_KG" NUMBER(10,2),
            "WEIGHT_LOSS" NUMBER(5,2),
            "ROAST_NOTES" VARCHAR(500),
            "SUBMISSION_TIMESTAMP" TIMESTAMP
        );
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_query)
            conn.commit()

def get_next_batch_id_from_table():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('SELECT MAX("BATCH_ID") FROM ROASTING_REPORTS')
            result = cursor.fetchone()
            return 1 if result[0] is None else result[0] + 1

def insert_record(record):
    insert_query = """
        INSERT INTO ROASTING_REPORTS 
        ("BATCH_ID", "ROAST_DATE", "ROASTERY", "BEAN_CODE", "ORIGIN", "MOISTURE_CONTENT", "ROAST_LEVEL", 
         "ROAST_DURATION_MINS", "FIRST_CRACK_TIME_MINS", "DEVELOPMENT_TIME_MINS", "GREEN_BEAN_WEIGHT_KG", 
         "ROASTED_WEIGHT_KG", "WEIGHT_LOSS", "ROAST_NOTES", "SUBMISSION_TIMESTAMP")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(insert_query, (
                record["BATCH_ID"],
                record["ROAST_DATE"],
                record["ROASTERY"],
                record["BEAN_CODE"],
                record["ORIGIN"],
                record["MOISTURE_CONTENT"],
                record["ROAST_LEVEL"],
                record["ROAST_DURATION_MINS"],
                record["FIRST_CRACK_TIME_MINS"],
                record["DEVELOPMENT_TIME_MINS"],
                record["GREEN_BEAN_WEIGHT_KG"],
                record["ROASTED_WEIGHT_KG"],
                record["WEIGHT_LOSS"],
                record["ROAST_NOTES"],
                record["SUBMISSION_TIMESTAMP"]
            ))
            conn.commit()

def main():
    initialize_table()

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #C8b49c;
        }
        [data-testid="stForm"] {
            background-color: #000000;
            color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image("logo.png", use_container_width=True)

    with st.form("roasting_form"):
        batch_id = get_next_batch_id_from_table()
        st.markdown("<h3 style='text-align: center;'>Roasting Report Form</h3>", unsafe_allow_html=True)
        st.markdown(f"Batch ID: {batch_id}", unsafe_allow_html=True)

        store_list = [
            "Martin Place Store", "Bondi Store", "Coogee Store",
            "Paddington Store", "Surry Hills Store", "Bronte Store", "Newtown Store"
        ]
        selected_store = st.selectbox("Select Roastery Location:", store_list, key="selected_store")

        roast_date = st.date_input("Roast Date:", value=date.today(), key="roast_date")
        bean_code = st.text_input("Bean Name:", placeholder="Enter bean name or code", key="bean_code")

        country_list = [
            "Ethiopia", "Brazil", "Colombia", "Kenya", "Costa Rica", "Guatemala", "Honduras", "Peru", "Mexico", "India",
            "Vietnam", "Indonesia", "Rwanda", "Tanzania", "Panama", "El Salvador", "Nicaragua", "Burundi", "Papua New Guinea",
            "Yemen", "Uganda", "China", "Thailand", "Philippines", "Zambia", "Malawi", "Dominican Republic", "Haiti",
            "Venezuela", "Cameroon", "Bolivia", "Laos", "Nepal", "Cuba", "Ivory Coast", "Sri Lanka", "Timor-Leste"
        ]
        bean_origin = st.selectbox("Bean Origin:", country_list, key="bean_origin")

        moisture_content = st.number_input(
            "Moisture Content (%):", 
            min_value=0.0, max_value=100.0,
            value=15.0, step=0.5, key="moisture_content"
        )
        roast_type = st.selectbox("Roast Level:", ["Light", "Medium", "Medium-Dark", "Dark"], key="roast_type")
        roast_duration = st.number_input(
            "Roast Duration (minutes):", 
            min_value=0, max_value=120,
            value=40, step=5, format="%d", key="roast_duration"
        )
        first_crack_time = st.number_input(
            "First Crack Time (minutes):", 
            min_value=0, max_value=120,
            value=30, step=5, format="%d", key="first_crack_time"
        )
        development_time = st.number_input(
            "Development Time (minutes):", 
            min_value=0, max_value=120,
            value=30, step=5, format="%d", key="development_time"
        )
        green_weight = st.number_input(
            "Green Bean Weight (kg):", 
            min_value=0.0, max_value=200.0,
            value=20.0, step=0.5, key="green_weight"
        )
        roasted_weight = st.number_input(
            "Final Roasted Weight (kg):", 
            min_value=0.0, max_value=200.0,
            value=20.0, step=0.5, key="roasted_weight"
        )
        roast_notes = st.text_area("Notes / Comments:", key="roast_notes", height=68, max_chars=200, placeholder="Optional")

        submitted = st.form_submit_button("Submit")

        if submitted:
            errors = []
            if not bean_code.strip():
                errors.append("Bean Name / Code is required.")
            if roast_duration <= 0:
                errors.append("Roast Duration must be greater than 0.")
            if first_crack_time <= 0:
                errors.append("First Crack Time must be greater than 0.")
            if development_time <= 0:
                errors.append("Development Time must be greater than 0.")
            if green_weight <= 0:
                errors.append("Green Bean Weight must be greater than 0.")
            if roasted_weight <= 0:
                errors.append("Final Roasted Weight must be greater than 0.")

            if errors:
                for error in errors:
                    st.error(error)
            else:
                weight_loss = round(((green_weight - roasted_weight) / green_weight) * 100, 2) if green_weight else 0

                aedt = pytz.timezone("Australia/Sydney")
                submission_ts = datetime.now(aedt).replace(microsecond=0)

                new_record = {
                    "BATCH_ID": batch_id,
                    "ROAST_DATE": roast_date,
                    "ROASTERY": selected_store,
                    "BEAN_CODE": bean_code,
                    "ORIGIN": bean_origin,
                    "MOISTURE_CONTENT": moisture_content,
                    "ROAST_LEVEL": roast_type,
                    "ROAST_DURATION_MINS": roast_duration,
                    "FIRST_CRACK_TIME_MINS": first_crack_time,
                    "DEVELOPMENT_TIME_MINS": development_time,
                    "GREEN_BEAN_WEIGHT_KG": green_weight,
                    "ROASTED_WEIGHT_KG": roasted_weight,
                    "WEIGHT_LOSS": weight_loss,
                    "ROAST_NOTES": roast_notes,
                    "SUBMISSION_TIMESTAMP": submission_ts
                }
                try:
                    insert_record(new_record)
                    st.success(
                        f"Roasting data submitted for {bean_code} (Batch #{batch_id}) on {roast_date} at {selected_store}."
                    )
                    st.info("Roasting Report successfully imported into database.")
                except Exception as exp:
                    st.error(f"Error inserting record into Snowflake: {exp}")

if __name__ == "__main__":
    main()