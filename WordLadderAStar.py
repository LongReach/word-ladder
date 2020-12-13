import word_graph as wg
import test_framework as test
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='A-Star solution to word ladder problem, please read documentation.')
parser.add_argument("-v", "--verbose", help="If set, print extra info", action="store_true")
parser.add_argument("--test", help="Which test to run: 0=simple, 1=full, 2=difficult words", type=int, default=1)
parser.add_argument("--seed", help="A seed for random number generation (to reproduce same set of games)", type=int, default=-1)
args = parser.parse_args()

test.set_verbose(args.verbose)
wg.set_random_seed(None if args.seed == -1 else args.seed)

# This implementation of Node is specific to the A-Star algorithm. It contains data that's not shared
# with other algorithms.
class AStarNode(wg.Node):

    open_list = []  # Known nodes where we haven't examined neighbors
    closed_list = []  # Known nodes where we've examined neighbors

    def __init__(self, word):
        super().__init__(word)
        self.open_list_flag = False
        self.closed_list_flag = False
        self.cost = 1000000
        self.est = 0
        self.parent = None

    # Call before each running of the algorithm
    @staticmethod
    def reset_lists():
        AStarNode.open_list.clear()
        AStarNode.closed_list.clear()
        for n in wg.Node.node_list:
            n.open_list_flag = False
            n.closed_list_flag = False
            n.cost = 1000000
            n.est = 1000000
            n.parent = None

    # Returns the most promising node from the open list, according to the general rules of A-Star
    @staticmethod
    def pop_best_open_node():
        index = 0
        lowest_score = 1000000
        for i, n in enumerate(AStarNode.open_list):
            score = n.cost + n.est
            if score < lowest_score:
                lowest_score = score
                index = i
        return AStarNode.open_list.pop(index)


def node_factory(word):
    return AStarNode(word)

wg.Node.set_factory_func(node_factory)
wg.create_nodes()
test.preliminary_test()

# A-star Solution
# --------------------------------------------
# The idea of A-star:
#
# This is a breadth-first way of finding a path through a connected graph. It's generally a faster approach than
# the recursive solution. It's analogous to pouring water on the start point; the water floods through the graph
# in all directions until the goal point is reached. After that, we continue to pour water until we've satisfied
# ourselves that it's not possible to find a better solution than those we've already uncovered. The water doesn't
# spread at the same rate in all directions, but prefers the direction the goal is in. Only after it's exhausted
# the direct approaches to the goal does it try the indirect ones.
#
# Heuristic:
#
# For each node, there's a cheapest known cost of getting to that node from the starting node and an estimate
# of the cost remaining to get to the goal node. As the algorithm progresses, these numbers are updated.
# We start with an open list, which contains known nodes for which we haven't yet examined the neighbors. As
# the open list is processed, neighbors are discovered and added to the end of the open list, and processed nodes are
# put in the closed list.
#
# If a neighbor being examined is already in the closed list, but we have a cheaper way of getting to it, we update
# that neighbor's cost and set a pointer back to the node we got there from.

def solve_a_star(src, dest):

    AStarNode.reset_lists()
    open_list = AStarNode.open_list
    closed_list = AStarNode.closed_list

    src.cost = 0
    src.open_list_flag = True
    open_list.append(src)

    final_node = None
    best_solution = 10000000
    worst_cost = 0

    # Helper function to change cost and estimate associated with next_node, also setting a pointer
    # back to prev_node
    def _set_node_values(next_node, prev_node):
        next_node.cost = prev_node.cost + 1
        # get estimate of cost remaining
        next_node.est = next_node.get_word_distance(dest)
        next_node.parent = prev_node

    while len(open_list) > 0:
        node = AStarNode.pop_best_open_node()
        node.open_list_flag = False
        # Go through neighbors
        for neighbor in node.neighbors:
            if neighbor.open_list_flag: # if in open_list
                pass
            elif neighbor.closed_list_flag: # if in closed_list
                if neighbor.cost > node.cost + 1:
                    # We've found a more efficient way to get to this neighbor
                    _set_node_values(neighbor, node)
                    if neighbor is dest:
                        if neighbor.cost < best_solution:
                            best_solution = neighbor.cost
            else:
                # Neighbor not in open or closed list
                _set_node_values(neighbor, node)
                if neighbor is dest:
                    # This is the solution
                    final_node = neighbor
                    if neighbor.cost < best_solution:
                        best_solution = neighbor.cost
                    if neighbor.cost > worst_cost:
                        worst_cost = neighbor.cost
                if neighbor.cost + neighbor.est <= best_solution:
                    # We only visit it if there's hope of beating the best solution found so far
                    neighbor.open_list_flag = True
                    open_list.append(neighbor)
        node.closed_list_flag = True
        closed_list.append(node)

    out_list = []
    while final_node is not None:
        out_list.insert(0, final_node)
        final_node = final_node.parent
    #print("Output list for {} to {} is: ".format(src, dest), wg.string_list(out_list))
    test.info("Closed list size {}, best cost {}, worst cost {}".format(len(closed_list), best_solution, worst_cost))
    return out_list

def do_word_ladder(src, dest, max_dist=20):
    if len(src) != len(dest): return None
    src_node = wg.Node.find_node(src)
    if src_node is None: return None
    dest_node = wg.Node.find_node(dest)
    if dest_node is None or dest_node is src_node: return None
    result = solve_a_star(src_node, dest_node)
    if result is None or len(result) == 0: return None
    str_list = wg.string_list(result)
    return str_list

test.set_word_ladder_func(do_word_ladder)
test.run_test(args.test)
