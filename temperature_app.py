import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import io

# Set page configuration
st.title("Random Temperature Data Generator")
st.write("Generate random temperature data every 30 minutes for a selected year range (18°C to 30°C)")

# Input fields for start and end year
start_year = st.number_input("Enter Start Year", min_value=2000, max_value=2100, value=2022, step=1)
end_year = st.number_input("Enter End Year", min_value=2000, max_value=2100, value=2024, step=1)

# Validate years
if start_year > end_year:
    st.error("End Year must be greater than or equal to Start Year")
else:
    # Function to generate random temperature data
    def generate_temperature_data(start_year, end_year):
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31, 23, 59)
        date_list = []
        temp_list = []
        
        current_date = start_date
        while current_date <= end_date:
            date_list.append(current_date.strftime("%d/%m/%Y %H:%M"))
            # Generate random temperature between 18 and 30 degrees Celsius
            temp = round(random.uniform(18, 30), 1)
            temp_list.append(temp)
            current_date += timedelta(minutes=30)
        
        # Create DataFrame
        df = pd.DataFrame({
            'DATETIME': date_list,
            'Temperature (°C)': temp_list
        })
        return df

    # Generate data
    data = generate_temperature_data(start_year, end_year)

    # Display data
    st.write("Preview of Generated Temperature Data:")
    st.dataframe(data.head(10))  # Show first 10 rows

    # Convert DataFrame to Excel
    def to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Temperature_Data')
        return output.getvalue()

    # Download button
    excel_data = to_excel(data)
    st.download_button(
        label="Download Temperature Data as Excel",
        data=excel_data,
        file_name="temperature_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )