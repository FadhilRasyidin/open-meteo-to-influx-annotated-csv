import csv
import os
import dload
import pandas as pd
import sys


def replace_slash_with_dash(column_name):
    return column_name.replace('/', '_')


def fetch_weather_data(url, output_filename):
    dload.save(url, output_filename, True)


def process_weather_data(input_csv_file, specs_csv_file, output_directory):
    with open(input_csv_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    # Extracting first two rows and writing to specs file
    first_two_rows = data[:2]
    with open(specs_csv_file, 'w', newline='') as new_file:
        writer = csv.writer(new_file)
        writer.writerows(first_two_rows)

    # Removing header rows and updating the CSV file
    del data[:3]
    with open(input_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    df = pd.read_csv(input_csv_file)
    df_specs = pd.read_csv(specs_csv_file)
    df_empty = pd.DataFrame(data={'': ['']})

    frames = [df_empty, df_specs, df]
    result = pd.concat(frames, axis=1)
    result = result.rename(columns=replace_slash_with_dash)
    result.ffill(inplace=True)

    os.makedirs(output_directory, exist_ok=True)

    for column in result.columns[8:]:
        selected_columns_df = result[
            ['', 'latitude', 'longitude', 'elevation', 'utc_offset_seconds', 'timezone',
             'timezone_abbreviation', 'time', 'is_day ()', 'weather_code (wmo code)', column]]

        output_file_path = os.path.join(output_directory, f'{column}.csv')
        selected_columns_df.to_csv(output_file_path, index=False, sep=',')


def main():
    latitude = sys.argv[1]
    longitude = sys.argv[2]

    # Forecast Weather Data
    forecast_url = (
        f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,'
        'relative_humidity_2m,dew_point_2m,apparent_temperature,precipitation_probability,precipitation,rain,showers,'
        'snowfall,snow_depth,weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,cloud_cover_mid,'
        'cloud_cover_high,visibility,evapotranspiration,et0_fao_evapotranspiration,vapour_pressure_deficit,'
        'wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_speed_180m,wind_direction_10m,wind_direction_80m,'
        'wind_direction_120m,wind_direction_180m,wind_gusts_10m,temperature_80m,temperature_120m,temperature_180m,'
        'uv_index,uv_index_clear_sky,is_day,cape,freezing_level_height,sunshine_duration,shortwave_radiation,'
        'direct_radiation,diffuse_radiation,direct_normal_irradiance,terrestrial_radiation,'
        'shortwave_radiation_instant,direct_radiation_instant,diffuse_radiation_instant,'
        'direct_normal_irradiance_instant,terrestrial_radiation_instant,temperature_1000hPa,relative_humidity_1000hPa,'
        'cloud_cover_1000hPa,windspeed_1000hPa,winddirection_1000hPa,'
        'geopotential_height_1000hPa&timeformat=unixtime&timezone=auto&models=best_match&format=csv')
    forecast_output = 'forecast.csv'
    location_specs_output = 'location_specs.csv'
    forecast_output_directory = f'ForecastParameters_{longitude[:6]}_{latitude[:6]}'

    fetch_weather_data(forecast_url, forecast_output)
    process_weather_data(forecast_output, location_specs_output, forecast_output_directory)


if __name__ == "__main__":
    main()
