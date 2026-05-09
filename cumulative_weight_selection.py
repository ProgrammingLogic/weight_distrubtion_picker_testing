from typing import List
from random import random

def pick(weights: List[float]) -> float:
    if len(weights) == 0:
        raise ValueError("weights cannot be empty")

    print(f"\tweights: {[f'{weight}, ' for weight in weights]}")

    sum = 0.0
    for weight in weights:
        sum += weight
    
    print(f"\tsum: {sum}")

    remaining_distance = random() * sum
    for weight in weights:
        print(f"\tremaining_distance {remaining_distance} - weight {weight} = {remaining_distance - weight}")
        remaining_distance -= weight

        if remaining_distance < 0:
            print(f"\tchoosen weight: {weight}")
            return weight
    
    print("\twarning: weight could not be chosen, defaulting to first weight")
    return weights[0]
    
if __name__ == "__main__":
    weight_list_variations = {
        "Sum is 0 with positive / negative weights": [0.1, -0.1, 0.2, -0.2, 0.3, -0.3, 0.4, -0.4,],
        "Sum is negative with only negative weights": [-.1, -.2, -.3, -.4],
        "Sum is negative with both postive and negative weights": [1, -10, 2, -9],
        "Sum is positive with only positive weights": [.1, .2, .3, .4],   
        "Sum is positive with both positive and negative weights": [.1, -.1, .2, -.2, .3,]
    }
    
    for key, value in weight_list_variations.items():
        print(f"testing {key}")
        pick(value)
