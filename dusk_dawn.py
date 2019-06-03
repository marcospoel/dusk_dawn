import ephem
from datetime import timedelta

def dusk_dawn_utc (datetime_utc, latitude_column=None, longitude_column=None, temperature_column=None, elevation_column=None, 
                   air_pressure_column=None, latitude_const='49.088964', longitude_const='20.070236', temperature_const=0, elevation_const=952,
                   air_pressure_const=1010, twilight_const='-6', horizon_const='-0:34', duration=False):

    '''
    dusk_dawn_utc will give you the categories (strings) "night", "dusk", "day", "dawn" based on the variables
    and optionally with the duration is a second variable.  
    The input time must be in UTC 

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

    Raises:
        KeyError: Raises an exception.
               
    See https://rhodesmill.org/pyephem/quick.html'''

    my_observer = ephem.Observer()
    my_observer.date = datetime_utc
    if latitude_column == None:
        my_observer.lat = str(latitude_const)
    else:
        my_observer.lat = str(latitude_column)

    if longitude_column == None:
        my_observer.lon = str(longitude_const)
    else:
        my_observer.lon = str(longitude_column)

    # %% these parameters are for super-precise estimates, not necessary.
    if elevation_column==None:
        my_observer.elevation = elevation_const
    else:
        my_observer.elevation = elevation_column

    if air_pressure_column == None:
        my_observer.pressure = air_pressure_const  # millibar. The difference between the lowest ever observed (923.6) and the highest ever observed (1072) in Europe is 36 seconds later
    else:
        my_observer.pressure = air_pressure_column

    if temperature_column==None:
        my_observer.temp = temperature_const # deg. Celcius. The difference between 0 deg. Celcius and 50 deg. Celcius = 37 seconds later
    else:
        my_observer.temp = temperature_column

    my_observer.horizon = str(horizon_const)

    sun = ephem.Sun()

    next_sunrise_utc = my_observer.next_rising(sun)
    next_sunset_utc = my_observer.next_setting(sun)

    if duration:
        previous_sunrise_utc = my_observer.previous_rising(sun)
        previous_sunset_utc = my_observer.previous_setting(sun)
    else:
        pass
    
    #Relocate the horizon to get twilight times
    #-6=civil twilight, -12=nautical, -18=astronomical
    my_observer.horizon = str(twilight_const)
    next_twilight_rise_utc = my_observer.next_rising(ephem.Sun(), use_center=True) #Begin dusk 
    next_twilight_set_utc  =my_observer.next_setting   (ephem.Sun(), use_center=True) #Begin dawn
    
    if duration:
        previous_twilight_rise_utc = my_observer.previous_rising(sun)
        previous_twilight_set_utc = my_observer.previous_setting(sun)
    else:
        pass


    result_dict= { 
                  "next_twilight_rise_utc":next_twilight_rise_utc,
                  "next_sunrise_utc":next_sunrise_utc,
                  "next_sunset_utc":next_sunset_utc,
                  "next_twilight_set_utc":next_twilight_set_utc
        }

    result_lowest=min(result_dict, key=result_dict.get)

    if result_lowest == "next_twilight_rise_utc":
        result="night"
    elif result_lowest == "next_sunrise_utc":
        result = "dawn"
    elif result_lowest == "next_sunset_utc":
        result = "day"
    elif result_lowest == "next_twilight_set_utc":
        result = "dusk"
    
    if duration:
        if result == "night":
            duration=str(timedelta(next_twilight_rise_utc-previous_twilight_set_utc))
        elif result == "dusk":
            duration=str(timedelta(next_sunrise_utc-previous_twilight_rise_utc))
        elif result == "day":
            duration=str(timedelta(next_sunset_utc-previous_sunrise_utc))
        elif result == "dawn":
            duration=str(timedelta(next_twilight_set_utc-previous_sunset_utc))
        else:
            result = 'Error defining the string dusk, day, dawn, night'
    else:
        pass
        
    if duration:
        return(result, duration)
    else:
        return(result)

def convert_to_utc (datetime, local_timezone):
    
    '''
    convert_to_utc will return the UTC time from your datetime given the timezone of the observation.
    
    Args:
        datetime:              a datetime variable 
        local_timezone:        a string resembling the timezone of the time observation  

    Returns:
        datetime in UTC

    Raises:
        KeyError: Raises an exception.
               
    '''    
    datetime_utc=datetime.tz_localize(local_timezone).tz_convert("UTC")
    return(datetime_utc)
