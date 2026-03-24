import requests
from django.http import JsonResponse, HttpResponse

def hello(request):
    return HttpResponse("Hello world!")

def get_chess_api(request, username):
    url = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {'User-Agent': 'chesstats-app (your@email.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            processed_data = {
                'username': username,
                
                'rapid_rating': raw_data.get('chess_rapid', {}).get('last', {}).get('rating', 0),
                'best_rapid': raw_data.get('chess_rapid', {}).get('best', {}).get('rating', 0),
                
                'blitz_rating': raw_data.get('chess_blitz', {}).get('last', {}).get('rating', 0),
                'best_blitz': raw_data.get('chess_blitz', {}).get('best', {}).get('rating', 0),
                
                'bullet_rating': raw_data.get('chess_bullet', {}).get('last', {}).get('rating', 0),
                'best_bullet': raw_data.get('chess_bullet', {}).get('best', {}).get('rating', 0),
                
                'daily_rating': raw_data.get('chess_daily', {}).get('last', {}).get('rating', 0),
                'best_daily': raw_data.get('chess_daily', {}).get('best', {}).get('rating', 0),
            }
            return JsonResponse(processed_data)
        else:
            return JsonResponse({'error': 'User not found on Chess.com'}, status=404)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)