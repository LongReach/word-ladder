import random
import word_graph as wg
import test_framework as test
import copy

test.preliminary_test()

def node_factory(word):
    return wg.Node(word)

wg.Node.set_factory_func(node_factory)

# MEMOIZATION
# -------------------------------------------------------

# Will contain lists of nodes
memoization_lists = []

def memoize_solution(the_list):
    # Only bother if list is long enough to be useful
    if len(the_list) <= 2:
        return
    new_list = copy.copy(the_list)
    memoization_lists.append(new_list)
    for n in new_list:
        n.add_memoize_list(new_list)

def get_overlapping_memoize_lists():
    results = []
    for l in memoization_lists:
        for n in l:
            overlaps = n.get_overlapping_memoize_lists(l)
            for ol in overlaps:
                if ol not in results:
                    results.append(ol)
    return results


# RECURSIVE SOLUTION
# -------------------------------------------------------

# Each node in the path under consideration, not counting very last node
explored_list = []
# Length of shortest successful path found so far
shortest_path_length: int = 20

# Returns a list containing the nodes between src and dest, excluding src
def get_steps(src, dest):
    if src is dest:
        return []
    memo_list = dest.get_memoize_list_with_node(src)
    if memo_list is not None:
        print("Memoization exists for {} to {}: ".format(src.word, dest.word), wg.string_list(memo_list))
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
        if m.word == dest.word:
            # this is our goal!
            result = explored_list + [m]
            print("A solution: ", wg.string_list(result))
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
    src_node = wg.Node.find_node(src)
    dest_node = wg.Node.find_node(dest)
    print("Word ladder from {} to {}".format(src, dest))
    result = [src_node] + get_steps(src_node, dest_node)
    memoize_solution(result)
    print("Steps are: ", wg.string_list(result))

test.set_word_ladder_func(do_word_ladder)
test.run_test()

print("")
print("MEMOIZATION LISTS")
for l in memoization_lists:
    print(wg.string_list(l))
print("")
print("OVERLAPPING MEMOIZATION LISTS")
overlapping_lists = get_overlapping_memoize_lists()
for ol in overlapping_lists:
    print(wg.string_list(ol))
