# Solution to Amazon Word Puzzle
import random

# List of all the words in the dictionary
word_list = []

file1 = open('FourLetterWords.txt', 'r')
file_lines = file1.readlines()

# Strips the newline character
for line in file_lines:
    words = line.strip().split(" ")
    # Remove any words of zero length, add remaining words to big list
    word_list = word_list + [w for w in filter(lambda x: len(x) > 0, words)]

# Given a wildcarded word (e.g. DOO*, CE*T), the wildcarded word is a key to a list of words that match
wildcard_word_dict = {}

for word in word_list:
    for l in range(4):
        wildcard_word = word[:l] + "*" + word[(l+1):]
        words = wildcard_word_dict.get(wildcard_word)
        if words is None:
            words = [word]
            wildcard_word_dict[wildcard_word] = words
        else:
            # Randomize the list so that depth-first search is less likely to go down ridiculously long path
            rand_idx = random.randrange(len(words))
            words.insert(rand_idx, word)

def find_matches(orig_word):
    matches = []
    for l in range(4):
        wildcard_word = orig_word[:l] + "*" + orig_word[(l+1):]
        words = wildcard_word_dict.get(wildcard_word)
        if words is not None:
            matches = matches + [w for w in words if w != orig_word]
    return matches

print("Matches for 'DUMB'")
print(find_matches("DUMB"))
print("Matches for 'CART'")
print(find_matches("CART"))

# Each node in the path under consideration, not counting very last node
explored_list = []
# Length of shortest successful path found so far
shortest_path_length: int = 20

# RECURSIVE SOLUTION

# Returns a list containing the words between src and dest, excluding src
def get_steps(src, dest):
    global shortest_path_length
    explored_list.append(src)
    if len(explored_list) >= shortest_path_length:
        # We already have a better solution, don't go further
        explored_list.pop(-1)
        return []

    best_subpath_count = 10000000
    best_subpath = []
    matches = find_matches(src)
    for m in matches:
        if m == dest:
            # this is our goal!
            result = explored_list + [m]
            print("A solution: ", result)
            shortest_path_length = len(explored_list)
            explored_list.pop(-1)
            return [m]
        if m not in explored_list:
            # See if there's a way between m and dest
            steps = get_steps(m, dest)
            count = len(steps)
            if count > 0 and count < best_subpath_count:
                best_subpath_count = count
                best_subpath = [m] + steps
    explored_list.pop(-1)
    #print("Result: ", best_list)
    return best_subpath

def do_word_ladder(src, dest):
    global shortest_path_length
    shortest_path_length = 20
    result = [src] + get_steps(src, dest)
    print("Steps are: ", result)

do_word_ladder("SEED", "TREE")
do_word_ladder("NOPE", "BOOM")
do_word_ladder("HEAD", "TAIL")
do_word_ladder("TOAD", "FROG")
do_word_ladder("COOK", "FISH")

# Do some random ladders
count = 20
while(count):
    word1 = word_list[random.randrange(len(word_list))]
    word2 = word_list[random.randrange(len(word_list))]
    print("Comparing random {} to {}".format(word1, word2))

    if len(word1) == len(word2):
        do_word_ladder(word1, word2)
        count = count - 1

# Dynamic programming:
# Go until we find a known strand

# Genetic
# Make a bunch of random pathways. They are scored by how close they get and how short they are.
# Pathways can mate if they have a node in common. Mutation affects the end of a pathway.