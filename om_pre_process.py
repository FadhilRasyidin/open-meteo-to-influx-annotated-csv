import pandas as pd
import csv
import os
import glob
import dload


# Define a function to replace '/' with '-'
def replace_slash_with_dash(column_name):
    return column_name.replace('/', '_')


# defining input csv file
url = ('https://api.open-meteo.com/v1/forecast?latitude=22.714183&longitude=120.337895&hourly=temperature_2m,'
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
dload.save(url, "forecast.csv", True)
input_csv_file = 'forecast.csv'

# pre-processing csv open-meteo
with open(input_csv_file, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

first_two_rows = data[:2]

with open('location specs.csv', 'w', newline='') as new_file:
    writer = csv.writer(new_file)
    writer.writerows(first_two_rows)

del data[:3]

with open(input_csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

# defining location data
location_specs = 'location specs.csv'

# specifying columns to concat and initiating dataframes
df = pd.read_csv(input_csv_file)
df2 = pd.read_csv(location_specs)
df3 = pd.DataFrame(data={'': ['']})

# concat the two dataframes
frames = [df3, df2, df]
result = pd.concat(frames, axis=1)

# iterate through the columns and rename them
result = result.rename(columns=replace_slash_with_dash)

# fill NaN
result.ffill(inplace=True)

# define the directory where you want to save the CSV files
output_directory = 'openMeteoParameters'

# make sure the directory exists, or create it if it doesn't
os.makedirs(output_directory, exist_ok=True)

# loop through the columns and save the CSV files to the specified directory
for column in result.columns[8:]:
    selected_columns_df = result[
        ['', 'latitude', 'longitude', 'elevation', 'utc_offset_seconds', 'timezone',
         'timezone_abbreviation', 'time', 'is_day ()', 'weather_code (wmo code)', column]]

    # construct the full path to the CSV file in the specified directory
    output_file_path = os.path.join(output_directory, f'{column}.csv')

    # save the DataFrame to the CSV file in the specified directory
    selected_columns_df.to_csv(output_file_path, index=False, sep=',')
