import pandas as pd
import copy
import bisect

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
        # heroes.sort_index(inplace=True,)
    return { "n" : num_heroes, "alg" : alg, "heroes" : heroes}

def write_output(hero_id, file_name):
    if hero_id == None:
        raise(Exception("output hero_id is none"))

    with open(file_name, "w") as f:
        output = "{}\n".format(hero_id)
        f.write(output)

def main():
    game_frame = build_game_frame("input.txt")
    next_hero = None

    if game_frame["alg"] == "minimax":
        # mm = MiniMax(game_frame["heroes"])
        # next_hero = mm.run()
        ab = AlphaBetaPruned(game_frame["heroes"])
        next_hero = ab.run()
    elif game_frame["alg"] == "ab":
        ab = AlphaBetaPruned(game_frame["heroes"])
        next_hero = ab.run()
    else:
        raise(Exception("Bad alg input"))

    write_output(next_hero, "output.txt")

class MiniMax(object):

    def __init__(self, heroes_df):
        self.init_available = set(self.get_available_players(heroes_df).index.tolist())
        self.init_max_heroes = set(self.get_selected_players(heroes_df, 1).index.tolist())
        self.init_min_heroes = set(self.get_selected_players(heroes_df, 2).index.tolist())

        self.heroes_data = { i : { "power" : r["power"], 1 : r["mastery_i"], 2 : r["mastery_j"] } for i, r in heroes_df[["power", "mastery_i", "mastery_j"]].iterrows() }
    def get_available_players(self, heroes_df):
        return heroes_df.loc[heroes_df["team_id"] == 0]
    
    def get_selected_players(self, heroes_df, player_id):
        return heroes_df.loc[heroes_df["team_id"] == player_id]

    def run(self):
        return self.minimax(self.init_max_heroes, self.init_min_heroes, self.init_available, True)[1]

    def minimax(self, max_heroes, min_heroes, available_players, isMaxPlayer):
        if self.get_num_selected_players(max_heroes, min_heroes) == 10:
            return self.calc_advantage(max_heroes, min_heroes), 0

        if isMaxPlayer:
            max_value = float("-inf")
            max_hero = 0

            for i in available_players:

                available_players.remove(i)
                max_heroes.add(i)

                val, _ = self.minimax(max_heroes, min_heroes, available_players, not isMaxPlayer)
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

                val, _ = self.minimax(max_heroes, min_heroes, available_players, not isMaxPlayer)
                # min
                if val < min_value:
                    min_value = val
                    min_hero = i
                elif val == min_value and i < min_hero:
                    min_hero = i
                    
                available_players.add(i)
                min_heroes.remove(i)

            return min_value, min_hero

    def get_num_selected_players(self, max_heroes, min_heroes):
        num = len(max_heroes) + len(min_heroes)
        return num
            
    def calc_advantage(self, max_heroes, min_heroes):
        # advatage = (synergy_bonus_max + sum(mastery_i_max * power_i_max) - (synergy_bonus_min + sum(mastery_i_min * power_i_min))
        return self.calc_player_advantage(max_heroes, 1) - self.calc_player_advantage(min_heroes, 2) 

    def calc_player_advantage(self, heroes_selected, player_id):
        # (synergy_bonus + sum(mastery_i * power_i)
        synergy_bonus = self.calc_synergy(heroes_selected)

        weighted_power = self.calc_weighted_power(heroes_selected, player_id)
        return synergy_bonus + weighted_power

    def calc_weighted_power(self, heroes_selected, player_id):
        # sum(mastery_i * power_i)
        total = 0
        for h in heroes_selected:
            total += self.heroes_data[h][player_id] * self.heroes_data[h]["power"]
        return total

    def calc_synergy(self, heroes_selected):
        last_set = set()
        for i in heroes_selected:
            last = i % 10
            if last in last_set:
                return 0
            last_set.add(last)
        return 120

class AlphaBetaPruned(MiniMax):

    def __init__(self, heroes_df):
        super(AlphaBetaPruned, self).__init__(heroes_df)
    
    def run(self):
        return self.alpha_beta(self.init_max_heroes, self.init_min_heroes, self.init_available, True, float("-inf"), float("inf") )[1]

    def alpha_beta(self, max_heroes, min_heroes, available_players, isMaxPlayer, alpha, beta):
        if self.get_num_selected_players(max_heroes, min_heroes) == 10:
            return self.calc_advantage(max_heroes, min_heroes), 0

        if isMaxPlayer:
            max_value = float("-inf")
            max_hero = 0

             # this bad but need balanced tree
            for i in sorted(available_players):

                available_players.remove(i)
                max_heroes.add(i)

                val, _ = self.alpha_beta(max_heroes, min_heroes, available_players, not isMaxPlayer, alpha, beta)
                # max
                if val > max_value:
                    max_hero = i
                    max_value = val
                elif val == max_value and i < max_hero:
                    max_hero = i

                available_players.add(i)
                max_heroes.remove(i)

                alpha = max(alpha, max_value)
                if alpha >= beta:
                    break

            return max_value, max_hero
        else:
            min_value = float("inf")
            min_hero = 0

            # this bad but need balanced tree
            for i in sorted(available_players):

                available_players.remove(i)
                min_heroes.add(i)

                val, _ = self.alpha_beta(max_heroes, min_heroes, available_players, not isMaxPlayer, alpha, beta)
                # min
                if val < min_value:
                    min_value = val
                    min_hero = i
                elif val == min_value and i < min_hero:
                    min_hero = i
                    
                available_players.add(i)
                min_heroes.remove(i)

                beta = min(beta, min_value)
                if alpha >= beta:
                    break

            return min_value, min_hero

if __name__ == "__main__":
    main()
    