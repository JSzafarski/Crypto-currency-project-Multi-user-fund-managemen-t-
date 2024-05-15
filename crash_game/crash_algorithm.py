from random import choices
import gameHashDb
import time
import numpy as np
import hashlib
import random
import string
import hmac
import time

salt = "0000000000000000000fa3b65e43e4240d71762a5bf397d5304b2596d116859c"
seed_game_hash = '100af1b49f5e9f87efc81f838bf9b1f5e38293e5b4cf6d0b366c004e0a8d9987'
game_hash_object = gameHashDb.GameHashDb()


def get_multiplier_result():
    if game_hash_object.get_latest_hash() == "":
        print("test")
        game_hash_object.add_hash(seed_game_hash)
    current_hash = game_hash_object.get_latest_hash()
    hm = hmac.new(str.encode(current_hash), b'', hashlib.sha256)
    hm.update(salt.encode("utf-8"))
    h = hm.hexdigest()
    next_hash = h
    game_hash_object.add_hash(next_hash)
    if int(h, 16) % 33 == 0:
        return 0
    h = int(h[:13], 16)
    e = 2 ** 52
    return (((100 * e - h) / (e - h)) // 1) / 100.0


def get_max_position(pool_size):
    twenty_percent_of_pool = int(0.2 * pool_size)  # in sol
    max_position_size = int(0.2 * twenty_percent_of_pool)
    return max_position_size


def get_max_win(pool_size):
    twenty_percent_of_pool = int(0.1 * pool_size)  # in sol
    return twenty_percent_of_pool


def determine_win_or_loss(position_size, pool_size):
    twenty_percent_of_pool = int(0.2 * pool_size)  # in sol
    max_position_size = int(0.2 * twenty_percent_of_pool)
    if position_size <= max_position_size:
        game_multiplier = get_multiplier_result()
        max_multiplier = int(twenty_percent_of_pool // position_size)
        if game_multiplier > max_multiplier:
            game_multiplier = max_multiplier  #upperbound
        if game_multiplier < 1.25:
            game_multiplier = 0
        return game_multiplier
    else:
        return 0


def test():
    bet_size = 0
    initial_capital = 0
    exit = 4  #wanna exit at 2x
    for x in range(0, 100):
        if x == 0:
            initial_capital = 25
            bet_size = 1
        mult = determine_win_or_loss(bet_size, 100)
        if mult == 0:
            temp = initial_capital - bet_size
            if temp < 0:
                print("all funds lost")
                break
            initial_capital = initial_capital - bet_size
        else:
            if mult > exit:
                initial_capital = initial_capital - bet_size
                temp = initial_capital - bet_size
                if temp < 0:
                    print("all funds lost")
                    break
                print("users funds atm", initial_capital, "mult: ", mult)
            else:
                initial_capital = (initial_capital - bet_size) + (bet_size * mult)
                print("users funds atm", initial_capital, "mult: ", mult)

#test()
