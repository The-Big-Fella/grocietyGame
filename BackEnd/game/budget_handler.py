class BudgetHandler:
    def __init__(self, total_budget: int):
        self.total_budget = total_budget
        self.sliders = [0, 0, 0]

    def reset(self):
        self.sliders = [0, 0, 0]

    def apply_slider_change(self, index: int, value: int):
        """
        Player wants slider[index] to be `value`.
        Other two sliders are adjusted equally.
        """
        value = max(0, min(value, self.total_budget))
        self.sliders[index] = value

        remaining = self.total_budget - value
        other_indices = [i for i in range(3) if i != index]

        # split remaining equally
        split = remaining // 2
        remainder = remaining - (split * 2)

        self.sliders[other_indices[0]] = split
        self.sliders[other_indices[1]] = split + remainder

        return self.sliders

    def reconcile(self, desired_sliders: list[int]):
        """
        Given raw controller sliders, figure out which one moved most
        and treat that as the intent.
        """
        diffs = [
            abs(desired_sliders[i] - self.sliders[i])
            for i in range(3)
        ]

        moved_index = diffs.index(max(diffs))
        return self.apply_slider_change(moved_index, desired_sliders[moved_index])

    def get_sliders(self):
        return list(self.sliders)
