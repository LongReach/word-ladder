import random
import word_graph as wg
import test_framework as test
import copy

# MEMOIZATION
# -------------------------------------------------------

class AStarNode(wg.Node):

    open_list = []  # Known nodes where we haven't examined neighbors
    closed_list = []  # Known nodes where we've examined neighbors

    def __init__(self, word):
        super().__init__(word)
        self.open_list_flag = False
        self.cost = 1000000
        self.est = 0
        self.parent = None

    @staticmethod
    def reset_lists():
        AStarNode.open_list.clear()
        AStarNode.closed_list.clear()
        for n in wg.Node.node_list:
            n.open_list_flag = False
            n.visited_flag = False
            n.cost = 1000000
            n.est = 1000000
            n.parent = None

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
# For each node, there's a cheapest known cost of getting to that node from the starting node and an estimate
# of the cost remaining to get to the goal node. As the algorithm progresses, these numbers are updated.
# We start with an open list, which contains known nodes for which we haven't yet examined the neighbors. As
# the open list is processed, neighbors are added to the end of the open list and processed nodes are put in
# the closed list.
#
# If a neighbor being examined is already in the closed list, but we have a cheaper way of getting to it, we update
# that neighbor's cost and set a pointer back to the node we got there from.

# Cached shortcut: at each node, see if there is a shortcut with that node in it. If there is, see if shortcut also
# includes the destination.

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

    def set_node_values(next_node, prev_node):
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
            elif neighbor.visited_flag: # if in closed_list
                if neighbor.cost > node.cost + 1:
                    # We've found a more efficient way to get to this node
                    set_node_values(neighbor, node)
                    if neighbor is dest:
                        if neighbor.cost < best_solution:
                            best_solution = neighbor.cost
            else:
                # Node not in open or closed list
                set_node_values(neighbor, node)
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
        node.visited_flag = True
        closed_list.append(node)

    out_list = []
    while final_node is not None:
        out_list.insert(0, final_node)
        final_node = final_node.parent
    #print("Output list for {} to {} is: ".format(src, dest), wg.string_list(out_list))
    print("Closed list size {}, best cost {}, worst cost {}".format(len(closed_list), best_solution, worst_cost))
    return out_list

def do_word_ladder(src, dest, max_dist=20):
    if len(src) != len(dest): return None
    src_node = wg.Node.find_node(src)
    if src_node is None: return None
    dest_node = wg.Node.find_node(dest)
    if dest_node is None or dest_node is src_node: return None
    print("Word ladder from {} to {}, max_dist={}".format(src, dest, max_dist))
    result = solve_a_star(src_node, dest_node)
    str_list = wg.string_list(result)
    print("Steps are: ", str_list)
    return str_list

test.set_word_ladder_func(do_word_ladder)
test.run_test()
