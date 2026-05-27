import requests
from django.http import JsonResponse, HttpResponse

class RankCheck():
    @staticmethod
    def get_best_elo_ensured_ranked(data: dict, tempo: str = 'daily') -> int:
        """Extracts the highest historical rating for a specific time control.
        
        If the tournament/ranked maximum rating is missing from the API response, 
        it falls back to the current rating.

        Args:
            data (dict): The raw JSON response dictionary from the Chess.com player stats API.
            tempo (str, optional): The game time control to check (e.g., 'rapid', 'blitz', 
                                   'bullet', 'daily'). Defaults to 'daily'.

        Returns:
            int: The best rating achieved in the specified tempo, or the current rating 
                 as a fallback. Returns 0 if no data is found.
        """
        tempo_data = data.get(f'chess_{tempo}', {})
        current = tempo_data.get('last', {}).get('rating', 0)
        best = tempo_data.get('best', {}).get('rating', current)
        return best