import { useState, useEffect } from "react";
import backend from "../api/backend";

export default function Practice() {
  const [questions, setQuestions] = useState([]);
  const [selected, setSelected] = useState("");
  const [problem, setProblem] = useState(null);
  const [showSolution, setShowSolution] = useState(false);

  useEffect(() => {
    backend.getQuestions().then(setQuestions);
  }, []);

  async function generate() {
    if (!selected) return;
    const data = await backend.generateProblem(selected, null, "repaso");
    setProblem(data);
    setShowSolution(false);
  }

  return (
    <div className="page-container">
      <h2 style={{ fontSize: "32px", marginBottom: "10px" }}>🧠 Práctica Libre</h2>
      <p style={{ color: "#555", marginBottom: "30px", fontSize: "17px" }}>
        Selecciona un ejercicio y practica con parámetros aleatorios.
      </p>

      {/* CARD — SELECTOR */}
      <div className="card">
        <label style={{ fontWeight: "600" }}>Ejercicio:</label>

        <select
          value={selected}
          onChange={(e) => setSelected(e.target.value)}
          style={{ width: "100%", marginTop: "12px" }}
        >
          <option value="">Seleccione un ejercicio…</option>
          {questions.map((q) => (
            <option key={q.id} value={q.id}>
              {q.topic} — {q.id}
            </option>
          ))}
        </select>

        <button
          className="btn btn-primary"
          onClick={generate}
          style={{ marginTop: "18px", width: "100%" }}
        >
          Generar ejercicio
        </button>
      </div>

      {/* ------------------------------------ */}
      {/*             RESULTADO                */}
      {/* ------------------------------------ */}
      {problem && (
        <div
          className="card"
          style={{
            background: "white",
            borderRadius: "14px",
            padding: "25px",
            marginTop: "25px",
          }}
        >
          <h3 style={{ marginTop: 0, fontSize: "24px" }}>Enunciado</h3>

          <p style={{ fontSize: "18px", lineHeight: "1.6", marginTop: "10px" }}>
            {problem.statement}
          </p>

          {/* TEORÍA */}
          {problem.doc_summary && (
            <div
              style={{
                background: "#eaf3ff",
                padding: "18px",
                borderRadius: "10px",
                marginTop: "25px",
                borderLeft: "5px solid #4A90E2",
                boxShadow: "0 2px 10px rgba(0,0,0,0.08)"
              }}
            >
              <h4 style={{ marginTop: 0, fontSize: "18px" }}>
                📘 Resumen teórico
              </h4>
              <p style={{ margin: 0, lineHeight: "1.5" }}>
                {problem.doc_summary}
              </p>
            </div>
          )}

          {/* DOCUMENTACIÓN */}
          {problem.doc_url && (
            <p style={{ marginTop: "20px" }}>
              <a
                href={problem.doc_url}
                target="_blank"
                rel="noopener noreferrer"
                style={{ fontWeight: "600" }}
              >
                📚 Ver documentación completa
              </a>
            </p>
          )}

          {/* BOTÓN SOLUCIÓN */}
          <div style={{ marginTop: "30px" }}>
            <button
              className={`btn ${showSolution ? "btn-gray" : "btn-success"}`}
              onClick={() => setShowSolution((v) => !v)}
            >
              {showSolution ? "Ocultar solución" : "Mostrar solución"}
            </button>

            {/* SOLUCIÓN */}
            {showSolution && (
              <div
                style={{
                  marginTop: "18px",
                  padding: "18px",
                  borderRadius: "10px",
                  background: "white",
                  border: "1px solid #cdd2d9",
                  boxShadow: "0 2px 10px rgba(0,0,0,0.07)",
                  animation: "fadeIn 0.25s ease"
                }}
              >
                <pre style={{ margin: 0 }}>
                  {JSON.stringify(problem.correct_answer, null, 2)}
                </pre>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}