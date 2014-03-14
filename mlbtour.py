import csv
import datetime

import tablib

NOTWORTHIT = 30  # if you can't see another game within 30 hours, forget it.
MAXDRIVE = 6  # 15 hours tops. (Because it's 14 SEA->bay area. TODO make SEA
               # the exception, not the rule.
DRIVINGSPEED = 55

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

    def __init__(self, startgame=None, tosee=None):
        self._schedule = get_schedule()
        self._distances = get_distances()
        self.time = None
        self.location = None
        self.gamelog = []
        self.longest = []
        if tosee is not None:
            self._ballparkstosee = set(tosee)
        if startgame is not None:
            self.see_game(startgame)

    def _ballpark_from_game(self, game_id):
        return dict(self._schedule.dict[game_id])['home team']

    def _first_pitch(self, game_id):
        return dict(self._schedule.dict[game_id])['datetime']

    def _time_after_game(self, game_id):
        return self._first_pitch(game_id) + datetime.timedelta(hours=3)

    def see_game(self, game_id):
        print 'oh boy going to game. GAME ID IS: {}'.format(game_id)
        newballpark = self._ballpark_from_game(game_id)
        print 'driving from {} to {}'.format(self.location, newballpark)
        self.location = newballpark
        self.time = self._time_after_game(game_id)
        self._removefromlist(newballpark)
        self.gamelog.append(game_id)

    def possible_games(self):
        toolate = self.time + datetime.timedelta(hours=NOTWORTHIT)
        upcominggames = self._games_in_range(self.time, toolate)
        possibilities = [game for game in upcominggames
                         if self._ballpark_from_game(game) in
                         self._ballparkstosee and
                         self._driveable(game)]
        return possibilities

    def _removefromlist(self, ballpark):
        self._ballparkstosee.remove(ballpark)

    def _addbacktolist(self, ballpark):
        self._ballparkstosee.add(ballpark)

    def _games_in_range(self, timestart, timeend):
        return [ii for ii, date in enumerate(self._schedule['datetime'])
                if timestart < date < timeend]

    def _driveable(self, game):
        timediff = (self._first_pitch(game) - self.time).total_seconds()/3600
        goingto = self._ballpark_from_game(game)
        drivetime = self._distances[self.location][goingto]/DRIVINGSPEED
        print "* #{: <6} {: <6} {: <2} hrs".format(game, goingto, drivetime)
        if timediff > drivetime and drivetime < MAXDRIVE:
            return True
        return False

    def seen_em_all(self):
        if not self._ballparkstosee:
            return True
        return False

    def unsee_game(self, badgame):
        print 'NEVERMIND'
        if len(self.gamelog) > len(self.longest):
            self.longest = list(self.gamelog)  # make a copy
        self.location = self._ballpark_from_game(self.gamelog[-2])
        self.time = self._time_after_game(self.gamelog[-2])
        self._addbacktolist(self._ballpark_from_game(badgame))
        self.gamelog.pop()


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
    """Get distances from ballpark to ballpark in a dict.

    Query by: distances['CHW']['CHI'].
    Distances are via highway, not as the bird flies. In miles.
    """
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
