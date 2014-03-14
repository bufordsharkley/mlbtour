import csv
import datetime

import tablib

_MAP_TO_SHORT = {'Rays': 'TB',
                 'Indians': 'CLE',
                 'Rangers': 'TEX',
                 'Twins': 'MIN',
                 'Cardinals': 'STL',
                 'Brewers': 'MIL',
                 'D-backs': 'ARI',
                 'Orioles': 'BAL',
                 'Mariners': 'SEA',
                 'Angels': 'LAA',
                 'Giants': 'SF',
                 'Dodgers': 'LAD',
                 'Tigers': 'DET',
                 'Royals': 'KC',
                 'Phillies': 'PHI',
                 'Blue Jays': 'TOR',
                 'Cubs': 'CHI',
                 'White Sox': 'CWS',
                 'Padres': 'SD',
                 'Rockies': 'COL',
                 'Braves': 'ATL',
                 'Red Sox': 'BOS',
                 'Athletics': 'OAK',
                 'Nationals': 'WSH',
                 'Yankees': 'NYY',
                 'Reds': 'CIN',
                 'Mets': 'NYM',
                 'Pirates': 'PIT',
                 'Marlins': 'MIA',
                 'Astros': 'HOU'}


class MLBTour(object):

    _all_ballparks = _MAP_TO_SHORT.values()

    def __init__(self, tosee=None):
        self._schedule = get_schedule()
        self._distances = get_distances()
        self.time = None
        self.location = None
        self.gamelog = []
        if tosee is not None:
            self._ballparkstosee = set(tosee)

    def _ballpark_from_game(self, game_id):
        return dict(self._schedule.dict[game_id])['home team']

    def _first_pitch(self, game_id):
        return dict(self._schedule.dict[game_id])['datetime']

    def _time_after_game(self, game_id):
        return self._first_pitch(game_id) + datetime.timedelta(hours=3)

    def see_game(self, game_id):
        # TODO: implement
        pass

    def possible_games(self):
        # TODO: implement
        # return list of possible game ids
        pass



def get_schedule():
    data = tablib.Dataset()
    data.headers = ['game id', 'datetime', 'away team', 'home team']
    with open('MLBSchedule2014.csv') as schedule:
        gamereader = csv.reader(schedule, delimiter=',')
        for game in gamereader:
            # put TBD games at 7pm; insert doubleheader like any other game:
            time = game[4] if not game[4] == 'TBD' else '07:10pm'
            datestring = '{} {} {} {}'.format(game[1],
                                              game[2].zfill(2),
                                              game[3].zfill(2),
                                              time.split()[-1].zfill(7))
            data.append([int(game[0])-1,
                        datetime.datetime.strptime(datestring,
                                                   '%Y %m %d %I:%M%p'),
                        _MAP_TO_SHORT[game[5]],
                        _MAP_TO_SHORT[game[6]]])
    return data


def get_distances():
    with open('ballpark_distances.csv') as distancesfile:
        tablereader = csv.reader(distancesfile, delimiter=',')
        tablereader.next()  # burn headers/notes
        teams = tablereader.next()[1:]
        distances = {team: {} for team in teams}
        for jj, row in enumerate(tablereader):
            team1 = row[0]
            for ii, distance in enumerate(row[1:1+jj]):
                distances[team1][teams[ii]] = int(distance)
                distances[teams[ii]][team1] = int(distance)
            distances[team1][team1] = 0
    return distances

_tour = MLBTour()

ballpark_from_game = _tour._ballpark_from_game
first_pitch_from_game = _tour._first_pitch

allballparks = _tour._all_ballparks
