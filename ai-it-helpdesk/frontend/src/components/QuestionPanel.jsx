function QuestionPanel({
    question,
    selectionReason,
    questionNumber,
    onAnswer,
    disabled = false,
}) {
    if (!question) {
        return null;
    }

    return (
        <div className="question-panel">

            {/* Progress */}
            <div className="question-progress">

                <span>
                    Diagnostic Question
                </span>

                <span>
                    Question {questionNumber || 1}
                </span>

            </div>

            <div className="progress-track">
                <div className="progress-fill dynamic-progress" />
            </div>


            {/* Question */}
            <div className="question-content">

                <p className="question-label">
                    CURRENT QUESTION
                </p>

                <h2>
                    {question.text}
                </h2>

                <p className="question-helper">
                    Select the option that best describes the current
                    system state.
                </p>

            </div>


            {/* Answer buttons */}
            <div className="answer-options">

                {question.options.map((option) => (
                    <button
                        key={option.fact}
                        className="answer-button"
                        disabled={disabled}
                        onClick={() => onAnswer(option)}
                    >
                        <span className="answer-label">
                            {option.label}
                        </span>

                        <span className="answer-arrow">
                            →
                        </span>
                    </button>
                ))}

            </div>


            {/* Question selection explanation */}
            {selectionReason && (
                <div className="question-reasoning">

                    <div className="reasoning-header">
                        <span className="reasoning-icon">
                            ?
                        </span>

                        <div>
                            <h3>
                                Why am I being asked this?
                            </h3>

                            <p>
                                {selectionReason.reason}
                            </p>
                        </div>
                    </div>

                    {selectionReason.rules_affected?.length > 0 && (
                        <div className="affected-rules">

                            <span className="affected-label">
                                Rules affected
                            </span>

                            <div className="rule-tags">
                                {selectionReason.rules_affected.map(
                                    (rule) => (
                                        <span
                                            key={rule}
                                            className="rule-tag"
                                        >
                                            {rule}
                                        </span>
                                    )
                                )}
                            </div>

                        </div>
                    )}

                </div>
            )}

        </div>
    );
}

export default QuestionPanel;