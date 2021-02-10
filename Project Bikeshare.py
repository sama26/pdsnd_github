import time
import pandas as pd

city_data = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bike share data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ''
    while city not in city_data:
        city = input('\nPlease select a city from the following list:\n'
                     '\nChicago'
                     '\nNew York City'
                     '\nWashington'
                     '\n\n').lower()

    # Get user input for month (all, january, february, ... , june)
    month = ''
    while month not in months:
        month = input('\nPlease select a month from the following list:\n'
                      '\nJanuary'
                      '\nFebruary'
                      '\nMarch'
                      '\nApril'
                      '\nMay'
                      '\nJune'
                      '\nAll'
                      '\n\n').lower()

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    while day not in days:
        day = input('\nPlease select a day of the week from the following list:\n'
                    '\nMonday'
                    '\nTuesday'
                    '\nWednesday'
                    '\nThursday'
                    '\nFriday'
                    '\nSaturday'
                    '\nSunday'
                    '\nAll'
                    '\n\n').lower()
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
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
    df = pd.read_csv(city_data[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[(df['month'] == month)]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day_num = days.index(day.lower()) + 1
        df = df[df['day_of_week'] == day_num]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel for the chosen city."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month

    # extract month from the Start Time column to create a month column
    df['month'] = pd.to_datetime(df['Start Time']).dt.month

    # Calculate the mode and print
    popular_month = df["month"].mode()[0]

    print('Most common month of the year: ', months[popular_month - 1].title())

    # Display the most common day of week

    # extract day of week from the Start Time column to create a day column
    df['day'] = pd.to_datetime(df['Start Time']).dt.dayofweek

    # Calculate the mode and print
    popular_day = df["day"].mode()[0]

    print('Most common day of the week: ', days[popular_day - 1].title())

    # Display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df["hour"].mode()[0]

    print('Most Frequent Start Hour: {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip for the chosen city."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]

    print('Most popular start station: ', popular_start_station)

    # display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]

    print('Most popular end station: ', popular_end_station)

    # Display most frequent combination of start station and end station trip

    # Create a new field with a concatenation of start and end stations
    df['Start and End'] = df['Start Station'].str.cat(df['End Station'], sep=" / ")
    
    # Calculate the mode
    popular_start_end = df["Start and End"].mode()[0]

    print('Most popular start and end station combination: ', popular_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration for the chosen city."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()

    print("Total travel time:\n{} days".format(int(total_travel_time / 2880)))

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()

    print("Mean travel time: {} minutes".format(int(mean_travel_time / 60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bike share users for the chosen city."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print("Breakdown of user types: \n\n", user_types)

    # Display counts of gender
    if city != 'washington':
        gender = df['Gender'].value_counts()

        print("\nBreakdown of gender: \n\n", gender)
    else:
        print("\nNo gender data available\n")

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        mode_birth_year = int(df['Birth Year'].mode())

        print("\nEarliest birth year: ", earliest_birth_year)
        print("Most recent birth year: ", recent_birth_year)
        print("Most common birth year: ", mode_birth_year)

    else:
        print("\nNo birth year data available\n")

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_data(df):
    """Shows 5 lines of data at a time as requested by the user, for the chosen city"""

    view_data = ''
    start_loc = 0
    while view_data not in ('yes', 'no'):
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
        while view_data == 'yes':
            print(df.iloc[start_loc:start_loc + 5])
            start_loc += 5
            view_data = input("Would you like to view 5 more rows? Enter yes or no?").lower()


def main() -> object:
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
