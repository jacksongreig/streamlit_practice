#Cloud Roasters Form Submission

import streamlit as st
import pandas as pd
import os
from datetime import date

# --- CSV storage utility ---
# You can replace this part with a proper DB integration or API call.
DATA_FILE = "coffee_shop_data.csv"

def load_data():
    """Load existing data from CSV if it exists, otherwise create an empty DataFrame."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Date", "Store", "Coffees Sold", "Pastries Sold", "Specials Sold", "Notes"])

def save_data(df):
    """Save DataFrame to CSV."""
    df.to_csv(DATA_FILE, index=False)

# --- Main Streamlit App ---
def main():
    st.title("☕ Daily Coffee Shop Report")
    
    # Load existing data
    data = load_data()

    # Create the form within a 'with' block for clarity
    with st.form("coffee_form", clear_on_submit=True):
        st.subheader("Daily Reporting Form")

        # Store selection (you can hardcode or dynamically generate from your DB)
        store_list = ["Martin Place Store", "Bondi Store", "Coogee Store", "Paddington Store", "Surry Hills Store", "Bronte Store", "Newtown Store"]
        selected_store = st.selectbox("Select Store", store_list)

        # Date input (default to today's date)
        report_date = st.date_input("Date", value=date.today())

        # Numeric inputs for daily metrics
        coffees_sold = st.number_input("Coffees Sold", min_value=0, max_value=100000, value=0, step=1)
        pastries_sold = st.number_input("Pastries Sold", min_value=0, max_value=100000, value=0, step=1)
        specials_sold = st.number_input("Specials Sold (e.g. seasonal drinks, combos, etc.)", min_value=0, max_value=100000, value=0, step=1)

        # Text area for additional notes
        additional_notes = st.text_area("Notes / Comments")

        # Submit button
        submitted = st.form_submit_button("Submit")

        # When the submit button is clicked
        if submitted:
            # Append the new record to our DataFrame
            new_record = {
                "Date": report_date,
                "Store": selected_store,
                "Coffees Sold": coffees_sold,
                "Pastries Sold": pastries_sold,
                "Specials Sold": specials_sold,
                "Notes": additional_notes
            }
            data = data.append(new_record, ignore_index=True)

            # Save updated data
            save_data(data)

            st.success(f"Data submitted for {selected_store} on {report_date}.")

    st.write("---")
    st.subheader("Current Data Overview")
    st.write("Below is the table of all submissions so far:")
    st.dataframe(data)

if __name__ == "__main__":
    main()



