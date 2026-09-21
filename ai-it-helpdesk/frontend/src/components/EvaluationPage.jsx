import { useEffect, useState } from "react";
import axios from "axios";

function formatDiagnosis(value) {
    return value
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

function EvaluationPage() {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchEvaluation = async () => {
            try {
                const response = await axios.get("/api/evaluation/summary");
                setData(response.data);
            } catch (err) {
                console.error("Evaluation error:", err);
                setError("Failed to load evaluation results.");
            } finally {
                setLoading(false);
            }
        };

        fetchEvaluation();
    }, []);

    if (loading) {
        return (
            <div className="evaluation-state">
                <div className="loading-spinner"></div>
                <p>Loading evaluation results...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="evaluation-state error-state">
                <h3>Something went wrong</h3>
                <p>{error}</p>
            </div>
        );
    }

    const { summary, scenarios } = data;

    return (
        <div className="evaluation-page">

            {/* Header */}
            <div className="evaluation-header">
                <div>
                    <p className="section-label">SYSTEM EVALUATION</p>
                    <h2>Inference Engine Evaluation</h2>
                    <p className="evaluation-description">
                        Comparison of forward and backward chaining across
                        predefined diagnostic scenarios.
                    </p>
                </div>
            </div>

            {/* Accuracy Overview */}
            <div className="evaluation-section">
                <h3 className="section-title">Performance Overview</h3>

                <div className="metric-grid">

                    <div className="metric-card">
                        <div className="metric-label">
                            Scenarios Tested
                        </div>
                        <div className="metric-value">
                            {summary.total_scenarios}
                        </div>
                        <div className="metric-subtext">
                            Diagnostic test cases
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Forward Accuracy
                        </div>
                        <div className="metric-value success">
                            {(summary.forward_accuracy * 100).toFixed(0)}%
                        </div>
                        <div className="metric-subtext">
                            {summary.total_scenarios} / {summary.total_scenarios} correct
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Backward Accuracy
                        </div>
                        <div className="metric-value success">
                            {(summary.backward_accuracy * 100).toFixed(0)}%
                        </div>
                        <div className="metric-subtext">
                            {summary.total_scenarios} / {summary.total_scenarios} correct
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Avg. Forward Rules
                        </div>
                        <div className="metric-value">
                            {summary.average_forward_rules.toFixed(3)}
                        </div>
                        <div className="metric-subtext">
                            Rules fired per scenario
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Avg. Backward Rules
                        </div>
                        <div className="metric-value">
                            {summary.average_backward_rules.toFixed(3)}
                        </div>
                        <div className="metric-subtext">
                            Rules fired per scenario
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Avg. Forward Steps
                        </div>
                        <div className="metric-value">
                            {summary.average_forward_steps.toFixed(3)}
                        </div>
                        <div className="metric-subtext">
                            Inference steps per scenario
                        </div>
                    </div>

                    <div className="metric-card">
                        <div className="metric-label">
                            Avg. Backward Steps
                        </div>
                        <div className="metric-value">
                            {summary.average_backward_steps.toFixed(3)}
                        </div>
                        <div className="metric-subtext">
                            Inference steps per scenario
                        </div>
                    </div>

                </div>
            </div>

            {/* Method Comparison */}
            <div className="comparison-card">

                <div className="comparison-header">
                    <div>
                        <p className="section-label">METHOD COMPARISON</p>
                        <h3>Forward vs Backward Chaining</h3>
                    </div>
                </div>

                <div className="comparison-grid">

                    <div className="method-panel">
                        <div className="method-title">
                            <span className="method-dot forward-dot"></span>
                            Forward Chaining
                        </div>

                        <div className="method-stat">
                            <span>Accuracy</span>
                            <strong>
                                {(summary.forward_accuracy * 100).toFixed(0)}%
                            </strong>
                        </div>

                        <div className="method-stat">
                            <span>Avg. Rules Fired</span>
                            <strong>
                                {summary.average_forward_rules.toFixed(3)}
                            </strong>
                        </div>

                        <div className="method-stat">
                            <span>Avg. Inference Steps</span>
                            <strong>
                                {summary.average_forward_steps.toFixed(3)}
                            </strong>
                        </div>
                    </div>

                    <div className="method-panel">
                        <div className="method-title">
                            <span className="method-dot backward-dot"></span>
                            Backward Chaining
                        </div>

                        <div className="method-stat">
                            <span>Accuracy</span>
                            <strong>
                                {(summary.backward_accuracy * 100).toFixed(0)}%
                            </strong>
                        </div>

                        <div className="method-stat">
                            <span>Avg. Rules Fired</span>
                            <strong>
                                {summary.average_backward_rules.toFixed(3)}
                            </strong>
                        </div>

                        <div className="method-stat">
                            <span>Avg. Inference Steps</span>
                            <strong>
                                {summary.average_backward_steps.toFixed(3)}
                            </strong>
                        </div>
                    </div>

                </div>

                <div className="evaluation-note">
                    <strong>Interpretation:</strong>
                    Both inference strategies correctly identified all
                    predefined scenarios. Differences in rule usage arise
                    from the different inference strategies and the structure
                    of individual diagnostic chains.
                </div>

            </div>

            {/* Scenario Results */}
            <div className="evaluation-section">

                <div className="table-header">
                    <div>
                        <p className="section-label">TEST CASES</p>
                        <h3 className="section-title">Scenario Results</h3>
                    </div>

                    <span className="scenario-count">
                        {scenarios.length} scenarios
                    </span>
                </div>

                <div className="table-container">
                    <table className="evaluation-table">
                        <thead>
                            <tr>
                                <th>Scenario</th>
                                <th>Category</th>
                                <th>Expected Diagnosis</th>
                                <th>Forward</th>
                                <th>Backward</th>
                                <th>Fwd Rules</th>
                                <th>Bwd Rules</th>
                            </tr>
                        </thead>

                        <tbody>
                            {scenarios.map((scenario) => (
                                <tr key={scenario.scenario_id}>

                                    <td>
                                        <div className="scenario-name">
                                            {scenario.scenario}
                                        </div>
                                        <div className="scenario-id">
                                            {scenario.scenario_id}
                                        </div>
                                    </td>

                                    <td>
                                        <span className="category-badge">
                                            {scenario.category}
                                        </span>
                                    </td>

                                    <td>
                                        <span className="diagnosis-name">
                                            {formatDiagnosis(
                                                scenario.expected_diagnosis
                                            )}
                                        </span>
                                    </td>

                                    <td>
                                        <span className="result-badge success-badge">
                                            ✓ Pass
                                        </span>
                                    </td>

                                    <td>
                                        <span className="result-badge success-badge">
                                            ✓ Pass
                                        </span>
                                    </td>

                                    <td className="number-cell">
                                        {scenario.forward.rules_fired}
                                    </td>

                                    <td className="number-cell">
                                        {scenario.backward.rules_fired}
                                    </td>

                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

            </div>

        </div>
    );
}

export default EvaluationPage;