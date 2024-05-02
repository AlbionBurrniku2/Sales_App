import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Define the list of products
products = ["Golden Eagle", "Birra Peja", "Lasko", "B52", "VIPA", "DR GERARD", "PATOS", "DORITOS", "JANA", "SKOPSKO"]

# Create a date range for the last year
start_date = datetime.now() - timedelta(days= 365 * 2)
end_date = datetime.now()

# Generate date range without any time information
date_range = pd.date_range(start=start_date, end=end_date, freq='D').date

# Create an empty list to hold the sales data
sales_data_list = []

# Loop through each day in the date range and generate random sales data for each product
for date in date_range:
    for product in products:
        # Generate random sales data for each time of day
        for time in ["Mengjes", "Mesdite", "Mbremje"]:
            sales = random.randint(1, 50)
            sales_data_list.append({"Produkti": product, "KohaDites": time, "Shitjet": sales, "Data": date})

# Create a DataFrame from the list of dictionaries
sales_data = pd.DataFrame(sales_data_list)

# Save the sales data to a CSV file
sales_data.to_csv("seti.csv", index=False)
