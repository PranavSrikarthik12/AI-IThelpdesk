function formatFact(fact) {
    return fact
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
}

function DiagnosisCard({
    diagnosis,
    inference,
    forwardInference,
    backwardInference = [],
}) {
    if (!diagnosis) {
        return null;
    }

    const forward = forwardInference || inference;

    const initialFacts = forward?.initial_facts || [];

    return (
        <div className="diagnosis-result">

            {/* ================================
                Diagnosis Header
               ================================ */}

            <div className="diagnosis-header">

                <div className="diagnosis-status">
                    DIAGNOSIS IDENTIFIED
                </div>

                <div className="diagnosis-title-row">
                    <div>
                        <h2>{diagnosis.title}</h2>

                        <p>
                            {diagnosis.description}
                        </p>
                    </div>

                    <span
                        className={`severity-badge ${diagnosis.severity.toLowerCase()}`}
                    >
                        {diagnosis.severity} Severity
                    </span>
                </div>

            </div>


            {/* ================================
                Observed Evidence
               ================================ */}

            {initialFacts.length > 0 && (
                <div className="evidence-section">

                    <div className="section-heading">
                        Observed Evidence
                    </div>

                    <p className="section-description">
                        Facts collected from the user's answers and supplied
                        to the inference engine.
                    </p>

                    <div className="evidence-list">

                        {initialFacts.map((fact) => (
                            <div
                                className="evidence-item"
                                key={fact}
                            >
                                <span className="evidence-check">
                                    ✓
                                </span>

                                <span>
                                    {formatFact(fact)}
                                </span>
                            </div>
                        ))}

                    </div>

                </div>
            )}


            {/* ================================
                Recommended Actions
               ================================ */}

            {diagnosis.recommended_actions?.length > 0 && (
                <div className="actions-section">

                    <div className="section-heading">
                        Recommended Actions
                    </div>

                    <div className="action-list">

                        {diagnosis.recommended_actions.map(
                            (action) => (
                                <div
                                    className="action-item"
                                    key={action.step}
                                >
                                    <span className="action-number">
                                        {action.step}
                                    </span>

                                    <span>
                                        {action.description}
                                    </span>
                                </div>
                            )
                        )}

                    </div>

                </div>
            )}


            {/* ================================
                Reasoning Explanation
               ================================ */}

            <div className="reasoning-section">

                <div className="section-heading">
                    How the System Reached This Diagnosis
                </div>

                <p className="section-description">
                    The expert system applies production rules to the
                    collected facts. Each successful rule derives a new
                    fact that can be used by subsequent rules.
                </p>


                {/* Forward Chaining */}

                <div className="inference-method">

                    <div className="method-heading">
                        <span className="method-indicator forward-indicator"></span>

                        <div>
                            <strong>Forward Chaining</strong>

                            <span className="method-description">
                                Fact-driven inference
                            </span>
                        </div>
                    </div>

                    {forward?.trace?.length > 0 ? (

                        <div className="reasoning-flow">

                            {forward.trace.map(
                                (step, index) => (
                                    <div
                                        className="reasoning-node"
                                        key={`${step.rule_id}-${index}`}
                                    >

                                        <div className="rule-box">

                                            <span className="rule-label">
                                                RULE
                                            </span>

                                            <strong>
                                                {step.rule_id}
                                            </strong>

                                        </div>

                                        <div className="rule-condition-box">

                                            <span className="flow-label">
                                                CONDITIONS
                                            </span>

                                            <div className="condition-list">

                                                {step.conditions.map(
                                                    (condition) => (
                                                        <span
                                                            className="condition-chip"
                                                            key={condition}
                                                        >
                                                            {formatFact(
                                                                condition
                                                            )}
                                                        </span>
                                                    )
                                                )}

                                            </div>

                                        </div>

                                        <div className="flow-arrow">
                                            ↓
                                        </div>

                                        <div className="conclusion-box">

                                            <span className="flow-label">
                                                DERIVED FACT
                                            </span>

                                            <strong>
                                                {formatFact(
                                                    step.conclusion
                                                )}
                                            </strong>

                                        </div>

                                        <p className="rule-explanation">
                                            {step.explanation}
                                        </p>

                                    </div>
                                )
                            )}

                        </div>

                    ) : (
                        <p className="no-trace">
                            No forward inference steps available.
                        </p>
                    )}

                </div>


                {/* Backward Chaining */}

                <div className="inference-method">

                    <div className="method-heading">
                        <span className="method-indicator backward-indicator"></span>

                        <div>
                            <strong>Backward Chaining</strong>

                            <span className="method-description">
                                Goal-driven inference
                            </span>
                        </div>
                    </div>

                    {backwardInference.length > 0 ? (

                        <div className="reasoning-flow">

                            {backwardInference.map(
                                (result, resultIndex) => (
                                    result.trace?.map(
                                        (step, index) => (
                                            <div
                                                className="reasoning-node"
                                                key={`${resultIndex}-${step.rule_id}-${index}`}
                                            >

                                                <div className="rule-box">

                                                    <span className="rule-label">
                                                        RULE
                                                    </span>

                                                    <strong>
                                                        {step.rule_id}
                                                    </strong>

                                                </div>

                                                <div className="rule-condition-box">

                                                    <span className="flow-label">
                                                        REQUIRED CONDITIONS
                                                    </span>

                                                    <div className="condition-list">

                                                        {step.conditions.map(
                                                            (condition) => (
                                                                <span
                                                                    className="condition-chip"
                                                                    key={condition}
                                                                >
                                                                    {formatFact(
                                                                        condition
                                                                    )}
                                                                </span>
                                                            )
                                                        )}

                                                    </div>

                                                </div>

                                                <div className="flow-arrow">
                                                    ↓
                                                </div>

                                                <div className="conclusion-box">

                                                    <span className="flow-label">
                                                        PROVED GOAL
                                                    </span>

                                                    <strong>
                                                        {formatFact(
                                                            step.conclusion
                                                        )}
                                                    </strong>

                                                </div>

                                                <p className="rule-explanation">
                                                    {step.explanation}
                                                </p>

                                            </div>
                                        )
                                    )
                                )
                            )}

                        </div>

                    ) : (
                        <p className="no-trace">
                            No backward inference steps available.
                        </p>
                    )}

                </div>

            </div>


            {/* ================================
                Final Explanation
               ================================ */}

            <div className="diagnosis-explanation">

                <div className="explanation-icon">
                    ✓
                </div>

                <div>
                    <strong>
                        Why this diagnosis?
                    </strong>

                    <p>
                        The collected evidence satisfied the production
                        rule conditions associated with{" "}
                        <strong>{diagnosis.title}</strong>.
                        The inference trace above shows the rules that
                        produced the diagnosis.
                    </p>
                </div>

            </div>

        </div>
    );
}

export default DiagnosisCard;