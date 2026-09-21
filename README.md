# AI-Based IT Helpdesk Expert System

A knowledge-based IT helpdesk system that uses **forward chaining**, **backward chaining**, and **rule-based diagnostic reasoning** to identify common IT problems and recommend corrective actions.

The system provides an interactive React interface, a FastAPI backend, an explainable inference engine, intelligent diagnostic question selection, and an evaluation framework for comparing forward and backward chaining.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives](#2-objectives)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Knowledge Representation](#5-knowledge-representation)
6. [Diagnostic Categories](#6-diagnostic-categories)
7. [Forward Chaining](#7-forward-chaining)
8. [Backward Chaining](#8-backward-chaining)
9. [Multi-Step Inference](#9-multi-step-inference)
10. [Intelligent Question Selection](#10-intelligent-question-selection)
11. [Explainability](#11-explainability)
12. [Recommended Actions](#12-recommended-actions)
13. [Evaluation Framework](#13-evaluation-framework)
14. [Evaluation Results](#14-evaluation-results)
15. [Testing](#15-testing)
16. [Project Structure](#16-project-structure)
17. [Running the Project](#17-running-the-project)
18. [API Endpoints](#18-api-endpoints)
19. [Future Improvements](#19-future-improvements)
20. [Conclusion](#20-conclusion)

---

## 1. Project Overview

Traditional IT helpdesk systems often rely on fixed decision trees or manual troubleshooting procedures. This project implements a symbolic AI approach in which IT troubleshooting knowledge is represented using **facts and production rules**.

The system collects evidence from the user, represents that evidence as symbolic facts, and applies inference rules to derive possible diagnoses.

Two classical inference strategies are implemented:

- **Forward Chaining** — fact-driven inference
- **Backward Chaining** — goal-driven inference

The system also records the reasoning process so that the user can see **why a diagnosis was reached**.

---

## 2. Objectives

The main objectives of the project are:

1. Represent IT troubleshooting knowledge using facts and production rules.
2. Implement a forward chaining inference engine.
3. Implement a backward chaining inference engine.
4. Support multi-step inference through derived facts.
5. Dynamically select diagnostic questions based on the remaining diagnostic rules.
6. Provide explanations for question selection and diagnostic reasoning.
7. Recommend corrective actions for identified IT problems.
8. Compare forward and backward chaining using predefined diagnostic scenarios.
9. Provide an interactive web-based user interface.

---

## 3. System Architecture

```text
                         ┌──────────────────────┐
                         │      React UI        │
                         │                      │
                         │ Diagnosis /          │
                         │ Evaluation           │
                         └──────────┬───────────┘
                                    │
                              REST / JSON
                                    │
                         ┌──────────▼───────────┐
                         │       FastAPI        │
                         │      REST API        │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │ Diagnostic Controller│
                         └──────────┬───────────┘
                                    │
                 ┌──────────────────┼──────────────────┐
                 │                  │                  │
                 ▼                  ▼                  ▼
        Question Selection     Knowledge Base      Evaluation
                 │                  │               Engine
                 │           ┌──────┴──────┐           │
                 │           │ Facts       │           │
                 │           │ Rules       │           │
                 │           │ Diagnoses   │           │
                 │           └──────┬──────┘           │
                 │                  │                  │
                 │       ┌──────────┴──────────┐       │
                 │       ▼                     ▼       │
                 │  Forward Chaining     Backward      │
                 │                       Chaining      │
                 │       └──────────┬──────────┘       │
                 │                  │                  │
                 └──────────────────▼──────────────────┘
                              Diagnosis +
                          Explanation Trace +
                          Recommended Actions
```

---

## 4. Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- Pytest

### Frontend

- React
- Vite
- Axios
- CSS

### AI Technique

- Knowledge representation
- Production rules
- Forward chaining
- Backward chaining
- Rule-based inference
- Explainable reasoning

---

## 5. Knowledge Representation

The system represents observations as symbolic facts.

Examples:

```text
wifi_connected
ip_address_valid
gateway_reachable
dns_resolution_failed
cpu_usage_high
memory_usage_high
disk_space_low
login_failed
account_locked
```

Production rules are represented using the following structure:

```text
IF conditions
THEN conclusion
```

Each rule contains:

- Rule ID
- Conditions
- Conclusion
- Explanation

For example:

```text
Rule: NET-004

IF:
    wifi_connected
    AND ip_address_valid
    AND gateway_reachable
    AND dns_resolution_failed

THEN:
    dns_failure
```

The rule also contains a natural-language explanation that is displayed as part of the reasoning trace.

---

## 6. Diagnostic Categories

The current knowledge base contains three major diagnostic categories.

### Network

Examples:

- Wi-Fi connection problem
- DHCP / IP configuration problem
- Gateway connectivity problem
- DNS resolution failure
- Possible ISP or upstream network problem

### System Performance

Examples:

- High CPU load
- Memory pressure
- Insufficient disk space

### Authentication

Examples:

- Invalid credentials
- Account locked
- Password expired

---

## 7. Forward Chaining

Forward chaining is a **fact-driven inference strategy**.

The system begins with facts collected from the user and repeatedly applies rules whose conditions are satisfied.

```text
Initial Facts
      │
      ▼
Find Applicable Rules
      │
      ▼
Fire Rule
      │
      ▼
Derive New Fact
      │
      ▼
Check Rules Again
      │
      ▼
Diagnosis
```

### Example

Suppose the system knows:

```text
wifi_connected
ip_address_valid
gateway_reachable
dns_resolution_failed
```

The rule `NET-004` can fire because all of its conditions are satisfied. Therefore, the fact `dns_failure` is derived.

Forward chaining can continue deriving additional reachable facts. This is useful when the objective is to determine all relevant consequences of the currently known evidence.

---

## 8. Backward Chaining

Backward chaining is a **goal-driven inference strategy**.

Instead of starting from all available consequences, the system starts with a target diagnosis and attempts to prove it.

```text
Target Diagnosis
       │
       ▼
Find Rule Producing Goal
       │
       ▼
Check Rule Conditions
       │
       ▼
Prove Conditions
       │
       ▼
Reach Known Facts
       │
       ▼
Goal Proven
```

### Example

To prove `dns_failure`, the system identifies rule `NET-004` and checks whether the following can be established:

```text
wifi_connected
ip_address_valid
gateway_reachable
dns_resolution_failed
```

If the conditions are satisfied, the diagnosis is proven.

---

## 9. Multi-Step Inference

The system supports chained rules in which one derived fact becomes a condition for another rule.

For example:

```text
wifi_connected
+
ip_address_valid
        │
        ▼
NET-006
        │
        ▼
local_network_configured
        │
        ▼
NET-007
        │
        ▼
local_network_reachable
        │
        ▼
NET-008
        │
        ▼
network_services_operational
        │
        ▼
NET-005
        │
        ▼
isp_or_upstream_problem
```

This demonstrates that the system is performing symbolic inference rather than simply mapping individual symptoms directly to diagnoses.

---

## 10. Intelligent Question Selection

The system does not always ask diagnostic questions in a fixed sequence.

The `QuestionService` evaluates the remaining diagnostic rules and selects questions that can distinguish between possible diagnoses.

The selection mechanism considers:

- Remaining candidate diagnostic rules
- Facts already collected
- Unanswered questions
- Which rules can be affected by each question
- Coverage of candidate rules
- Balance between possible answer paths

The interface also explains:

> Why am I being asked this?

and displays the rules affected by the selected question.

This provides transparency into the diagnostic process.

---

## 11. Explainability

The system provides explanations at multiple stages.

### Question Selection

The UI explains why a particular diagnostic question was selected.

### Rule Reasoning

Each fired rule contains an explanation describing why its conclusion follows from its conditions.

### Diagnosis

The final diagnosis displays:

- Observed evidence
- Recommended actions
- Forward chaining trace
- Backward chaining trace
- Explanation of the final diagnosis

This makes the reasoning process inspectable rather than presenting only a final answer.

---

## 12. Recommended Actions

Each diagnosis is associated with a set of recommended troubleshooting actions.

For example, a diagnosed network problem may provide a sequence of corrective steps.

Actions are represented using:

```text
Step
Description
```

and are displayed in the diagnosis interface.

---

## 13. Evaluation Framework

The project contains a deterministic evaluation framework with **11 predefined diagnostic scenarios**.

The scenarios cover:

### Network

1. Wi-Fi disconnected
2. DHCP failure
3. Gateway unreachable
4. DNS resolution failure
5. ISP or upstream failure

### System Performance

6. High CPU load
7. Memory pressure
8. Insufficient storage

### Authentication

9. Invalid credentials
10. Locked account
11. Expired password

Each scenario specifies:

- Initial facts
- Diagnostic category
- Expected diagnosis

Both inference engines are executed independently against every scenario.

---

## 14. Evaluation Results

Current evaluation results:

| Metric                  | Forward Chaining | Backward Chaining |
| ----------------------- | ---------------: | ----------------: |
| Scenarios tested        |               11 |                11 |
| Correct diagnoses       |               11 |                11 |
| Accuracy                |             100% |              100% |
| Average rules fired     |            1.545 |             1.273 |
| Average inference steps |            1.545 |             1.273 |

Both methods correctly identified all 11 predefined diagnostic scenarios.

The difference in average rule usage reflects the different inference strategies and the structure of individual diagnostic chains.

> **Note:** The evaluation measures **rule firings and inference steps on the predefined scenarios**. The benchmark is deterministic and hand-designed, so these results are not a measure of real-world accuracy, and they are not intended to establish general runtime or computational superiority of one inference strategy.

---

## 15. Testing

The backend currently contains **37 automated tests**.

The test suite covers:

- Forward chaining
- Backward chaining
- Multi-step inference
- Diagnostic services
- Diagnostic controller
- Question selection
- API endpoints
- Evaluation scenarios
- Evaluation summary

Run the tests from the `backend/` directory:

```bash
pytest -q
```

Current result:

```text
37 passed
```

---

## 16. Project Structure

```text
ai-it-helpdesk/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── diagnosis.py
│   │   │   ├── evaluation.py
│   │   │   └── health.py
│   │   │
│   │   ├── engine/
│   │   │   ├── backward_chaining.py
│   │   │   └── forward_chaining.py
│   │   │
│   │   ├── evaluation/
│   │   │   ├── evaluator.py
│   │   │   ├── scenarios.py
│   │   │   └── summary.py
│   │   │
│   │   ├── knowledge/
│   │   │   ├── diagnoses.py
│   │   │   ├── knowledge_base.py
│   │   │   ├── questions.py
│   │   │   └── rules.py
│   │   │
│   │   ├── models/
│   │   │   ├── api.py
│   │   │   ├── diagnosis.py
│   │   │   ├── inference.py
│   │   │   ├── question.py
│   │   │   ├── rule.py
│   │   │   └── session.py
│   │   │
│   │   ├── services/
│   │   │   ├── api_diagnostic_service.py
│   │   │   ├── diagnostic_controller.py
│   │   │   ├── diagnostic_service.py
│   │   │   ├── question_service.py
│   │   │   └── session_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_backward_chaining.py
│   │   ├── test_chained_inference.py
│   │   ├── test_diagnostic_controller.py
│   │   ├── test_diagnostic_service.py
│   │   ├── test_evaluation_summary.py
│   │   ├── test_evaluator.py
│   │   ├── test_forward_chaining.py
│   │   └── test_question_service.py
│   │
│   ├── pyproject.toml
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CategorySelector.jsx
│   │   │   ├── DiagnosisCard.jsx
│   │   │   ├── EvaluationPage.jsx
│   │   │   └── QuestionPanel.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js
│   │   │
│   │   ├── App.jsx
│   │   └── index.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md
```

---

## 17. Running the Project

### Backend

Navigate to the backend directory:

```bash
cd backend
```

Create/activate the Python environment and install dependencies:

```bash
pip install -r requirements.txt
```

Run the FastAPI server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API is available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

The React application runs through the Vite development server.

---

## 18. API Endpoints

### Start Diagnosis

```text
POST /api/diagnosis/start
```

Starts a diagnostic session for a selected category.

Example request:

```json
{
    "category": "Network"
}
```

### Submit Answer

```text
POST /api/diagnosis/{session_id}/answer
```

Submits the selected fact for the current diagnostic question.

### Evaluation

```text
GET /api/evaluation/summary
```

Returns:

- Overall evaluation metrics
- Individual scenario results
- Forward inference results
- Backward inference results

---

## 19. Future Improvements

Possible future extensions include:

- Expanding the knowledge base with additional IT problems
- Adding more complex diagnostic dependencies
- Persistent session storage
- User authentication and helpdesk ticket integration
- Logging and analytics
- More extensive evaluation datasets
- Runtime benchmarking
- Confidence or uncertainty handling for ambiguous symptoms
- Integration with real system/network monitoring data

---

## 20. Conclusion

The project demonstrates a complete symbolic AI expert-system workflow for IT troubleshooting.

It combines:

- Knowledge representation
- Production rules
- Forward chaining
- Backward chaining
- Multi-step inference
- Intelligent question selection
- Explainable reasoning
- Recommended troubleshooting actions
- Automated evaluation
- A web-based user interface

The current implementation successfully diagnoses all 11 predefined evaluation scenarios using both forward and backward chaining, with both approaches achieving 100% accuracy on the test set.

---

## Author

**AI-Based IT Helpdesk Expert System**

Built as an Artificial Intelligence / Expert Systems project using symbolic rule-based inference.