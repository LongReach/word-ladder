import random
import time
import re
import os.path

# List of all the words in the dictionary
word_list = []
the_random_seed = 0

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

    # Each node is a part of a network of mutually connected nodes, each network has own number
    # Contains lists of nodes, one for each network
    networks = []

    factory_func = None

    def __init__(self, word):
        self.word = word
        self.neighbors = []
        self.network_number = -1 # See explanation of networks above

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

    # Determines what nodes belong to what networks. This is useful because no connection is possible between
    # nodes in separate networks
    @staticmethod
    def find_isolated_nodes():
        current_network = 0
        while(True):
            # find a node without a network tag
            start_node = None
            for n in Node.node_list:
                if n.network_number == -1:
                    start_node = n
                    break
            if start_node is None:
                # We've processed all the nodes, exit while loop
                break

            nodes_in_network = []

            # open_list will contain nodes we need to visit, b/c they're connected to a node we've already been to.
            open_list = [start_node]
            while len(open_list) > 0:
                node = open_list.pop(0)
                for m in node.neighbors:
                    if m.network_number == -1 and m not in open_list:
                        open_list.append(m)
                nodes_in_network.append(node)
                node.network_number = current_network

            # We've completed a network
            Node.networks.append(nodes_in_network)
            current_network = current_network + 1

def process_text_files(src_file=None):
    global word_list
    # Process the text files
    file_list = []
    if src_file is None:
        file_list = file_list + [os.path.join("data", "FourLetterWords.txt"), os.path.join("data", "ThreeLetterWords.txt")]
    else:
        file_list.append(src_file)

    word_set = set()
    for f_name in file_list:
        with open(f_name) as words_file:
            lines = words_file.readlines()
            for line in lines:
                words = re.findall("[a-zA-Z]+", line)
                for word in words:
                    uc = word.upper()
                    if len(uc) >= 3 and len(uc) <= 5:
                        word_set.add(uc)
    word_list = list(word_set)

def create_nodes(word_file=None):
    process_text_files(word_file)
    Node.populate_nodes_from_word_list(word_list)
    Node.find_isolated_nodes()

# Return all the words that are one letter away from the one passed in
def find_matches(word):
    node = Node.find_node(word)
    return node.list_matches() if node is not None else []

# Given a node list, return a list of words
def string_list(node_list):
    if node_list is None:
        return []
    return [n.word for n in node_list]

# First return value: whether or not a path is possible
# Second return value: True if both nodes are valid
def is_path_possible(word1, word2):
    node1 = Node.find_node(word1)
    node2 = Node.find_node(word2)
    if node1 is None or node2 is None: return False, False
    return node1.network_number == node2.network_number, True

def set_random_seed(seed):
    global the_random_seed
    if seed is None:
        # choose a seed at random (sort of)
        seed = int(time.time()) % 100000
    the_random_seed = seed
    random.seed(the_random_seed)

def get_random_seed():
    return the_random_seed

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

