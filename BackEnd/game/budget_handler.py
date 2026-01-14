class BudgetHandler:
    def __init__(self, total_budget: int, max_round_budget: int):
        self.total_budget = total_budget  # Total game budget
        self.max_round_budget = max_round_budget  # Max per round
        self.sliders = [0, 0, 0]

    def reset_round(self):
        self.sliders = [0, 0, 0]

    def apply_slider_change(self, index: int, value: int):
        # Limit slider to max_round_budget
        value = max(0, min(value, self.max_round_budget))
        self.sliders[index] = value

        used = sum(self.sliders)
        if used > self.max_round_budget:
            excess = used - self.max_round_budget
            self.sliders[index] -= excess

        return self.sliders

    def reconcile(self, desired_sliders: list[int]):
        return [min(max(0, s), self.max_round_budget) for s in desired_sliders]

    def spend_round_budget(self):
        spent = sum(self.sliders)
        spent = min(spent, self.total_budget)
        self.total_budget -= spent
        return spent

    def is_budget_empty(self):
        return self.total_budget <= 0
