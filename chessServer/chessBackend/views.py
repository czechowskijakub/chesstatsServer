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
            
            daily_data = raw_data.get('chess_daily', {})
            current_daily = daily_data.get('last', {}).get('rating', 0)
            best_daily = daily_data.get('best', {}).get('rating', current_daily)
            
            processed_data = {
                'username': username,
                
                'rapid_rating': raw_data.get('chess_rapid', {}).get('last', {}).get('rating', 0),
                'best_rapid': raw_data.get('chess_rapid', {}).get('best', {}).get('rating', 0),
                'rapid_wins': raw_data.get('chess_rapid', {}).get('record', {}).get('win', 0),
                'rapid_draws': raw_data.get('chess_rapid', {}).get('record', {}).get('draw', 0),
                'rapid_losses': raw_data.get('chess_rapid', {}).get('record', {}).get('loss', 0),
                
                'blitz_rating': raw_data.get('chess_blitz', {}).get('last', {}).get('rating', 0),
                'best_blitz': raw_data.get('chess_blitz', {}).get('best', {}).get('rating', 0),
                'blitz_wins': raw_data.get('chess_blitz', {}).get('record', {}).get('win', 0),
                'blitz_draws': raw_data.get('chess_blitz', {}).get('record', {}).get('draw', 0),
                'blitz_losses': raw_data.get('chess_blitz', {}).get('record', {}).get('loss', 0),
                
                'bullet_rating': raw_data.get('chess_bullet', {}).get('last', {}).get('rating', 0),
                'best_bullet': raw_data.get('chess_bullet', {}).get('best', {}).get('rating', 0),
                'bullet_wins': raw_data.get('chess_bullet', {}).get('record', {}).get('win', 0),
                'bullet_draws': raw_data.get('chess_bullet', {}).get('record', {}).get('draw', 0),
                'bullet_losses': raw_data.get('chess_bullet', {}).get('record', {}).get('loss', 0),
                
                'daily_rating': raw_data.get('chess_daily', {}).get('last', {}).get('rating', 0),
                'best_daily': best_daily,
                'daily_wins': raw_data.get('chess_daily', {}).get('record', {}).get('win', 0),
                'daily_draws': raw_data.get('chess_daily', {}).get('record', {}).get('draw', 0),
                'daily_losses': raw_data.get('chess_daily', {}).get('record', {}).get('loss', 0),
                
            }
            print(raw_data)
            return JsonResponse(processed_data)
        else:
            return JsonResponse({'error': 'User not found on Chess.com'}, status=404)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)