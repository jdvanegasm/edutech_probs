const API_URL = "http://127.0.0.1:8000";

async function getQuestions() {
  const res = await fetch(`${API_URL}/questions`);
  return res.json();
}

async function generateProblem(id, paramsOverride = null, mode = "normal") {
  const res = await fetch(`${API_URL}/generate-problem`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      id,
      params_override: paramsOverride,
      mode,
    }),
  });
  return res.json();
}

async function generateTest(numQuestions) {
  const res = await fetch(`${API_URL}/generate-test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ num_questions: numQuestions }),
  });
  return res.json();
}

async function gradeTest(answers) {
  const res = await fetch(`${API_URL}/grade-test`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answers }),
  });
  return res.json();
}

export default {
  getQuestions,
  generateProblem,
  generateTest,
  gradeTest,
};