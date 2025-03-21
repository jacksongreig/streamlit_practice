import streamlit as st  # type: ignore
from datetime import date

if "batch_id" not in st.session_state:
    st.session_state.batch_id = 1

# set background colour, keep form black
def main():
    st.markdown(
        """
        <style>
        /* Set the overall app background */
        [data-testid="stAppViewContainer"] {
            background-color: #C8b49c;
        }
        /* Set the form container background to black */
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

    # create form
    with st.form("roasting_form"):
        st.markdown("<h3 style='text-align: center;'>Roasting Report Form</h3>", unsafe_allow_html=True)
        st.markdown(f"Batch ID: {st.session_state.batch_id}", unsafe_allow_html=True)

        store_list = [
            "Martin Place Store", "Bondi Store", "Coogee Store",
            "Paddington Store", "Surry Hills Store", "Bronte Store", "Newtown Store"
        ]
        selected_store = st.selectbox("Select Roastery Location:", store_list, key="selected_store")

        roast_date = st.date_input("Roast Date:", value=st.session_state.get("roast_date", date.today()), key="roast_date")
        formatted_date = roast_date.strftime('%Y-%m-%d')

        # add a placeholder to the bean code input
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
            value=st.session_state.get("roast_duration", 40), step=10, format="%d", key="roast_duration"
        )
        first_crack_time = st.number_input(
            "First Crack Time (minutes):", min_value=0, max_value=120,
            value=st.session_state.get("first_crack_time", 30), step=10, format="%d", key="first_crack_time"
        )
        development_time = st.number_input(
            "Development Time (minutes):", min_value=0, max_value=120,
            value=st.session_state.get("development_time", 30), step=10, format="%d", key="development_time"
        )

        green_weight = st.number_input(
            "Green Bean Weight (kg):", min_value=0.0, max_value=200.0,
            value=st.session_state.get("green_weight", 20.0), step=0.5, key="green_weight"
        )
        roasted_weight = st.number_input(
            "Final Roasted Weight (kg):", min_value=0.0, max_value=200.0,
            value=st.session_state.get("roasted_weight", 20.0), step=0.5, key="roasted_weight"
        )

        roast_notes = st.text_area("Roast Profile Notes / Comments (optional):", key="roast_notes")

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

                new_record = {
                    "Batch ID": st.session_state.batch_id,
                    "Roast Date": formatted_date,
                    "Roastery": selected_store,
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

                st.success(
                    f"Roasting data submitted for {bean_code} (Batch #{st.session_state.batch_id}) "
                    f"on {formatted_date} at {selected_store}."
                )
                st.json(new_record)

                # increment batch ID for the next submission
                st.session_state.batch_id += 1

                # manually clear form fields after a successful submission
                st.session_state.selected_store = store_list[0]
                st.session_state.roast_date = date.today()
                st.session_state.bean_code = ""
                st.session_state.bean_origin = country_list[0]
                st.session_state.moisture_content = 10.0
                st.session_state.roast_type = "Light"
                st.session_state.roast_duration = 0
                st.session_state.first_crack_time = 0
                st.session_state.development_time = 0
                st.session_state.green_weight = 0.0
                st.session_state.roasted_weight = 0.0
                st.session_state.roast_notes = ""

if __name__ == "__main__":
    main()