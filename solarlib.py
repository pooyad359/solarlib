import numpy as np
import matplotlib.pyplot as plt
import datetime
deg2rad=np.pi/180
rad2deg=180/np.pi
def SolarDeclination(DayOfYear):
    '''
    calculate solar declination angle (deg)
    DayOfYear=0 ---> January 1st
    '''
    sin_delta=np.sin(-23.44*deg2rad)*np.cos(2*np.pi/365.24*(DayOfYear+2)+2*0.0167*(2*np.pi/365.24*(DayOfYear-2)))
    delta=np.arcsin(sin_delta)
    return delta
def ZenithAngle(Latitude,DayOfYear,HourOfDay):
    '''
    calculate solar zenith angle (deg)
    Latitude: (+) North, (-) South
    DayOfYear: 0 for January 1st
    HourOfDay: hours since midnight
    '''
    delta=SolarDeclination(DayOfYear)
    HourAngle=15*(HourOfDay-12)*deg2rad
    phi=Latitude*deg2rad
    cosz=np.sin(phi)*np.sin(delta)+np.cos(phi)*np.cos(delta)*np.cos(HourAngle)
    zenith=np.arccos(cosz)*rad2deg
    return zenith
def SolarIrradiance(Latitude,DayOfYear,HourOfDay):
    '''
    calculate solar irradiance (kW)
    Latitude: (+) North, (-) South
    DayOfYear: 0 for January 1st
    HourOfDay: hours since midnight
    '''
    z=ZenithAngle(Latitude,DayOfYear,HourOfDay)
    irr=1050.*np.cos(z*deg2rad)
    irr[irr<0]=0
    return irr
def DailyIrradiance(Latitude,DayOfYear,display=False):
    '''
    return solar irradiance for every 5 min
    Latitude: (+) North, (-) South
    DayOfYear: 0 for January 1st
    '''
    h=np.linspace(0,24,24*12+1)
    irr=SolarIrradiance(Latitude,DayOfYear,h)
    if display:
        plt.plot(h,irr)
    return h,irr
def Sunrise(Latitude,DayOfYear):
    '''
    calculate sunrise time
    Latitude: (+) North, (-) South
    DayOfYear: 0 for January 1st
    '''
    f=lambda h:np.cos(ZenithAngle(Latitude,DayOfYear,h)*deg2rad)
    hl,hr=0,12
    h_sunrise=Bisection(f,hl,hr)
    sr_time=hour2time(h_sunrise)
    return h_sunrise,sr_time

def Sunset(Latitude,DayOfYear):
    '''
    calculate sunset time
    Latitude: (+) North, (-) South
    DayOfYear: 0 for January 1st
    '''
    f=lambda h:np.cos(ZenithAngle(Latitude,DayOfYear,h)*deg2rad)
    hl,hr=12,24
    h_sunset=Bisection(f,hl,hr)
    ss_time=hour2time(h_sunset)
    return h_sunset,ss_time

def Bisection(func,a,b,max_iter=10000,epsilon=1e-9):
    '''
    bisection method for finding root of a function
    func: a single variable function
    a,b: upper and lower bounds
    '''
    if func(a)*func(b)>0:
        return None
    elif abs(func(a))<epsilon:
        return a
    elif abs(func(b))<epsilon:
        return b
    
    for i in range(max_iter):
        x=(a+b)/2
        if abs(func(x))<epsilon:
            return x
        if func(x)*func(a)<0:
            b=x
        elif func(x)*func(b)<0:
            a=x
        else:
            return None
    print('Maximum number of iterations reached without conversion')
    return x

def hour2time(HourOfDay):
    '''
    convert hour of day (hours since midnight) to time
    '''
    h=np.int0(HourOfDay)
    m=np.int0((HourOfDay-h)*60)
    s=np.int0((HourOfDay-h)*3600-60*m)
    time=datetime.time(h,m,s).isoformat()
    return time

    