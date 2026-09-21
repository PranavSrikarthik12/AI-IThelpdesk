from app.evaluation.evaluator import InferenceEvaluator


class EvaluationSummary:
    def __init__(self, results):
        self.results = results

    def calculate(self):
        total = len(self.results)

        forward_correct = sum(
            1 for result in self.results
            if result["forward"]["correct"]
        )

        backward_correct = sum(
            1 for result in self.results
            if result["backward"]["correct"]
        )

        forward_rules = [
            result["forward"]["rules_fired"]
            for result in self.results
        ]

        backward_rules = [
            result["backward"]["rules_fired"]
            for result in self.results
        ]

        forward_steps = [
            result["forward"]["steps"]
            for result in self.results
        ]

        backward_steps = [
            result["backward"]["steps"]
            for result in self.results
        ]

        return {
            "total_scenarios": total,

            "forward_accuracy": (
                forward_correct / total
                if total else 0.0
            ),

            "backward_accuracy": (
                backward_correct / total
                if total else 0.0
            ),

            "average_forward_rules": (
                sum(forward_rules) / total
                if total else 0.0
            ),

            "average_backward_rules": (
                sum(backward_rules) / total
                if total else 0.0
            ),

            "average_forward_steps": (
                sum(forward_steps) / total
                if total else 0.0
            ),

            "average_backward_steps": (
                sum(backward_steps) / total
                if total else 0.0
            ),
        }


def generate_summary():
    evaluator = InferenceEvaluator()
    results = evaluator.evaluate_all()

    summary = EvaluationSummary(results)

    return summary.calculate()