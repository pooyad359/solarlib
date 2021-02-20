from solarlib.error_handling import ValueOutOfRange,raise_type_error,type_check
from solarlib.solar import sunrise, sunset, estimated_irradiance
class Location:
    def __init__(self, latitude, longitude, timezone=None):
        self.set_timezone(timezone)
        self.set_latitude(latitude)
        self.set_longitude(longitude)

    def set_latitude(self, latitude):
        if not type_check(latitude, [int, float]):
            raise_type_error('latitude', type(latitude))
        elif -90 <= latitude <= 90:
            self.__latitude = latitude
        else:
            raise ValueError(
                f'latitude must be between -90 and 90 degrees but recieved {latitude}'
            )
            
    def set_longitude(self, longitude):
        if not type_check(longitude, [int, float]):
            raise_type_error('longitude', type(longitude))
        elif -180 <= longitude <= 180:
            self.__longitude = longitude
        else:
            raise ValueError(
                f'longitude must be between -180 and 180 degrees but recieved {longitude}'
            )
            
    def set_timezone(self,timezone):
        if timezone is None:
            self.__timezone = pytz.timezone('UTC')
        elif isinstance(timezone,str):
            self.__timezone = pytz.timezone(timezone)
        elif isinstance(timezone,float) or isinstance(timezone,int):
            timezone_hours = round(timezone*2)/2
            timedelta = datetime.timedelta(hours = timezone_hours)
            self.__timezone = datetime.timezone(timedelta)
        else:
            raise_type_error('timezone',type(timezone))
    
    @property
    def latitude(self):
        return self.__latitude
    
    @property
    def longitude(self):
        return self.__longitude
    
    @property
    def timezone(self):
        return self.__timezone
    
    def __repr__(self):
        lat = self.__latitude
        lon = self.__longitude
        tz = self.__timezone
        output = f'''Location(latitude = {lat}, 
            longitude = {lon}, 
            timezone = {str(tz)})'''
        return output.replace(' '*4,'').replace('\n','')
    
    def __str__(self):
        return repr(self)
    
    def sunrise(self,date,fmt = '%Y-%m-%d'):
        date = self.__parse_date(date,fmt = '%Y-%m-%d')
        lat = self.latitude
        lon = self.longitude
        base = sunrise(date,lat, lon)
        return sunrise(base,lat, lon)
        
        
    def sunset(self,date,fmt = '%Y-%m-%d'):
        date = self.__parse_date(date,fmt = fmt)
        lat = self.latitude
        lon = self.longitude
        base = sunset(date,lat, lon)
        return sunset(base,lat, lon)
    
    def solar_irradiance(self,time,fmt = '%Y-%m-%d %H:%M:%S'):
        time = self.__parse_time(time,fmt = fmt)
        lat = self.latitude
        lon = self.longitude
        return estimated_irradiance(time,lat,lon)
    
    def daily_irradiance(self,date,fmt = '%Y-%m-%d',freq_min = 30):
        date = self.__parse_date(date,fmt = fmt)
        delta = datetime.timedelta(minutes = freq_min)
        n = 1440//freq_min +1
        output = [
            (
                date+i*delta,
                self.solar_irradiance(date+i*delta)
            ) for i in range(n)
        ]
        return output
    
    def day_length(self,date,fmt = '%Y-%m-%d'):
        date = self.__parse_date(date,fmt = fmt)
        rise_time = self.sunrise(date,fmt)
        set_time = self.sunset(date,fmt)
        return set_time-rise_time
    
    def solar_noon(self,date,fmt = '%Y-%m-%d'):
        date = self.__parse_date(date,fmt = fmt)
        lat = self.latitude
        lon = self.longitude
        base = solar_noon(date, lon)
        return solar_noon(base, lon)

    def __parse_date(self,date,fmt = '%Y-%m-%d'):
        if isinstance(date,str):
            return datetime.datetime.strptime(date,fmt)
        elif isinstance(date,datetime.datetime):
            return date
        elif isinstance(date,datetime.date):
            time = datetime.time()
            return datetime.datetime.combine(date,time)
        else:
            raise_type_error('date',datetime.datetime)
    
    def __parse_time(self,date,fmt = '%Y-%m-%d %H:%M:%S'):
        if isinstance(date,str):
            return datetime.datetime.strptime(date,fmt)
        elif isinstance(date,datetime.datetime):
            return date
        else:
            raise_type_error('date',datetime.datetime)
        