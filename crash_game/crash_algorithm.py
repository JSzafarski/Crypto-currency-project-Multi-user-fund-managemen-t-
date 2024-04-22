from random import choices


# for now test with fake balance and no database


def get_max_position(pool_size):
    twenty_percent_of_pool = int(0.2 * pool_size)  # in sol
    max_position_size = int(0.2 * twenty_percent_of_pool)
    return max_position_size


def get_max_win(pool_size):
    twenty_percent_of_pool = int(0.2 * pool_size)  # in sol
    return twenty_percent_of_pool


def determine_win_or_loss(position_size, pool_size):
    win_or_lose_large_plays = [1, 0]  # for big plays > 20% of the max be size
    weights_large_plays = [0.2, 0.8]
    win_or_lose_small_plays = [1, 0]  # for small plays < 20% of max bet size
    weights_small_plays = [0.19, 0.7]
    twenty_percent_of_pool = int(0.2 * pool_size)  # in sol
    max_position_size = int(0.2 * twenty_percent_of_pool)
    if position_size <= max_position_size:
        win_loose = 0
        if position_size > max_position_size * 0.8:
            win_loose = choices(win_or_lose_large_plays, weights_large_plays)[0]
        else:
            win_loose = choices(win_or_lose_small_plays, weights_small_plays)[0]
        if win_loose == 1:
            yes_no = "yes"
        else:
            yes_no = "no"
        max_multiplier = int(twenty_percent_of_pool // position_size)
        temp_array = []
        temp_weights = []
        initial_probability = 0.5
        step_interval = 0.25  # percent%
        adjusted_max = int(max_multiplier / 0.25)
        for iterator in range(5, adjusted_max):
            multiplier_step = iterator * step_interval
            temp_array.append(multiplier_step)
            temp_weights.append(initial_probability)
            initial_probability = initial_probability * 0.8  # to be tweaked later
        randomly_chosen_multiplier_upperbound = choices(temp_array, temp_weights)[0]
        return randomly_chosen_multiplier_upperbound, yes_no
    else:
        return 0, 0  # allowable bet size exceeded
