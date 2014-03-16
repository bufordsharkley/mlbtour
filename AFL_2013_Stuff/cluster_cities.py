#!/usr/local/bin/pythonw

import scipy.cluster.hierarchy
import scipy.cluster.vq
#import fastcluster

teamfile = open('team_list.txt', 'r')
i = 0
team_number = dict()
distances_array = [[]]
TEAMS = 30
teamlist = []

for line in teamfile:
    line = line.rstrip()
    team_number[line] = i
    teamlist.append(line)
    i += 1

teamfile.close()

distances_array = [[0 for x in xrange(TEAMS)] for x in xrange(TEAMS)]

timesfile = open('distances_in_hours.txt', 'r')

for line in timesfile:
    line = line.rstrip()
    mylist = line.split(":")
    distances_array[team_number[mylist[0]]][team_number[mylist[1]]] = mylist[2]
#    distances_array[team_number[mylist[1]]][team_number[mylist[0]]] = mylist[2]

timesfile.close()

myclusters = scipy.cluster.hierarchy.linkage(distances_array)
#tocluster = scipy.cluster.vq.whiten(distances_array)
#myclusters = scipy.cluster.vq.kmeans(tocluster, 5)

nameclusters = [[0 for x in xrange(5)] for x in xrange(TEAMS - 1)]

for num in range(len(myclusters)):
    if myclusters[num][0] < 30:
        nameclusters[num][0] = teamlist[int(myclusters[num][0])]
    else:
        nameclusters[num][0] = myclusters[num][0]
    if myclusters[num][1] < 30:
        nameclusters[num][1] = teamlist[int(myclusters[num][1])]
    else:
        nameclusters[num][1] = myclusters[num][1]
    nameclusters[num][2] = myclusters[num][2]
    nameclusters[num][3] = myclusters[num][3]
    nameclusters[num][4] = 30 + num

print myclusters
print nameclusters

#mydend = scipy.cluster.hierarchy.dendrogram(myclusters)

#print mydend
