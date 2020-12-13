import random

print("*** WORD GRAPH ***")

# Both the recursive and A-Star solutions to the word ladder problem rely on a connected graph. Each node
# on the graph represents a word, and its neighbors are the nodes that can be reached by changing a single
# letter in the word. Thus, "TREE" would be neighbors with "FREE", but not with "BUSH". To get to "BUSH",
# several nodes would have to be traversed.
#
# The code in this file processes some text files to generate a list of three and four-letter words. The
# words are then processed into Node objects, and the nodes are connected to one another.

# This is a base class, meant to be subclassed by the different algorithms
class Node(object):

    node_list = []
    # Given a wildcard-ed word (e.g. "DOO*", "CE*T"), the wildcard-ed word is a key to a list of nodes that match
    # The entry for "DOO*" would contain "DOOM" and "DOOR"
    wildcard_node_dict = {}

    factory_func = None

    def __init__(self, word):
        self.word = word
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    # Returns a copy of the neighbor list, but in random order
    def get_randomized_neighbor_list(self):
        new_list = []
        for n in self.neighbors:
            size = len(new_list)
            idx = 0 if size == 0 else random.randrange(size)
            new_list.insert(idx, n)
        return new_list

    # Gets an estimated distance between this node's word and the other node's.
    # The distance is the minimum number of letter changes required in the game to get between the two words.
    # The actual solution might take more steps than that.
    def get_word_distance(self, other_node):
        if self is other_node: return 0
        dist = 0
        for idx in range(len(self.word)):
            if self.word[idx] != other_node.word[idx]:
                dist = dist + 1
        return dist

    # Returns a list of neighboring words
    def list_matches(self):
        return [node.word for node in self.neighbors]

    # The factory function allows us to make instances of Node subclasses
    @staticmethod
    def set_factory_func(factory_fn):
        Node.factory_func = factory_fn

    @staticmethod
    def make_node(word):
        if Node.factory_func is not None:
            return Node.factory_func(word)
        else:
            return Node(word)

    # Given a list of words, generate all the nodes
    @staticmethod
    def populate_nodes_from_word_list(list_of_words):
        # Construct all the nodes and populate the wildcard node dictionary
        for word in list_of_words:
            node = Node.make_node(word)
            Node.node_list.append(node)
            # if word is "SALT", it can be found via "*ALT", "S*LT", "SA*T", and "SAL*"
            for l in range(len(word)):
                wildcard_word = word[:l] + "*" + word[(l + 1):]
                nodes = Node.wildcard_node_dict.get(wildcard_word)
                if nodes is None:
                    nodes = []
                    Node.wildcard_node_dict[wildcard_word] = nodes
                nodes.append(node)

        # Now that all nodes exist, set the neighbor connections
        for node in Node.node_list:
            word = node.word
            for l in range(len(word)):
                wildcard_word = word[:l] + "*" + word[(l + 1):]
                nodes = Node.wildcard_node_dict.get(wildcard_word)
                if nodes is not None:
                    for adj in nodes:
                        if adj is not node:
                            node.add_neighbor(adj)

    # Given a word, return the appropriate node, if it exists.
    @staticmethod
    def find_node(word):
        for l in range(len(word)):
            wildcard_word = word[:l] + "*" + word[(l+1):]
            nodes = Node.wildcard_node_dict.get(wildcard_word)
            if nodes is not None:
                for node in nodes:
                    if node.word == word:
                        return node
            return None


# List of all the words in the dictionary
word_list = []

# Process the text files
file_list = ["FourLetterWords.txt", "ThreeLetterWords.txt"]
for f_name in file_list:
    file1 = open(f_name, 'r')
    file_lines = file1.readlines()

    # Strips the newline character
    for line in file_lines:
        words = line.strip().split(" ")
        # Remove any words of zero length, add remaining words to big list
        word_list = word_list + [w for w in filter(lambda x: len(x) > 0, words)]

def create_nodes():
    Node.populate_nodes_from_word_list(word_list)

# Return all the words that are one letter away from the one passed in
def find_matches(word):
    node = Node.find_node(word)
    return node.list_matches() if node is not None else []

# Given a node list, return a list of words
def string_list(node_list):
    return [n.word for n in node_list]

# Return a random word from the words available
def get_random_word(length=0):
    word = ""
    for i in range(1000):
        word = word_list[random.randrange(len(word_list))]
        if length == 0 or len(word) == length:
            break
    return word

# Given a starting word, we wander randomly around the connecting graph for some distance and return
# whatever word we arrive at. Function also returns the list of nodes traversed. This is useful for
# finding two words that can actually be connected, though there's likely to be a much more efficient
# connection than the random path.
def get_word_by_random_wander(src_word, distance):
    node = Node.find_node(src_word)
    if node is None: return
    visted_nodes = [node]
    while distance > 0:
        # Attempt to get a neighbor we haven't visited yet
        success = False
        neighbors = node.get_randomized_neighbor_list()
        for n in neighbors:
            if n not in visted_nodes:
                node = n
                success = True
                visted_nodes.append(node)
                break
        if not success:
            break
        distance = distance - 1
    return node.word, visted_nodes

