import requests
from tqdm import tqdm
from typing import Union, Optional, List, Dict
from collections import OrderedDict
import re

BASE_URL = 'https://solarsystem.linea.org.br'
# BASE_URL = 'http://host.docker.internal'

class BaseAPI:
    """
    BaseAPI class for interacting with the API.

    Args:
        base_url (Optional[str]): The base URL of the API. Defaults to API_URL.
        endpoint (str): The endpoint of the API.

    Attributes:
        base_url (str): The base URL of the API.
        endpoint (str): The endpoint of the API.

    Methods:
        _format_name_values: Formats the name values.
        _format_name: Formats a list of names.
        _replace_key: Replaces a key in a dictionary.
        get_data: Retrieves data from the API.

    """

    def __init__(self, base_url: str = BASE_URL, endpoint: str = "", page_size: int = 1000):
        self.base_url = base_url
        self.endpoint = endpoint
        self.page_size = page_size
    

    def _parse_values(self, params: dict) -> dict:
        if "name" in params.keys():
            segments_in_name = params["name"].strip().split(' ')
            if len(segments_in_name) == 1:
                name = params["name"].strip().capitalize()
            else:
                name = " ".join([segment.upper() for segment in segments_in_name])
            params["name"] = name
        
        if "principal_designation" in params.keys():
            params["principal_designation"] = params["principal_designation"].strip().upper()

        if "date_time_after" in params.keys():
            try:
                self._validate_datetime(params["date_time_after"])
            except ValueError:
                raise InvalidDatetimeFormat
        
        if "date_time_before" in params.keys():
            try:
                self._validate_datetime(params["date_time_before"])
            except ValueError:
                raise InvalidDatetimeFormat
        
        return params

    def _validate_datetime(self, date_string):
        iso_8601_regex = re.compile(
            r'^\d{4}-\d{2}-\d{2}$|'  # Date only (YYYY-MM-DD)
            # r'^\d{4}-\d{2}-\d{2}[T\s]\d{2}$|'  # Date and hour (YYYY-MM-DDTHH or YYYY-MM-DD HH)
            r'^\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}$|'  # Date, hour, and minute (YYYY-MM-DDTHH:MM or YYYY-MM-DD HH:MM)
            r'^\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$'  # Full date and time (YYYY-MM-DDTHH:MM:SS[.fff][Z|±HH:MM] or YYYY-MM-DD HH:MM:SS[.fff][Z|±HH:MM])
        )
        if bool(iso_8601_regex.match(date_string)):
            return True
        else:
            raise InvalidDatetimeFormat()

    def _replace_key(self, data: dict, old_key: str, new_key: str):
        """
        Replaces a key in a dictionary.

        Args:
            data (dict): The dictionary to be modified.
            old_key (str): The key to be replaced.
            new_key (str): The new key.

        Returns:
            dict: The modified dictionary.

        """
        if old_key in data:
            items = list(data.items())
            index = [key for key, value in items].index(old_key)
            items[index] = (new_key, data.pop(old_key))
            return dict(OrderedDict(items))
        return data
    
    def _fetch_data(self, params: dict, id: Optional[int] = None) -> dict:
        """
        Fetches data from the API.

        Args:
            params (dict): The parameters for the API request.
            id (Optional[int]): The ID of the data to fetch. Defaults to None.

        Returns:
            dict: The fetched data.

        """
        if id is not None:
            url = f"{self.base_url}{self.endpoint}/{id}"
            response = requests.get(url, params={})
            if response.status_code == 200:
                result = {'count': 1, 'results':[response.json()]}
                return result
        else:
            url = f"{self.base_url}{self.endpoint}"
            response = requests.get(url, params=params)
            result = response.json()
            return result
        
        if response.status_code != 200:
            return {'count': 0, 
                    'results': [{'error': 'An error occurred fetching the data', 'status_code': response.status_code}]}
    
    def _drop_columns(self, data: List[dict]) -> List[str]:
        columns_to_remove = ["map_url","proper_motion","ct","multiplicity_flag",
                   "g_mag_vel_corrected","rp_mag_vel_corrected",
                   "h_mag_vel_corrected","instant_uncertainty",
                   "ra_star_with_pm","dec_star_with_pm","ra_star_to_date",
                   "dec_star_to_date","ra_target_apparent","dec_target_apparent",
                   "e_ra_target","e_dec_target","ephemeris_version",
                   "rms","last_obs_included","obs_source","orb_ele_source",
                   "nima","job_id"]
        filtered_data = [{k: v for k, v in item.items() if k not in columns_to_remove} for item in data]
        return filtered_data
    
    def get_data(self, params: Optional[Union[dict, None]]=None, id: Optional[int]=None, limit: Optional[Union[int, str, None]]=None, show_bar: Optional[bool]=True) -> dict:
        """
        Retrieves data from the API.

        Args:
            params (Optional[Union[dict, None]]): The parameters for the API request. Defaults to None.
            id (Optional[int]): The ID of the data to retrieve. Defaults to None.
            limit (Optional[Union[int, None]]): The maximum number of results to retrieve. Defaults to PAGE_SIZE.
            show_bar (Optional[bool]): Whether to show a progress bar. Defaults to True.

        Returns:
            dict: The retrieved data.

        """
        params = params if params is not None else {}
        
        limit = self.page_size if limit is None else limit
        params['pageSize'] = self.page_size
        params['page'] = 1

        # parse ill formated values
        params = self._parse_values(params)
        
        fetch_results = self._fetch_data(params, id=id)
        
        limit = fetch_results['count'] if limit == 'all' else limit # forçar pegar todos os resultados.
        # isto é calculado para criar o iterador tqdm. usar while 'next' is not None tornaria a barra de progresso muito complicada
        n_pages = (limit // self.page_size) + 1 if (limit % self.page_size) > 0 else (limit // self.page_size)
        
        output = fetch_results['results']
        if fetch_results['count'] == 0:
            return output

        iterable = range(1, n_pages)
        if show_bar and n_pages > 1:
            iterable = tqdm(iterable, desc='Retrieving predictions', bar_format='{l_bar}{bar}|')
        
        for i in iterable:
            params['page'] = i + 1 
            fetch_results = self._fetch_data(params, id=id)
            if 'results' in fetch_results:
                output += fetch_results['results']

        #TODO: The api should return the correct key, update this when the api is fixed
        output = [self._replace_key(item, 'principal_designation', 'provisional_designation') for item in output[0:limit]]
        # output = self._drop_columns(output)
        return output
    
    def by_provisional_designation(self, provisional_designation: str, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> Union[dict, List[dict]]:
        """Fetches the prediction by provisional designation.

        Args:
            provisional_designation (str): The provisional designation of the asteroid.
            limit (Optional[Union[int, str, None]], optional): Limit for the results. Defaults to 'all'.
            show_bar (Optional[bool], optional): Whether to show the progress bar. Defaults to True.

        Returns:
            A dictionary if the result contains only one entry, or a list of dictionaries if more.
        """
        # Type checking for provisional_designation
        if not isinstance(provisional_designation, str):
            raise TypeError(f"The provisional_designation must be a string, got {type(provisional_designation).__name__} instead.")
        
        params = {'name': provisional_designation}
        
        # Fetch the data
        result = self.get_data(params, limit=limit, show_bar=show_bar)

        # If the result is a list with a length of 1, return the first element
        if isinstance(result, list) and len(result) == 1:
            return result[0]

        # Otherwise, return the entire result (list of dictionaries)
        return result

    
    def by_name(self, name: str, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> Union[dict, List[dict]]:
        """Fetches the prediction by name.

        Args:
            name (str): The name of the asteroid.
            limit (Optional[Union[int, str, None]], optional): Limit for the results. Defaults to 'all'.
            show_bar (Optional[bool], optional): Whether to show the progress bar. Defaults to True.

        Raises:
            TypeError: If `name` is not a string.

        Returns:
            A dictionary if the result contains only one entry, or a list of dictionaries if more.
        """
        # Type checking for name
        if not isinstance(name, str):
            raise TypeError(f"The name must be a string, got {type(name).__name__} instead.")
        
        params = {'name': name}
        
        # Fetch the data
        result = self.get_data(params, limit=limit, show_bar=show_bar)

        # If the result is a list with a length of 1, return the first element
        if isinstance(result, list) and len(result) == 1:
            return result[0]

        # Otherwise, return the entire result (list of dictionaries)
        return result

    
    def by_number(self, number: int, limit: Optional[Union[int, str, None]]='all', show_bar: Optional[bool]=True) -> Union[dict, List[dict]]:
        """Fetches the prediction by number.

        Args:
            number (int or float): The number of the asteroid.
            limit (Optional[Union[int, str, None]], optional): Limit for the results. Defaults to 'all'.
            show_bar (Optional[bool], optional): Whether to show the progress bar. Defaults to True.

        Raises:
            TypeError: If `number` is not an int or float.

        Returns:
            A dictionary if the result contains only one entry, or a list of dictionaries if more.
        """
        # Check if number is an int or float
        if not isinstance(number, (int, float)):
            raise TypeError(f"The number must be an int or float, got {type(number).__name__} instead.")
        
        params = {'number': number}
        
        # Fetch the data
        result = self.get_data(params, limit=limit, show_bar=show_bar)

        # If the result is a list with a length of 1, return the first element
        if isinstance(result, list) and len(result) == 1:
            return result[0]

        # Otherwise, return the entire result (list of dictionaries)
        return result

    
 
class InvalidDatetimeFormat(Exception):
    def __init__(self, message="The provided string does not match the accepted date/datetime format."):
        self.message = message
        self.examples = [
            "Date only:                 YYYY-MM-DD",                    # Date only
            "Date, hour, and minute:    YYYY-MM-DDTHH:MM",              # Date, hour, and minute
            "Date and time (UTC):       YYYY-MM-DDTHH:MM:SSZ",          # Date and time (UTC)
            "Date and time with offset: YYYY-MM-DDTHH:MM:SS±HH:MM"      # Date and time with offset
        ]
        super().__init__(self.message)

    def __str__(self):
        example_str = "\n".join(self.examples)
        return f"{self.message}\nAccepted formats:\n{example_str}"