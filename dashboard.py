# Import library
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

st.title('Proyek Analisis Data: Bike Sharing')

# Membaca dataset
all_df = pd.read_csv('df_cleaned.csv') 

# Membuat fungsi helper
def create_monthly_rent(df):
    monthly_rent = df.groupby(['yr','mnth'])['cnt'].sum().reset_index()
    return monthly_rent

def create_daily_rent(df):
    daily_rent = df.groupby('dteday')[['casual', 'registered']].sum().reset_index()
    return daily_rent

def create_hour_rent(df):
    hour_rent = df.groupby('hr')['cnt'].mean().reset_index()
    return hour_rent

# Membuat komponen filter
min_date = all_df['dteday'].min()
max_date = all_df['dteday'].max()

# Membuat sidebar
with st.sidebar:
    st.sidebar.header("Filter:")

    # Mengambil start date & end date dari date input
    start_date, end_date = st.date_input(
        label='Date Filter',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Untuk menyimpan nilai filter
main_df = all_df[(all_df['dteday'] >= str(start_date)) & 
                (all_df['dteday'] <= str(end_date))]

# Memanggil fungsi helper
monthly_rent = create_monthly_rent(main_df)
daily_rent = create_daily_rent(main_df)
hour_rent = create_hour_rent(main_df)

# Dashboard 1
st.subheader("Tren Penyewaan Sepeda Berdasarkan Bulan Pada 2011 dan 2012")
fig, ax = plt.subplots(figsize=(7, 5))
sns.lineplot(
    x='mnth',
    y='cnt',
    hue='yr',
    data=monthly_rent,
    marker="o",
    palette="Spectral")
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.legend(['2011', '2012'])
st.pyplot(fig)

# Dashboard 2
st.subheader("Tren Penyewaan Harian Sepeda Casual vs Registered")
fig2, ax = plt.subplots(figsize=(7, 5))
sns.lineplot(
    x='dteday',
    y='casual',
    label='casual',
    color='red',
    data=daily_rent)

sns.lineplot(
    x='dteday',
    y='registered',
    label='registered',
    color='blue',
    data=daily_rent)

plt.xlabel('Hari')
plt.ylabel('Jumlah Penyewaan')
plt.legend()
st.pyplot(fig2)

# Dashboard 3
st.subheader("Penyewaan Sepeda Berdasarkan Jam")
fig3 = px.line(hour_rent,
              x='hr',
              y='cnt',
              markers=True,
              title='').update_layout(xaxis_title='Jam', yaxis_title='Total Penyewaan')

st.plotly_chart(fig3)

st.caption('created by Shofura Tsabitah')




