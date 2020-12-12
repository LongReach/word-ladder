# Solution to Amazon Word Puzzle
import random

# List of all the words in the dictionary
word_list = []

file_list = ["FourLetterWords.txt", "ThreeLetterWords.txt"]
for f_name in file_list:
    file1 = open(f_name, 'r')
    file_lines = file1.readlines()

    # Strips the newline character
    for line in file_lines:
        words = line.strip().split(" ")
        # Remove any words of zero length, add remaining words to big list
        word_list = word_list + [w for w in filter(lambda x: len(x) > 0, words)]

# Given a wildcarded word (e.g. DOO*, CE*T), the wildcarded word is a key to a string containing letters that can
# replace the *
wildcard_word_dict = {}

for word in word_list:
    for l in range(len(word)):
        wildcard_word = word[:l] + "*" + word[(l+1):]
        letter_str = wildcard_word_dict.get(wildcard_word)
        if letter_str is None:
            letter_str = ""
        wildcard_word_dict[wildcard_word] = letter_str + word[l:(l+1)]

def find_matches(orig_word):
    matches = []
    for l in range(len(orig_word)):
        wildcard_word = orig_word[:l] + "*" + orig_word[(l+1):]
        letter_str = wildcard_word_dict.get(wildcard_word)
        if letter_str is not None:
            # Reconstruct word list
            for c in letter_str:
                word = orig_word[:l] + c + orig_word[(l+1):]
                if word != orig_word:
                    matches.append(word)
    return matches

def num_letters_different(word1, word2):
    num_lets = len(word1) if len(word1) < len(word2) else len(word2)
    count = 0
    for i in range(num_lets):
        if word1[i] != word2[i]:
            count = count + 1
    return count

print("Matches for 'DUMB'")
print(find_matches("DUMB"))
print("Matches for 'CART'")
print(find_matches("CART"))

# A-star Solution
# --------------------------------------------
# The idea of A-star:
#
# For each node, there's a cheapest known cost of getting to that node from the starting node and an estimate
# of the cost remaining to get to the goal node. As the algorithm progresses, these numbers are updated.
# We start with an open list, which contains known nodes for which we haven't yet examined the neighbors. As
# the open list is processed, neighbors are added to the end of the open list and processed nodes are put in
# the closed list.
#
# If a neighbor being examined is already in the closed list, but we have a cheaper way of getting to it, we update
# that neighbor's cost and set a pointer back to the node we got there from.

class Node():
    node_dict = {}
    open_list = []  # Known nodes where we haven't examined neighbors
    closed_list = []  # Known nodes where we've examined neighbors
    slow_find_count = 0
    fast_find_count = 0
    num_iterations = 0
    avg_closed_list_size = 0

    def __init__(self, word):
        self.word = word
        self.cost = 1000000
        self.est = 0
        self.parent = None
        self.neighbors = None

    def find_matches(self):
        if self.neighbors is None:
            Node.slow_find_count = Node.slow_find_count + 1
            return find_matches(self.word)
        else:
            Node.fast_find_count = Node.fast_find_count + 1
            words = [n.word for n in self.neighbors]
            return words

    def set_neighbor_node_list(self, node_list):
        if self.neighbors is None:
            self.neighbors = node_list

    def reset_lists():
        closed_list_size = len(Node.closed_list)
        Node.open_list.clear()
        Node.closed_list.clear()
        for v in Node.node_dict.values():
            v.cost = 1000000
            v.est = 0
            v.parent = None
        Node.slow_find_count = 0
        Node.fast_find_count = 0
        Node.avg_closed_list_size = (Node.num_iterations * Node.avg_closed_list_size + closed_list_size) / (Node.num_iterations + 1)
        Node.num_iterations = Node.num_iterations + 1

    def get_node(word):
        node = Node.node_dict.get(word)
        if node is None:
            node = Node(word)
            Node.node_dict[word] = node
        return node

    def pop_best_open_node():
        index = 0
        lowest_score = 1000000
        for i, n in enumerate(Node.open_list):
            score = n.cost + n.est
            if score < lowest_score:
                lowest_score = score
                index = i
        return Node.open_list.pop(index)

def solve_a_star(src, dest):

    Node.reset_lists()
    open_list = Node.open_list
    closed_list = Node.closed_list

    first_node = Node.get_node(src)
    first_node.cost = 0
    open_list.append(first_node)

    final_node = None
    best_cost = 10000000
    worst_cost = 0

    def set_node_values(next_node, prev_node):
        next_node.cost = prev_node.cost + 1
        # get estimate of cost remaining
        next_node.est = num_letters_different(next_node.word, dest)
        next_node.parent = prev_node

    while len(open_list) > 0:
        node = Node.pop_best_open_node()
        neighbor_words = node.find_matches()
        neighbor_node_list = []
        for w in neighbor_words:
            neighbor_node = Node.get_node(w)
            neighbor_node_list.append(neighbor_node)
            if neighbor_node in open_list:
                pass
            elif neighbor_node in closed_list:
                if neighbor_node.cost > node.cost + 1:
                    # We've found a more efficient way to get to this word
                    set_node_values(neighbor_node, node)
                    if neighbor_node is final_node:
                        if neighbor_node.cost < best_cost:
                            best_cost = neighbor_node.cost
            else:
                # Node not in open or closed list
                set_node_values(neighbor_node, node)
                if neighbor_node.word == dest:
                    # This is the solution
                    final_node = neighbor_node
                    if neighbor_node.cost < best_cost:
                        best_cost = neighbor_node.cost
                    if neighbor_node.cost > worst_cost:
                        worst_cost = neighbor_node.cost
                if neighbor_node.cost <= best_cost:
                    # We only visit it if there's hope of beating the best solution found so far
                    open_list.append(neighbor_node)
        node.set_neighbor_node_list(neighbor_node_list)
        closed_list.append(node)

    out_list = []
    while final_node is not None:
        out_list.insert(0, final_node.word)
        final_node = final_node.parent
    print("Output list for {} to {} is: ".format(src, dest), out_list)
    print("    Slow count {}, fast count {}".format(Node.slow_find_count, Node.fast_find_count))
    print("    Closed list size {}, best cost {}, worst cost {}".format(len(closed_list), best_cost, worst_cost))


def do_word_ladder(src, dest):
    solve_a_star(src, dest)

do_word_ladder("SEED", "TREE")
do_word_ladder("NOPE", "BOOM")
do_word_ladder("HIZZ", "OLIO")
do_word_ladder("HEAD", "TAIL")
do_word_ladder("TOAD", "FROG")
do_word_ladder("COOK", "FISH")

# Do some random ladders
count = 20
while(count):
    word1 = word_list[random.randrange(len(word_list))]
    word2 = word_list[random.randrange(len(word_list))]

    if len(word1) == len(word2):
        do_word_ladder(word1, word2)
        count = count - 1

print("Average closed list size: {}".format(Node.avg_closed_list_size))





