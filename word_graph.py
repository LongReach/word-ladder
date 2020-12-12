import random

print("*** WORD GRAPH ***")

class Node():

    node_list = []
    # Given a wildcard-ed word (e.g. "DOO*", "CE*T"), the wildcard-ed word is a key to a list of nodes that match
    wildcard_node_dict = {}

    factory_func = None

    def __init__(self, word):
        self.word = word
        self.neighbors = []
        # All known memoization lists that have this node on their route
        self.memoization_lists = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

    def get_randomized_neighbor_list(self):
        new_list = []
        for n in self.neighbors:
            size = len(new_list)
            idx = 0 if size == 0 else random.randrange(size)
            new_list.insert(idx, n)
        return new_list

    def list_matches(self):
        return [node.word for node in self.neighbors]

    def add_memoize_list(self, the_list):
        self.memoization_lists.append(the_list)

    def get_memoize_list_with_node(self, node):
        for l in self.memoization_lists:
            for n in l:
                if n is node:
                    return l
        return None

    def get_overlapping_memoize_lists(self, a_list):
        results = []
        for l in self.memoization_lists:
            if l is not a_list:
                results.append(l)
        return results

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

file_list = ["FourLetterWords.txt", "ThreeLetterWords.txt"]
for f_name in file_list:
    file1 = open(f_name, 'r')
    file_lines = file1.readlines()

    # Strips the newline character
    for line in file_lines:
        words = line.strip().split(" ")
        # Remove any words of zero length, add remaining words to big list
        word_list = word_list + [w for w in filter(lambda x: len(x) > 0, words)]

Node.populate_nodes_from_word_list(word_list)

def find_matches(word):
    node = Node.find_node(word)
    return node.list_matches() if node is not None else []

def string_list(node_list):
    return [n.word for n in node_list]

def get_random_word(length=0):
    word = ""
    for i in range(1000):
        word = word_list[random.randrange(len(word_list))]
        if length == 0 or len(word) == length:
            break
    return word

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

