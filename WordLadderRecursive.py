import random
import word_graph as wg
import test_framework as test
import copy

test.preliminary_test()

# MEMOIZATION
# -------------------------------------------------------

class MemNode(wg.Node):

    memoized_nodes = []

    def __init__(self, word):
        super().__init__(word)
        # All known memoization lists that have this node on their route
        self.memoization_list = None
        self.visited_flag = False

    def set_memoize_list(self, the_list):
        self.memoization_list = the_list

    def get_memoize_list(self):
        return self.memoization_list

    # the_list contains a path from the first node in the list to the destination node, which is last
    @staticmethod
    def memoize_solution(the_list):
        # Only bother if list is long enough to be useful
        if the_list is None or len(the_list) <= 2:
            return
        first_node = the_list[0]
        first_node.set_memoize_list(the_list[1:])
        MemNode.memoized_nodes.append(first_node)

    @staticmethod
    def clear_memoization():
        for n in MemNode.memoized_nodes:
            n.set_memoize_list(None)
        MemNode.memoized_nodes.clear()

def node_factory(word):
    return MemNode(word)

wg.Node.set_factory_func(node_factory)
wg.create_nodes()


# RECURSIVE SOLUTION
# -------------------------------------------------------
#
# The idea is to start from the source node and do a depth-first search through the connected graph to try to find the
# destination node. Once it is reached, we take note of the length of the the solution and continue on with
# the depth-first search. We prune the search tree to avoid pursuing solutions that are more costly than
# the best solution we have so far.
#
# The memoization feature takes advantage of the fact that separate branches of the search tree may overlap,
# sharing subbranches. If we've already solved a subbranch, we can just reuse the cached solution. Another way to
# explain it: once we know the best route between Boston and New York, any potential route from London to New York
# that passes through Boston only needs to be solved as far as Boston. Once we get there, we can use the already
# cached instructions for getting from Boston to New York.

# Given a path (a list of Nodes), try to compute the remainder of the path to the dest node.
#
# Params:
#     path: list of nodes forming a path. The start node is always at the beginning
#     dest: destination node
#     remaining_steps: number of steps we are permitted to get from last node in path to dest node
# Returns a list of remaining nodes to destination (excluding those already in path) if any can be found, otherwise None
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
    MemNode.memoize_solution(best_subpath)
    return best_subpath

def do_word_ladder(src, dest, max_dist=20):
    if len(src) != len(dest): return None
    src_node = wg.Node.find_node(src)
    if src_node is None: return None
    path = [src_node]
    dest_node = wg.Node.find_node(dest)
    if dest_node is None or dest_node is src_node: return None
    print("Word ladder from {} to {}, max_dist={}".format(src, dest, max_dist))
    MemNode.clear_memoization()
    result = [src_node] + get_steps(path, dest_node, max_dist)
    str_list = wg.string_list(result)
    print("Steps are: ", str_list)
    return str_list

test.set_word_ladder_func(do_word_ladder)
test.run_test()

