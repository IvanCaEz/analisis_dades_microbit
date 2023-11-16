import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def get_data() -> pd.DataFrame:
    # Read data from CSV file and make a dataframe using pandas
    dataframe = pd.read_csv('data/microbit_sensor.csv')
    # Each reset of the sample-id means a new measurements so I will treat as a new interval
    # I will use the cumsum function to count the number of measurements
    dataframe['interval'] = (dataframe['sample-id'] == 0).cumsum()
    # Now I can group the data by measurement and return the grouped object to make the plots
    data_by_interval = dataframe.groupby('interval')
    # Get the number of intervals by counting the number of groups
    print(data_by_interval.ngroups)
    return data_by_interval

data_by_interval = get_data()
# Get the intervals as dataframes
first_interval = data_by_interval.get_group(1)
second_interval = data_by_interval.get_group(2)
third_interval = data_by_interval.get_group(3)
# Make a list of intervals
list_of_intervals = [first_interval, second_interval, third_interval]


def all_data(list_of_intervals: list):
    for interval in list_of_intervals:
        plt.title('interval {}'.format(interval['interval'].iloc[0])) # Automatically gets the interval number
        # Plot all data except Time and sample-id
        plt.plot(interval.loc[:, ~interval.columns.isin(['Time (seconds)', 'sample-id'])])
        plt.xlabel('Sample ID')
        plt.ylabel('Values')
        plt.legend(interval.loc[:, ~interval.columns.isin(['Time (seconds)', 'sample-id'])])
        plt.show()
    

def correlations(data: pd.DataFrame):
    print(data.corr())
    

def historic_temperatura(list_of_intervals: list):
    fig, axs = plt.subplots(len(list_of_intervals), 1)
    for i, interval in enumerate(list_of_intervals):
        axs[i].set_title('interval {}'.format(interval['interval'].iloc[0])) # Automatically gets the interval number 
        # Convert the seconds to hours to make the plot more readable
        axs[i].scatter(interval['Time (seconds)']/3600, interval['temp'], label='Temperature', color='orange')
        # Set the ticks of the y axis to be more readable
        axs[i].set_yticks(np.arange(interval['temp'].min(), interval['temp'].max()+1, 1))
        
    axs[1].set_ylabel('Temperature (ºC)')
    fig.suptitle('Temperature over time')
    plt.xlabel('Time (hours)')
    plt.show()
        
def historic_light(list_of_intervals: list):
    fig, axs = plt.subplots(len(list_of_intervals), 1)
    for i, interval in enumerate(list_of_intervals):

        axs[i].plot(interval['Time (seconds)']/3600, interval['light'], label='Light', marker='o', color='green')
        axs[i].set_title('interval {}'.format(interval['interval'].iloc[0]))
    
    axs[1].set_ylabel('Light')
    fig.suptitle('Ligth over time')
    plt.xlabel('Time (hours)')
    plt.show()
        

def historic_compass_heading(list_of_intervals: list):
    fig, axs = plt.subplots(1, len(list_of_intervals))
    labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # Divide the compass heading values into 8 bins
    # The first bin is from -22.5 to 22.5 degrees so it will be labeled as N and we will start from there
    bins = np.linspace(-22.5, 360-22.5, 9)
    for i, interval in enumerate(list_of_intervals):
        # Use pandas.cut to bin the compass heading values
        binned = pd.cut(interval['compass-heading'], bins=bins, labels=labels)
        # Count the number of values in each bin
        counts = binned.value_counts()
        # Remove the labels that are 0%
        counts = counts[counts != 0]
        # Plot the pie chart
        axs[i].pie(counts, labels=counts.index, autopct='%1.1f%%', pctdistance=0.8)
        axs[i].set_title('interval {}'.format(interval['interval'].iloc[0]))
        centre_circle = plt.Circle((0, 0), 0.65, fc='white')
        axs[i].add_artist(centre_circle)
    
    

    fig.suptitle('Compass heading')
    plt.show()

       
def print_menu():
    print('Select the data you want to see:')
    print('1. All data')
    print('2. Temperature')
    print('3. Light')
    print('4. Compass heading')

    print('9. Exit')
    return int(input('Option: '))

def menu():
    while True:
        option = print_menu()
        if option == 1:
            all_data(list_of_intervals)
        elif option == 2:
            historic_temperatura(list_of_intervals)
        elif option == 3:
            historic_light(list_of_intervals)
        elif option == 8:
            historic_compass_heading(list_of_intervals)
        elif option == 9:
            print('Exiting...')
            break
        else:
            pass
        
historic_compass_heading(list_of_intervals)

