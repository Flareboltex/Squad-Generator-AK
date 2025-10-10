import tkinter as tk
import random
from collections import defaultdict

class Operator:
    def __init__(self, name, meta_score, subjective_score, role):
        self.name = name
        self.meta_score = meta_score
        self.subjective_score = subjective_score
        self.role = role
        self.weighted_score = 0
        self.probability = 0

    def calculate_weighted_score(self):
        return (self.meta_score*0.35 + self.subjective_score*0.65)

    
operators = []

def load_operators_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            name, meta_score, subjective_score, role = line.strip().split(',')
            operators.append(Operator(name, int(meta_score), int(subjective_score), role))
    return operators

def calculate_probabilities(operators):
    total_weighted_score = sum(c.calculate_weighted_score() for c in operators)
    
    
    for operator in operators:
        operator.probability = (operator.calculate_weighted_score() / total_weighted_score
        if total_weighted_score > 0 else 0)
        
def group_operators_by_role(operators):
    operators_by_role = defaultdict(list)
    for operator in operators:
        operators_by_role[operator.role].append(operator)
    return operators_by_role

def select_one_per_role(operators_by_role, selected_squad, max_size):
    import random
    for role, role_operators in operators_by_role.items():
        if len(selected_squad) >= max_size:
            break
        if role_operators:
            selected_operator = random.choices(
                role_operators, [op.probability for op in role_operators], k=1
            )[0]
            selected_squad.append(selected_operator)
            role_operators.remove(selected_operator)

def fill_remaining_slots(operators_by_role, selected_squad, remaining_slots):
    import random
    remaining_operators = [
        op for ops in operators_by_role.values() for op in ops
    ]
    if remaining_operators and remaining_slots > 0:
        selected_squad.extend(
            random.choices(
                remaining_operators,
                [op.probability for op in remaining_operators],
                k=remaining_slots
            )
        )

def select_operators(operators, num_to_select):
    calculate_probabilities(operators)
    selected_squad = []

    operators_by_role = group_operators_by_role(operators)
    select_one_per_role(operators_by_role, selected_squad, num_to_select)

    remaining_slots = num_to_select - len(selected_squad)
    fill_remaining_slots(operators_by_role, selected_squad, remaining_slots)

    return selected_squad

def display_squad(selected_operators):
    print("Selected Squad:")
    for character in selected_operators:
        print(f"- {character.name} (Meta Score: {character.meta_score},Subjective Score: {character.subjective_score})")

def main(file_path, num_to_select):
    operators = load_operators_from_file(file_path)
    selected_operators = select_operators(operators, num_to_select)
    display_squad(selected_operators)
