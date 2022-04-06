import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = (input("Please enter the city name: ")).lower()
    # Checking if the user inputted the right city
    while city not in CITY_DATA:
        print("Try again.")
        city = (input("Please enter the city name: ")).lower()


    # get user input for month (all, january, february, ... , june)
    months_and_all = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    month = (input("Please enter the month or all for no month filter: ")).lower()
    while month not in months_and_all:
        month = (input("Please enter the month or all for no month filter: ")).lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_and_all = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    day = (input("Please enter the day or all for no day filter: ")).lower()
    while day not in days_and_all:
        day = (input("Please enter the day or all for no day filter: ")).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day): # Copied this from Practice Problem #3
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    # display the most common month
    # print(df['month'].isnull().sum().sum())
    common_month = df['month'].mode().at[0]
    print("This is the common month: ", common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode().at[0]
    print("This is the common day: ", common_day)

    # display the most common start hour
    common_start_time = pd.to_datetime(df['Start Time'].mode().at[0])
    common_hour = common_start_time.hour
    print("This is the common hour: ", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode().at[0]
    print("This is the popular Start Station: ", common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode().at[0]
    print("This is the popular End Station: ", common_end_station)

    # display most frequent combination of start station and end station trip

    # Creating a list of combination of start and end stations
    index = df['Start Station'].index
    data = [(df['Start Station'].at[i], df['End Station'].at[i]) for i in index]
    combo_station = pd.Series(data, index)

    # Getting the popular start and end station and displaying the results
    common_combo_station = combo_station.mode().at[0]
    print("The frequent combination of start station and end station trip: {0} and {1}".format(common_combo_station[0], common_combo_station[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].dropna(axis = 0).sum() # Filtered any NaN data in the column
    print("This is the total travel time:", round(total_time/60,1), "minutes.")

    # display mean travel time
    avg_time = total_time/df['Trip Duration'].dropna(axis = 0).size
    print("This is the average travel time:", round(avg_time/60,1), "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    try:
        # Display counts of user types
        if df['User Type'].isnull().sum():
            user_type = df['User Type'].value_counts()
            print("This is the user count:\n", user_type.to_string())
        else:
            print("User Type information is not available")

    except KeyError:
        print("User Type information is not available")

    try:

        # Checking if there is a NaN value
        if df['Gender'].isnull().sum():
            gender = df['Gender'].value_counts()
            print("This is the gender count:\n", gender.to_string())
        else:
            print("Gender information is not available")


    except KeyError:
        print("Gender information is not available")

    try:
        if df['Birth Year'].isnull().sum():
            early_birth_year = df['Birth Year'].min()
            print("The earliest birth year:", np.int64(early_birth_year))

            # Getting latest year
            recent_birth_year = df['Birth Year'].max()
            print("The recent birth year:", np.int64(recent_birth_year))

            # Getting common year
            common_birth_year = df['Birth Year'].mode().at[0]
            print("This is the common birth year:", np.int64(common_birth_year))
        else:
            print("Birth Year information is not available")
    except KeyError:
        print("Birth Year information is not available")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df): # Viewing raw data, data that was used for computing stats
    """ Asking the user if they want to see the raw data; five rows out of a time """
    i = 0
    user_input = input("Would like to see the data that was used? ").lower()
    pd.set_option('display.max_columns',200)
    num_rows = df.shape[0] # Getting the number of rows

    while True:
        if user_input == 'no':
            break
        elif user_input == 'yes':
            if i < num_rows: # Checking to see if we're over the number of rows
                print(df[i:i+5]) # Even if i+5 > num_rows, it will display everything, not giving the EmptyDataFrame message
                user_input = input("Would like to see more data that was used? ").lower()
                i += 5
            else:
                print("There are no more data to display, ending...\n") # We are at the end of the data set, ending it here
                break
        else:
            user_input = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
