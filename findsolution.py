import mlbtour


def main():
    tosee = mlbtour.allballparks  # see them all.
    tour = mlbtour.MLBTour(tosee)
    if can_find_shortest_path(tour):
        print tour.gamelog


def can_find_shortest_path(tour):
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
