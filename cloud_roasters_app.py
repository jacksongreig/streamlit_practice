import streamlit as st  
from datetime import date 
import snowflake.connector

# create table if it doesn't already exist
def initialize_table():
    # Connect to Snowflake (creds in secrets.toml)
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    cursor = conn.cursor()
    try:
        # SQL command to create the table with the necessary columns
        create_query = """
            CREATE TABLE IF NOT EXISTS ROASTING_REPORTS (
                "Batch ID" INTEGER PRIMARY KEY,
                "Roastery" VARCHAR(255),
                "Roast Date" DATE,
                "Bean Code" VARCHAR(255),
                "Origin" VARCHAR(255),
                "Moisture Content (%%)" NUMBER(5,2),
                "Roast Level" VARCHAR(50),
                "Roast Duration (mins)" INTEGER,
                "First Crack Time (mins)" INTEGER,
                "Development Time (mins)" INTEGER,
                "Green Bean Weight (kg)" NUMBER(10,2),
                "Roasted Weight (kg)" NUMBER(10,2),
                "Weight Loss (%%)" NUMBER(5,2),
                "Roast Notes" VARCHAR(500)
            );
        """
        # Commit the table creation and close the cursor and connection
        cursor.execute(create_query)
        conn.commit()  
    finally:
        cursor.close()
        conn.close()

# Function to insert a record into the Snowflake table
def insert_record(record):
    # Connect to Snowflake (creds in secrets.toml)
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    cursor = conn.cursor()
    try:
        # SQL INSERT command with placeholders for parameterized query
        insert_query = """
            INSERT INTO ROASTING_REPORTS 
            ("Batch ID", "Roast Date", "Roastery", "Bean Code", "Origin", "Moisture Content (%%)", "Roast Level", 
             "Roast Duration (mins)", "First Crack Time (mins)", "Development Time (mins)", "Green Bean Weight (kg)", 
             "Roasted Weight (kg)", "Weight Loss (%%)", "Roast Notes")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Execute the query using the values from the record dictionary
        cursor.execute(insert_query, (
            record["Batch ID"],
            record["Roast Date"],
            record["Roastery"],
            record["Bean Code"],
            record["Origin"],
            record["Moisture Content (%)"],
            record["Roast Level"],
            record["Roast Duration (mins)"],
            record["First Crack Time (mins)"],
            record["Development Time (mins)"],
            record["Green Bean Weight (kg)"],
            record["Roasted Weight (kg)"],
            record["Weight Loss (%)"],
            record["Roast Notes"]
        ))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

# Initialize a session state variable for the batch ID if it hasn't been set already
if "batch_id" not in st.session_state:
    st.session_state.batch_id = 1

def main():
    # Ensure the table exists by calling the initialization function
    initialize_table()

    # To change background colour and form colour of app
    st.markdown(
        """
        <style>
        /* Overall app background color */
        [data-testid="stAppViewContainer"] {
            background-color: #C8b49c;
        }
        /* Form container styling: background, text color, padding, and border radius */
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

    # Create a form
    with st.form("roasting_form"):

        st.markdown("<h3 style='text-align: center;'>Roasting Report Form</h3>", unsafe_allow_html=True)
        st.markdown(f"Batch ID: {st.session_state.batch_id}", unsafe_allow_html=True)

        store_list = [
            "Martin Place Store", "Bondi Store", "Coogee Store",
            "Paddington Store", "Surry Hills Store", "Bronte Store", "Newtown Store"
        ]

        selected_store = st.selectbox("Select Roastery Location:", store_list, key="selected_store")

        roast_date = st.date_input("Roast Date:", value=st.session_state.get("roast_date", date.today()), key="roast_date")
        formatted_date = roast_date.strftime('%Y-%m-%d')  # Format the date for display and storage

        bean_code = st.text_input("Bean Name:", placeholder="Enter bean name or code", key="bean_code")

        country_list = [
            "Ethiopia", "Brazil", "Colombia", "Kenya", "Costa Rica", "Guatemala", "Honduras", "Peru", "Mexico", "India",
            "Vietnam", "Indonesia", "Rwanda", "Tanzania", "Panama", "El Salvador", "Nicaragua", "Burundi", "Papua New Guinea",
            "Yemen", "Uganda", "China", "Thailand", "Philippines", "Zambia", "Malawi", "Dominican Republic", "Haiti",
            "Venezuela", "Cameroon", "Bolivia", "Laos", "Nepal", "Cuba", "Ivory Coast", "Sri Lanka", "Timor-Leste"
        ]

        bean_origin = st.selectbox("Bean Origin:", country_list, key="bean_origin")

        moisture_content = st.number_input(
            "Moisture Content (%):", min_value=0.0, max_value=100.0,
            value=st.session_state.get("moisture_content", 15.0), step=0.5, key="moisture_content"
        )

        roast_type = st.selectbox("Roast Level:", ["Light", "Medium", "Medium-Dark", "Dark"], key="roast_type")

        roast_duration = st.number_input(
            "Roast Duration (minutes):", min_value=0, max_value=120,
            value=st.session_state.get("roast_duration", 40), step=5, format="%d", key="roast_duration"
        )
        first_crack_time = st.number_input(
            "First Crack Time (minutes):", min_value=0, max_value=120,
            value=st.session_state.get("first_crack_time", 30), step=5, format="%d", key="first_crack_time"
        )
        development_time = st.number_input(
            "Development Time (minutes):", min_value=0, max_value=120,
            value=st.session_state.get("development_time", 30), step=5, format="%d", key="development_time"
        )

        green_weight = st.number_input(
            "Green Bean Weight (kg):", min_value=0.0, max_value=200.0,
            value=st.session_state.get("green_weight", 20.0), step=0.5, key="green_weight"
        )
        roasted_weight = st.number_input(
            "Final Roasted Weight (kg):", min_value=0.0, max_value=200.0,
            value=st.session_state.get("roasted_weight", 20.0), step=0.5, key="roasted_weight"
        )

        # Optional text area for additional roast notes or comments
        roast_notes = st.text_area("Notes / Comments:", key="roast_notes", height=68, max_chars=200, placeholder="Optional")

        # Submit button for the form
        submitted = st.form_submit_button("Submit")

        # When the form is submitted, validate inputs and process the data
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

            # Display any errors encountered during validation
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Calculate the weight loss percentage from the provided weights
                weight_loss = round(((green_weight - roasted_weight) / green_weight) * 100, 2) if green_weight else 0

                # Build a dictionary containing all form data to represent the new record
                new_record = {
                    "Batch ID": st.session_state.batch_id,
                    "Roastery": selected_store,
                    "Roast Date": formatted_date,
                    "Bean Code": bean_code,
                    "Origin": bean_origin,
                    "Moisture Content (%)": moisture_content,
                    "Roast Level": roast_type,
                    "Roast Duration (mins)": roast_duration,
                    "First Crack Time (mins)": first_crack_time,
                    "Development Time (mins)": development_time,
                    "Green Bean Weight (kg)": green_weight,
                    "Roasted Weight (kg)": roasted_weight,
                    "Weight Loss (%)": weight_loss,
                    "Roast Notes": roast_notes
                }

                # Show a success message with details of the submission
                st.success(
                    f"Roasting data submitted for {bean_code} (Batch #{st.session_state.batch_id}) "
                    f"on {formatted_date} at {selected_store}."
                )
                
                # Attempt to insert the new record into Snowflake and display status info
                try:
                    insert_record(new_record)
                    st.info("Record successfully inserted into Snowflake.")
                except Exception as e:
                    st.error(f"Error inserting record into Snowflake: {e}")

                # Increment the batch ID in session state for the next submission
                st.session_state.batch_id += 1

# Run the main function if this script is executed
if __name__ == "__main__":
    main()