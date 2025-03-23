import pandas as pd
from constant import us_states_abbr_to_full

file_path = "data/national_places.txt"
cities_df = pd.read_csv(file_path, delimiter='|', dtype=str, encoding="latin1")

unique_cities_df = cities_df[['STATE', 'PLACENAME']].drop_duplicates()

unique_cities_with_states = unique_cities_df.apply(
    lambda row: f"{row['PLACENAME']} {us_states_abbr_to_full[row['STATE']]}",
    axis=1
)
output_path = "data/unique_cities.txt"
unique_cities_with_states.to_csv(output_path, index=False, header=False)
