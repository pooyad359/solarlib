from solarlib.exceptions import ValueOutOfRange,raise_type_error,type_check

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