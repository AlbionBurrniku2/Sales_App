import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import plotly.graph_objs as go

# Function to preprocess the data
def preprocess_data(df):
    df['KohaDites'] = df['KohaDites'].map({'Mengjes': '08:00-12:00', 'Mesdite': '13:00-17:00', 'Mbremje': '18:00-22:00'})
    return df

# Function to train the model
def train_model(df):
    X = pd.DataFrame(df['Data'])
    y = pd.DataFrame(df['Shitjet'])

    regressor = DecisionTreeRegressor(random_state=0)
    regressor.fit(X, y)
    return regressor

# Function to display sales over time of day
def display_sales_over_time(df, selected_product, selected_year):
    selected_product_data = df[(df['Produkti'] == selected_product) & (df['Data'].dt.year == int(selected_year))]
    grouped_data_koha = selected_product_data.groupby(['KohaDites'], as_index=False)['Shitjet'].sum()

    koha_fig = go.Figure()
    koha_fig.add_trace(go.Bar(x=grouped_data_koha['KohaDites'], y=grouped_data_koha['Shitjet']))
    koha_fig.update_layout(title=f'Sales Prediction over Time of Day for {selected_product} in {selected_year}')
    st.plotly_chart(koha_fig)

# Function to display sales over months
def display_sales_over_months(df, selected_product, selected_year):
    selected_product_data = df[(df['Produkti'] == selected_product) & (df['Data'].dt.year == int(selected_year))]
    grouped_data_month = selected_product_data.groupby(['Data'], as_index=False)['Shitjet'].sum()
    best_month = grouped_data_month.loc[grouped_data_month['Shitjet'].idxmax(), 'Data'].strftime('%B')

    month_fig = go.Figure()
    month_fig.add_trace(go.Bar(x=grouped_data_month['Data'], y=grouped_data_month['Shitjet']))
    month_fig.update_layout(title=f'Sales Prediction over Months for {selected_product} in {selected_year}')
    st.plotly_chart(month_fig)

    st.write(f"The month with the highest sales for {selected_product} is {best_month}")

# Main function
def main():
    st.title("Sales Prediction of Products")
    st.write("Dataset duhet te permbaj keto kolona: Produkti, KohaDites, Shitjet dhe Data")
    st.write("\n \n Ndersa KohaDites duhet te permbaj ne vete kohet si: Mengjes, Mesdite dhe Mbremje")
    # File uploader widget
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the dataset
        df = pd.read_csv(uploaded_file, parse_dates=['Data'])

        # Preprocess the data
        df = preprocess_data(df)

        # Sidebar - Product selection
        st.sidebar.header('Select a Product')
        product_names = df['Produkti'].unique()
        selected_product = st.sidebar.selectbox('Select a product', product_names)

        # Sidebar - Year selection
        st.sidebar.header('Select a Year')
        years = df['Data'].dt.year.unique().astype(str)
        selected_year = st.sidebar.selectbox('Select a year', years)

        # Display sales over time of day
        display_sales_over_time(df, selected_product, selected_year)

        # Display sales over months
        display_sales_over_months(df, selected_product, selected_year)

# Call the main function
if __name__ == "__main__":
    main()
