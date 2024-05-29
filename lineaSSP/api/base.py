import requests
from tqdm import tqdm
from typing import Union, Optional, List
from collections import OrderedDict
from .config import API_URL, PAGE_SIZE



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

    def __init__(self, base_url: Optional[str] = API_URL, endpoint: str = ""):
        self.base_url = base_url
        self.endpoint = endpoint
    
    def _format_name_values(self, name: str) -> str:  
        """
        Formats the name values.

        Args:
            name (str): The name to be formatted.

        Returns:
            str: The formatted name.

        """
        formated_name = name if name == '' else name.lower().replace(name[0].lower(), name[0].upper(), 1)
        formated_name = formated_name.upper() if formated_name[0].isdigit() else formated_name
        return formated_name

    def _format_name(self, list_of_names: List[Union[str,int]]) -> str:
        """
        Formats a list of names.

        Args:
            list_of_names (List[Union[str,int]]): The list of names to be formatted.

        Returns:
            str: The formatted names separated by commas.

        """
        return ','.join([self._format_name_values(str(name)) for name in list_of_names])
    
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
    
    
    def get_data(self, params: Optional[Union[dict, None]]=None, id: Optional[int]=None, limit: Optional[Union[int, None]]=PAGE_SIZE, show_bar: Optional[bool]=True) -> dict:
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
        
        if ('name' in params.keys()) and (isinstance(params['name'], list)):        
            params['name'] = self._format_name(params['name'])
        
        fetch_results = self._fetch_data(params, id=id)

        limit = limit if limit is not None else fetch_results['count']
        n_pages = (limit // PAGE_SIZE) + 1 if (limit % PAGE_SIZE) > 0 else (limit // PAGE_SIZE)
        
        output = fetch_results['results']
        if fetch_results['count'] == 0:
            return output

        params['pageSize'] = limit if (limit is not None) and (limit < PAGE_SIZE) else PAGE_SIZE
        iterable = range(1, n_pages)
        if show_bar and n_pages > 1:
            iterable = tqdm(iterable, desc='Retrieving predictions')

        for i in iterable:
            params['page'] = i
            fetch_results = self._fetch_data(params, id=id)
            if 'results' in fetch_results:
                output += fetch_results['results']
        
        #TODO: The api should return the correct key, update this when the api is fixed
        output = [self._replace_key(item, 'principal_designation', 'provisional_designation') for item in output[0:limit]]

        return output