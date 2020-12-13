import random
import word_graph as wg

# This is a framework for running a series of word ladder games, some pre-determined, some random.
# The code here is designed to be used with either algorithm. A callback function provides a hook
# to the algorithm being used.

word_ladder_func = None
test_results = []
success_count = 0
average_result = 0
longest_result = 0

# Decorates the function below. Collects some metrics.
def ladder_func_wrapper(func_to_wrap):
    def wrapper(word1, word2, max_dist=20):
        result = func_to_wrap(word1, word2, max_dist=max_dist)
        if result is None:
            result = ["Failure from {} to {}".format(word1, word2)]
        else:
            global success_count
            global average_result
            global longest_result
            average_result = (average_result * success_count + len(result)) / (success_count + 1)
            success_count = success_count + 1
            if len(result) > longest_result:
                longest_result = len(result)
        test_results.append(result)
        return result
    return wrapper

# Call this to set the function that runs one instance of the game. That function will run the desired algorithm.
def set_word_ladder_func(func):
    global word_ladder_func
    word_ladder_func = ladder_func_wrapper(func)

# A simple test to prove that word matching words
def preliminary_test():
    print("Matches for 'DUMB'")
    print(wg.find_matches("DUMB"))
    print("Matches for 'CART'")
    print(wg.find_matches("CART"))

# A very bare-bones test
def run_simple_test():
    word_ladder_func("SEED", "TREE")
    word_ladder_func("COOK", "FISH")

# A more elaborate test. Executes a series of games.
def run_test():
    word_ladder_func("SEED", "TREE")
    word_ladder_func("NOPE", "BOOM")
    word_ladder_func("ULNA", "BLAB")
    #word_ladder_func("HEAD", "TAIL")
    #word_ladder_func("TOAD", "FROG")
    #word_ladder_func("COOK", "FISH")

    # Do some random ladders
    count = 40
    while (count):
        word1 = wg.get_random_word()
        word2, random_list = wg.get_word_by_random_wander(word1, 30)

        word_ladder_func(word1, word2, max_dist=20)
        count = count - 1

    print("")
    print("TEST RESULTS:")
    for l in test_results:
        print(l)
    print("Average length: ", average_result)
    print("Longest length: ", longest_result)