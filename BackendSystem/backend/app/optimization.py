from typing import List, Dict, Any
import numpy as np
from datetime import datetime, timedelta

def calculate_distance(point1: Dict[str, float], point2: Dict[str, float]) -> float:
    """Calculate Euclidean distance between two points"""
    return np.sqrt((point1['x'] - point2['x'])**2 + (point1['y'] - point2['y'])**2)

def calculate_total_distance(waypoints: List[Dict[str, float]]) -> float:
    """Calculate total distance of a path"""
    total = 0
    for i in range(len(waypoints) - 1):
        total += calculate_distance(waypoints[i], waypoints[i + 1])
    return total

def optimize_for_battery(waypoints: List[Dict[str, float]], battery_level: int) -> List[Dict[str, float]]:
    """Optimize path based on battery level"""
    if battery_level < 20:
        # For low battery, reduce path length by selecting key points
        return waypoints[::2]  # Take every other point
    elif battery_level < 50:
        # For medium battery, moderate optimization
        return waypoints[::1]  # Keep original path but optimize order
    return waypoints  # For high battery, keep original path

def optimize_for_coverage(waypoints: List[Dict[str, float]], area_bounds: Dict[str, float]) -> List[Dict[str, float]]:
    """Optimize path for maximum area coverage"""
    # Calculate area coverage using grid-based approach
    grid_size = 10  # 10x10 grid
    coverage_matrix = np.zeros((grid_size, grid_size))
    
    # Mark covered areas
    for point in waypoints:
        x_idx = int((point['x'] - area_bounds['min_x']) / (area_bounds['max_x'] - area_bounds['min_x']) * (grid_size - 1))
        y_idx = int((point['y'] - area_bounds['min_y']) / (area_bounds['max_y'] - area_bounds['min_y']) * (grid_size - 1))
        coverage_matrix[x_idx, y_idx] = 1
    
    # Add points for uncovered areas
    new_waypoints = waypoints.copy()
    for i in range(grid_size):
        for j in range(grid_size):
            if coverage_matrix[i, j] == 0:
                x = area_bounds['min_x'] + (area_bounds['max_x'] - area_bounds['min_x']) * i / (grid_size - 1)
                y = area_bounds['min_y'] + (area_bounds['max_y'] - area_bounds['min_y']) * j / (grid_size - 1)
                new_waypoints.append({'x': x, 'y': y})
    
    return new_waypoints

def optimize_for_time(waypoints: List[Dict[str, float]], speed_limit: float) -> List[Dict[str, float]]:
    """Optimize path for time efficiency"""
    # Use nearest neighbor algorithm for basic TSP solution
    optimized = [waypoints[0]]  # Start with first point
    remaining = waypoints[1:]
    
    while remaining:
        current = optimized[-1]
        nearest = min(remaining, key=lambda x: calculate_distance(current, x))
        optimized.append(nearest)
        remaining.remove(nearest)
    
    return optimized

def avoid_obstacles(waypoints: List[Dict[str, float]], obstacles: List[Dict[str, float]]) -> List[Dict[str, float]]:
    """Modify path to avoid known obstacles"""
    safe_waypoints = []
    min_distance = 2.0  # Minimum safe distance from obstacles
    
    for point in waypoints:
        is_safe = True
        for obstacle in obstacles:
            if calculate_distance(point, obstacle) < min_distance:
                is_safe = False
                # Add alternative point
                alt_x = point['x'] + min_distance
                alt_y = point['y'] + min_distance
                safe_waypoints.append({'x': alt_x, 'y': alt_y})
                break
        if is_safe:
            safe_waypoints.append(point)
    
    return safe_waypoints

def consider_historical_data(waypoints: List[Dict[str, float]], historical_data: List[Dict[str, Any]]) -> List[Dict[str, float]]:
    """Optimize path based on historical performance data"""
    # Weight points based on historical success
    weighted_points = []
    for point in waypoints:
        weight = 1.0
        for hist in historical_data:
            if calculate_distance(point, hist['location']) < 1.0:
                if hist['success_rate'] > 0.8:
                    weight += 0.2
                elif hist['success_rate'] < 0.4:
                    weight -= 0.2
        point['weight'] = max(0.1, min(2.0, weight))  # Keep weight between 0.1 and 2.0
        weighted_points.append(point)
    
    # Sort points by weight and reconstruct path
    return sorted(weighted_points, key=lambda x: x['weight'], reverse=True)

def optimize_patrol_path(
    waypoints: List[Dict[str, float]],
    battery_level: int,
    area_bounds: Dict[str, float],
    speed_limit: float,
    obstacles: List[Dict[str, float]],
    historical_data: List[Dict[str, Any]]
) -> List[Dict[str, float]]:
    """Main optimization function combining all strategies"""
    
    # Step 1: Battery optimization
    optimized = optimize_for_battery(waypoints, battery_level)
    
    # Step 2: Coverage optimization
    optimized = optimize_for_coverage(optimized, area_bounds)
    
    # Step 3: Time efficiency
    optimized = optimize_for_time(optimized, speed_limit)
    
    # Step 4: Obstacle avoidance
    optimized = avoid_obstacles(optimized, obstacles)
    
    # Step 5: Historical data consideration
    optimized = consider_historical_data(optimized, historical_data)
    
    return optimized
