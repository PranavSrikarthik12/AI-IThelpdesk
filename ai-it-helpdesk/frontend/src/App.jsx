import { useState } from "react";

import CategorySelector from "./components/CategorySelector";
import QuestionPanel from "./components/QuestionPanel";
import DiagnosisCard from "./components/DiagnosisCard";
import EvaluationPage from "./components/EvaluationPage";

import {
    startDiagnosis,
    submitAnswer,
} from "./services/api";


function App() {

    const [view, setView] = useState("diagnosis");

    const [sessionId, setSessionId] = useState(null);

    const [category, setCategory] = useState(null);

    const [question, setQuestion] = useState(null);

    const [selectionReason, setSelectionReason] = useState(null);

    const [diagnosis, setDiagnosis] = useState(null);

    const [inference, setInference] = useState(null);

    const [forwardInference, setForwardInference] = useState(null);

    const [backwardInference, setBackwardInference] = useState([]);

    const [questionNumber, setQuestionNumber] =
        useState(1);

    const [loading, setLoading] =
        useState(false);

    const [error, setError] =
        useState(null);


    const handleCategorySelect = async (
        selectedCategory
    ) => {

        try {

            setLoading(true);
            setError(null);

            const data = await startDiagnosis(
                selectedCategory
            );

            setSessionId(data.session_id);

            setCategory(data.category);

            setQuestion(data.question);

            setSelectionReason(data.selection_reason || null);

            setQuestionNumber(1);

        } catch (err) {

            console.error(err);

            setError(
                "Unable to start the diagnostic session."
            );

        } finally {

            setLoading(false);

        }
    };


    const handleAnswer = async (option) => {

        // QuestionPanel passes the selected option object; extract the
        // underlying fact so this also works if a bare fact is passed.
        const fact = option?.fact ?? option;

        try {

            setLoading(true);
            setError(null);

            const response = await submitAnswer(
                sessionId,
                question.id,
                fact
            );

            setInference(response.inference || null);

            setForwardInference(response.forward_inference || null);

            setBackwardInference(response.backward_inference || []);

            if (response.status === "diagnosed") {

                setDiagnosis(response.diagnoses?.[0] || null);
                setQuestion(null);
                setSelectionReason(null);

            } else if (response.status === "question_required") {

                setQuestion(response.question);
                setSelectionReason(response.selection_reason || null);
                setQuestionNumber((previous) => previous + 1);

            } else if (response.status === "insufficient_information") {

                setQuestion(null);
                setSelectionReason(null);
                setDiagnosis(null);

            }

        } catch (err) {

            console.error(err);

            setError(
                err.response?.data?.detail ||
                "Something went wrong while processing your answer."
            );

        } finally {

            setLoading(false);

        }
    };


    const resetDiagnosis = () => {

        setSessionId(null);
        setCategory(null);
        setQuestion(null);
        setSelectionReason(null);
        setDiagnosis(null);
        setInference(null);
        setForwardInference(null);
        setBackwardInference([]);
        setQuestionNumber(1);
        setError(null);

    };


    return (

        <div className="app">

            <header className="app-header">

                <h1>
                    AI IT Helpdesk
                </h1>

                <p>
                    Knowledge-Based Diagnostic Expert System
                </p>

            </header>


            <nav className="navigation">

                <button
                    className={`nav-button ${
                        view === "diagnosis" ? "active" : ""
                    }`}
                    onClick={() => setView("diagnosis")}
                >
                    Diagnosis
                </button>

                <button
                    className={`nav-button ${
                        view === "evaluation" ? "active" : ""
                    }`}
                    onClick={() => setView("evaluation")}
                >
                    Evaluation
                </button>

            </nav>


            <main className="app-main">

                {view === "diagnosis" && (

                    <>

                        {error && (

                            <div className="error-card">
                                <h3>Something went wrong</h3>
                                <p>{error}</p>
                            </div>

                        )}


                        {!category && (

                            <CategorySelector
                                onSelect={
                                    handleCategorySelect
                                }
                            />

                        )}


                        {category && loading && (

                            <div className="status-card">
                                <p>Analyzing your answers...</p>
                            </div>

                        )}


                        {category && !loading && question && !diagnosis && (

                            <QuestionPanel
                                question={question}
                                onAnswer={handleAnswer}
                                questionNumber={questionNumber}
                                selectionReason={selectionReason}
                            />

                        )}


                        {!loading && diagnosis && (

                            <>

                                <DiagnosisCard
                                    diagnosis={diagnosis}
                                    inference={inference}
                                    forwardInference={forwardInference}
                                    backwardInference={backwardInference}
                                />

                                <button
                                    className="restart-button"
                                    onClick={resetDiagnosis}
                                >
                                    Start New Diagnosis
                                </button>

                            </>

                        )}


                        {category && !loading && !question && !diagnosis && (

                            <div className="status-card">

                                <h2>Unable to determine the problem</h2>

                                <p>
                                    The available answers did not provide enough
                                    information to identify a known IT problem.
                                </p>

                                {inference && inference.trace?.length > 0 && (

                                    <div className="reasoning-section">

                                        <h3>Reasoning</h3>

                                        {inference.trace.map((step, index) => (

                                            <div
                                                className="reasoning-step"
                                                key={index}
                                            >
                                                <strong>{step.rule_id}</strong>
                                                <p>{step.explanation}</p>
                                            </div>

                                        ))}

                                    </div>

                                )}

                                <button
                                    className="restart-button"
                                    onClick={resetDiagnosis}
                                >
                                    Start New Diagnosis
                                </button>

                            </div>

                        )}

                    </>

                )}


                {view === "evaluation" && (

                    <EvaluationPage />

                )}

            </main>

        </div>

    );
}


export default App;