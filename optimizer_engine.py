import sqlite3
import pandas as pd

def get_global_trust_weights():
    try:
        conn = sqlite3.connect('antigravity_aar.db')
        cursor = conn.cursor()
    
        # Extract all agent trust coefficients globally (bypassing Regime JOINs mapping native parameters)
        cursor.execute("SELECT agent_name, trust_coefficient FROM agent_attribution")
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        rows = []
        
    # Base Weights (Total = 1.0) mathematically distributed securely
    weights = {
        "WhaleWatcher": 0.25,
        "Fundamental": 0.20,
        "Technical": 0.15,
        "Geopolitical": 0.15,
        "Critic": 0.25 
    }

    swarm_performance_avg = 1.0 # Default perfection prior to loss detection
    swarm_agents = [r for r in rows if r[0] != 'Critic']
    
    if swarm_agents:
        swarm_performance_avg = sum(r[1] for r in swarm_agents) / len(swarm_agents)

    # RECURSIVE TUNING LOGIC: Organism memory calculation
    # If Swarm Trust < 50%, boost Critic weight by 20% for every 10% drop mathematically decoupling bad targets
    if swarm_performance_avg < 0.50:
        boost_factor = 1 + (0.50 - swarm_performance_avg) * 2
        weights["Critic"] = min(0.60, weights["Critic"] * boost_factor)
        
        # Normalize other weights to ensure sum strictly = 1.0 avoiding formula crashes in the CIO prompt
        remaining_weight = 1.0 - weights["Critic"]
        other_sum = sum(weights[k] for k in weights if k != "Critic")
        for k in weights:
            if k != "Critic":
                weights[k] = (weights[k] / other_sum) * remaining_weight

    return weights, swarm_performance_avg
