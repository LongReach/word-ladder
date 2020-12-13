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

memoized_nodes = []

# the_list contains a path from the first node in the list to the destination node, which is last
def memoize_solution(the_list):
    # Only bother if list is long enough to be useful
    if the_list is None or len(the_list) <= 2:
        return
    first_node = the_list[0]
    first_node.set_memoize_list(the_list[1:])
    memoized_nodes.append(first_node)

def clear_memoization():
    for n in memoized_nodes:
        n.set_memoize_list(None)
    memoized_nodes.clear()

# RECURSIVE SOLUTION
# -------------------------------------------------------

# Given a path (a list of Nodes), try to compute the remainder of the path to the dest node
# remaining_steps: number of steps we are permitted to get from last node in path to dest
# Returns a remaining list of nodes (excluding those already in path) if any can be found, otherwise None
def get_steps(path, dest, remaining_steps):
    if remaining_steps == 0:
        # We already have a better solution, don't go further
        return None

    current_node = path[-1]
    if current_node.get_word_distance(dest) > remaining_steps:
        # No point to continuing, we don't have enough steps left to get to the other word
        return None

    if current_node.memoization_list is not None:
        # We already have a best solution from current_node to dest, so try to use it
        if len(current_node.memoization_list) > remaining_steps:
            # The memoization list isn't useful; the best solution from here takes too many steps.
            return None
        else:
            result = path + current_node.memoization_list
            print("A fast solution: ", wg.string_list(result))
            return current_node.memoization_list

    current_node.visited_flag = True
    matches = current_node.neighbors
    # First, search all neighbors for goal. If we find one, this saves us from any more recursion.
    for m in matches:
        if m is dest:
            # this is our goal!
            result = path + [m]
            print("A slow solution: ", wg.string_list(result))
            current_node.visited_flag = False
            return [m]

    # Goal node has not been found, attempt recursion into branches. We will choose the branch with the most
    # efficient remaining path.
    new_remaining_steps = remaining_steps - 1 # deducting one step for the neighbor, m
    best_subpath_count = 1000000
    best_subpath = None
    for m in matches:
        if not m.visited_flag:
            # See if there's a way between m and dest
            path.append(m)
            subpath = get_steps(path, dest, new_remaining_steps)
            if subpath is not None:
                subpath = [m] + subpath
                if len(subpath) < best_subpath_count:
                    best_subpath_count = len(subpath)
                    # The next branch will be even more limited in terms of remaining steps
                    # deducting one step for the neighbor, m, and one step because result must be better then the same.
                    new_remaining_steps = best_subpath_count - 2
                    best_subpath = subpath
            path.pop(-1)
    current_node.visited_flag = False
    # Save the path from m to dest so we can use it later
    memoize_solution(best_subpath)
    return best_subpath

def do_word_ladder(src, dest, max_dist=20):
    if len(src) != len(dest): return None
    src_node = wg.Node.find_node(src)
    if src_node is None: return None
    path = [src_node]
    dest_node = wg.Node.find_node(dest)
    if dest_node is None or dest_node is src_node: return None
    print("Word ladder from {} to {}, max_dist={}".format(src, dest, max_dist))
    clear_memoization()
    result = [src_node] + get_steps(path, dest_node, max_dist)
    str_list = wg.string_list(result)
    print("Steps are: ", str_list)
    return str_list

test.set_word_ladder_func(do_word_ladder)
test.run_test()

