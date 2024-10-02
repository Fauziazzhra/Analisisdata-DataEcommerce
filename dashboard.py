# dashboard.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Mengatur tema seaborn
sns.set_theme(style="whitegrid")

# Memuat data
orders = pd.read_csv('all_data.csv')
order_payments = pd.read_csv('all_data.csv')

# Menambahkan kolom waktu tambahan
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['year'] = orders['order_purchase_timestamp'].dt.year
orders['month'] = orders['order_purchase_timestamp'].dt.month
orders['day_of_week'] = orders['order_purchase_timestamp'].dt.day_name()

# Judul Dashboard
st.title("Dashboard Analisis Pembelian E-Commerce")

# Kalender Tangga untuk Memilih Rentang Tanggal
st.subheader("Pilih Rentang Tanggal")
start_date = st.date_input("Mulai Tanggal", orders['order_purchase_timestamp'].min())
end_date = st.date_input("Akhir Tanggal", orders['order_purchase_timestamp'].max())

# Filter data berdasarkan rentang tanggal yang dipilih
filtered_orders = orders[(orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) & 
                         (orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))]

# Menghitung total pembelian per metode pembayaran
total_payment_value = order_payments.groupby('payment_type')['payment_value'].sum().reset_index()

# Visualisasi total pembelian berdasarkan metode pembayaran
st.subheader('Total Pembelian berdasarkan Metode Pembayaran')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='payment_value', y='payment_type', data=total_payment_value, palette='pastel', ax=ax)
ax.set_title('Total Pembelian berdasarkan Metode Pembayaran')
ax.set_xlabel('Total Pembelian (IDR)')
ax.set_ylabel('Metode Pembayaran')
st.pyplot(fig)

# Menghitung jumlah pembelian per bulan berdasarkan rentang tanggal yang dipilih
monthly_sales = filtered_orders.groupby('month').size().reset_index(name='sales_count')

# Visualisasi jumlah pembelian per bulan
st.subheader('Jumlah Pembelian per Bulan')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='month', y='sales_count', data=monthly_sales, palette='pastel', ax=ax)
ax.set_title('Jumlah Pembelian per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Pembelian')
ax.set_xticks(range(12))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig)

# Menghitung jumlah pembelian per hari dalam seminggu berdasarkan rentang tanggal yang dipilih
weekly_sales = filtered_orders.groupby('day_of_week').size().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
).reset_index(name='sales_count')

# Visualisasi jumlah pembelian per hari dalam seminggu
st.subheader('Jumlah Pembelian per Hari dalam Seminggu')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='day_of_week', y='sales_count', data=weekly_sales, palette='pastel', ax=ax)
ax.set_title('Jumlah Pembelian per Hari dalam Seminggu')
ax.set_xlabel('Hari dalam Seminggu')
ax.set_ylabel('Jumlah Pembelian')
st.pyplot(fig)

# Menghitung jumlah pembelian per tahun berdasarkan rentang tanggal yang dipilih
yearly_sales = filtered_orders.groupby('year').size().reset_index(name='sales_count')

# Visualisasi tren pembelian tahunan
st.subheader('Tren Pembelian Tahunan')
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='year', y='sales_count', data=yearly_sales, marker='o', ax=ax)
ax.set_title('Tren Pembelian Tahunan')
ax.set_xlabel('Tahun')
ax.set_ylabel('Jumlah Pembelian')
ax.set_xticks(yearly_sales['year'])
st.pyplot(fig)
