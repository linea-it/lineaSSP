# Linea Solar System Portal (lineaSSP)

`lineaSSP` is a Python package designed to simplify interactions with the Solar System Portal API. The package allows users to retrieve and analyze data related to asteroids, their predictions, occultation events, and more.

## Features

- **Prediction Queries**: Access detailed occultation prediction events.
- **Asteroid Queries**: Retrieve detailed information about asteroids based on various parameters such as name, number, and dynamical class.
- **Map Generation**: Create visual maps for occultation events to assist with observation planning.
- **Geographical Filtering**: Filter predictions based on visibility from a specific geographic location.

## Installation

To install the `lineaSSP` package, use pip:

```bash
pip install lineaSSP
```

## Usage

Below are detailed examples demonstrating how to use the `lineaSSP` package.


### Initializing the API

Before making any requests, you need to initialize the API with the desired endpoint:

```python
from lineaSSP import Prediction, Asteroid

# Initialize the Prediction API
prediction_api = Prediction()

# Initialize the Asteroid API
asteroid_api = Asteroid()
```



### Fetching Asteroids by Name

To retrieve information about asteroids by their name:

```python
from lineaSSP import Asteroid

# Initialize the Prediction API
asteroid_api = Asteroid()

# Fetch asteroids by name
asteroids = asteroid_api.by_name(name='Ceres')
print(asteroids)
```

### Fetching Asteroids with Predictions

To get a list of asteroids that have prediction data available:

```python
from lineaSSP import Prediction

# Initialize the Prediction API
prediction_api = Prediction()

# Fetch asteroids with predictions
asteroids_with_predictions = prediction_api.asteroids_with_prediction()
print(asteroids_with_predictions)
```

### Fetching Occultation Predictions by Asteroid Name

To retrieve occultation predictions for a specific asteroid by its name:

```python
from lineaSSP import Prediction

# Initialize the Prediction API
prediction_api = Prediction()

# Fetch occultation predictions for a specific asteroid by its name
predictions = prediction_api.by_name('Chariklo', limit='all')

# Print the predictions
print(predictions)

```
> **IMPORTANT - Queries are paginated by default**
> 
> Use the parameter `limit = 'all'` to retrive all predictions returned by the query. Due to pagination, the query is limited to 1000 entries by default.


### Fetching Occultations Predictions by Date Range

Retrieve occultation events occurring within a specific date range:

```python
params = {
    'date_time_after': '2024-01-01T00:00:00Z',
    'date_time_before': '2024-12-31T23:59:59Z'
}

occultations = prediction_api.get_data(params=params)
print(occultations)
```



### Generating a Map for an Occultation Event

Generate a map directly from the results of an occultation prediction query. 

**Disclaimer:** When using maps generated by `lineaSSP`, please cite the [SORA package](https://sora.readthedocs.io). To customize maps further, please refer to the detailed documentation available at [SORA maps generation documentation](https://sora.readthedocs.io/latest/examples/prediction/maps.html).


This allows for easy visualization of where an occultation event will be observable:

```python
from lineaSSP import generate_map

# Initialize the Prediction API
prediction_api = Prediction()

# Fetch occultations within a certain date range
params = {
    'date_time_after': '2024-01-01T00:00:00Z',
    'date_time_before': '2024-12-31T23:59:59Z'
}
occultations = prediction_api.get_data(params=params)

# Generate the map using the fetched data
# the fucntion will iterate generation all maps in the list
generate_map(data=occultations, dpi=300, path='./')
```
You can use the genearte_map function as a wrapper of the original SORA function passing directly `*args`and `**kwargs`. Please follow the SORA maps documentantion, specially docstrings, to check it out.

### Filtering Predictions by Geographical Location with `geofilter`

The `geofilter` method allows you to filter occultation predictions to see which ones are visible from a specific geographical location. This is particularly useful for planning observations:

```python
from lineaSSP import geofilter, Predictions

latitude = -23.55  # Latitude of the location (e.g., São Paulo, Brazil)
longitude = -46.63  # Longitude of the location
radius = 100  # Search radius in kilometers

# Initialize the Prediction API
prediction_api = Prediction()

# Fetch occultations within a certain date range
params = {
    'date_time_after': '2024-01-01T00:00:00Z',
    'date_time_before': '2024-12-31T23:59:59Z'
}
predictions = prediction_api.get_data(params=params)

# Filter these occultations by geographical visibility
filtered_predictions = prediction_api.geofilter(predictions, latitude=latitude, longitude=longitude, radius=radius)

print(filtered_predictions)
```


## API Query Parameters

The `lineaSSP` package allows querying the API with various parameters to retrieve specific data when passing the `params` dictionary. Below is a detailed table of all the parameters that can be used with the `Prediction` and `Asteroid` classes.

### Asteroid Query Parameters

| Parameter              | Description                                                       | Type    |
|------------------------|-------------------------------------------------------------------|---------|
| `base_dynclass`        | Object's base dynamical classification (e.g., KBO, Centaur)       | String  |
| `dynclass`             | Object's dynamical subclass (e.g., Resonant, Inner)               | String  |
| `name`                 | Object name (official or provisional designation)                 | String  |
| `number`               | Object number (not all objects have numbers assigned)             | Integer |
| `provisional_designation`| Provisional


### Occultation Query Parameters

| Parameter              | Description                                                       | Type    |
|------------------------|-------------------------------------------------------------------|---------|
| `date_time_after`      | Fetch occultations occurring after this date                      | String  |
| `date_time_before`     | Fetch occultations occurring before this date                     | String  |
| `diameter_max`         | Maximum diameter (km)                                             | Double  |
| `diameter_min`         | Minimum diameter (km)                                             | Double  |
| `base_dynclass`        | Object's base dynamical classification  (Skybot)                  | String  |
| `dynclass`             | Object's dynamical subclass (Skybot)                              | String  |
| `event_duration_max`   | Maximum event duration (seconds)                                  | Double  |
| `event_duration_min`   | Minimum event duration (seconds)                                  | Double  |
| `jobid`                | Job ID of the occultation event                                   | Integer |
| `latitude`             | Latitude for geographical filtering                               | Double  |
| `local_solar_time_after`| Local Solar Time After                                           | String  |
| `local_solar_time_before`| Local Solar Time Before                                         | String  |
| `location_radius`      | Radius around the location to check for visibility                | Double  |
| `longitude`            | Longitude for geographical filtering                              | Double  |
| `magnitude_drop_max`   | Maximum expected star's magnitude drop                            | Double  |
| `magnitude_drop_min`   | Minimum expected star's magnitude drop                            | Double  |
| `magnitude_max`        | Maximum magnitude (Gaia G magnitude)                              | Double  |
| `magnitude_min`        | Minimum magnitude (Gaia G magnitude)                              | Double  |
| `nightside`            | Filter for occultations on the nightside                          | Boolean |
| `name`                 | Object name (multiple values may be separated by commas)          | Array of Strings |
| `number`               | Object number (multiple values may be separated by commas)        | Array of Strings |
| `provisional_designation`| Provisional designation assigned by the International Astronomical Union (IAU) | String  |



## Contributing

We welcome contributions to enhance the functionality of `lineaSSP`. Please submit issues and pull requests on the [GitHub repository](https://github.com/linea-it/lineaSSP).



## License

This project is licensed under the MIT License. See the LICENSE file for more details.



