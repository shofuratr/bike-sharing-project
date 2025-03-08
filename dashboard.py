# Import library
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title='Bike Sharing Dashboard - Shofura')

st.title('Bike Sharing Dashboard :bar_chart:')

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

def create_wind_rent(df):
   wind_rent = df.groupby('wind_cluster')['cnt'].sum().reset_index()
   return wind_rent

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
wind_rent = create_wind_rent(main_df)

col1, col2, col3 = st.columns(3)

with col1:
    total_user = main_df['cnt'].sum()
    st.metric("Total All User", value=total_user)
with col2:
    total_casual = main_df['casual'].sum()
    st.metric("Total Casual User", value=total_casual)
with col3:
    total_registered = main_df['registered'].sum()
    st.metric("Total Registered User", value=total_registered)

# Dashboard 1
st.subheader("Bagaimana tren penyewaan sepeda tiap bulannya pada tahun 2011 dan 2012?")
fig1 = px.line(monthly_rent,
               x='mnth',
               y='cnt',
               line_group='yr',
               color='yr',
               markers=True,
               title="Tren Penyewaan Sepeda Berdasarkan Bulan Pada 2011 dan 2012").update_layout(xaxis_title='Bulan', yaxis_title='Jumlah Penyewaan')
st.plotly_chart(fig1)

# Dashboard 2
st.subheader("Bagaimana perbandingan sewa sepeda pengguna casual vs registered pada tiap harinya?")
fig2 = px.line(daily_rent,
               x='dteday',
               y=['casual','registered'],
               title='Tren Penyewaan Harian Sepeda Casual vs Registered').update_layout(xaxis_title='Hari', yaxis_title='Jumlah Penyewaan')
st.plotly_chart(fig2)

# Dashboard 3
st.subheader("Bagaimana tren penyewaan sepeda berdasarkan jam?")
fig3 = px.line(hour_rent,
              x='hr',
              y='cnt',
              markers=True,
              title='Penyewaan Sepeda Berdasarkan Jam').update_layout(xaxis_title='Jam', yaxis_title='Total Penyewaan')

st.plotly_chart(fig3)

# Dashboard 4
st.subheader("Analisis Lanjutan : Windspeed Clustering")

def wind_cluster(windspeed):
  if windspeed < 0.3:
    return 'Ringan'
  elif windspeed < 0.6:
    return 'Sedang'
  else:
    return 'Kuat'

all_df['wind_cluster'] = all_df['windspeed'].apply(wind_cluster)

fig3 = px.bar(wind_rent,
              x='wind_cluster',
              y='cnt',
              color='wind_cluster',
              color_discrete_map={'Kuat':'red','Ringan':'green','Sedang':'blue'},
              title='Penyewaan Sepeda Berdasarkan Kecepatan Angin').update_layout(xaxis_title='Kategori Angin', yaxis_title='Jumlah Penyewaan')
st.plotly_chart(fig3)

st.caption('created by Shofura Tsabitah')




