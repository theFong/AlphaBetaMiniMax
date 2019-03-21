
def build_game_frame(file_name):
    with open(file_name, "r") as f:
        num_heroes = int(f.next())
        alg = f.next().replace("\n", "")
        heroes = []
        for h in f:
            heroes.append([ float(a) for a in h.split(",") ])
    return { "n" : num_heroes, "alg" : alg, "heroes" : heroes}

def write_output(hero_id, file_name):
    with open(file_name, "w") as f:
        output = "{}\n".format(hero_id)
        f.write(output)

def main():
    game_frame = build_game_frame("input.txt")
    next_hero = None
    if game_frame["alg"] == "minimax":
        next_hero = minimax(game_frame["heroes"])

    elif game_frame["alg"] == "ab":
        next_hero = alpha_beta_pruning(game_frame["heroes"])
    
    else:
        raise(Exception("Bad alg on input"))

    write_output(next_hero, "output.txt")

def minimax(heroes):
    return 58502

def alpha_beta_pruning(heroes):
    return 0

if __name__ == "__main__":
    main()
    