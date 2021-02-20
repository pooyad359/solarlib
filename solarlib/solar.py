import datetime
from math import degrees, radians, atan2, asin, acos, sin, cos
from solarlib.calendar import julian_century

def geom_mean_long(time):
    '''
    Sun mean longitude (degrees)
    '''
    julian_cent = julian_century(time)
    angle = 280.46646 + julian_cent * (julian_cent * 3.032e-4 + 36000.76983)
    return angle % 360


def geom_mean_anom(time):
    '''
    Sun Mean Anomaly (degrees)
    '''
    julian_cent = julian_century(time)
    angle = 357.52911 + julian_cent * (35999.05029 - julian_cent * 1.537e-4)
    return angle


def eccent_earth_orbit(time):
    '''
    Eccentricity of Earth orbit
    '''
    julian_cent = julian_century(time)
    return 0.016708634 - julian_cent * (4.2037e-5 + 1.267e-7 * julian_cent)


def equation_of_center(time):
    '''
    Sun Equation of Center
    '''
    julian_cent = julian_century(time)
    anom = geom_mean_anom(time)
    anom = radians(anom)
    t1 = sin(anom) * (1.914602 - julian_cent * (0.004817 + 1.4e-5 * julian_cent))
    t2 = sin(2 * anom) * (0.019993 - 0.000101 * julian_cent)
    t3 = sin(3 * anom) * 0.000289
    return t1 + t2 + t3


def true_longitude(time):
    return geom_mean_long(time) + equation_of_center(time)


def true_anomaly(time):
    return geom_mean_anom(time) + equation_of_center(time)


def rad_vector(time):
    '''
    in Astronomical Unit (AUs)
    '''
    ecc = eccent_earth_orbit(time)
    anom = true_anomaly(time)
    return (1.000001018 * (1 - ecc * ecc)) / (1 + ecc * cos(radians(anom)))


def app_long(time):
    julian_cent = julian_century(time)
    tlon = true_longitude(time)
    return tlon - 0.00569 - 0.00478 * sin(
        radians(125.04 - 1934.136 * julian_cent))


def mean_obliq_ecliptic(time):
    julian_cent = julian_century(time)
    res = 46.815 + julian_cent * (0.00059 - julian_cent * 0.001813)
    res = 21.448 - julian_cent * (res)
    res = 23 + (26 + res / 60) / 60
    return res


def obeliq_corr(time):
    julian_cent = julian_century(time)
    moe = mean_obliq_ecliptic(time)
    return moe + 0.00256 * cos(radians(125.04 - 1934.136 * julian_cent))


def solar_ascention(time):
    lon = app_long(time)
    oblq = obeliq_corr(time)
    a = cos(radians(oblq)) * sin(radians(lon))
    b = cos(radians(lon))
    ascn = atan2(a, b)
    return degrees(ascn)


def solar_declination(time):
    lon = app_long(time)
    oblq = obeliq_corr(time)
    decn = asin(sin(radians(oblq)) * sin(radians(lon)))
    return degrees(decn)


def equation_of_time(time):
    oblq = obeliq_corr(time)
    lon = geom_mean_long(time) 
    anom = geom_mean_anom(time) 
    ecc = eccent_earth_orbit(time) 
    var_y = tan(radians(oblq / 2)) * tan(radians(oblq / 2))
    result = [
        var_y * sin(2 * radians(lon)), -2 * ecc * sin(radians(anom)),
        4 * ecc * var_y * sin(radians(anom)) * cos(2 * radians(lon)),
        -0.5 * var_y * var_y * sin(4 * radians(lon)),
        -1.25 * ecc * ecc * sin(2 * radians(anom))
    ]
    return 4 * degrees(sum(result))


def sunrise_hour_angle(time, latitude):
    decn = radians(solar_declination(time))
    a1 = cos(radians(90.833)) / (cos(radians(latitude)) * cos(decn))
    a2 = tan(radians(latitude)) * tan(decn)
    return degrees(acos(a1 - a2))


def solar_noon(time, longitude):
    '''
    Solar noon time
    '''
    tz = time.tzinfo
    utc = pytz.timezone('UTC')
    julian_cent = julian_century(time)
    eot = equation_of_time(julian_cent)
    noon_offset = (720 - 4 * longitude - eot) / 1440
    midnight = datetime.datetime.combine(
        time.date(), datetime.time(tzinfo=pytz.timezone('UTC')))
    noon_utc = midnight + datetime.timedelta(days=noon_offset)
    return noon_utc.astimezone(tz)


def sunrise(time, latitude, longitude):
    '''
    Sunrise time
    '''
    noon = solar_noon(time, longitude)
    julian_cent = julian_century(time)
    hour_angle = sunrise_hour_angle(julian_cent, latitude)
    delta = datetime.timedelta(minutes=4 * hour_angle)
    return noon - delta


def sunset(time, latitude, longitude):
    '''
    Sunset time
    '''
    noon = solar_noon(time, longitude)
    julian_cent = julian_century(time)
    hour_angle = sunrise_hour_angle(julian_cent, latitude)
    delta = datetime.timedelta(minutes=4 * hour_angle)
    return noon + delta


def daytime_length(time, latitude):
    '''
    Length of day time (Sunlight duration) in hours.
    '''
    julian_cent = julian_century(time)
    hour_angle = sunrise_hour_angle(julian_cent, latitude)
    return 8 * hour_angle / 60


def true_solar_time(time, longitude):
    '''
    True solar time in minutes from midnight
    '''
    utc = pytz.timezone('UTC')
    julian_cent = julian_century(time)
    eot = equation_of_time(julian_cent)
    delta = datetime.timedelta(minutes=eot + longitude * 4)
    true_time = (time + delta).astimezone(utc)
    hour = true_time.hour
    minute = true_time.minute
    second = true_time.second
    return get_minutes(true_time)


def hour_angle(time, longitude):
    solar_time = true_solar_time(time, longitude)
    return solar_time / 4 - 180



def solar_zenith(time, latitude, longitude):
    '''
    Solar Zenith Angle in degrees
    '''
    julian_cent = julian_century(time)
    decn = solar_declination(julian_cent)
    h_angle = hour_angle(time, longitude)
    a1 = sin(radians(latitude)) * sin(radians(decn))
    a2 = cos(radians(latitude)) * cos(radians(decn)) * cos(radians(h_angle))
    return degrees(acos(a1 + a2))


def solar_elevation_angle(time, latitude, longitude):
    '''
    Solar Elevation Angle in degrees
    '''
    return 90 - solar_zenith(time, latitude, longitude)


def atmospheric_refraction(time, latitude, longitude):
    '''
    Approximate atmospheric refraction in degrees
    '''
    elev = solar_elevation_angle(time, latitude, longitude)
    if elev > 85:
        refraction = 0
    elif elev > 5:
        refraction = 58.1 / tan(radians(elev)) - 0.07 / pow(
            tan(radians(elev)), 3) + 0.000086 / pow(tan(radians(elev)), 5)
    elif elev > -.575:
        refraction = 1735 + elev * (-518.2 + elev * (103.4 + elev *
                                                     (-12.79 + elev * 0.711)))
    else:
        refraction = -20.772 / tan(radians(elev))

    return refraction / 3600


def corrected_solar_elevation(time, latitude, longitude):
    '''
    Solar Elevation corrected for atmospheric refraction
    '''
    elev = solar_elevation_angle(time, latitude, longitude)
    refr = atmospheric_refraction(time, latitude, longitude)
    return elev + refr


def solar_azimuth(time, latitude, longitude):
    '''
    Azimuth angle (measured Clockwise from North)
    '''
    julian_cent = julian_century(time)
    zenith = radians(solar_zenith(time, latitude, longitude))
    decln = radians(solar_declination(julian_cent))
    h_angle = hour_angle(time, longitude)
    lat = radians(latitude)
    if h_angle > 0:
        a1 = sin(lat) * cos(zenith) - sin(decln)
        a2 = cos(lat) * sin(zenith)
        azimuth = degrees(acos( a1 / a2)) + 180
        return azimuth%360

    else:
        a1 = sin(lat) * cos(zenith) - sin(decln)
        a2 = cos(lat) * sin(zenith)
        azimuth = 540 - degrees(acos(a1 /a2))
        return azimuth%360

def estimated_irradiance(time, latitude, longitude):
    '''
    Estimated solar irradiance in kW/m^2
    '''
    zenith = solar_zenith(time, latitude, longitude)
    zenith = min(zenith,92)
    if zenith<92:
        amf = 1/cos(radians(zenith)) # Air Mass Factor
        amf = 1/(cos(radians(zenith))+0.50572*(96.07995-zenith)**(-1.6364))
        return 1.353*0.7**(amf**0.678)
    else:
        return 0
