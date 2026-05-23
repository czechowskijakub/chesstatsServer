class MonthsOpenings:
    @staticmethod
    def get_months_openings(game: dict, color: str, username: str, colors_openings: dict):
        if game.get(color).get('username', '').lower() == username:
            opening = game.get('eco')
            result_status = game.get(color).get('result')
            if  result_status == 'win':
                outcome = 'win'
            elif result_status in ['repetition', 'stalemate', 'insufficient', 'timevsinsufficient', 'agreed']:
                outcome = 'draw'
            else:
                outcome = 'loss'
            
            if opening not in colors_openings:
                colors_openings[opening] = {'win': 0, 'draw': 0, 'loss': 0, 'count': 0}
                colors_openings[opening][outcome] = 1
                
            else:
                colors_openings[opening][outcome] += 1
                
            colors_openings[opening]['count'] += 1
            
    @staticmethod
    def get_most_played(base: dict):
        if not base:
            return None
        
        most_played_opening = list(base.keys())[0]
        for opening in base:
            if base[opening]['count'] > base[most_played_opening]['count']:
                most_played_opening = opening
                
        return most_played_opening
    
    @staticmethod
    def processed_opening_name(opening_url: str):
        raw_name = opening_url.split('/openings/')[-1]
        words_list = raw_name.split('-')
        return " ".join(words_list)