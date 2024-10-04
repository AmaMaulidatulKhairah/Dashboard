import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

st.title("Bike Rental Analysis Dashboard")


all_df = pd.read_csv('all_data.csv')

hourly_rentals = all_df.groupby('hr')['cnt_y'].sum().reset_index()

peak_hours = hourly_rentals.sort_values(by='cnt_y', ascending=False)

## Display the peak hours
st.write("Peak Hours for Bike Rentals:")
st.write(peak_hours)

# Visualization
plt.figure(figsize=(10, 6))
plt.bar(peak_hours['hr'], peak_hours['cnt_y'], color='skyblue')
plt.title('Total Bike Rentals by Hour', fontsize=20)
plt.xlabel('Hour of the Day')
plt.ylabel('Total Rentals')
plt.xticks(range(0, 24))  
plt.grid(axis='y')
st.pyplot(plt)

## Display Average Bike Rentals on Weekdays vs. Weekends
plt.figure(figsize=(10, 6))

average_rentals = all_df.groupby('is_weekend')['cnt_y'].mean()

plt.bar(['Weekday', 'Weekend'], average_rentals.values)

# Set plot title and labels
plt.title('Average Bike Rentals on Weekdays vs Weekends', fontsize=20)
plt.xlabel('Day Type')
plt.ylabel('Average Bike Rentals')

st.pyplot(plt)

##Display Average Bike Rentals on Weekdays vs. Weekends by hour
plt.figure(figsize=(10, 6))
weekend_df = all_df[all_df['weekday_x'].isin([6, 0])]
weekday_df = all_df[~all_df['weekday_x'].isin([6, 0])]

# Calculate the average number of bicycle rentals per hour for weekends and weekdays
avg_weekend_rentals = weekend_df.groupby('hr')['cnt_y'].mean()
avg_weekday_rentals = weekday_df.groupby('hr')['cnt_y'].mean()

# Plot using Matplotlib
plt.figure(figsize=(10, 6))
plt.plot(avg_weekend_rentals.index, avg_weekend_rentals.values, label='Weekend')
plt.plot(avg_weekday_rentals.index, avg_weekday_rentals.values, label='Weekday')

# Add title, labels, and legend to the chart
plt.title('Average Bike Rentals by Hour: Weekend vs Weekday', fontsize=20)
plt.xlabel('Hour of the Day')
plt.ylabel('Average Bike Rentals')

st.pyplot(plt)

## Display Temperature vs Bike Rentals
plt.figure(figsize=(10, 6))

average_rentals = all_df.groupby('temp_x')['cnt_y'].mean()
plt.plot(average_rentals.index, average_rentals.values)

plt.title('Average Effect of Temperature on the Number of Bicycle Rentals', fontsize=20)
plt.xlabel('Temperature')
plt.ylabel('Bike Rentals')
st.pyplot(plt)


##Display Analisis Lanjutan
all_df['dteday'] = pd.to_datetime(all_df['dteday'])  
all_df['Recency'] = (all_df['dteday'].max() - all_df['dteday']).dt.days

# Frequency (jumlah penyewaan per hari) -> Gunakan kolom 'cnt'
all_df['Frequency'] = all_df['cnt_y']

# Monetary -> Gunakan kolom 'cnt'
all_df['Monetary'] = all_df['cnt_y']

# Membuat label kuantil untuk R, F, M
r_labels = range(4, 0, -1)
f_labels = range(1, 5)
m_labels = range(1, 5)

all_df['R'] = pd.qcut(all_df['Recency'], q=4, labels=r_labels)
all_df['F'] = pd.qcut(all_df['Frequency'], q=4, labels=f_labels)
all_df['M'] = pd.qcut(all_df['Monetary'], q=4, labels=m_labels)

# Gabungkan skor RFM menjadi satu kolom
all_df['RFM_Score'] = all_df['R'].astype(str) + all_df['F'].astype(str) + all_df['M'].astype(str)

# Berdasarkan RFM_Score, beri label segmentasi
def segment_rfm(score):
    if score in ['444', '443', '434', '433', '344', '343', '334', '333']:
        return 'Best Day'
    elif score in ['422', '421', '412', '411', '322', '321', '312', '311', 
                   '244', '243', '234', '233', '224', '223', '214', '213']:
        return 'Normal Day'
    else:
        return 'Worst Day'

all_df['RFM_Segment'] = all_df['RFM_Score'].apply(segment_rfm)

# Analisis karakteristik setiap segmen RFM
rfm_segment_summary = all_df.groupby('RFM_Segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).reset_index()

# Tampilkan data RFM Segment Summary di Streamlit
st.title("RFM Segment Summary")

# Tampilkan tabel segmentasi
st.write("opportunities to improve business performance")
st.dataframe(rfm_segment_summary)


with st.sidebar:
    
    st.header('BIKE RENTALS HORIZON')
    
    values = st.image("5-53679_jersey-vector-sepeda-gambar-sepeda-ontel-vector-hd.png")