3/15/14

Alex Lovejoy

This is the set of codes and information files from my 2013 attempt to find a short, reasonable MLB road trip.  Even if my code did work (never got it to), I would be unable to claim it was the minimal distance, but it should be a reasonably short distance in any case.

First, make team_list.txt.  A list of every MLB team of the format "Baltimore Orioles".

Then, run get_stadium_addresses.pl, which gets the html page from mlb.com listing all the team addresses, and prints it in a readable format.  Output to stadium_address_webpage.txt.

Then, run find_address.pl to make a file (address_list.txt) of the format Team:Stadium Street Address City State Zip.

Then, run get_stadium_distances.pl to make a file (distances_list.txt) of the pairwise distances between stadia of the format Team1:Team2:Time (x days x hours x mins).  Running the script convert_times_to_hours.pl gives the file distances_in_hours.txt with the same format, where the time between stadia is listed in hours.

To get each team's home schedule, run get schedules.pl to make a file (all_home_games.txt) of every MLB home game for the season of the format Team:Date:Time
NOTE: A different script should be used with Mark's csv file to do this for each new season.

I then used cluster_cities.py to get a heirarchical clustering of the 30 MLB teams by distance between stadia.  k-means would probably be a better way to cluster, but I got heirarchical to work first.  By eye, I decided where to cut the tree to split the teams, and it ended up with 6 clusters.  team_cluster_list.txt lists the cluster for each time in the format "Baltimore Orioles:0", etc.

Finally, using the script make_trip.py (and make_trip_2.py), I take in the distances between stadia, the list of home games, and the cluster information.  The script tries to find the minimal trip for each cluster, then find the minimal trip connecting all 6 clusters.  It assumes one is willing to drive 8 hours a day, and that one can drive and see a game that night.  However, one is not allowed to drive on the same day one sees a game unless the game starts after 7 PM local.

...At least in theory, that's how the make_trip.py code works.  Currently, it doesn't actually work.  I think my issues were that the code wouldn't let one travel and see a game on the same day no matter what.  It was giving much longer than the minimal distances for each clusters.

Also, I was terrible about commenting my code.  Sorry.

Some is done in perl, and some in python.
