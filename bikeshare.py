import time
import random
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#-------------------------My proposal-------------------------------------------
month = 'all'
day = 'all'
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    month = 'all'
    day = 'all'
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    #HINT: Use a while loop to handle invalid inputs
    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            city = input('\nWould you like to see data for Chicago,New York city or Washington ?\n').lower()
            while city not in ['chicago' ,'new york city' , 'washington']:
                city = input('Enter a correct city name (Chicago,New York city or Washington):\n').lower()
            break

        except:
            print('That is not valid city name')
    while True:
        try:
            option = input('Would you like to filter data by month, day, both or not at all? Type "none" for no time filter.\n').lower()
            while option not in ['none' , 'month' , 'day' ,'both']:
                option = input('Enter a correct option name (month, day, both or none):\n').lower()
            break
        except:
            print('That is not valid option name')
    if option == 'month' :
        while True:
            try:
                month = input('\nWhich month? All, January, February, March, April, May or June?\n').lower()
                while month not in ['all' ,'january' ,'february' ,'march' ,'april','may' ,'june']:
                    month = input('Enter a correct month name (All, January, February, March, April, May or June):\n').lower()
                break
            except:
                print('That is not valid month name.')
    if option == 'day':
        while True:
            try:
                day = input('\nWhich day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday?\n').lower()
                while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',  'sunday']:
                    day = input('Enter a correct day name (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday):\n').lower()
                break
            except:
                print('That is not valid day name.')
    if option == 'both':
        while True:
            try:
                month = input('\nWhich month? All, January, February, March, April, May or June?\n').lower()
                while month not in ['all' ,'january' ,'february' ,'march' ,'april','may' ,'june']:
                    month = input('Enter a correct month name (All, January, February, March, April, May or June):\n').lower()
                break
            except:
                print('That is not valid month name.')
        while True:
            try:
                day = input('\nWhich day? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday?\n').lower()
                while day not in ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday',  'sunday']:
                    day = input('Enter a correct day name (All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, and Sunday):\n').lower()
                break
            except:
                print('That is not valid day name.')

    print('\nYour search criteria are : ', 'The city: ',city,',The month: ',month,',The day: ' ,day)

    print('-'*40)
    return city, month, day
#-------------------------Loading data------------------------------------------

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
    print('\n-------Start loading data---------------')
    start_time = time.time()
    filename = CITY_DATA[city]
    df= pd.read_csv(filename)
    print(df.columns)
    while True:
        try:
            mean_birth_year = round(df['Birth Year'].mean(),0)# avg of float birth year rounded to nearest integer
            df['Birth Year'] = df['Birth Year'].fillna(mean_birth_year)# fill nan value in birt year to put mean instead
            df['Birth Year'] = df['Birth Year'].astype(int)
        except:
            print('\nThis city has no gender list!')
        break

    df.rename(columns = {'Trip Duration':'Trip Duration in seconds'}, inplace = True)

    df.info()
    # Add month Col#
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    #----Convert month disply from integer to string
    months_list = ['january', 'february', 'march', 'april', 'may', 'june']
    for i in range(1,7):
        df.loc[df['month'] == i, 'month'] = months_list[i-1].title()
    #----Criteria for month selection
    if month != 'all' :
        df = df[df['month'] == month.title()]
    #----Add day Col + Criteria for day selection
    df['day_of_week'] = pd.to_datetime(df['Start Time']).dt.day_name()
    if day != 'all' :
        df = df[df['day_of_week'] == day.title()]
    #-----ADD START HOUR + END HOUR + COMBINE START AND END STATIONS  COLs
    df['Start_hour'] =  pd.to_datetime(df['Start Time']).dt.hour
    df['End_hour'] =  pd.to_datetime(df['End Time']).dt.hour
    df["St_End_togeth"] = df[["Start Station", "End Station"]].apply("-".join, axis=1)

    print("\nThis took %s seconds." % round((round(time.time(),2) - start_time),2))
    print('-'*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('\nThe most common month : ',df['month'].mode())

    # display the most common day of week
    print('\nThe most common day of week : ',df['day_of_week'].mode())

    # display the most common start hour
    print('\nThe most common Start_hour : ',df['Start_hour'].mode())

    print("\nThis took %s seconds." % round((round(time.time(),2) - start_time),2))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station : ',df['Start Station'].mode())

    # display most commonly used end station
    print('\nThe most commonly used end station : ',df['End Station'].mode())

    # display most frequent combination of start station and end station trip
    print('\nThe most frequent combination of start station and end station trip : ',df['St_End_togeth'].mode())

    print("\nThis took %s seconds." % round((round(time.time(),2) - start_time),2))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total travel time : ',df['Trip Duration in seconds'].sum(),' seconds')

    # display mean travel time
    print('\nThe mean travel time : ',df['Trip Duration in seconds'].mean(),' seconds')

    print("\nThis took %s seconds." % round((round(time.time(),2) - start_time),2))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('\nCounts of user types : ',df['User Type'].value_counts())


    # Display counts of gender
    while True:
        try:
            print('\nCounts of user types : ',df['Gender'].value_counts())
        except:
            print('\nThis city has no gender list!')
        break

    # Display earliest, most recent, and most common year of birth
    while True:
        try:
            print('\nEarliest year of birth : ',df['Birth Year'].min())
            print('\nMost recent year of birth : ',df['Birth Year'].max())
            print('\nMost common year of birth : ',df['Birth Year'].mode())
        except:
            print('\nThis city has no birth year list!')
        break

    print("\nThis took %s seconds." % round((round(time.time(),2) - start_time),2))
    print('-'*40)

def display_sample_of_raw_data(city):

    """ Ask user: Would you like to present a sample of raw data ?"""

    df= pd.read_csv(CITY_DATA[city])
    while True:
        try:
            mean_birth_year = round(df['Birth Year'].mean(),0)# avg of float birth year rounded to nearest integer
            df['Birth Year'] = df['Birth Year'].fillna(mean_birth_year)# fill nan value in birt year to put mean instead
            df['Birth Year'] = df['Birth Year'].astype(int)
        except:
            print('\nThis city has no gender list!')
        break
    df.rename(columns = {'Trip Duration':'Trip Duration in seconds'}, inplace = True)
    while True :
        try:
            ask_user = input('\nWould you like to present a sample of data? type "yes" if you like.\n').lower()
            while ask_user not in ['yes', 'no'] :
                ask_user = input('\nPlease type "yes" or "no" : \n')
            if ask_user != 'yes':
                print('\nOk, thanks to answer next question.!')
                break
            while ask_user == 'yes' :
                r=df.shape[0]
                for i in range(0,5):
                    n=random.randint(0,r)
                    print(df.loc[n])
                ask_user = input('\nWould you like to present more data? type "yes" if you like.\n').lower()
                while ask_user not in ['yes', 'no'] :
                    ask_user = input('\nPlease type "yes" or "no" : \n')
            if ask_user != 'yes':
                print('\nOk, thanks to answer next question.!')
                break
            break
        except:
            print('\n This is invalid input!')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_sample_of_raw_data(city)
        while True:
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n')
                while restart.lower() not in ['yes','no']:
                    restart = input('\nPlease type "yes" or "no" : \n')
                break
            except:
                print('Invalid input!')
        if restart.lower() != 'yes':
            print('\nThank you for using bikeshare!')
            break

if __name__ == "__main__":
	main()
