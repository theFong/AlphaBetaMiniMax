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
    return minimax(heroes, True)

def minimax(heroes, isMaxPlayer):
    if len(get_num_selected_players(heroes)) == 10: # if at leaf node #TODO possible bugs exist here
        selected_players = get_selected_players(heroes, isMaxPlayer)
        return calc_advantage(selected_players, isMaxPlayer)

    available_players = get_available_players(heroes)
    if isMaxPlayer:
        max_value = float("-inf")
        max_hero = 0
        for i, r in available_players.iterrows():
            nf = available_players.copy()
            nf.loc[i]["team_id"] = 1
            val, _ = minimax(nf, not isMaxPlayer)
            # max
            if val > max_value:
                max_hero = i
                max_value = val
        return max_value, max_hero
    else:
        min_value = float("inf")
        min_hero = 0
        for i, r in available_players.iterrows():
            nf = available_players.copy()
            nf.loc[i]["team_id"] = 2
            val, _ = minimax(nf, not isMaxPlayer)
            # min
            if val < min_value:
                min_value = val
                min_hero = i
        return min_value, min_hero

def get_selected_players(heroes_df, isMaxPlayer):
    player_id = 1 if isMaxPlayer else 2
    return heroes_df.loc[heroes_df["team_id"] == player_id]

def get_num_selected_players(heroes_df):
    return len(heroes_df.loc[heroes_df["team_id"] == 1]) + len(heroes_df.loc[heroes_df["team_id"] == 1])

def get_available_players(heroes_df):
    return heroes_df.loc[heroes_df["team_id"] == 0]
        
def calc_advantage(selected_players, isMaxPlayer):
    player_id = 1 if isMaxPlayer else 2
    return 0


def apply_alpha_beta_pruning(heroes):
    return 0

if __name__ == "__main__":
    main()
    