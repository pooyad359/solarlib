from setuptools import find_packages, setup

setup(
    name='solarlib',
    packages=find_packages(),
    version='0.1.0',
    description='A library for calculating solar irradiance, sunrise, sunset, and more. ',
    author='Pooya Darvehei',
    url='https://github.com/pooyad359/solarlib',
    download_url='https://github.com/pooyad359/solarlib/archive/v0.1.0.tar.gz',
    license='MIT',
    install_requires=['pytz']
)
