from typing import Optional, List, Union
from .base import BaseAPI, BASE_URL
from .prediction import Prediction
import requests

class Asteroid(BaseAPI):
    """
    Represents an Asteroid API.

    Args:
        base_url (str, optional): The base URL of the API. Defaults to API_URL.

    Attributes:
        base_url (str): The base URL of the API.
        endpoint (str): The endpoint for the Asteroid API.

    """

    def __init__(self, base_url: str=BASE_URL, endpoint: str=""):
        super().__init__(base_url=base_url, endpoint=endpoint)
        self.endpoint = "/api/asteroids"       
    
    def _fetch_endpoint(self, endpoint: str, name: Optional[str]=None) -> str:
        """
        Fetches data from the specified endpoint.

        Args:
            endpoint (str): The endpoint to fetch data from.
            name (str, optional): The name parameter for the endpoint. Defaults to None.

        Returns:
            str: The fetched data as a JSON string.

        Raises:
            dict: If an error occurs while fetching the data, a dictionary with the error message and status code is returned.
        """
        obj_name = f"" if name is None else f"?name={name}"
        if name is None and endpoint == 'with_prediction':
            print("Warning: This endpoint requires a name. Please provide a name.")
            return {'error': 'This endpoint requires a name. Please provide a name.'}
        url = f"{self.base_url}{self.endpoint}/{endpoint}/{obj_name}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'An error occurred fetching the data', 'status_code': response.status_code}
    
    def dynamical_classes(self) -> Union[str,List[dict]]:
        """
        Fetches the dynamical classes from the 'base_dynclasses' endpoint.

        Returns:
            A list of dictionaries representing the dynamical classes.
        """
        dynamical_classes = self._fetch_endpoint('base_dynclasses')
        dynamical_classes = dynamical_classes['results'].sort() if 'results' in dynamical_classes.keys() else 'Unavailable'
        return dynamical_classes
    
    def count(self) -> Union[str,int]:
        """
        Retrieves the count of asteroids from the API.

        Returns:
            A list of dictionaries containing the count of asteroids.
        """
        count = self._fetch_endpoint('count')
        count = count['count'] if 'count' in count.keys() else 'Unavailable'
        return count
    
    def dynamical_subclasses(self) -> List[dict]:
        """
        Fetches the dynamical subclasses of the asteroid.

        Returns:
            A list of dictionaries representing the dynamical subclasses.
        """
        dynamical_subclasses = self._fetch_endpoint('dynclasses')
        dynamical_subclasses = dynamical_subclasses['results'].sort() if 'results' in dynamical_subclasses.keys() else 'Unavailable'
        return dynamical_subclasses
    
    def get_predictions_by_provisional_designation(self, provisional_designation: str, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> List[dict]:
        return Prediction().by_provisional_designation(provisional_designation, limit=limit, show_bar=show_bar)

    def get_predictions_by_name(self, name: str, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> List[dict]:
        return Prediction().by_name(name, limit=limit, show_bar=show_bar)

    def get_predictions_by_number(self, number: int, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> List[dict]:
        return Prediction().by_number(number, limit=limit, show_bar=show_bar)