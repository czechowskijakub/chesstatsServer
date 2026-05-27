import requests
from django.http import JsonResponse, HttpResponse
import utils.time_handler as th
import utils.rank_check as rc
import utils.opening_classifier as oc

def hello(request):
    return HttpResponse("Hello world!")

def get_chess_api(request, username: str):
    url = f"https://api.chess.com/pub/player/{username}/stats"
    headers = {'User-Agent': 'chesstats-app (your@email.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            processed_data = {
                'username': username,
                
                'rapid_rating': raw_data.get('chess_rapid', {}).get('last', {}).get('rating', 0),
                'best_rapid': rc.RankCheck.get_best_elo_ensured_ranked(raw_data, tempo='rapid'),
                'rapid_wins': raw_data.get('chess_rapid', {}).get('record', {}).get('win', 0),
                'rapid_draws': raw_data.get('chess_rapid', {}).get('record', {}).get('draw', 0),
                'rapid_losses': raw_data.get('chess_rapid', {}).get('record', {}).get('loss', 0),
                
                'blitz_rating': raw_data.get('chess_blitz', {}).get('last', {}).get('rating', 0),
                'best_blitz': rc.RankCheck.get_best_elo_ensured_ranked(raw_data, tempo='blitz'),
                'blitz_wins': raw_data.get('chess_blitz', {}).get('record', {}).get('win', 0),
                'blitz_draws': raw_data.get('chess_blitz', {}).get('record', {}).get('draw', 0),
                'blitz_losses': raw_data.get('chess_blitz', {}).get('record', {}).get('loss', 0),
                
                'bullet_rating': raw_data.get('chess_bullet', {}).get('last', {}).get('rating', 0),
                'best_bullet': rc.RankCheck.get_best_elo_ensured_ranked(raw_data, tempo='bullet'),
                'bullet_wins': raw_data.get('chess_bullet', {}).get('record', {}).get('win', 0),
                'bullet_draws': raw_data.get('chess_bullet', {}).get('record', {}).get('draw', 0),
                'bullet_losses': raw_data.get('chess_bullet', {}).get('record', {}).get('loss', 0),
                
                'daily_rating': raw_data.get('chess_daily', {}).get('last', {}).get('rating', 0),
                'best_daily': rc.RankCheck.get_best_elo_ensured_ranked(raw_data, tempo='daily'),
                'daily_wins': raw_data.get('chess_daily', {}).get('record', {}).get('win', 0),
                'daily_draws': raw_data.get('chess_daily', {}).get('record', {}).get('draw', 0),
                'daily_losses': raw_data.get('chess_daily', {}).get('record', {}).get('loss', 0),
            }
            
            return JsonResponse(processed_data)
        else:
            return JsonResponse({'error': 'User not found on Chess.com'}, status=404)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_openings_by_result(request, username: str):
    current_year = th.TimeHandler.get_year_str()
    current_month = th.TimeHandler.get_month_str()
    
    url = f"https://api.chess.com/pub/player/{username}/games/{current_year}/{current_month}"
    headers = {'User-Agent': 'chesstats-app (your@email.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Couldnt download games'}, status=response.status_code)
            
        raw_data = response.json()
        game_list = raw_data.get('games', [])
        
        if not game_list:
            return JsonResponse({'error': 'No games played this month'}, status=404)
        
        white_openings = {}
        black_openings = {}
        user_lower = username.lower()
        
        for game in game_list:
            oc.MonthsOpenings.get_months_openings(game, 'white', user_lower, white_openings)
            oc.MonthsOpenings.get_months_openings(game, 'black', user_lower, black_openings)
            
        most_played_white = oc.MonthsOpenings.get_most_played(white_openings)
        most_played_black = oc.MonthsOpenings.get_most_played(black_openings)
        
        mp_white_wins = white_openings[most_played_white]['win']
        mp_white_draws = white_openings[most_played_white]['draw']
        mp_white_losses = white_openings[most_played_white]['loss']
        mp_white_count = white_openings[most_played_white]['count']
        
        mp_white_stats = [
            round((mp_white_wins / mp_white_count) * 100, 2),
            round((mp_white_draws / mp_white_count) * 100, 2),
            round((mp_white_losses / mp_white_count) * 100, 2),
        ]
        
        mp_black_wins = black_openings[most_played_black]['win']
        mp_black_draws = black_openings[most_played_black]['draw']
        mp_black_losses = black_openings[most_played_black]['loss']
        mp_black_count = black_openings[most_played_black]['count']
        
        mp_black_stats = [
            round((mp_black_wins / mp_black_count) * 100, 2),
            round((mp_black_draws / mp_black_count) * 100, 2),
            round((mp_black_losses / mp_black_count) * 100, 2),
        ]
        
        mp_white_opening_name = oc.MonthsOpenings.processed_opening_name(most_played_white)
        mp_black_opening_name = oc.MonthsOpenings.processed_opening_name(most_played_black)
        
        processed_data = {
            'most_played_white_opening': mp_white_opening_name,
            'most_played_white_wins': mp_white_stats[0],
            'most_played_white_draws': mp_white_stats[1],
            'most_played_white_losses': mp_white_stats[2],
            
            'most_played_black_opening': mp_black_opening_name,
            'most_played_black_wins': mp_black_stats[0],
            'most_played_black_draws': mp_black_stats[1],
            'most_played_black_losses': mp_black_stats[2],
        }
        
        return JsonResponse(processed_data)
        
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Internal err: {str(e)}'}, status=500)
    
def get_month_games(request, username: str):
    current_year = th.TimeHandler.get_year_str()
    current_month = th.TimeHandler.get_month_str()
    user_lower = username.lower()
    
    url = f"https://api.chess.com/pub/player/{username}/games/{current_year}/{current_month}"
    headers = {'User-Agent': 'chesstats-app (your@email.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Couldnt download games'}, status=response.status_code)
        
        raw_data = response.json()
        game_list = raw_data.get('games', [])
        if not game_list:
            return JsonResponse({'error': 'No games played this month'}, status=404)
        
        games_dict = {}
        count = 1
        
        for game in game_list:
            if game.get('white', {}).get('username', '').lower() == user_lower:
                opponent = game.get('black', {}).get('username', '')
                result = game.get('white', {}).get('result', '')
            elif game.get('black', {}).get('username', '').lower() == user_lower:
                opponent = game.get('white', {}).get('username', '')
                result = game.get('black', {}).get('result', '')
            else:
                continue
            
            games_dict[count] = {
                'tempo': game.get('time_class', ''),
                'result': result,
                'opening': oc.MonthsOpenings.processed_opening_name(game.get('eco')),
                'vs': opponent
            }
            count += 1
        
        return JsonResponse(games_dict)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': f'Internal err: {str(e)}'}, status=500)