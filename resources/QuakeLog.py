import re

class QuakeLog:
    def __init__(self):
        self.games = {}

    def read_file(self, file):
        '''
            Reads lines from a given file.
            
            Args:
            - file (str): Path to the file to read.
        '''
        
        try:
            with open(file, 'r') as f:
                lines = f.readlines()
            return lines
        except FileNotFoundError:
            print(f"Error: File '{file}' not found.")
        except Exception as e:
            print(f"Unexpected error reading file '{file}': {e}")
            raise 

    def extract_informations(self, lines):
        '''
            Extracts game information from lines of a log.

            Args:
            - lines (list): List of strings.

            Returns:
            - dict: Dictionary containing extracted game information organized by game ID.
                    Structure: {

                        \n'games_1': {
                        \n    'total_kills': 0,
                        \n    'players': [],
                        \n    'kills': {},
                        \n    'kills_by_means': []
                        }

                    }
        '''

        current_game = None
        current_players = {}

        for line in lines:
            try:
                if re.search(r'^\s*\d{1,2}:\d{2}\s+InitGame:', line):
                    game_id = len(self.games) + 1
                    current_game = f'game_{game_id}'
                    self.games[current_game] = {
                        'total_kills': 0,
                        'players': [],
                        'kills': {},
                        'kills_by_means': []
                    }
                    current_players = {}

                elif re.search(r'^\s*\d{1,2}:\d{2}\s+ClientUserinfoChanged:', line):
                    match = re.search(r'n\\([^\\]+)', line)
                    if match:
                        player_name = match.group(1)
                        self._add_new_player(player_name, current_players, current_game)

                elif re.search(r'^\s*\d{1,2}:\d{2}\s+Kill:', line):
                    match = re.search(r'Kill: \d+ \d+ \d+: (\w+) killed (\w+) by (MOD_\w+)', line)
                    if match:
                        killer, killed, death_cause = match.groups()
                        if killer != '<world>':  
                            self._add_new_player(killer, current_players, current_game)
                        self._add_new_player(killed, current_players, current_game)
                        self._update_kills(killer, current_players, current_game)
                        self.games[current_game]['kills_by_means'].append(death_cause)
                        self.games[current_game]['kills'] = current_players

            except Exception as e:
                print(f'Error processing line: {line.strip()}. Error: {e}')

        return self.games
    
    def generate_game_report(self):
        '''
            Generates a report with general game statistics.

            Returns:
            str: A formatted string containing game statistics including total kills,
             players in each game, and each player kills count. 
        '''

        report = ''
        for game_id, game_data in self.games.items():
            report += f'\nGame: {game_id}\n'
            report += f'Total Kills: {game_data['total_kills']}\n'
            report += f'Players: {', '.join(game_data['players'])}\n'
            report += f'Kills: {game_data['kills']}\n'
        return report
        

    def generate_kill_by_means_report(self):
        '''
            Generates a report with .

            Returns:
            str: A formatted string containing the count of  'kill by means' occurrence across all games.
        '''
        kill_by_means_counts = {}
        report = ''

        for game_id, game_data in self.games.items():
            report += f'\nGame: {game_id}\n'

            for kill in game_data['kills_by_means']:
                if kill in kill_by_means_counts:
                    kill_by_means_counts[kill] += 1
                else:
                    kill_by_means_counts[kill] = 1

            for kill, count in kill_by_means_counts.items():
                report += f'{kill}: {count}\n'

            kill_by_means_counts = {}

        return report
    
# private functions
    def _add_new_player(self, player_name, current_players, current_game):
        if player_name not in current_players:
            current_players[player_name] = 0
            self.games[current_game]['players'].append(player_name)

    def _update_kills(self, killer, current_players, current_game):
        if killer in current_players:
            current_players[killer] += 1
            self.games[current_game]['total_kills'] += 1
