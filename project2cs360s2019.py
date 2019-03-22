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

def apply_minimax(heroes):
    return minimax(heroes, True)[1]

def minimax(heroes, isMaxPlayer):
    if get_num_selected_players(heroes) == 10: # if at leaf node #TODO possible bugs exist here
        return calc_advantage(heroes), 0

    available_players = get_available_players(heroes)
    if isMaxPlayer:
        max_value = float("-inf")
        max_hero = 0
        for i, _ in available_players.iterrows():
            nf = heroes.copy()
            nf.at[i, "team_id"] = 1
            val, _ = minimax(nf, not isMaxPlayer)
            # max
            if val > max_value:
                max_hero = i
                max_value = val
        return max_value, max_hero
    else:
        min_value = float("inf")
        min_hero = 0
        for i, _ in available_players.iterrows():
            nf = heroes.copy()
            nf.at[i, "team_id"] = 2
            val, _ = minimax(nf, not isMaxPlayer)
            # min
            if val < min_value:
                min_value = val
                min_hero = i
        return min_value, min_hero

def get_selected_players(heroes_df, isMaxPlayer):
    player_id = 1 if isMaxPlayer else 2
    return heroes_df.loc[heroes_df["team_id"] == player_id]

# this may need to be optimized
def get_num_selected_players(heroes_df):
    num = len(heroes_df.loc[heroes_df["team_id"] == 1]) + len(heroes_df.loc[heroes_df["team_id"] == 2])
    if num == 8 or num == 9 or num == 10:
        print(heroes_df)
    return num

# this may need to be optimized
def get_available_players(heroes_df):
    return heroes_df.loc[heroes_df["team_id"] == 0]
        
def calc_advantage(heroes_df):
    # advatage = (synergy_bonus_max + sum(mastery_i_max * power_i_max) - (synergy_bonus_min + sum(mastery_i_min * power_i_min))
    return calc_player_advantage(heroes_df, 1) - calc_player_advantage(heroes_df, 2) 

def calc_player_advantage(heroes_df, player_id):
    # (synergy_bonus + sum(mastery_i * power_i)
    heroes_selected = heroes_df.loc[heroes_df["team_id"] == player_id]
    synergy_bonus = 120 if calc_synergy(heroes_selected) else 0

    mastery_column = ""
    if player_id == 1:
        mastery_column = "mastery_i"
    elif player_id == 2:
        mastery_column = "mastery_j"
    else:
        raise(Exception("Invalid player id when calculating advantage"))

    mastery = heroes_selected[[mastery_column]]
    power = heroes_selected[["power"]]

    return synergy_bonus + mastery.T.dot(power).iloc[0,0]

def calc_synergy(heroes_selected):
    last_set = set()
    for i in heroes_selected.index:
        last = str(i)[-1]
        if last in last_set:
            return False
        last_set.add(last)
    return True

def apply_alpha_beta_pruning(heroes):
    return 0

if __name__ == "__main__":
    main()
    