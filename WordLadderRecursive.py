import random
import word_graph as wg
import test_framework as test

test.preliminary_test()

def node_factory(word):
    return wg.Node(word)

wg.Node.set_factory_func(node_factory)


# Each node in the path under consideration, not counting very last node
explored_list = []
# Length of shortest successful path found so far
shortest_path_length: int = 20

# RECURSIVE SOLUTION

# Returns a list containing the nodes between src and dest, excluding src
def get_steps(src, dest_word):
    global shortest_path_length
    explored_list.append(src)
    if len(explored_list) >= shortest_path_length:
        # We already have a better solution, don't go further
        explored_list.pop(-1)
        return []

    best_subpath_count = 10000000
    best_subpath = []
    matches = src.neighbors
    for m in matches:
        if m.word == dest_word:
            # this is our goal!
            result = explored_list + [m]
            print("A solution: ", wg.string_list(result))
            shortest_path_length = len(explored_list)
            explored_list.pop(-1)
            return [m]
        if m not in explored_list:
            # See if there's a way between m and dest
            steps = get_steps(m, dest_word)
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
    src_node = wg.find_node(src)
    print("Word ladder from {} to {}".format(src, dest))
    result = [src_node] + get_steps(src_node, dest)
    print("Steps are: ", wg.string_list(result))

test.set_word_ladder_func(do_word_ladder)
test.run_test()

