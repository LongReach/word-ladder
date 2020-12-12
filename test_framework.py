import random
import word_graph as wg

word_ladder_func = None

def set_word_ladder_func(func):
    global word_ladder_func
    word_ladder_func = func

def preliminary_test():
    print("Matches for 'DUMB'")
    print(wg.find_matches("DUMB"))
    print("Matches for 'CART'")
    print(wg.find_matches("CART"))

def run_test():
    word_ladder_func("SEED", "TREE")
    word_ladder_func("NOPE", "BOOM")
    word_ladder_func("HEAD", "TAIL")
    word_ladder_func("TOAD", "FROG")
    word_ladder_func("COOK", "FISH")

    # Do some random ladders
    count = 20
    while (count):
        word1 = wg.get_random_word()
        word2 = wg.get_random_word()

        if len(word1) == len(word2):
            word_ladder_func(word1, word2)
            count = count - 1
