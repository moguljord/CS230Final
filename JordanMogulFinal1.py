"""
CS230:      Section HB1
Name:       Jordan Mogul
Data:       Ride Share Data - file in program is named ridesharesample.csv
Description: Final Project
This program has three visualizations: a map, a bar chart, and a pie chart.
The map display drop off locations using latitude and longitude and filtered by pick up location and the car type.
The bar chart is a frequency counter of drop off locations filtered by the ride share company and distance.
The pie chart is a frequency counter of weather conditions during the ride filtered by temperature, pick up location, and the time.

I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
URL:       N/A
"""

# import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

RIDESHARE = 'ridesharesample.csv'
FILTERS = ('hour', 'source', 'destination', 'cab_type', 'name', 'price', 'distance', 'latitude', 'longitude', 'temperature', 'short_summary')
SMALL_SIZE = 8


def add_space():
    st.text(" ")
    st.text(" ")


def stats():
    df_mean = dfRideShare.mean(axis=0, numeric_only=True)
    df_median = dfRideShare.median(axis=0, numeric_only=True)
    st.write(f'The average distance is {df_mean["Distance"]:.2f} miles and the median is {df_median["Distance"]:.2f} miles.')
    st.write(f'The average price is ${df_mean["Price"]:.2f} and the median is ${df_median["Price"]:.2f}.')
    st.write(f'The median hour is {df_median["Hour"]:.0f}.')
    st.write(f'The average temperature is {df_mean["Temperature"]:.2f}℉ and the median is {df_median["Temperature"]:.2f}℉.')

    df_source_vc = dfRideShare['Source'].value_counts(ascending=True)
    st.write(f'The least used pick up location was {df_source_vc.index[0]} with {df_source_vc[0]} pick ups.')
    st.write(f'The most used pick up location was {df_source_vc.index[-1]} with {df_source_vc[-1]} pick ups.')


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)
    return my_autopct


def max_value(df_column, dtype):
    y = dtype(dfRideShare[df_column].max())
    return y


def min_value(df_column, dtype):
    x = dtype(dfRideShare[df_column].min())
    return x


def find_unique(df_column):
    z = dfRideShare[df_column].unique()
    return z


# setting font size for pie/bar chart
plt.rc('font', size=SMALL_SIZE)

# creating the initial dataframe
dfRideShare = pd.read_csv(RIDESHARE)
dfRideShare = dfRideShare.filter(FILTERS)

# changing column names
dfRideShare = dfRideShare.rename(columns={'temperature': 'Temperature', 'distance': 'Distance', 'price':'Price', 'name':'Car Type', 'hour': 'Hour', 'latitude': 'lat', 'longitude': 'lon', 'cab_type': 'Company', 'destination': 'Destination','source': 'Source', 'short_summary': 'Weather'})


# changing data types in the CSV file from str to float
dfRideShare['lat'] = dfRideShare['lat'].astype(float)
dfRideShare['lon'] = dfRideShare['lon'].astype(float)
dfRideShare['Price'] = dfRideShare['Price'].astype(float)

# rounding data for necessary columns
dfRideShare = dfRideShare.round({'Temperature': 0})
dfRideShare = dfRideShare.round({'Distance': 1})

# page settings
st.set_page_config(page_title='Jordan Mogul Final', page_icon='🌻', layout='centered')

# title
st.title('Jordan Mogul - Final Project')

# nav
st.sidebar.subheader('Select a Page')
page = st.sidebar.selectbox('', ('Home', 'Data', 'Map of Drop Off Locations', 'Bar Chart of Drop Off Locations', 'Pie Chart of Weather'))

# home page
if page == 'Home':

    st.header("About the Project")

    # setting two columns for this page
    col1, col2 = st.beta_columns(2)

    # col1 - text
    col1.write('This project was created by Jordan Mogul for CS230, Fall Semester 2020 using ride share data from Uber and Lyft in the Boston Area.')
    col1.write('The data set consists of 7000 rows with 57 columns. Columns include data such as pick up and drop off locations, date and time, distance of the ride, and weather.')
    col1.write("I applied a filter to select 11 columns that would be useful for me to work with. The filtered dataframe as well as some high level statistics can be viewed on the 'Data' Page. ")
    col1.write("From the filtered data, I created 3 different visualizations: a map, a bar chart, and a pie chart. These visualizations can be viewed on their respective pages.")

    # col2 - images
    col2.image(image='https://logos-world.net/wp-content/uploads/2020/05/Uber-Emblem.png', use_column_width=True)
    col2.image(image='https://cdn.freebiesupply.com/images/thumbs/2x/lyft-logo.png', use_column_width=True)

# data
elif page == 'Data':
    st.header('Data')

    # changing order of columns
    dfRideShare = dfRideShare[['Company', 'Car Type', 'Source', 'Destination', 'Distance', 'Price', 'Hour', 'Temperature', 'Weather', 'lat', 'lon']]

    st.write(dfRideShare)

    # putting the statistics into a collapsable container
    with st.beta_expander('Quick Statistics', False):
        stats()

# visualization 1: map of drop off
elif page == 'Map of Drop Off Locations':

    add_space()
    st.header('Visualization 1')
    st.sidebar.subheader('Filters')

    # select box: source
    source_options = find_unique('Source')
    source_map = st.sidebar.selectbox('Pick Up Location', source_options)

    # radio: type
    type_options = find_unique('Car Type')
    type_map = st.sidebar.radio("Type of Car", type_options)

    # applying filters for the map
    map_filter = dfRideShare[dfRideShare['Source'] == source_map]
    map_filter = map_filter[map_filter['Car Type'] == type_map]
    st.subheader('Map of Drop Off Locations by Pick Up Location and Car Type')

    # only create map if data is selected
    count_map = len(map_filter.index)
    if count_map != 0:
        st.map(map_filter)
    else:
        st.write('No Data Fits this Description')

# visualization 2: bar chart of destinations
elif page == 'Bar Chart of Drop Off Locations':

    add_space()
    st.header('Visualization 2')
    st.sidebar.subheader('Filters')

    # slider: distance
    min_distance = min_value('Distance', float)
    max_distance = max_value('Distance', float)
    distance = st.sidebar.slider('Ride Distance', min_distance, max_distance, (2.2, 5.7), step=.10)

    # multi select: uber or lyft
    company = st.sidebar.multiselect('Ride Share Company', ['Uber', 'Lyft'])

    # applying filters for the bar chart
    bar_filter = dfRideShare[dfRideShare['Distance'] <= distance[1]]
    bar_filter = bar_filter[bar_filter['Distance'] >= distance[0]]
    filter_company = bar_filter['Company'].isin(company)
    bar_filter = bar_filter[filter_company]
    st.subheader('Bar Chart of Drop Off Location by Ride Distance and Company')

    # only create bar chart if data is selected
    count_bar = len(bar_filter.index)
    if count_bar != 0:
        destination_freq = (bar_filter['Destination'].value_counts())
        destination_index = destination_freq.index.tolist()

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(destination_index, destination_freq, color='#9dcdcf')
        plt.xlabel('Drop Off Location')
        plt.ylabel('Number of Drop Offs')
        plt.xticks(rotation=70)
        plt.grid(axis='y')

        # adding column counts
        for index, data in enumerate(destination_freq):
            plt.text(x=index-0.2, y=data+2, s=f"{data}")

        st.pyplot(fig)
    else:
        st.write('No Data Fits this Description')

# visualization 3: pie chart of weather
elif page == 'Pie Chart of Weather':

    add_space()
    st.header('Visualization 3')
    st.sidebar.subheader('Filters')

    # number input: temperatures
    min_temp = min_value('Temperature', int)
    max_temp = max_value('Temperature', int)
    avg_temp = dfRideShare['Temperature'].median()
    temp = st.sidebar.number_input('Temperature (in Fahrenheit)', min_temp, max_temp, value=int(avg_temp), step=1)

    # multi select: source
    source_options = find_unique('Source')
    source_bar = st.sidebar.multiselect('Pick Up Locations', source_options)

    # slider: hour
    min_hour = min_value('Hour', int)
    max_hour = max_value('Hour', int)
    time = st.sidebar.slider('Hour', min_hour, max_hour, (6, 18), step=1)

    # applying filters for the pie chart
    pie_filter = dfRideShare[dfRideShare['Temperature'] == temp]
    pie_filter = pie_filter[pie_filter['Hour'] <= time[1]]
    pie_filter = pie_filter[pie_filter['Hour'] >= time[0]]
    filter_source = pie_filter['Source'].isin(source_bar)
    pie_filter = pie_filter[filter_source]
    st.subheader('Pie Chart of Weather by Temperature, Hour, and Pick Up Location')

    # only displays the pie chart if there are rows available in the DF
    count_pie = len(pie_filter.index)
    if count_pie != 0:
        weather_freq = 100*(pie_filter['Weather'].value_counts(normalize=True))
        weather_index = weather_freq.index.tolist()

        # making the pie chart look nice
        wp = {'linewidth': 0.5, 'edgecolor': 'black'}

        # displaying the pie chart
        fig, ax = plt.subplots()
        ax.pie(weather_freq, labels=weather_index, wedgeprops=wp, autopct=make_autopct(weather_freq))
        ax.legend(weather_index, title='Weather', loc='center left', bbox_to_anchor=(1.05, 1))
        st.pyplot(fig)
    else:
        st.write('No Data Fits this Description')
