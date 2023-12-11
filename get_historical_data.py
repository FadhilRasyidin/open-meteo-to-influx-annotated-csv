from om_pre_process import *


def main():
    latitude = sys.argv[1]
    longitude = sys.argv[2]

    # Historical Weather Data
    historical_url = (
        f'https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date=2010-01-01'
        '&end_date=2023-11-24&hourly=temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,'
        'precipitation,rain,snowfall,snow_depth,weather_code,pressure_msl,surface_pressure,cloud_cover,'
        'cloud_cover_low,cloud_cover_mid,cloud_cover_high,et0_fao_evapotranspiration,vapour_pressure_deficit,'
        'wind_speed_10m,wind_speed_100m,wind_direction_10m,wind_direction_100m,wind_gusts_10m,is_day,'
        'sunshine_duration,shortwave_radiation,direct_radiation,diffuse_radiation,direct_normal_irradiance,'
        'terrestrial_radiation,shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,'
        'direct_normal_irradiance_instant,'
        'terrestrial_radiation_instant&timeformat=unixtime&timezone=auto&models=best_match&format=csv')
    historical_output = 'historical.csv'
    historical_specs_output = 'historical_specs.csv'
    historical_output_directory = f'HistoricalParameters_{longitude[:6]}_{latitude[:6]}'

    fetch_weather_data(historical_url, historical_output)
    process_weather_data(historical_output, historical_specs_output, historical_output_directory)


if __name__ == "__main__":
    main()
