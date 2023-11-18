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

print(plt.style.available)

def all_data(list_of_intervals: list):
    plt.style.use('fivethirtyeight')
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
    
def historic_temperature(list_of_intervals: list):
    # Convert the seconds to minutes to make the plot more readable
    plt.style.use('fivethirtyeight')

    plt.scatter(list_of_intervals[0]['Time (seconds)']/60, list_of_intervals[0]['temp'], color='pink', edgecolor='black')
    plt.scatter(list_of_intervals[1]['Time (seconds)']/60, list_of_intervals[1]['temp'], color='orange', edgecolor='black')
    plt.scatter(list_of_intervals[2]['Time (seconds)']/60, list_of_intervals[2]['temp'], color='green', edgecolor='black')
    # Set the ticks of the y axis to be more readable
    plt.yticks(np.arange(24, 35, 1))        
    plt.ylabel('Temperature (ºC)')
    plt.suptitle('Temperature over time', fontsize=16)
    plt.xlabel('Time (minutes)')
    plt.xticks(np.arange(0, 240, 15))
    plt.legend(['Interval 1', 'Interval 2', 'Interval 3'])
    plt.grid(True)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/scatter_temperature.png', bbox_inches ="tight", dpi=200)
    plt.show()
    
def historic_light(list_of_intervals: list):
    plt.style.use('fivethirtyeight')
    fig, axs = plt.subplots(len(list_of_intervals), 1)
    bins = np.linspace(0, 300, 3) 
    labels = ['Dark', 'Light']
    colors = ['#6a5acd', '#ffc61a']
    
    for i, interval in enumerate(list_of_intervals):
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        binned = pd.cut(interval['light'], bins=bins, labels=labels,  right=False)  # Set right=False to include the rightmost edge
        # Count the number of values in each bin
        counts = binned.value_counts()
        # Remove the labels that are 0%
        counts = counts[counts != 0]   
        axs[i].barh(counts.index, counts, color=colors, edgecolor='black') 
        # Calculate the percentage for each bin
        percentages = counts / counts.sum() * 100
        # Add percentage labels to the bars
        for j, (count, percentage) in enumerate(zip(counts, percentages)):
            axs[i].text(count, j, f' {percentage:.1f}%', va='center')
    
    axs[1].set_ylabel('Light level (lux)')
    fig.suptitle('Light level', fontsize=16)
    plt.xlabel('Nº of measurements')
    plt.get_current_fig_manager().window.state('zoomed')
    plt.subplots_adjust(hspace=0.55)
    plt.savefig('charts/barh_light.png', bbox_inches ="tight", dpi=200)
    plt.show()
     
def historic_sound(list_of_intervals: list):
    plt.style.use('fivethirtyeight')

    fig, axs = plt.subplots(1, len(list_of_intervals), sharex=True)
    for i, interval in enumerate(list_of_intervals):
        
        axs[i].hist(interval['sound-level'], color='gray', edgecolor='black')
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        axs[i].set_xticks(np.arange(0, 220, 20))
        axs[i].axvline(x=70, color='red', label='Threshold')
        axs[i].axvline(x=interval['sound-level'].mean(), color='orange', label='Mean')
        
    plt.legend()
    axs[1].set_xlabel('Sound level (dB)')
    axs[0].set_ylabel('Nº of measurements')
    fig.suptitle('Sound level', fontsize=16)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/hist_sound_level.png', bbox_inches ="tight", dpi=200)
    plt.show()
    
def historic_acceleration(list_of_intervals: list):
    plt.style.use('fivethirtyeight')
    fig, axs = plt.subplots(len(list_of_intervals), 1)
    for i, interval in enumerate(list_of_intervals):
        axs[i].plot(interval['sample-id'], interval['acc-x'], color='#ff3333', label='X')  
        axs[i].plot(interval['sample-id'], interval['acc-y'], color='#a64dff', label='Y')  
        axs[i].plot(interval['sample-id'], interval['acc-z'], color='#33cccc', label='Z')
    
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))
        axs[i].set_yticks(np.arange(-2050, 2500, 500))
        
        # Annotate maximum and minimum values
        # First define the coordinates of the values
        max_x = interval['sample-id'][interval['acc-x'].idxmax()]
        max_y = interval['sample-id'][interval['acc-y'].idxmax()]
        max_z = interval['sample-id'][interval['acc-z'].idxmax()]
        min_x = interval['sample-id'][interval['acc-x'].idxmin()]
        min_y = interval['sample-id'][interval['acc-y'].idxmin()]
        min_z = interval['sample-id'][interval['acc-z'].idxmin()]
        # Annotate the values
        axs[i].annotate(f'Max: {interval['acc-x'].max()}', xy=(max_x, interval['acc-x'].max()), xytext=(max_x, interval['acc-x'].max() + 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
        axs[i].annotate(f'Max: {interval['acc-y'].max()}', xy=(max_y, interval['acc-y'].max()), xytext=(max_y, interval['acc-y'].max() + 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
        axs[i].annotate(f'Max: {interval['acc-z'].max()}', xy=(max_z, interval['acc-z'].max()), xytext=(max_z, interval['acc-z'].max() + 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
        axs[i].annotate(f'Min: {interval['acc-x'].min()}', xy=(min_x, interval['acc-x'].min()), xytext=(min_x, interval['acc-x'].min() - 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
        axs[i].annotate(f'Min: {interval['acc-y'].min()}', xy=(min_y, interval['acc-y'].min()), xytext=(min_y, interval['acc-y'].min() - 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
        axs[i].annotate(f'Min: {interval['acc-z'].min()}', xy=(min_z, interval['acc-z'].min()), xytext=(min_z, interval['acc-z'].min() - 750),
                        arrowprops=dict(facecolor='black', arrowstyle='simple'))
    
    plt.legend()
    axs[1].set_ylabel('Acceleration (mg)')
    plt.xlabel('Nº of measurements')
    fig.suptitle('Acceleration or deceleration', fontsize=16)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.subplots_adjust(hspace=0.55)
    plt.savefig('charts/plot_accel.png', bbox_inches ="tight", dpi=200)
    plt.show()
        

def historic_compass_heading(list_of_intervals: list):
    fig, axs = plt.subplots(1, len(list_of_intervals))
    labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # We need to divide the compass heading values into 8 bins
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
    
def correlations(list_of_intervals: list):
    fig, axs = plt.subplots(1, len(list_of_intervals), figsize=(8, 5))
    
    for i, interval in enumerate(list_of_intervals):
        corr_matrix = interval.corr()
        # We need to exclude the last row and column for getting rid of the blank space
        corr_matrix = corr_matrix.iloc[:-1, :-1]  
        im = axs[i].matshow(corr_matrix, cmap='coolwarm')
        cb = plt.colorbar(im, ax=axs[i])
        axs[i].set_title('Interval {}'.format(interval['interval'].iloc[0]))

    fig.suptitle('Correlation Heatmap', fontsize=16)
    plt.subplots_adjust(wspace=0.45)
    plt.get_current_fig_manager().window.state('zoomed')
    plt.savefig('charts/correlation_heatmap.png', dpi=200)
    plt.show()
    
def print_menu():
    print('Select the data you want to see:')
    print('1. All data')
    print('2. Temperature')
    print('3. Light')
    print('4. Sound level')
    print('5. Accelerometer')
    print('6. Compass heading')
    print('7. Correlation matrix')
    print('8. Exit')
    try: 
        return int(input('Option: '))
    except ValueError:
        print('Please enter a number')
        return print_menu()

def menu():
    while True:
        option = print_menu()
        if option == 1:
            all_data(list_of_intervals)
        elif option == 2:
            historic_temperature(list_of_intervals)
        elif option == 3:
            historic_light(list_of_intervals)
        elif option == 4:
            historic_sound(list_of_intervals)
        elif option == 5:
            historic_acceleration(list_of_intervals)
        elif option == 6:
            historic_compass_heading(list_of_intervals)
        elif option == 7:
            correlations(list_of_intervals)
        elif option == 8:
            print('Exiting...')
            break
        else:
            pass
        
menu()

