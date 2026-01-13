class BudgetHandler:
    def __init__(self, total_budget: int, max_round_budget: int):
        self.total_budget = total_budget
        self.max_round_budget = max_round_budget
        self.sliders = [0, 0, 0]

    def reset_round(self):
        self.sliders = [0, 0, 0]

    def apply_slider_change(self, index: int, value: int):
        # slider-waarde begrenzen door max inzet per ronde
        value = max(0, min(value, self.max_round_budget))
        self.sliders[index] = value

        used = sum(self.sliders)
        if used > self.max_round_budget:
            excess = used - self.max_round_budget
            self.sliders[index] -= excess

        return self.sliders

    def reconcile(self, desired_sliders: list[int]):
        diffs = [
            abs(desired_sliders[i] - self.sliders[i])
            for i in range(3)
        ]
        moved_index = diffs.index(max(diffs))
        return self.apply_slider_change(moved_index, desired_sliders[moved_index])

    def spend_round_budget(self):
        spent = sum(self.sliders)
        spent = min(spent, self.total_budget)
        self.total_budget -= spent
        return spent

    def is_budget_empty(self):
        return self.total_budget <= 0
