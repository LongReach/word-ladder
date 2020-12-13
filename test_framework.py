import word_graph as wg
import time

# This is a framework for running a series of word ladder games, some pre-determined, some random.
# The code here is designed to be used with either algorithm. A callback function provides a hook
# to the algorithm being used.

verbose_mode = False

def set_verbose(verbose):
    global verbose_mode
    verbose_mode = verbose

def info(*args, **kvargs):
    global verbose_mode
    if verbose_mode:
        print(*args, **kvargs)

word_ladder_func = None
# List of dictionaries.
test_results = []

# Decorates the function below. Collects some metrics.
def ladder_func_wrapper(func_to_wrap):
    def wrapper(word1, word2, max_dist=20):
        print("Word ladder from {} to {}, max_dist={}".format(word1, word2, max_dist))
        start_time = time.time()
        result = func_to_wrap(word1, word2, max_dist=max_dist)
        end_time = time.time()
        print("Steps are: ", result)
        success = True
        if result is None:
            result = []
            success = False
        test_outcome_dict = {'words':result, 'src':word1, 'dest':word2, 'success':success, 'time':(end_time-start_time)}
        test_results.append(test_outcome_dict)
        return result
    return wrapper

# Call this to set the function that runs one instance of the game. That function will run the desired algorithm.
def set_word_ladder_func(func):
    global word_ladder_func
    word_ladder_func = ladder_func_wrapper(func)

# A simple test to prove that word matching words
def preliminary_test():
    info("Matches for 'DUMB'")
    info(wg.find_matches("DUMB"))
    info("Matches for 'CART'")
    info(wg.find_matches("CART"))

# A very bare-bones test
def simple_test():
    word_ladder_func("SEED", "TREE")
    word_ladder_func("COOK", "FISH")
    print("random word: ", wg.get_random_word())
    print("random word: ", wg.get_random_word())
    print("Random seed: ", wg.get_random_seed())

def difficult_words_test():
    word_ladder_func("NOVA", "SPRY")
    word_ladder_func("FISC", "UMPY")
    word_ladder_func("LOGE", "UDON")
    word_ladder_func("MAZE", "UFOS")
    word_ladder_func("YUKY", "EGMA")
    word_ladder_func("WHIO", "EXUL") # "EXUL" is unreachable
    word_ladder_func("FRET", "YGOE")

    process_test_results()

# A more elaborate test. Executes a series of games.
def full_test():
    # basic tests
    word_ladder_func("SEED", "TREE")
    word_ladder_func("NOPE", "BOOM")
    word_ladder_func("ULNA", "BLAB")
    word_ladder_func("HEAD", "TAIL")
    word_ladder_func("TOAD", "FROG")
    word_ladder_func("COOK", "FISH")

    # bad data
    word_ladder_func("BUTT", "BUTT")
    word_ladder_func("TEAM", "ME")
    word_ladder_func("WORD", "XXXX")
    word_ladder_func("YYYY", "WORD")
    word_ladder_func("FFFF", "----")

    # Do some random ladders
    # These words have a connection between them
    for i in range(20):
        word1 = wg.get_random_word()
        word2, random_list = wg.get_word_by_random_wander(word1, 30)
        word_ladder_func(word1, word2, max_dist=20)

    # These words might or might not have a connection between them
    for i in range(20):
        word1 = wg.get_random_word()
        word2 = wg.get_random_word(length=len(word1))
        word_ladder_func(word1, word2, max_dist=20)

    process_test_results()

def run_test(test_type):
    print("Running test ", test_type)
    if test_type == 0:
        print("simple test")
        simple_test()
    elif test_type == 1:
        full_test()
    elif test_type == 2:
        difficult_words_test()

def process_test_results():

    success_count = 0
    total_length = 0
    longest_result_entry = {'words':[]}
    total_time = 0
    longest_time_entry = {'time':0}

    problem_length = 8
    problem_length_entries = []
    problem_time = 2.0
    problem_time_entries = []

    print("")
    print("TEST RESULTS:")
    for t_o in test_results:
        if t_o['success']:
            print("{} to {}:".format(t_o['src'], t_o['dest']), t_o['words'], " time={}".format(t_o['time']))
            success_count = success_count + 1
            total_length = total_length + len(t_o['words'])
            if len(t_o['words']) > len(longest_result_entry['words']):
                longest_result_entry = t_o
            if len(t_o['words']) > problem_length:
                problem_length_entries.append(t_o)
        else:
            print("Failed for: {} to {}".format(t_o['src'], t_o['dest']))

        total_time = total_time + t_o['time']
        if t_o['time'] > longest_time_entry['time']:
            longest_time_entry = t_o
        if t_o['time'] > problem_time:
            problem_time_entries.append(t_o)

    print("Average length: ", total_length / success_count)
    print("Longest length: ", len(longest_result_entry['words']), " ", longest_result_entry['words'])
    print("Average time: ", total_time / len(test_results))
    print("Longest time: ", longest_time_entry['time'], " ", longest_time_entry['words'])
    print("Random seed: ", wg.get_random_seed())

    if len(problem_length_entries) > 0:
        print("")
        print("PROBLEM LENGTH ENTRIES:")
        for t_o in problem_length_entries:
            print(t_o['words'], " length={}".format(len(t_o['words'])))

    if len(problem_time_entries) > 0:
        print("")
        print("PROBLEM TIME ENTRIES:")
        for t_o in problem_time_entries:
            print(t_o['words'], " time={}".format(t_o['time']))
