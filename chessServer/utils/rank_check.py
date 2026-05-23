import requests
from django.http import JsonResponse, HttpResponse

class RankCheck():
    @staticmethod
    def get_best_elo_ensured_ranked(data, tempo='daily'):
        tempo_data = data.get(f'chess_{tempo}', {})
        current = tempo_data.get('last', {}).get('rating', 0)
        best = tempo_data.get('best', {}).get('rating', current)
        return best
