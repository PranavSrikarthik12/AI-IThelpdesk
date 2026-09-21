import axios from "axios";


const api = axios.create({
    baseURL: "/api",
    headers: {
        "Content-Type": "application/json",
    },
});


export const startDiagnosis = async (category) => {
    const response = await api.post(
        "/diagnosis/start",
        {
            category,
        }
    );

    return response.data;
};


export const submitAnswer = async (
    sessionId,
    questionId,
    fact
) => {
    const response = await api.post(
        `/diagnosis/${sessionId}/answer`,
        {
            question_id: questionId,
            fact,
        }
    );

    return response.data;
};


export default api;