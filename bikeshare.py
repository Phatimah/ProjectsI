import calendar
import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
days_r  = {2:'Monday', 3:'Tuesday', 4:'Wednesday', 5:'Thursday', 6:'Friday', 7:'Saturday', 1:'Sunday'}

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
    city = ''
    while city not in ('chicago', 'new york city', 'washington'):
        city = input('Would you like to see data for Chicago, New York or Washington ?')
        if city not in ('chicago', 'new york city', 'washington'):
            print('Invalid input')

    filter = ''
    while filter not in ('month', 'day', 'both', 'none'):
        filter = input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.')
        if filter not in ('month', 'day', 'both', 'none'):
            print('Invalid input')

    # get user input for month (all, january, february, ... , june)
    month = ''
    if filter in ('month', 'both'):
        while month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            month = input('Which month? january, february, march, april, may or june')
            if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
                print('Invalid input')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    if filter in ('day', 'both'):
        while day not in ('1', '2', '3', '4', '5', '6', '7'):
            day = input('Which day? please type your response as an integer (e.g., 1=Sunday)')
            if day not in ('1', '2', '3', '4', '5', '6', '7'):
                print('Invalid input')

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
    days    = {'Monday':2 , 'Tuesday':3,  'Wednesday':4, 'Thursday':5, 'Friday':6, 'Saturday':7, 'Sunday':1}
    if city == 'chicago':
        df = pd.read_csv('chicago.csv')

    elif city == 'new york':
        df = pd.read_csv('new_york_city.csv')

    elif city == 'washington':
        df = pd.read_csv('washington.csv')

    df['Start Time'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S')
    df['Month'] = df.apply(lambda row: row[1].strftime('%m'), axis=1)
    df['Month'] = df['Month'].apply(lambda x: calendar.month_name[int(x)])
    df['Hour'] = df.apply(lambda row: row[1].strftime('%H'), axis=1)
    df['Day'] = df.apply(lambda row: row[1].strftime('%A'), axis=1)
    df['Day'] = df['Day'].map(days)

    if month:
        df = df[df['Month'].str.lower() == month.lower()]

    if day:
        df = df[df['Day'].str.lower() == day.lower()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most Common Month: ', df['Month'].value_counts().idxmax())

    # display the most common day of week
    print('Most Common Day: ', days_r.get(df['Day'].value_counts().idxmax()))

    # display the most common start hour
    print('Most Common Start Hour: ', df['Hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most Commonly Used Start Station: ', df['Start Station'].value_counts().idxmax())

    # display most commonly used end station
    print('Most Commonly Used End Station: ', df['End Station'].value_counts().idxmax())

    # display most frequent combination of start station and end station trip
    df1 = df
    df1[['Start Station','End Station']].value_counts()
    df1.value_counts(ascending=False).reset_index(name='count')
    df1 = df1.head(1)
    print('Most frequent combination of Start and End Station: ', df1['Start Station'].values[0], ' - ', df1['End Station'].values[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Travel Time: ', df['Trip Duration'].sum())

    # display mean travel time
    print('Mean Travel Time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of User Types: ', df['User Type'].nunique())

    # Display counts of gender
    print('Count of Gender: ', df['Gender'].nunique())

    # Display earliest, most recent, and most common year of birth
    list = df['Birth Year'].unique().tolist()
    list.sort()
    print('Earliest Year of Birth: ', list[0])
    print('Most Recent Year of Birth: ', list[len(list) - 1 ])
    print('Most Common Year of Birth: ', df['Birth Year'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
