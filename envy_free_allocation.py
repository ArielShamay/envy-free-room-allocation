"""
Envy-Free Room Allocation using Maximum Weight Matching and Longest Path in Envy Graph.

This module implements a fair division algorithm for the rent division problem,
ensuring that the final allocation is envy-free.
"""

import numpy as np
from scipy.optimize import linear_sum_assignment
import unittest


def envy_free_room_allocation(valuations: list[list[float]], rent: float) -> tuple[dict, dict]:
    """
    Calculates an envy-free allocation of rooms and prices.
    
    Args:
        valuations: A list of lists where valuations[i][j] is the value player i assigns to room j.
        rent: The total rent sum to be divided among players.
        
    Returns:
        A tuple containing:
        1. Assignment dictionary: {player_index: room_index}
        2. Pricing dictionary: {room_index: price}
    """
    n = len(valuations)
    valuations_array = np.array(valuations)
    
    # ===================================================================
    # Phase A: Assignment (Maximizing Social Welfare)
    # ===================================================================
    # Use linear_sum_assignment to find maximum weight matching.
    # Since it minimizes cost, we negate the valuations to maximize.
    cost_matrix = -valuations_array
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Create assignment dictionary: player -> room
    assignment = {player: room for player, room in zip(row_ind, col_ind)}
    
    # ===================================================================
    # Phase B: Pricing (Eliminating Envy)
    # ===================================================================
    
    # Build the Envy Graph
    # Edge weight from player i to player j is:
    # envy(i,j) = value_i(room_j) - value_i(room_i)
    envy_graph = np.zeros((n, n))
    for i in range(n):
        room_i = assignment[i]
        for j in range(n):
            room_j = assignment[j]
            # Envy of player i towards player j
            envy_graph[i][j] = valuations_array[i][room_j] - valuations_array[i][room_i]
    
    # Calculate subsidies (q_i) using Bellman-Ford algorithm
    # q_i is the weight of the longest path starting from node i
    # 
    # WHY Bellman-Ford?
    # - The envy graph may have negative edges (when player i prefers their own room)
    # - We need to find LONGEST paths, which we do by finding SHORTEST paths 
    #   in the negated graph (multiply weights by -1)
    # - Bellman-Ford handles negative edges and detects negative cycles
    # - Since our assignment maximizes social welfare, there are no positive cycles
    #   in the envy graph (equivalently, no negative cycles in the negated graph)
    
    q = np.zeros(n)
    for start_node in range(n):
        # Find longest paths from start_node to all other nodes
        # by finding shortest paths in the negated graph
        distances = bellman_ford_longest_path(envy_graph, start_node, n)
        # q_i is the maximum (longest) path weight from node i
        q[start_node] = np.max(distances)
    
    # Calculate final prices
    # WHY this formula?
    # - S = sum of subsidies represents the total "envy reduction" needed
    # - R = total rent to be collected
    # - We distribute (R + S) equally among players as a base amount: (R+S)/n
    # - Then subtract each player's subsidy q_i to get their room price
    # - This ensures: 
    #   1. Sum of prices = R (total rent collected)
    #   2. Each player's utility (value - price) is envy-free
    S = np.sum(q)
    base_amount = (rent + S) / n
    
    pricing = {}
    for player in range(n):
        room = assignment[player]
        price = base_amount - q[player]
        pricing[room] = price
    
    return assignment, pricing


def bellman_ford_longest_path(graph: np.ndarray, start: int, n: int) -> np.ndarray:
    """
    Find longest paths from start node to all other nodes using Bellman-Ford.
    
    We negate the edge weights and find shortest paths, which gives us longest paths
    in the original graph.
    
    Args:
        graph: Adjacency matrix with edge weights
        start: Starting node
        n: Number of nodes
        
    Returns:
        Array of longest path distances from start to each node
    """
    # Initialize distances (use negative infinity for longest path)
    distances = np.full(n, -np.inf)
    distances[start] = 0
    
    # Relax edges n-1 times
    for _ in range(n - 1):
        updated = False
        for i in range(n):
            if distances[i] == -np.inf:
                continue
            for j in range(n):
                if i != j:  # No self-loops
                    new_dist = distances[i] + graph[i][j]
                    if new_dist > distances[j]:
                        distances[j] = new_dist
                        updated = True
        if not updated:
            break
    
    # Set unreachable nodes to 0 (no path means no subsidy)
    distances[distances == -np.inf] = 0
    
    return distances


def print_allocation(valuations: list[list[float]], assignment: dict, pricing: dict):
    """
    Print the allocation in a human-readable format.
    
    Args:
        valuations: The original valuations matrix
        assignment: Player to room assignment
        pricing: Room to price mapping
    """
    for player in sorted(assignment.keys()):
        room = assignment[player]
        value = valuations[player][room]
        price = pricing[room]
        print(f"Player {player} gets room {room} with value {value}, and pays {price}")


class TestEnvyFreeAllocation(unittest.TestCase):
    """Unit tests for the envy-free room allocation algorithm."""
    
    def test_case1_free_rider(self):
        """Test Case 1: The Free-Rider Problem"""
        print("\n" + "="*60)
        print("Test Case 1: Free-Rider Problem")
        print("="*60)
        
        valuations = [[150, 0], [140, 10]]
        rent = 100
        
        assignment, pricing = envy_free_room_allocation(valuations, rent)
        
        print_allocation(valuations, assignment, pricing)
        
        # Verify sum of prices equals total rent
        total_price = sum(pricing.values())
        print(f"\nTotal rent: {rent}, Sum of prices: {total_price:.2f}")
        self.assertAlmostEqual(total_price, rent, places=6, 
                              msg="Sum of prices should equal total rent")
        
        # Verify envy-freeness
        self.assertTrue(self._is_envy_free(valuations, assignment, pricing),
                       "Allocation should be envy-free")
        
        # Verify Player 1 pays negative (gets subsidy)
        player1_room = assignment[1]
        player1_price = pricing[player1_room]
        print(f"Player 1 price: {player1_price:.2f} (should be negative)")
        self.assertLess(player1_price, 0, 
                       "Player 1 should pay a negative price in free-rider problem")
        
        print("✓ Test Case 1 PASSED")
    
    def test_case2_standard(self):
        """Test Case 2: Standard example from class"""
        print("\n" + "="*60)
        print("Test Case 2: Standard Example")
        print("="*60)
        
        valuations = [
            [35, 40, 25],
            [35, 60, 40],
            [25, 40, 20]
        ]
        rent = 100
        
        assignment, pricing = envy_free_room_allocation(valuations, rent)
        
        print_allocation(valuations, assignment, pricing)
        
        # Verify sum of prices equals total rent
        total_price = sum(pricing.values())
        print(f"\nTotal rent: {rent}, Sum of prices: {total_price:.2f}")
        self.assertAlmostEqual(total_price, rent, places=6,
                              msg="Sum of prices should equal total rent")
        
        # Verify envy-freeness
        self.assertTrue(self._is_envy_free(valuations, assignment, pricing),
                       "Allocation should be envy-free")
        
        print("✓ Test Case 2 PASSED")
    
    def _is_envy_free(self, valuations, assignment, pricing):
        """
        Check if the allocation is envy-free.
        
        For every player i and every other player j:
        utility_i(own_room) >= utility_i(other_room)
        where utility = value - price
        """
        n = len(valuations)
        for i in range(n):
            room_i = assignment[i]
            price_i = pricing[room_i]
            utility_i = valuations[i][room_i] - price_i
            
            for j in range(n):
                if i != j:
                    room_j = assignment[j]
                    price_j = pricing[room_j]
                    utility_i_if_took_j = valuations[i][room_j] - price_j
                    
                    if utility_i < utility_i_if_took_j - 1e-6:  # Allow small numerical error
                        print(f"\nEnvy detected!")
                        print(f"Player {i} envies player {j}")
                        print(f"  Current utility: {utility_i:.4f} (room {room_i}, value {valuations[i][room_i]}, price {price_i:.4f})")
                        print(f"  If took room {room_j}: {utility_i_if_took_j:.4f} (value {valuations[i][room_j]}, price {price_j:.4f})")
                        return False
        
        print("\n✓ Allocation is envy-free for all players")
        return True


if __name__ == '__main__':
    print("="*60)
    print("ENVY-FREE ROOM ALLOCATION")
    print("Algorithm: Maximum Weight Matching + Longest Path in Envy Graph")
    print("="*60)
    
    # Run the unit tests
    unittest.main(verbosity=2)
