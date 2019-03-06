# dusk_dawn

The dusk_dawn function will return the categories "dusk, day, dawn and night" given the imput parameters. It the option duration=TRUE will be used the function will also return the duration of the observation. It it is night it returns the total time of the observation "night".

# assumptions

For the examples it is assumed that you have your data in a pandas DataFrame

# function header
`def dusk_dawn_utc (datetime_utc, latitude_column=None, longitude_column=None, temperature_column=None, elevation_column=None, 
                   air_pressure_column=None, latitude_const='49.088964', longitude_const='20.070236', temperature_const=0,                        elevation_const=952, air_pressure_const=1010, twilight_const='-6', horizon_const='-0:34', duration=False):`
## args
    Args:
        datetime_utc,          the column name containing the UTC time of the observation

        If the *_column variables are not provided than it is assumed that these values are provides as constant 
        for all observations 
        
        latitude_column:       the column name containing the latitude of the observation  
        longitude_column:      the column name containing the longitude of the observation
        temperature_column:    the temperature in degrees celcius at the moment of the observation at the 
                               location of the observation
        elevation_column:      the column name containing the number of meters above sealevel of the location of 
                               the observation 
        air_pressure_column:   the column name containing the air preassure at the moment of the observation on the 
                               location


        In case the variables are not present at the observation these values are provides as constant for 
        all observations
        
        latitude_cons          the latitude of the observation  
        longitude_const        the longitude of the observation
        temperature_const:     the temperature in degrees celcius at the moment of the observation
        elevation_const        the number of meters above sealevel of the observation
        air_pressure_const:    the air preassure at the moment of the observation


        constants for observation and twilight calculation
        twilight_const='-6':   the twilight start -6 is civil, -12 is nautic and -18 is astronomical 
                               the value should be entered as a string ('-6', '-12'' '-18')
        horizon_const='-0:34') the horizon attribute defines your horizon, the altitude of the upper limb of a body 
                               at the moment you consider it to be rising and setting. The United States Naval Observatory, 
                               rather than computing refraction dynamically, uses a constant estimate of 34’ of refraction 
                               at the horizon.

        duration:              gives the timedelta between the events and gives how long the night, dusk, day and 
                               dawn took. If "True" the function returns a second variable with the duration of the 
                               observed dusk, day, dawn, night.

    Returns:
        a string with one of the labels "night", "dusk", "day", "dawn"
        or when duration=True 
        returns a the label mentioned above and the duration

# usage

The usage:
`df['duskdawn~_category'] = df.apply(lambda x: dusk_dawn_utc(datetime_utc=x['datetime_utc_column'],              
                                     latitude_column=x['lat_column'], longitude_column=x['long_column'], 
                                     temperature_const=0, elevation_const=0, air_pressure_const=1010, twilight_const='-6',
                                     horizon_const='-0:34', duration=False), axis=1)

If your data has observations of the elevation (altitude), temperature and airpressure on the location of the observation at the time of the observation these columns can be used over a const. They are not very material for the results (of by seconds).

# bonus usage to create an UTC datetime primitive from a local timezone

Inspiration for conversion to UTC

`# if all timestamps in 1 zone
local_timezone="America/New_York"

#this function will create a new column with the UTC representation of the timestamp
df["new_datetime_utc_column"]=df.apply(lambda x: convert_to_utc(datetime=x['source_datetime_column'], local_timezone=local_timezone), axis=1)`

or 

`#this function will create a new column with the UTC representation of the timestamp
df["new_datetime_utc_column"]=df.apply(lambda x: convert_to_utc(datetime=x['source_datetime_column'], local_timezone=x['source_datetime_tz']), axis=1)`


