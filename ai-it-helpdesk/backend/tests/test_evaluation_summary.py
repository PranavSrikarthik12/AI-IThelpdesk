from app.evaluation.summary import generate_summary


def test_evaluation_summary():
    summary = generate_summary()

    assert summary["total_scenarios"] == 11

    assert summary["forward_accuracy"] == 1.0
    assert summary["backward_accuracy"] == 1.0

    assert summary["average_forward_rules"] > 0
    assert summary["average_backward_rules"] > 0

    assert summary["average_forward_steps"] > 0
    assert summary["average_backward_steps"] > 0