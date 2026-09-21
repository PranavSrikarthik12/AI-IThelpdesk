from app.evaluation.evaluator import InferenceEvaluator
from app.evaluation.scenarios import SCENARIOS


def test_all_scenarios_are_evaluated():
    evaluator = InferenceEvaluator()

    results = evaluator.evaluate_all()

    assert len(results) == len(SCENARIOS)


def test_forward_chaining_correctly_diagnoses_all_scenarios():
    evaluator = InferenceEvaluator()

    results = evaluator.evaluate_all()

    assert all(
        result["forward"]["correct"]
        for result in results
    )


def test_backward_chaining_correctly_diagnoses_all_scenarios():
    evaluator = InferenceEvaluator()

    results = evaluator.evaluate_all()

    assert all(
        result["backward"]["correct"]
        for result in results
    )


def test_evaluation_contains_inference_metrics():
    evaluator = InferenceEvaluator()

    results = evaluator.evaluate_all()

    for result in results:

        assert "rules_fired" in result["forward"]
        assert "steps" in result["forward"]

        assert "rules_fired" in result["backward"]
        assert "steps" in result["backward"]