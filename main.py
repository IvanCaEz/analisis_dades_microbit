import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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
        plt.title('Interval {}'.format(interval['interval'].iloc[0])) # Automatically gets the interval number
        # Plot all data except Time and sample-id
        plt.plot(interval.loc[:, ~interval.columns.isin(['Time (seconds)', 'sample-id'])])
        plt.xlabel('Sample ID')
        plt.ylabel('Values')
        plt.legend(interval.loc[:, ~interval.columns.isin(['Time (seconds)', 'sample-id'])])
        plt.get_current_fig_manager().window.state('zoomed')
        plt.savefig('charts/plot_alldata{}.png'.format(interval['interval'].iloc[0]), dpi=200)
        plt.show()
    

def historic_temperatura(list_of_intervals: list):
    # Convert the seconds to minutes to make the plot more readable
    plt.scatter(list_of_intervals[0]['Time (seconds)']/60, list_of_intervals[0]['temp'], color='pink')
    plt.scatter(list_of_intervals[1]['Time (seconds)']/60, list_of_intervals[1]['temp'], color='orange')
    plt.scatter(list_of_intervals[2]['Time (seconds)']/60, list_of_intervals[2]['temp'], color='green')

    # Set the ticks of the y axis to be more readable
    plt.yticks(np.arange(24, 35, 1))        
    plt.ylabel('Temperature (ºC)')
    plt.suptitle('Temperature over time')
    plt.xlabel('Time (minutes)')
    plt.xticks(np.arange(0, 240, 15))
    plt.legend(['Interval 1', 'Interval 2', 'Interval 3'])
    plt.grid(True)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/scatter_temperature.png', bbox_inches ="tight", dpi=200)

    plt.show()

        
def historic_light(list_of_intervals: list):
    fig, axs = plt.subplots(len(list_of_intervals), 1)
    bins = np.linspace(0, 300, 3) 
    labels = ['Dark', 'Light']
    
    for i, interval in enumerate(list_of_intervals):
        
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        
        binned = pd.cut(interval['light'], bins=bins, labels=labels, right=False)  # Set right=False to include the rightmost edge
        # Count the number of values in each bin
        counts = binned.value_counts()
        # Remove the labels that are 0%
        counts = counts[counts != 0]
        # Plot the bar chart
        axs[i].barh(counts.index, counts, edgecolor='black', color='yellow')  # Swap the arguments for barh
    
    
    axs[1].set_ylabel('Light level (lux)')
    fig.suptitle('Light level')
    plt.xlabel('Nº of measurements')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.subplots_adjust(hspace=0.55)
    plt.savefig('charts/barh_light.png', bbox_inches ="tight", dpi=200)
    plt.show()
    
    
def historic_sound(list_of_intervals: list):
    fig, axs = plt.subplots(1, len(list_of_intervals), sharex=True)
    for i, interval in enumerate(list_of_intervals):
        
        axs[i].hist(interval['sound-level'], color='gray', edgecolor='black')
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        axs[i].set_xticks(np.arange(0, 220, 20))
    
    axs[1].set_xlabel('Sound level (dB)')
    axs[0].set_ylabel('Nº of measurements')
    fig.suptitle('Sound level')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/hist_sound_level.png', bbox_inches ="tight", dpi=200)
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
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        centre_circle = plt.Circle((0, 0), 0.65, fc='white')
        axs[i].add_artist(centre_circle)
    
    fig.suptitle('Compass heading')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/pie_compass_heading.png', dpi=200)
    plt.show()

       
def print_menu():
    print('Select the data you want to see:')
    print('1. All data')
    print('2. Temperature')
    print('3. Light')
    print('4. Sound level')
    print('5. Accelerometer')
    print('6. Compass heading')
    print('7. Exit')
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
        elif option == 4:
            historic_sound(list_of_intervals)
        elif option == 6:
            historic_compass_heading(list_of_intervals)
        elif option == 7:
            print('Exiting...')
            break
        else:
            pass
        
menu()

