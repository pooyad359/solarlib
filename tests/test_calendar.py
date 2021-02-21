import unittest
from solarlib.calendar import julian_century, julian_day
from solarlib.solar import (
    geom_mean_long,
    geom_mean_anom,
    eccent_earth_orbit,
    equation_of_center,
    true_longitude,
    true_anomaly,
    rad_vector,
    app_long,
    mean_obliq_ecliptic,
    obeliq_corr,
    solar_ascention,
    solar_declination,
    equation_of_time,
    sunrise_hour_angle,
    daytime_length,
    true_solar_time,
    hour_angle,
    solar_zenith,
    solar_elevation_angle,
    atmospheric_refraction,
    corrected_solar_elevation,
    solar_azimuth,
    estimated_irradiance,
)
import datetime
import pytz


class TestCalendar(unittest.TestCase):
    def test_julian_day(self):
        tz = pytz.timezone('Australia/Perth')
        time = datetime.datetime(2010, 6, 21, 4, 45)
        time = tz.localize(time)
        self.assertAlmostEqual(julian_day(time), 2455368.364583, 3)

    def test_julian_century(self):
        tz = pytz.timezone('Australia/Perth')
        time = datetime.datetime(2010, 6, 21, 4, 45)
        time = tz.localize(time)
        self.assertAlmostEqual(julian_century(time), 0.10467801733972)


class TestSolarCalculations(unittest.TestCase):
    tz = pytz.timezone('Australia/Perth')
    time = datetime.datetime(2010, 6, 21, 4, 45)
    time = tz.localize(time)
    longitude = 115
    latitude = 40

    def test_geom_mean_long(self):
        output = geom_mean_long(self.time)
        expected = 88.95567
        self.assertAlmostEqual(output, expected, 3)

    def test_geom_mean_anom(self):
        output = geom_mean_anom(self.time)
        expected = 4125.838
        self.assertAlmostEqual(output, expected, 3)

    def test_eccent_earth_orbit(self):
        output = eccent_earth_orbit(self.time)
        expected = 0.01670423
        self.assertAlmostEqual(output, expected, 5)

    def test_equation_of_center(self):
        output = equation_of_center(self.time)
        expected = 0.4590157
        self.assertAlmostEqual(output, expected, 5)

    def test_true_longitude(self):
        output = true_longitude(self.time)
        expected = 89.414687
        self.assertAlmostEqual(output, expected, 3)

    def test_true_anomaly(self):
        output = true_anomaly(self.time)
        expected = 4126.29733
        self.assertAlmostEqual(output, expected, 3)

    def test_rad_vector(self):
        output = rad_vector(self.time)
        expected = 1.0162139168
        self.assertAlmostEqual(output, expected, 4)

    def test_app_long(self):
        output = app_long(self.time)
        expected = 89.413662
        self.assertAlmostEqual(output, expected, 3)

    def test_mean_obliq_ecliptic(self):
        output = mean_obliq_ecliptic(self.time)
        expected = 23.43792
        self.assertAlmostEqual(output, expected, 3)

    def test_obeliq_corr(self):
        output = obeliq_corr(self.time)
        expected = 23.438487
        self.assertAlmostEqual(output, expected, 3)

    def test_solar_ascention(self):
        output = solar_ascention(self.time)
        expected = 89.36093602
        self.assertAlmostEqual(output, expected, 3)

    def test_solar_declination(self):
        output = solar_declination(self.time)
        expected = 23.43718671
        self.assertAlmostEqual(output, expected, 3)

    def test_equation_of_time(self):
        output = equation_of_time(self.time)
        expected = -1.62156698
        self.assertAlmostEqual(output, expected, 3)

    def test_sunrise_hour_angle(self):
        output = sunrise_hour_angle(self.time, self.latitude)
        expected = 112.609120
        self.assertAlmostEqual(output, expected, 3)

    def test_daytime_length(self):
        output = daytime_length(self.time, self.latitude)
        expected = 15.014549
        self.assertAlmostEqual(output, expected, 3)

    def test_true_solar_time(self):
        output = true_solar_time(self.time, self.longitude)
        expected = 263.378
        self.assertAlmostEqual(output, expected, 3)

    def test_hour_angle(self):
        output = hour_angle(self.time, self.longitude)
        expected = -114.15539
        self.assertAlmostEqual(output, expected, 3)

    def test_solar_zenith(self):
        output = solar_zenith(self.time, self.latitude, self.longitude)
        expected = 91.830788
        self.assertAlmostEqual(output, expected, 3)

    def test_solar_elevation_angle(self):
        output = solar_elevation_angle(self.time,
                                       self.latitude,
                                       self.longitude)
        expected = -1.830788
        self.assertAlmostEqual(output, expected, 3)

    def test_atmospheric_refraction(self):
        output = atmospheric_refraction(self.time,
                                        self.latitude,
                                        self.longitude)
        expected = 0.1805146
        self.assertAlmostEqual(output, expected, 3)

    def test_corrected_solar_elevation(self):
        output = corrected_solar_elevation(self.time,
                                           self.latitude,
                                           self.longitude)
        expected = -1.65027424
        self.assertAlmostEqual(output, expected, 3)

    def test_solar_azimuth(self):
        output = solar_azimuth(self.time, self.latitude, self.longitude)
        expected = 56.8862138
        self.assertAlmostEqual(output, expected, 3)

    def test_estimated_irradiance(self):
        output = estimated_irradiance(self.time, self.latitude, self.longitude)
        expected = 0.0032605
        self.assertAlmostEqual(output, expected, 4)
