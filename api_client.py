import requests
import streamlit as st

class FootballAPIClient:
    def __init__(self):
        # Accessing the API key from Streamlit Secrets
        self.api_key = st.secrets["FOOTBALL_DATA_API_KEY"]
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {"X-Auth-Token": self.api_key}

    def get_available_leagues(self):
        """Returns the list of leagues supported by the free tier."""
        return {
            "La Liga": "PD", 
            "Premier League": "PL", 
            "Bundesliga": "BL1", 
            "Serie A": "SA", 
            "Ligue 1": "FL1"
        }

    def get_standings(self, league_code):
        """Fetches the current league table with goals and games played."""
        url = f"{self.base_url}/competitions/{league_code}/standings"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()
            # Grabbing the 'Total' standings table
            table = data['standings'][0]['table']
            # Map team name to its full statistics dictionary
            return {entry['team']['name']: entry for entry in table}
        except Exception as e:
            st.error(f"Error loading standings: {e}")
            return {}

    def get_team_matches(self, team_id):
        """Fetches all season matches for a specific team."""
        url = f"{self.base_url}/teams/{team_id}/matches"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.json().get('matches', [])
        except:
            return []

    def get_fixtures(self, league_code, date_obj):
        """Fetches matches for a specific date across the league."""
        url = f"{self.base_url}/competitions/{league_code}/matches"
        ds = date_obj.isoformat()
        params = {"dateFrom": ds, "dateTo": ds}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            return response.json().get('matches', [])
        except:
            return []