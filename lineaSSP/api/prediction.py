import requests
from typing import Optional, List
from .base import BaseAPI, BASE_URL
from sora.prediction.occmap import plot_occ_map

from typing import Optional, List, Dict, Any

def generate_map(*args, 
                 data: Optional[List[Dict[str, Any]]] = None, 
                 lncolor="#00468D", 
                 ptcolor="#00468D", 
                 ercolor="#D32F2F", 
                 outcolor="#D3D3D3", 
                 **kwargs) -> None:
    """
    Generates a map based on either the provided data from an API query or direct arguments, utilizing the `plot_occ_map` function.

    This function can be used in two primary ways:
    1. By passing a list of dictionaries via the `data` parameter, where each dictionary is the result of an API query.
    2. By providing direct arguments to the `plot_occ_map` function along with optional keyword arguments.

    Parameters:
    -----------
    *args: 
        Positional arguments passed directly to `generate_map` when not using `data`.
    
    data: Optional[List[Dict[str, Any]]]
        A list of dictionaries obtained from an API query, each containing the necessary parameters for plotting.
        Each dictionary should include the following keys:
            - name (str): Name of the object to be plotted.
            - diameter (float): Diameter of the object.
            - ra_star_candidate (str): Right Ascension of the object.
            - dec_star_candidate (str): Declination of the object.
            - date_time (str): Date and time of the event.
            - closest_approach (float): Closest approach distance.
            - position_angle (float): Position angle.
            - velocity (float): Velocity of the object.
            - delta (float): Distance to the object.
            - g_star (float): Magnitude of the object.
            - long (float): Longitude of the object.
    
    lncolor: str, optional, default="#00468D"
        Color of the lines in the map.
    
    ptcolor: str, optional, default="#00468D"
        Color of the points in the map.
    
    ercolor: str, optional, default="#D32F2F"
        Color of the error lines in the map.
    
    outcolor: str, optional, default="#D3D3D3"
        Color of the outer region of the map.
    
    **kwargs:
        Additional keyword arguments passed to `plot_occ_map`. Only the following are allowed:
        - alpha, arrow, atcolor, atm, centermap_delta, centermap_geo, centerproj, chcolor, 
          chord_delta, chord_geo, countries, cpoints, cscale, dpi, ercolor, error, fmt, hcolor, 
          heights, labels, lncolor, mapsize, mapstyle, meridians, nameimg, nscale, offset, outcolor, 
          parallels, path, pscale, ptcolor, resolution, ring, rncolor, site_name, sites, sscale, 
          states, zoom, site_box_alpha, band

    Raises:
    -------
    ValueError:
        If `data` is not a dictionary or a list of dictionaries.
    
    Examples:
    ---------
    Example 1: Using the function with a list of dictionaries obtained from an API query via `data` parameter:
    
    ```python
    data = api_query()  # Assume this is a function that fetches data from an API and returns a list of dictionaries

    generate_map(data=data, zoom=10, dpi=300)
    ```

    Example 2: Using the function with direct arguments:
    
    ```python
    generate_map(
        'Object2', 5.0, '12 30 00 -45 00 00', '2024-08-01T12:00:00', 0.1, 110.5, 
        7.0, 10.5, mag=14.0, longi=60.0, error=100
    )
    ```

    Notes:
    ------
    - The `plot_occ_map` function is called internally within this function, and any exception 
      that occurs during its execution will be caught and printed.
    - Ensure that the `kwargs` provided are in the list of allowed keyword arguments; 
      otherwise, they will be filtered out.
    """
    allowed_kwargs = [
        'alpha', 'arrow', 'atcolor', 'atm', 'centermap_delta', 'centermap_geo', 'centerproj',
        'chcolor', 'chord_delta', 'chord_geo', 'countries', 'cpoints', 'cscale', 'dpi', 'ercolor',
        'error', 'fmt', 'hcolor', 'heights', 'labels', 'lncolor', 'mapsize', 'mapstyle', 'meridians',
        'nameimg', 'nscale', 'offset', 'outcolor', 'parallels', 'path', 'pscale', 'ptcolor',
        'resolution', 'ring', 'rncolor', 'site_name', 'sites', 'sscale', 'states', 'zoom',
        'site_box_alpha', 'band'
    ]
    
    if data is not None:
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("`data` must be a dictionary or a list of dictionaries.")
        
        for value in data:
            name = value.get('name', '').replace(' ', '_')
            radius = value.get('diameter', 0) / 2 if value.get('diameter') else 0
            coord = f"{value.get('ra_star_candidate', '')} {value.get('dec_star_candidate', '')}"
            time = value.get('date_time', '')
            ca = value.get('closest_approach', 0)
            pa = value.get('position_angle', 0)
            vel = value.get('velocity', 0)
            dist = value.get('delta', 0)
            mag = value.get('g_star', 0)
            longi = value.get('long', 0)
            
            # Filter kwargs to include only allowed keys before calling plot_occ_map
            filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_kwargs}

            try:
                plot_occ_map(
                    name, radius, coord, time, ca, pa, vel, dist, mag=mag, longi=longi, lncolor=lncolor, ptcolor=ptcolor, ercolor=ercolor, outcolor=outcolor, **filtered_kwargs
                )
            except Exception as e:
                print(f"Error while plotting map for {name}: {str(e)}")
    else:
        # Filter kwargs to include only allowed keys before calling plot_occ_map
        filtered_kwargs = {k: v for k, v in kwargs.items() if k in allowed_kwargs}

        try:
            plot_occ_map(*args, lncolor=lncolor, ptcolor=ptcolor, ercolor=ercolor, outcolor=outcolor, **filtered_kwargs)
        except Exception as e:
            print(f"Error while plotting map: {str(e)}")



class Prediction(BaseAPI):
    """
    Represents a prediction object that interacts with the prediction API.

    Raises:
        Exception: If no valid endpoint is found.
    """

    def __init__(self, base_url: str=BASE_URL, endpoint: str=""):
        # Call the superclass's __init__ method with the appropriate base_url
        super().__init__(base_url=base_url, endpoint=endpoint)
        self.endpoint = self._detect_endpoint()

    #TODO: Update this method when the api endpoint is fixed
    def _detect_endpoint(self) -> str:
        """
        Detects the valid endpoint for the prediction API.

        Returns:
            str: The valid endpoint URL.

        Raises:
            Exception: If no valid endpoint is found.
        """
        endpoints = {
            "predictions": "/api/predictions",
            "occultations": "/api/occultations",
        }
        for key, endpoint in endpoints.items():
            url = f"{self.base_url}{endpoint}"
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return endpoint
            except requests.RequestException:
                continue
        raise Exception("No valid endpoint found")

    def _fetch_endpoint(self, endpoint: str, id: Optional[int]=None) -> str:
        """
        Fetches data from the specified endpoint.

        Args:
            endpoint (str): The endpoint to fetch data from.
            id (Optional[int]): The ID of the data to fetch (default: None).

        Returns:
            str: The fetched data in JSON format if successful, otherwise a dictionary
                 with an error message and the HTTP status code.

        """
        id_map = f"{id}/" if id is not None else ""
        url = f"{self.base_url}{self.endpoint}/{id_map}{endpoint}/"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'An error occurred fetching the data', 'status_code': response.status_code}
    
    def asteroids_with_prediction(self) -> List[dict]:
        """Fetches the asteroids with prediction from the endpoint.

        Returns:
            A list of dictionaries representing the asteroids with prediction.
        """
        return self._fetch_endpoint('asteroids_with_prediction')
    
    def dynamical_classes_with_prediction(self) -> List[dict]:
        """Fetches the endpoint 'base_dynclass_with_prediction' and returns the result.

        Returns:
            A list of dictionaries representing the dynamical classes with prediction.
        """
        return self._fetch_endpoint('base_dynclass_with_prediction')
    
    def dynamical_subclasses_with_prediction(self) -> List[dict]:
        """Fetches the endpoint 'dynclass_with_prediction' and returns the result.

        Returns:
            A list of dictionaries representing the dynamical subclasses with prediction.
        """
        return self._fetch_endpoint('dynclass_with_prediction')                            


