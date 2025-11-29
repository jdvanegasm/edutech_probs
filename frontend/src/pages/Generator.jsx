import { useState, useEffect } from "react";
import backend from "../api/backend";

export default function Generator() {
  const [questions, setQuestions] = useState([]);
  const [selected, setSelected] = useState("");
  const [resolvedId, setResolvedId] = useState(null);

  const [result, setResult] = useState(null);
  const [customParams, setCustomParams] = useState(null);
  const [paramRanges, setParamRanges] = useState(null);

  // ---------------------------------------
  // CARGAR SOLO PREGUNTAS INDIVIDUALES
  // ---------------------------------------
  useEffect(() => {
    fetch("http://127.0.0.1:8000/questions/full")
      .then((r) => r.json())
      .then((data) => setQuestions(data));
  }, []);

  // ---------------------------------------
  // Resolver min/max dinámicamente
  // ---------------------------------------
  function resolveRange(key) {
    if (!paramRanges || !customParams) return { min: null, max: null };

    const rule = paramRanges[key];
    let minVal = rule.min;
    let maxVal = rule.max;

    if (typeof minVal === "string") minVal = customParams[minVal];
    if (typeof maxVal === "string") maxVal = customParams[maxVal];

    return { min: minVal, max: maxVal };
  }

  // ---------------------------------------
  // GENERAR EJERCICIO
  // ---------------------------------------
  async function handleGenerate() {
    if (!selected) return;

    const finalId = selected;
    setResolvedId(finalId);

    const qInfo = questions.find((q) => q.id === finalId);
    if (qInfo) setParamRanges(qInfo.params);

    const data = await backend.generateProblem(finalId, null, "repaso");

    setResult(data);
    setCustomParams(data.params);
  }

  // Actualizar parámetro
  function updateParam(key, value) {
    const n = Number(value);
    setCustomParams({ ...customParams, [key]: isNaN(n) ? value : n });
  }

  // Resolver con parámetros manuales
  async function handleSolveCustom() {
    if (!resolvedId || !customParams) return;

    const data = await backend.generateProblem(resolvedId, customParams, "repaso");
    setResult(data);
  }

  return (
    <div className="page-container">
      <h2 style={{ fontSize: "32px", marginBottom: "10px" }}>⚙️ Generar Ejercicio</h2>
      <p style={{ color: "#555", marginBottom: "30px", fontSize: "17px" }}>
        Selecciona un ejercicio y ajusta los parámetros para ver cómo cambia el resultado.
      </p>

      {/* CARD: SELECTOR */}
      <div className="card">
        <label style={{ fontWeight: "600" }}>Seleccione ejercicio:</label>

        <select
          value={selected}
          onChange={(e) => {
            const val = e.target.value;
            setSelected(val);
            setResult(null);
            setCustomParams(null);
            setParamRanges(null);
            setResolvedId(null);
          }}
          style={{ width: "100%", marginTop: "12px" }}
        >
          <option value="">Seleccione una opción</option>

          {questions.map((q) => (
            <option key={q.id} value={q.id}>
              {q.id} — {q.topic}
            </option>
          ))}
        </select>

        <button
          className="btn btn-primary"
          onClick={handleGenerate}
          style={{ marginTop: "18px", width: "100%" }}
        >
          Generar ejercicio
        </button>
      </div>

      {/* RESULTADO */}
      {result && (
        <div
          className="card"
          style={{
            marginTop: "25px",
            animation: "fadeIn 0.25s ease",
          }}
        >
          <h3 style={{ fontSize: "24px", marginBottom: "10px" }}>Enunciado</h3>
          <p style={{ fontSize: "18px", lineHeight: "1.6" }}>{result.statement}</p>

          {/* PARÁMETROS */}
          <h4 style={{ marginTop: "30px", marginBottom: "12px" }}>Modificar parámetros</h4>

          {customParams &&
            Object.keys(customParams).map((key) => {
              const { min, max } = resolveRange(key);

              return (
                <div key={key} style={{ marginBottom: "25px" }}>
                  <label style={{ fontWeight: "600", display: "block", marginBottom: "8px" }}>
                    {key}:{" "}
                    <span style={{ color: "#4A90E2", fontWeight: "700" }}>
                      {customParams[key]}
                    </span>
                    <span style={{ color: "#777", marginLeft: "6px" }}>
                      ({min} – {max})
                    </span>
                  </label>

                  <input
                    type="range"
                    min={min}
                    max={max}
                    step="any"
                    value={customParams[key]}
                    onChange={(e) => updateParam(key, e.target.value)}
                    style={{
                      width: "100%",
                      cursor: "pointer",
                      marginBottom: "8px"
                    }}
                  />

                  <input
                    type="number"
                    value={customParams[key]}
                    min={min}
                    max={max}
                    step="any"
                    onChange={(e) => updateParam(key, e.target.value)}
                    style={{ width: "140px" }}
                  />
                </div>
              );
            })}

          <button
            className="btn btn-success"
            onClick={handleSolveCustom}
            style={{ marginTop: "10px" }}
          >
            Resolver con parámetros personalizados
          </button>

          {/* RESULTADO */}
          <h4 style={{ marginTop: "25px" }}>Resultado</h4>
          <pre
            style={{
              background: "#f4f7ff",
              padding: "14px",
              borderRadius: "10px",
              border: "1px solid #c9d8ff",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
            }}
          >
            {JSON.stringify(result.correct_answer, null, 2)}
          </pre>

          {/* DOCUMENTACIÓN */}
          {result.doc_url && (
            <>
              <h4 style={{ marginTop: "25px" }}>📚 Documentación</h4>

              <a
                href={result.doc_url}
                target="_blank"
                rel="noopener noreferrer"
                style={{ fontWeight: "600" }}
              >
                Ver documentación oficial
              </a>

              {result.doc_summary && (
                <div
                  style={{
                    background: "#eaf3ff",
                    marginTop: "15px",
                    padding: "18px",
                    borderRadius: "10px",
                    borderLeft: "5px solid #4A90E2",
                    boxShadow: "0 2px 10px rgba(0,0,0,0.08)"
                  }}
                >
                  <strong>Resumen teórico:</strong>
                  <p style={{ marginTop: "8px" }}>{result.doc_summary}</p>
                </div>
              )}
            </>
          )}

          <button
            className="btn btn-primary"
            onClick={handleGenerate}
            style={{ marginTop: "25px" }}
          >
            Generar otro ejercicio del mismo tipo
          </button>
        </div>
      )}
    </div>
  );
}