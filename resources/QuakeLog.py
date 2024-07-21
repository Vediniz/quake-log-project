import re

class QuakeLog:
    def __init__(self):
        self.games = {}

    def read_file(self, file):
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
        current_game = None
        current_players = {}

        for line in lines:
            try:
                if re.search(r'^\s*\d{1,2}:\d{2}\s+InitGame:', line):
                    game_id = len(self.games) + 1
                    current_game = f"games_{game_id}"
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

            except Exception as e:
                print(f"Error processing line: {line.strip()}. Error: {e}")

        if current_game is not None:
            self.games[current_game]['kills'] = current_players

        return self.games
    
# private functions
    def _add_new_player(self, player_name, current_players, current_game):
        if player_name not in current_players:
            current_players[player_name] = 0
            self.games[current_game]['players'].append(player_name)

    def _update_kills(self, killer, current_players, current_game):
        if killer in current_players:
            current_players[killer] += 1
            self.games[current_game]['total_kills'] += 1
