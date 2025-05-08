import requests
import json

class LeantimeClient:
    def __init__(self, base_url, api_key, logger):
        """
        Initialize the Leantime client with API key authentication.

        Args:
            base_url (str): The base URL of your Leantime installation
            api_key (str): Your Leantime API key (format: lt_USER_KEY)
            logger: Logger object
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        }
        self.logger = logger
        self.logger.info(f"Initialized Leantime client for {base_url}")


    def _filter_results(self, date: dict) -> list:
        filtered_results = []
        for item in date:
            # Create a new dictionary with only the non-numeric keys
            filtered_data = {k: v for k, v in item.items() if not k.isdigit()}
            filtered_results.append(filtered_data)

        return filtered_results



    def get_all_open_user_tickets(self, user_id=None):
        """
        Get all open tickets for a specific user across all projects.
        If user_id is None, gets open tickets for the authenticated user (via API key).

        Args:
            user_id (int, optional): User ID to get tickets for. Defaults to current user.

        Returns:
            list: List of ticket objects
        """
        endpoint = f"{self.base_url}/api/jsonrpc"

        # Build parameters
        params = {}
        if user_id:
            params['userId'] = user_id

        # Create JSON-RPC request
        payload = {
            "jsonrpc": "2.0",
            "method": "leantime.rpc.Tickets.getAllOpenUserTickets",
            "params": params,
            "id": 1
        }

        self.logger.debug(f"Sending request to {endpoint} with payload: {json.dumps(payload)}")

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json()
            self.logger.debug(f"Received response: {json.dumps(result)[:500]}...")  # Truncate long responses

            if 'error' in result:
                self.logger.error(f"API error: {result['error']}")
                return []

            user_tickets = result.get('result', [])

            return self._filter_results(user_tickets)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            raise


    def get_users(self):
        endpoint = f"{self.base_url}/api/jsonrpc"

        payload = {
            "jsonrpc": "2.0",
            "method": "leantime.rpc.Users.getAll",
            "params": {
                "activeOnly": False  # Set to True if you only want active users
            },
            "id": 1  # Request identifier
        }

        self.logger.debug(f"Getting user details")

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()

            result = response.json()

            users = result.get('result', [])
            result = self._filter_results(users)

            if 'error' in result:
                self.logger.error(f"API error when getting users: {result['error']}")
                return {}

            self.logger.debug(f"Successfully retrieved users")
            return result

        except Exception as e:
            self.logger.error(f"Error getting ticket users: {str(e)}")
            raise
