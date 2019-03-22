import pandas as pd

def build_game_frame(file_name):
    with open(file_name, "r") as f:
        num_heroes = int(f.next())
        alg = f.next().replace("\n", "")
        heroes = []
        for h in f:
            row = h.split(",")
            heroes.append([int(row[0]), float(row[1]), float(row[2]), float(row[3]), int(row[4])])
        heroes = pd.DataFrame(heroes, columns=["id", "power", "mastery_i", "mastery_j", "team_id"])
        heroes.set_index("id", inplace=True)
        heroes.sort_index(inplace=True,)
    return { "n" : num_heroes, "alg" : alg, "heroes" : heroes}

def write_output(hero_id, file_name):
    with open(file_name, "w") as f:
        output = "{}\n".format(hero_id)
        f.write(output)

def main():
    game_frame = build_game_frame("input.txt")
    next_hero = None

    if game_frame["alg"] == "minimax":
        next_hero = apply_minimax(game_frame["heroes"])
    elif game_frame["alg"] == "ab":
        next_hero = apply_alpha_beta_pruning(game_frame["heroes"])
    else:
        raise(Exception("Bad alg input"))

    write_output(next_hero, "output.txt")

def apply_minimax(heroes_df):
    available = set(get_available_players(heroes_df).index.tolist())
    max_heroes = set(get_selected_players(heroes_df, 1).index.tolist())
    min_heroes = set(get_selected_players(heroes_df, 2).index.tolist())

    return minimax(heroes_df[["power", "mastery_i", "mastery_j"]], max_heroes, min_heroes, available, True)[1]

def minimax(heroes, max_heroes, min_heroes, available_players, isMaxPlayer):
    if get_num_selected_players(max_heroes, min_heroes) == 10:
        return calc_advantage(heroes, max_heroes, min_heroes), 0

    if isMaxPlayer:
        max_value = float("-inf")
        max_hero = 0

        for i in available_players:

            available_players.remove(i)
            max_heroes.add(i)

            val, _ = minimax(heroes, max_heroes, min_heroes, available_players, not isMaxPlayer)
            # max
            if val > max_value:
                max_hero = i
                max_value = val
            elif val == max_value and i < max_hero:
                max_hero = i

            available_players.add(i)
            max_heroes.remove(i)

        return max_value, max_hero
    else:
        min_value = float("inf")
        min_hero = 0

        for i in available_players:

            available_players.remove(i)
            min_heroes.add(i)

            val, _ = minimax(heroes, max_heroes, min_heroes, available_players, not isMaxPlayer)
            # min
            if val < min_value:
                min_value = val
                min_hero = i
            elif val == min_value and i < min_hero:
                min_hero = i

            available_players.add(i)
            min_heroes.remove(i)

        return min_value, min_hero

def get_selected_players(heroes_df, id):
    return heroes_df.loc[heroes_df["team_id"] == id]

# this may need to be optimized
def get_num_selected_players(max_heroes, min_heroes):
    num = len(max_heroes) + len(min_heroes)
    # num = len(heroes_df.loc[heroes_df["team_id"] == 1]) + len(heroes_df.loc[heroes_df["team_id"] == 2])
    return num

# this may need to be optimized
def get_available_players(heroes_df):
    return heroes_df.loc[heroes_df["team_id"] == 0]
        
def calc_advantage(heroes_df, max_heroes, min_heroes):
    # advatage = (synergy_bonus_max + sum(mastery_i_max * power_i_max) - (synergy_bonus_min + sum(mastery_i_min * power_i_min))
    return calc_player_advantage(heroes_df, max_heroes, 1) - calc_player_advantage(heroes_df, min_heroes, 2) 

def calc_player_advantage(heroes_df, heroes_selected, player_id):
    # (synergy_bonus + sum(mastery_i * power_i)
    synergy_bonus = calc_synergy(heroes_selected)

    mastery_column = ""
    if player_id == 1:
        mastery_column = "mastery_i"
    elif player_id == 2:
        mastery_column = "mastery_j"
    else:
        raise(Exception("Invalid player id when calculating advantage"))

    selected = heroes_df.loc[ heroes_selected ]
    mastery = selected[[mastery_column]]
    power = selected[["power"]]

    return synergy_bonus + mastery.T.dot(power).iloc[0,0]

def calc_synergy(heroes_selected):
    last_set = set()
    for i in heroes_selected:
        last = str(i)[-1]
        if last in last_set:
            return 0
        last_set.add(last)
    return 120

def apply_alpha_beta_pruning(heroes):
    return 0

if __name__ == "__main__":
    main()
    