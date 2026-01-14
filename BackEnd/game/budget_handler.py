class BudgetHandler:
    def __init__(self, total_budget: int, max_round_budget: int):
        self.total_budget = total_budget
        self.max_round_budget = max_round_budget
        self.sliders = [0, 0, 0]

    def reset_round(self):
        self.sliders = [0, 0, 0]

    def apply_slider_change(self, index: int, value: int):
    # zet gewenste slider
        self.sliders[index] = value
        return self.sliders


    def reconcile(self, desired_sliders: list[int]):
        self.sliders = desired_sliders.copy()
        return self.sliders

    def spend_round_budget(self):
        spent = sum(self.sliders)
        spent = min(spent, self.total_budget)
        self.total_budget -= spent
        return spent

    def is_budget_empty(self):
        return self.total_budget <= 0
