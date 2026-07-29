from vectorized_pathfinding import find_path
from heuristics import _euclidean_heuristic


CLUSTER_RADIUS = 4.0
MIN_CLUSTER_SIZE = 2
MAX_CLUSTER_SIZE = 4
MAX_CLUSTER_WIDTH = 5
MAX_CLUSTER_HEIGHT = 5
DEBRIS_REWARD = 10 


### <------ Sums the true move cost along a path (straight=1, diagonal=sqrt2 + hazard penalties), ------> ###
### <------ matching the same cost model used by vectorized_pathfinding._neighbors_of ------------------> ###
### <------ Returns float("inf") if there is no path. --------------------------------------------------> ###
def calculate_path_cost(path, hazards_positions):
    if path is None:
        return float("inf")
    if len(path) < 2:
        return 0.0

    hazards_positions = hazards_positions or {}
    total = 0.0
    for i in range(len(path) - 1):
        x1, z1 = path[i]
        x2, z2 = path[i + 1]
        dx, dz = abs(x2 - x1), abs(z2 - z1)
        step_cost = 1.4142135623730951 if (dx == 1 and dz == 1) else 1.0

        if (x2, z2) in hazards_positions:
            hazard_type = hazards_positions[(x2, z2)]
            if hazard_type == "pit":
                step_cost += 1000
            elif hazard_type == "electrical":
                step_cost += 10000

        total += step_cost

    return total
### <------ Sums the true move cost along a path (straight=1, diagonal=sqrt2 + hazard penalties), ------> ###
### <------ matching the same cost model used by vectorized_pathfinding._neighbors_of ------------------> ###
### <------ Returns float("inf") if there is no path. --------------------------------------------------> ###



### <------ Returns the horizontal width and vertical height of a cluster ------> ###
def _cluster_dimensions(cluster):
    x_positions = [position[0] for position in cluster]
    z_positions = [position[1] for position in cluster]

    width = max(x_positions) - min(x_positions)
    height = max(z_positions) - min(z_positions)

    return width, height
### <------ Returns the horizontal width and vertical height of a cluster ------> ###



### <------ Checking whether a candidate debris position can join a cluster ------> ###
def _candidate_can_join_cluster(cluster, candidate):
    if len(cluster) >= MAX_CLUSTER_SIZE:
        return False

    proposed_cluster = cluster | {candidate}

    width, height = _cluster_dimensions(proposed_cluster)

    if width > MAX_CLUSTER_WIDTH:
        return False

    if height > MAX_CLUSTER_HEIGHT:
        return False

    return True
### <------ Checking whether a candidate debris position can join a cluster ------> ###



### <----------------- Creating compact debris clusters -----------------> ###
def create_debris_clusters(debris_positions):
    remaining = set(debris_positions)
    clusters = []
    unclustered = set()

    while remaining:
        seed = min(remaining, key=lambda position: (position[1], position[0]))

        remaining.remove(seed)

        candidates = []

        for candidate in remaining:
            distance_from_seed = _euclidean_heuristic(seed, candidate)

            if distance_from_seed <= CLUSTER_RADIUS:
                candidates.append(candidate)

        candidates.sort(key=lambda candidate: _euclidean_heuristic(seed, candidate))

        cluster = {seed}

        for candidate in candidates:
            if len(cluster) >= MAX_CLUSTER_SIZE:
                break

            if _candidate_can_join_cluster(cluster, candidate):
                cluster.add(candidate)

        if len(cluster) >= MIN_CLUSTER_SIZE:
            clusters.append(cluster)
            remaining.difference_update(cluster)
        else:
            unclustered.add(seed)

    clustered_positions = set()

    for cluster in clusters:
        clustered_positions.update(cluster)

    unclustered.update(set(debris_positions) - clustered_positions)

    return clusters, unclustered
### <----------------- Creating compact debris clusters -----------------> ###



### <------ Estimating a route for collecting all debris in one cluster ------> ###
def estimate_cluster_route(grid, cluster, entry, algorithm="astar", hazards_positions=None):
    hazards_positions = hazards_positions or {}

    remaining = set(cluster)
    remaining.discard(entry)

    route = [entry]
    current = entry
    total_cost = 0.0

    while remaining:
        best_target = None
        best_path = None
        best_cost = float("inf")

        for candidate in remaining:
            path = find_path(grid, current, candidate, algorithm=algorithm, hazards_positions=hazards_positions)
            path_cost = calculate_path_cost(path, hazards_positions)

            if path_cost < best_cost:
                best_cost = path_cost
                best_target = candidate
                best_path = path

        if best_target is None or best_path is None:
            return None, float("inf")

        total_cost += best_cost
        route.append(best_target)

        current = best_target
        remaining.remove(best_target)

    return route, total_cost
### <------ Estimating a route for collecting all debris in one cluster ------> ###



### <------ Evaluates a cluster using: utility = reward_benefit - path_cost ------> ###
def evaluate_cluster(grid, agent_position, cluster, algorithm="astar", hazards_positions=None):
    hazards_positions = hazards_positions or {}

    best_utility = float("-inf")
    best_route = None

    for entry in cluster:
        path_to_entry = find_path(grid, agent_position, entry, algorithm=algorithm, hazards_positions=hazards_positions)
        cost_to_entry = calculate_path_cost(path_to_entry, hazards_positions)

        if cost_to_entry == float("inf"):
            continue

        cluster_route, internal_cost = estimate_cluster_route(grid, cluster, entry, algorithm=algorithm, hazards_positions=hazards_positions)

        if cluster_route is None:
            continue

        total_path_cost = cost_to_entry + internal_cost
        reward = len(cluster) * DEBRIS_REWARD
        utility = reward - total_path_cost

        if utility > best_utility:
            best_utility = utility
            best_route = cluster_route

    return best_utility, best_route
### <------ Evaluates a cluster using: utility = reward_benefit - path_cost ------> ###



### <--------------- Choosing the cluster with the highest utility ---------------> ###
def choose_best_cluster(grid, agent_position, debris_positions, algorithm="astar", hazards_positions=None):
    hazards_positions = hazards_positions or {}

    clusters, unclustered = create_debris_clusters(debris_positions)

    best_cluster = None
    best_route = None
    best_utility = float("-inf")

    for cluster in clusters:
        utility, route = evaluate_cluster(grid, agent_position, cluster, algorithm=algorithm, hazards_positions=hazards_positions)

        print("Cluster:", cluster, "Utility:", utility, "Route:", route)

        if route is not None and utility > best_utility:
            best_utility = utility
            best_cluster = cluster
            best_route = route

    return best_cluster, best_route, best_utility, unclustered
### <--------------- Choosing the cluster with the highest utility ---------------> ###



### <--------------- Choosing the individual debris with the highest utility ---------------> ###
def choose_best_individual_debris(grid, agent_position, debris_positions, algorithm="astar", hazards_positions=None):
    hazards_positions = hazards_positions or {}

    best_debris = None
    best_utility = float("-inf")

    for debris in debris_positions:
        path = find_path(grid, agent_position, debris, algorithm=algorithm, hazards_positions=hazards_positions)
        path_cost = calculate_path_cost(path, hazards_positions)

        if path_cost == float("inf"):
            continue

        utility = DEBRIS_REWARD - path_cost

        if utility > best_utility:
            best_utility = utility
            best_debris = debris

    return best_debris, best_utility
### <--------------- Choosing the individual debris with the highest utility ---------------> ###



### <----------- Choosing between the best cluster and the best individual debris -----------> ###
def plan_next_debris_targets(grid, agent_position, debris_positions, final_goal=None, algorithm="astar", hazards_positions=None):
    hazards_positions = hazards_positions or {}

    if not debris_positions:
        return {"type": "none",
                "cluster": None,
                "targets": [],
                "utility": float("-inf"),
                "unclustered": set()}

    selected_cluster, cluster_route, cluster_utility, unclustered = choose_best_cluster(grid, agent_position, debris_positions, algorithm=algorithm, hazards_positions=hazards_positions)

    individual_target, individual_utility = choose_best_individual_debris(grid, agent_position, debris_positions, algorithm=algorithm, hazards_positions=hazards_positions)

    print("Best cluster utility:", cluster_utility)
    print("Best individual utility:", individual_utility)

    if selected_cluster is not None and cluster_route and cluster_utility >= individual_utility:
        return {
            "type": "cluster",
            "cluster": selected_cluster,
            "targets": cluster_route,
            "utility": cluster_utility,
            "unclustered": unclustered}

    if individual_target is not None:
        return {
            "type": "individual",
            "cluster": None,
            "targets": [individual_target],
            "utility": individual_utility,
            "unclustered": unclustered}

    return {"type":
            "none",
            "cluster": None,
            "targets": [],
            "utility": float("-inf"),
            "unclustered": set(debris_positions)}
### <----------- Choosing between the best cluster and the best individual debris -----------> ###



### <----------- Entry point for the "Clustering" menu button -----------> ###
def run_clustering(grid, agent_position, debris_positions, algorithm="astar", hazards_positions=None):
    plan = plan_next_debris_targets(grid, agent_position, debris_positions, algorithm=algorithm, hazards_positions=hazards_positions)
    print("Clustering plan:", plan)
    return plan
### <----------- Entry point for the "Clustering" menu button -----------> ###

#©Vardan Grigoryan