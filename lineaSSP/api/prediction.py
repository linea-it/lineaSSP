import requests
from typing import Optional, List
from .base import BaseAPI
from .config import API_URL

class Prediction(BaseAPI):
    """
    Represents a prediction object that interacts with the prediction API.

    Args:
        base_url (str, optional): The base URL of the API. Defaults to API_URL.

    Raises:
        Exception: If no valid endpoint is found.

    Attributes:
        base_url (str): The base URL of the API.
    """

    def __init__(self, base_url: Optional[str] = API_URL):
        self.base_url = base_url
        endpoint = self._detect_endpoint()
        super().__init__(base_url, endpoint)

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
    
    def get_or_create_map(self, id: int) -> List[dict]:
            """Fetches the map with the given ID if it exists, otherwise creates a new map.

            Args:
                id (int): The ID of the map.

            Returns:
                List[dict]: A list of dictionaries representing the map.
            """
            return self._fetch_endpoint('get_or_create_map', id=id)

