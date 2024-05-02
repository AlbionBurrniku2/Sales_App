import streamlit as st
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import plotly.graph_objs as go

# Leximi i datasetit pra leximi i te dhenave qe ne kemi
df = pd.read_csv("dataset_streamlit.csv", parse_dates=['Data'])

#Vendosja e titullit per aplikacionin tone
st.title("Parashikimi i shitjeve te produkteve")

# Sidebar- Zgjedhja e produktit qe ne duam te shohim
st.sidebar.header('Zgjidhni produktin')
product_names = df['Produkti'].unique()
selected_product = st.sidebar.selectbox('Zgjidhni një produkt', product_names)

# Sidebar - Zgjedhja e vitit qe ne duam nga 2021-2023
st.sidebar.header('Zgjidhni vitin')
years = ['2021', '2022', '2023']
selected_year = st.sidebar.selectbox('Zgjidhni një vit', years)

# Filtro të dhënat sipas produktit dhe vitit
selected_product_data = df[(df['Produkti'] == selected_product) & (df['Data'].dt.year == int(selected_year))]

# Konvertoni KohaDites në kohë
selected_product_data['KohaDites'] = selected_product_data['KohaDites'].map({'Mengjes': '08:00-12:00', 'Mesdite': '13:00-17:00', 'Mbremje': '18:00-22:00'})

# Grupimi i te dhenave per KohaDites
grouped_data_koha = selected_product_data.groupby(['KohaDites'], as_index=False)['Shitjet'].sum()

# Shfaqja e plot/char per KohaDites
koha_fig = go.Figure()
koha_fig.add_trace(go.Bar(x=grouped_data_koha['KohaDites'], y=grouped_data_koha['Shitjet']))
koha_fig.update_layout(title=f'Parashikimi i shitjeve per kohen e dites per produktin: {selected_product} ne vitin:    {selected_year}')
st.plotly_chart(koha_fig)

# Grupimi i te dhenave per muaj
grouped_data_month = selected_product_data.groupby(['Data'], as_index=False)['Shitjet'].sum()

# Me e gjet ne cilin muaj produkti i caktuar ka pasur shitjen me te mire
best_month = grouped_data_month.loc[grouped_data_month['Shitjet'].idxmax(), 'Data']

# Shfaqja e plot/char per muajin
month_fig = go.Figure()
month_fig.add_trace(go.Bar(x=grouped_data_month['Data'], y=grouped_data_month['Shitjet']))
month_fig.update_layout(title=f'Parashikimi i shitjeve per muajin e vitit per produktin:  {selected_product} ne vitin:    {selected_year}')
st.plotly_chart(month_fig)

st.write(f"Muaji me me se shumti shitje per produktin:  {selected_product} eshte    {best_month}")

# Perdorimi i modelit Decision Tree
X = pd.DataFrame(selected_product_data['Data'])
y = pd.DataFrame(selected_product_data['Shitjet'])

regressor = DecisionTreeRegressor(random_state=0)
regressor.fit(X, y)

