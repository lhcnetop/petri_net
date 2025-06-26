#!/usr/bin/env python3
"""
Simple example demonstrating the core Petri net functionality.
This replaces the mRNA-specific main.py that will be moved to the mrna_petrinet repository.
"""

import json
from petrinet.pnet import PNet

def main():
    print("Petri Net Core - Basic Example")
    print("=" * 40)
    
    # Create a simple Petri net example
    example_pnet = {
        "places": {
            "p_start": 1,
            "p_middle": 0,
            "p_end": 0
        },
        "transitions": {
            "t_1": {
                "consume": {"p_start": 1},
                "produce": {"p_middle": 1}
            },
            "t_2": {
                "consume": {"p_middle": 1},
                "produce": {"p_end": 1}
            }
        }
    }
    
    # Create Petri net instance
    pnet = PNet(example_pnet)
    
    print("Initial marking:")
    print(json.dumps(pnet.get_tokens(), indent=2))
    
    print("\nAvailable transitions:")
    valid_transitions = []
    for transition in pnet.transitions_dict:
        if pnet.check_fireability(transition)[0]:
            valid_transitions.append(transition)
    for transition in valid_transitions:
        print(f"  - {transition}")
    
    print("\nRunning simulation with 2 steps...")
    pnet.simulate_petrinet(2, law='random')
    print("Final marking:")
    print(json.dumps(pnet.get_tokens(), indent=2))
    
    print("\nFiring sequence:")
    print(pnet.get_firing_sequence())
    
    print("\nExample completed successfully!")

if __name__ == "__main__":
    main()
