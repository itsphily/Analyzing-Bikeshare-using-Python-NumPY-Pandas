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
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input('which city do you want to analyze (select Chicago, New York City, or Washington): ').lower()
    while city.lower()!='chicago' and city.lower()!='new york city' and city.lower()!='washington':
        print('input was invalid! Please choose one of the three cities (Chicago, New York City, or Washington)')
        city=input('which city do you want to analyze: ').lower()

    # Get user input for month (all, january, february, ... , june)
    month=input('which month do you want data for(from January to June) or type all: ').lower()
    while month.lower() not in ['january', 'february', 'march', 'april', 'may', 'june','all']:
        print('input was invalid! Remember choose a month between January and June')
        month=input('which month do you want data for: ').lower()


    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day=input('Choose a day for which you want data or type all: ').lower()
    while day.lower() not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
        print('input was invalid!')
        day=input('which day do you want data for: ').lower()

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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # Filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # Filter by month to create the new dataframe
        df = df[df['month']==month]

    # Filter by day of week if applicable
    if day != 'all':
        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    month_result=''

    # Display the most common month
    try:
        month_count = df['month'].value_counts()
        month_list=['January', 'February', 'March', 'April', 'May', 'June']
        ''' Checks if there are several indexes for the maximum value of month count'''
        i=0
        for i in range(len(month_count)):
            if month_count.values[i]==month_count.values[i+1]:
                month_result+=month_list[month_count.index.tolist()[i]-1]+","
                i+=1
            else:
                month_result+=month_list[month_count.index.tolist()[i]-1]+'.\n'
                i+=1
                break
        print('The most common month is: '+ month_result, end='')
    except:
        pass

    # Display the most common day of week
    try:
        day_count = df['day_of_week'].value_counts()
        ''' Checks if there are several indexes for the maximum value of day count'''
        day_result=''
        i=0
        for i in range(len(day_count)):
            if day_count.values[i]==day_count.values[i+1]:
                day_result += day_count.index.tolist()[i]+","
                i+=1
            else:
                day_result += day_count.index.tolist()[i]+'.\n'
                i+=1
                break
        print('The most common day is: '+ day_result, end='')
    except:
        pass

    # Display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    hour_count = df['start_hour'].value_counts()
    print("the most common start hour(s) is(are): ",end="")

    ''' Checks if there are several indexes for the maximum value of hour count'''
    i=0
    for i in range(len(hour_count)):
        if hour_count.values[i]==hour_count.values[i+1]:
            print(hour_count.index.tolist()[i], end=",")
            i+=1
        else:
            print(hour_count.index.tolist()[i],end='.\n')
            i+=1
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    start_station_count=df['Start Station'].value_counts()
    ''' checks if there are equally popular start stations'''
    print('The most common start station is: ', end='')
    i=0
    for i in range(len(start_station_count)):
        if start_station_count.values[i]==start_station_count.values[i+1]:
            print(start_station_count.index.tolist()[i], end=",")
            i+=1
        else:
            print(start_station_count.index.tolist()[i],end='.\n')
            i+=1
            break

    # Display most commonly used end station
    end_station_count=df['End Station'].value_counts()
    ''' checks if there are equally popular end stations'''
    print('The most common end station is: ', end='')
    i=0
    for i in range(len(end_station_count)):
        if end_station_count.values[i]==end_station_count.values[i+1]:
            print(end_station_count.index.tolist()[i], end=",")
            i+=1
        else:
            print(end_station_count.index.tolist()[i],end='.\n')
            i+=1
            break

    # Display most frequent combination of start station and end station trip
    df['Combo Station']='start station: '+ df['Start Station'] + ' to end station: '+df['End Station']
    count_combo=df['Combo Station'].value_counts()
    ''' checks if there are equally popular start/end station combinations'''
    print('The most common path goes from ', end='')
    i=0
    for i in range(len(count_combo)):
        if count_combo.values[i]==count_combo.values[i+1]:
            print(count_combo.index.tolist()[i], end="\n")
            i+=1
        else:
            print(count_combo.index.tolist()[i],end='.\n')
            i+=1
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    hours_total=int(df['Trip Duration'].sum()/3600)
    minutes_total= int((df['Trip Duration'].sum()-hours_total*3600)/60)
    seconds_total=int(df['Trip Duration'].sum()%60)

    print('The total travel time is: '+ str(hours_total)+' hours, '+ str(minutes_total)+' minutes, and '+ str(seconds_total)+' seconds!')

    # Display mean travel time
    hours_total=int(df['Trip Duration'].mean()/3600)
    minutes_total= int((df['Trip Duration'].mean()-hours_total*3600)/60)
    seconds_total=int(df['Trip Duration'].mean()%60)

    print('The mean travel time is: '+ str(hours_total)+' hours, '+ str(minutes_total)+' minutes, and '+ str(seconds_total)+' seconds!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts().to_frame(),'\n')

    # Display counts of gender (only available for NYC and Chicago)
    try:
        print(df['Gender'].value_counts().to_frame(),'\n')
    except:
       print('We don\'t have the gender information for this city!')

    # Display earliest, most recent, and most common year of birth (only available for NYC and Chicago)
    try:
        print('The earliest date of birth is:',int(df['Birth Year'].min()))
        print('The most recent date of birth is:',int(df['Birth Year'].max()))
        print('The most common date of birth is:',int(df['Birth Year'].dropna().mode()))
    except:
        print('We don\'t have the date of birth information for this city!')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        i=0
        peek =input("would you like to look at 5 lines of the dataset(type no if you would like to skip this step):\n")
        while peek.lower()!="no" and peek.lower()!="stop":
            print(len(df))
            if i>len(df):
                print('You went through the whole dataset!')
                break
            print(df.loc[i:i+4])
            i+=5
            peek =input("would you like to look at 5 more lines of the dataset(type stop to exit):\n")
        print('\n','-'*40)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    print('\nHave a nice day  :-)')


if __name__ == "__main__":
	main()
