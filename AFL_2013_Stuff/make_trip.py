#!/usr/bin/python

import time
import itertools

teamfile = open('team_cluster_list.txt', 'r')
i = 0
team_number = dict()
distances_array = [[]]
TEAMS = 30
team_list = []
cluster_list = []
clusters = [[]]
MAX_DRIVE_DAY = 8
FIRST_DAY = 90
SEASON_LENGTH = 183
CLUSTERS = 6
FIRST_START_DAY = 0
LAST_START_DAY = 120
PERMUTE_CLUSTERS = 100
#PERMUTE_CLUSTERS = 1
EARLIEST_TIME = 19
team_objects = []

def get_day(date):
    mydate = time.strptime(mylist[1], "%m/%d/%y")
    index = mydate[7] - FIRST_DAY
    return index

def get_time(toparse):
    mytime = time.strptime(toparse, "%I:%M %p")
    time_for_list = mytime[3] + mytime[4] / 60
    return time_for_list

clusters = [[] for x in xrange(CLUSTERS)]

for line in teamfile:
    line = line.rstrip()
    mylist = line.split(":")
    team_number[mylist[0]] = i
    team_list.append(mylist[0])
    cluster_list.append(mylist[1])
    clusters[int(mylist[1])].append(i)
    i += 1

teamfile.close()

distances_matrix = [[0 for x in xrange(TEAMS)] for x in xrange(TEAMS)]

timesfile = open('distances_in_hours.txt', 'r')

for line in timesfile:
    line = line.rstrip()
    mylist = line.split(":")
    distances_matrix[team_number[mylist[0]]][team_number[mylist[1]]] = float(mylist[2]) // MAX_DRIVE_DAY + 1

timesfile.close()

schedule_matrix = [[0 for x in xrange(SEASON_LENGTH)] for x in xrange(TEAMS)]

sched_file = open('all_home_games.txt', 'r')

for line in sched_file:
    line = line.rstrip()
    mylist = line.split(",")
    myday = get_day(mylist[1])
    mytime = get_time(mylist[2])
    schedule_matrix[team_number[mylist[0]]][myday] = mytime

#print team_number, team_list, distances_matrix
#print schedule_matrix
#print team_number, team_list, cluster_list
#print clusters

sched_file.close()

class Team:
    def __init__(self, name, cluster, schedule, distances):
        self.name = name
        self.cluster = cluster
        self.schedule = schedule
        self.distances = distances
    
    def get_name(self):
        return self.name

    def get_cluster(self):
        return self.cluster

    def get_schedule(self):
        return self.schedule
    
    def game_on_day(self, day):
        return self.schedule[day]

    def distance_to_team(self, team):
        return int(self.distances[team])

for i in range(TEAMS):
    team_objects.append(Team(team_list[i], cluster_list[i], schedule_matrix[i], distances_matrix[i]))

#print team_objects[13].get_name(), team_objects[13].get_cluster(), team_objects[13].game_on_day(50), team_objects[13].distance_to_team(12)

class Trip:
    def __init__(self, date, team):
        self.games = {date : team}
    
    def get_trip(self):
        return self.games

    def add_game(self, date, team):
        self.games[date] = team

    def get_first_game(self):
        sorted_keys = self.games.keys()
        sorted_keys.sort()
        return [sorted_keys[0], self.games[sorted_keys[0]]]

    def get_last_game(self):
        sorted_keys = self.games.keys()
        sorted_keys.sort()
        return [sorted_keys[-1], self.games[sorted_keys[0]]]

    def get_length(self):
        sorted_keys = self.games.keys()
        sorted_keys.sort()
        return sorted_keys[-1] - sorted_keys[0]

def get_next_date(team, date):
    to_check = date
    if team_objects[team].game_on_day(to_check) >= EARLIEST_TIME:
        return to_check
    else:
        to_check += 1
        while team_objects[team].game_on_day(to_check) == 0:
            to_check += 1
            if to_check > 182:
                return 182
        return to_check

minimal_trips = []

j = 0

for mycluster in clusters:
    minimal_trips.append([])
#    print cluster
    myperms = list(itertools.permutations(mycluster))
#    for run in range(PERMUTE_CLUSTERS):
    for cluster in myperms:
        if j == 4:
            break
#        random.shuffle(cluster)
#        print cluster
        for start_day in range(FIRST_START_DAY,LAST_START_DAY):
            team = cluster[0]
            if team_objects[team].game_on_day(start_day) == 0:
                continue
            day = start_day
            day = get_next_date(team,day)
            possible_trip = Trip(day, team)
#            print possible_trip.get_length()
            for i in range(1,len(cluster)):
                day = day + team_objects[cluster[i - 1]].distance_to_team(cluster[i])
                day = get_next_date(cluster[i], day)
#                print day
                possible_trip.add_game(day, cluster[i])
            if (minimal_trips[j] == []) or  (minimal_trips[j][0].get_length() == possible_trip.get_length()):
                minimal_trips[j].append(possible_trip)
            elif minimal_trips[j][0].get_length() > possible_trip.get_length:
                minimal_trips[j] = [possible_trip]
    j += 1


start_day = FIRST_START_DAY
while start_day < LAST_START_DAY:
    team = 19
    day = get_next_date(team,start_day)
    trip = Trip(day, team)
#    print trip.get_length(), trip.get_first_game()
    minimal_trips[4].append(trip)
    start_day = day

#for array in minimal_trips:
#    for trip in array:
#        print trip.get_length(), trip.get_first_game()

for array in minimal_trips:
    print array[0].get_length(), array[0].get_trip()

#for trip in minimal_trips[4]:
#    print trip.get_length(), trip.get_first_game()
