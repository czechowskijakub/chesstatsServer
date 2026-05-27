class MonthsOpenings:
    @staticmethod
    def get_months_openings(game: dict, color: str, username: str, colors_openings: dict):
        """Function formats Chess.com API's endpoint from games' position and
           fetches most played opening for black and white

        Args:
            game (dict): API's game position
            color (str): Which color to fetch (black/white)
            username (str): Chess.com username
            colors_openings (dict): Dictionary with one color's openings
            
        Returns:
            Modifies colors_openings dict in place
        """
        
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
        """Finds the most frequently played opening from the collected stats.

        Args:
            base (dict): Dictionary containing chess openings as keys and their 
                         calculated statistics (including 'count') as values.

        Returns:
            str: The key (usually a URL or ECO code) of the most played opening,
                 or None if the base dictionary is empty.
        """
        if not base:
            return None
        
        most_played_opening = list(base.keys())[0]
        for opening in base:
            if base[opening]['count'] > base[most_played_opening]['count']:
                most_played_opening = opening
                
        return most_played_opening
    
    @staticmethod
    def processed_opening_name(opening_url: str):
        """Extracts and formats a human-readable opening name from a Chess.com URL.

        Args:
            opening_url (str): The raw opening URL from the Chess.com API 
                               (e.g., '.../openings/Queens-Gambit-Accepted').

        Returns:
            str: A formatted string with words separated by spaces 
                 (e.g., 'Queens Gambit Accepted').
        """
        raw_name = opening_url.split('/')[-1]
        words_list = raw_name.split('-')
        return " ".join(words_list)