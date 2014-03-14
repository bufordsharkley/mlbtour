import mlbtour


def main():
    tosee = mlbtour.allballparks  # see them all.
    startgame = 381
    tour = mlbtour.MLBTour(startgame, tosee)
    if can_find_shortest_path(tour):
        "BEST PATH: {}".format(tour.gamelog)
    print "LONGEST PATH ACHIEVED: {}".format(tour.longest)


def can_find_shortest_path(tour):
    # for moment, just sees if there IS a path
    if tour.seen_em_all():
        return True
    possibilities = tour.possible_games()
    if not possibilities:
        return False
    startat = tour.location
    for game in possibilities:
        tour.see_game(game)
        if can_find_shortest_path(tour):
            return True
        # else take back move
        tour.unsee_game(game)
    return False


def print_game_info(listofgames):
    """Given a list of games, prints the tour."""
    tour = mlbtour.MLBTour()
    for game in listofgames:
        print "{} {}".format(mlbtour.ballpark_from_game(game),
                             mlbtour.first_pitch_from_game(game))


if __name__ == '__main__':
    # test the decoder:
    longestsofar = [381, 395, 403, 423, 434, 440, 455, 470, 486, 498, 515, 525, 546]
    print_game_info(longestsofar)
    # run code...
    main()
