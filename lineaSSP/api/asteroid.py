from typing import Optional, List, Union
from .base import BaseAPI
from .config import API_URL
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

    def __init__(self, base_url: Optional[str] = API_URL):
        self.base_url = base_url
        endpoint = '/api/asteroids/'
        super().__init__(base_url, endpoint)
    
    def _format_name(self, list_of_names: List[Union[str,int]]) -> str:
            """
            Format the name of the asteroid.

            Args:
                list_of_names (List[Union[str,int]]): A list of names.

            Returns:
                str: The formatted name of the asteroid.

            """
            if len(list_of_names) > 1:
                print(f'Warning: This endpoint only accepts one name at a time. Using the first name: {list_of_names[0]}')
            name = list_of_names[0]
            # if it a string, firt letter is uppercase
            formated_name = name if name == '' else name.lower().replace(name[0].lower(), name[0].upper(), 1)
            # if starts with a number, all letters are uppercase
            formated_name = formated_name.upper() if formated_name[0].isdigit() else formated_name
            return formated_name
    
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
    
    def dynamical_classes(self) -> List[dict]:
            """
            Fetches the dynamical classes from the 'base_dynclasses' endpoint.

            Returns:
                A list of dictionaries representing the dynamical classes.
            """
            return self._fetch_endpoint('base_dynclasses')
    
    def count(self) -> List[dict]:
            """
            Retrieves the count of asteroids from the API.

            Returns:
                A list of dictionaries containing the count of asteroids.
            """
            return self._fetch_endpoint('count')
    
    def dynamical_subclasses(self) -> List[dict]:
            """
            Fetches the dynamical subclasses of the asteroid.

            Returns:
                A list of dictionaries representing the dynamical subclasses.
            """
            return self._fetch_endpoint('dynclasses')
    
    def with_prediction(self, name: Optional[str]=None) -> List[dict]:
            """
            Retrieves a list of dictionaries containing predictions for the specified asteroid.

            Args:
                name (str, optional): The name of the asteroid. If not provided, will return an error.

            Returns:
                List[dict]: A list of dictionaries containing predictions for the specified asteroid(s).
            """
            return self._fetch_endpoint('with_prediction', name=name)
