
import requests
import pandas as pd
from datetime import datetime
import os

# API Details
API_KEY = "xx"

BASE_URL = "https://finnhub.io/api/v1/quote"


# Function to Extract Data from API
def extract_data(symbol):
    """Fetch financial data for a given stock symbol."""
    url = f"{BASE_URL}?symbol={symbol}&token={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if all(key in data for key in ["c", "h", "l", "o", "pc"]):  # Validate all required keys are present
            print(f"Data for {symbol}: {data}")
            return data
        else:
            print(f"Incomplete data for {symbol}: {data}")
            return None
    else:
        print(f"Failed to fetch data for {symbol}. Status Code: {response.status_code}")
        return None


# Function to Transform Data
def transform_data(raw_data, symbol):
    """Clean and structure the raw financial data."""
    if raw_data:
        transformed_data = {
            "Symbol": symbol,
            "Current Price": raw_data.get("c"),
            "High Price": raw_data.get("h"),
            "Low Price": raw_data.get("l"),
            "Open Price": raw_data.get("o"),
            "Previous Close": raw_data.get("pc"),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return pd.DataFrame([transformed_data])
    else:
        print("No data to transform.")
        return None


# Function to Store Data in CSV
def store_data(dataframe, file_name="financial_data.csv"):
    """Save the dataframe to a CSV file."""
    if not dataframe.empty:
        # Check if the file already exists
        if os.path.exists(file_name):
            dataframe.to_csv(file_name, mode="a", header=False, index=False)  # Append to existing file
            print(f"Data appended to {file_name}.")
        else:
            dataframe.to_csv(file_name, mode="w", header=True, index=False)  # Create a new file
            print(f"Data saved to {file_name}.")
    else:
        print("No data to store.")


# Main Program
if __name__ == "__main__":
    stock_symbol = "AAPL"  # Replace with desired stock symbol
    raw_data = extract_data(stock_symbol)

    if raw_data:
        transformed_df = transform_data(raw_data, stock_symbol)

        if transformed_df is not None:
            print("\nTransformed Data:")
            print(transformed_df)
            store_data(transformed_df)