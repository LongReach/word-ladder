class Node():

    factory_func = None

    def __init__(self, word):
        self.word = word
        self.neighbors = []

    def add_neighbor(self, node):
        self.neighbors.append(node)

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

node_list = []
# Given a wildcard-ed word (e.g. "DOO*", "CE*T"), the wildcard-ed word is a key to a list of nodes that match
wildcard_node_dict = {}

# Construct all the nodes and populate the wildcard node dictionary
for word in word_list:
    node = Node.make_node(word)
    node_list.append(node)
    # if word is "SALT", it can be found via "*ALT", "S*LT", "SA*T", and "SAL*"
    for l in range(len(word)):
        wildcard_word = word[:l] + "*" + word[(l+1):]
        nodes = wildcard_node_dict.get(wildcard_word)
        if nodes is None:
            nodes = []
            wildcard_node_dict[wildcard_word] = nodes
        nodes.append(node)

# Now that all nodes exist, set the neighbor connections
for node in node_list:
    word = node.word
    for l in range(len(word)):
        wildcard_word = word[:l] + "*" + word[(l+1):]
        nodes = wildcard_node_dict.get(wildcard_word)
        if nodes is not None:
            for adj in nodes:
                if adj is not node:
                    node.add_neighbor(adj)

def find_node(word):
    for l in range(len(word)):
        wildcard_word = word[:l] + "*" + word[(l+1):]
        nodes = wildcard_node_dict.get(wildcard_word)
        if nodes is not None:
            for node in nodes:
                if node.word == word:
                    return node
        return None

def find_matches(word):
    node = find_node(word)
    return node.list_matches() if node is not None else []

def string_list(node_list):
    return [n.word for n in node_list]
