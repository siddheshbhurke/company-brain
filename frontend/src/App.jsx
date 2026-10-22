
import { useEffect, useState } from "react";
import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  BookOpen,
  Brain,
  Check,
  ChevronDown,
  ChevronRight,
  CircleAlert,
  FileText,
  FolderOpen,
  GitBranch,
  LayoutDashboard,
  LoaderCircle,
  Network,
  Play,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Workflow,
} from "lucide-react";
import "./App.css";

const API = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

const navigation = [
  { id: "overview", label: "Overview", icon: LayoutDashboard },
  { id: "knowledge", label: "Knowledge", icon: Network },
  { id: "skills", label: "Skill library", icon: FolderOpen },
  { id: "planner", label: "Agent planner", icon: Workflow },
];

async function request(path, options = {}) {
  const response = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : `Request failed (${response.status})`
    );
  }

  return data;
}

function Status({ state }) {
  const connected = state === "connected";

  return (
    <span className={`status ${connected ? "status-ok" : "status-offline"}`}>
      <span className="status-dot" />
      {connected ? "Backend connected" : "Backend unavailable"}
    </span>
  );
}

function SectionHeading({ eyebrow, title, description, action }) {
  return (
    <div className="section-heading">
      <div>
        {eyebrow && <p className="eyebrow">{eyebrow}</p>}
        <h1>{title}</h1>
        {description && <p className="section-description">{description}</p>}
      </div>
      {action}
    </div>
  );
}

function EmptyState({ icon: Icon = FileText, title, description }) {
  return (
    <div className="empty-state">
      <Icon size={24} strokeWidth={1.5} />
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  );
}

export default function App() {
  const [page, setPage] = useState("overview");
  const [apiState, setApiState] = useState("checking");
  const [skills, setSkills] = useState([]);
  const [loadingSkills, setLoadingSkills] = useState(false);
  const [selectedSkillId, setSelectedSkillId] = useState("");
  const [selectedSkill, setSelectedSkill] = useState(null);
  const [skillLoading, setSkillLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [inputs, setInputs] = useState({});
  const [availableTools, setAvailableTools] = useState("");
  const [plan, setPlan] = useState(null);
  const [planLoading, setPlanLoading] = useState(false);
  const [compileResult, setCompileResult] = useState(null);
  const [compileLoading, setCompileLoading] = useState(false);
  const [error, setError] = useState("");

  async function checkBackend() {
    try {
      await request("/health");
      setApiState("connected");
    } catch {
      setApiState("offline");
    }
  }

  async function loadSkills() {
    setLoadingSkills(true);
    setError("");

    try {
      const data = await request("/api/skills");
      setSkills(data.skills || []);
      setApiState("connected");

      if (
        data.skills?.length &&
        !data.skills.some((skill) => skill.skill_id === selectedSkillId)
      ) {
        setSelectedSkillId(data.skills[0].skill_id);
      }
    } catch (err) {
      setApiState("offline");
      setError(err.message);
    } finally {
      setLoadingSkills(false);
    }
  }

  async function openSkill(skillId) {
    if (!skillId) return;

    setSelectedSkillId(skillId);
    setSelectedSkill(null);
    setInputs({});
    setPlan(null);
    setCompileResult(null);
    setError("");
    setSkillLoading(true);

    try {
      const data = await request(
        `/api/skills/${encodeURIComponent(skillId)}`
      );
      setSelectedSkill(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setSkillLoading(false);
    }
  }

  useEffect(() => {
    checkBackend();
    loadSkills();
    // Initial load only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (selectedSkillId) openSkill(selectedSkillId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedSkillId]);

  async function createPlan(event) {
    event.preventDefault();
    if (!selectedSkillId) return;

    setPlanLoading(true);
    setPlan(null);
    setError("");

    try {
      const toolList = availableTools
        .split(",")
        .map((tool) => tool.trim())
        .filter(Boolean);

      const data = await request("/api/plans", {
        method: "POST",
        body: JSON.stringify({
          skill_id: selectedSkillId,
          inputs,
          available_tools: toolList,
        }),
      });

      setPlan(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setPlanLoading(false);
    }
  }

  async function compileSkill() {
    if (!selectedSkillId) return;

    setCompileLoading(true);
    setCompileResult(null);
    setError("");

    try {
      const data = await request(
        `/api/skills/${encodeURIComponent(selectedSkillId)}/compile`,
        { method: "POST" }
      );
      setCompileResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setCompileLoading(false);
    }
  }

  const filteredSkills = skills.filter((skill) =>
    `${skill.name} ${skill.description} ${skill.skill_id}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  function changePage(nextPage) {
    setPage(nextPage);
    setError("");
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <button
          className="brand"
          onClick={() => changePage("overview")}
          aria-label="Company Brain home"
        >
          <span className="brand-mark">
            <Brain size={21} strokeWidth={1.7} />
          </span>
          <span className="brand-copy">
            <strong>company brain</strong>
            <small>Organizational intelligence</small>
          </span>
        </button>

        <div className="sidebar-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              className={`nav-item ${page === id ? "nav-item-active" : ""}`}
              onClick={() => changePage(id)}
            >
              <Icon size={18} strokeWidth={1.7} />
              <span>{label}</span>
              {id === "skills" && skills.length > 0 && (
                <span className="nav-count">{skills.length}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="sidebar-bottom">
          <div className="sidebar-note">
            <ShieldCheck size={18} />
            <div>
              <strong>Governed by design</strong>
              <p>Plans are reviewed before execution.</p>
            </div>
          </div>
          <div className="sidebar-footer">
            <span className="footer-mark">CB</span>
            <div>
              <strong>Company Brain</strong>
              <small>Review-III prototype · v0.1</small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            Workspace <ChevronRight size={14} />{" "}
            {navigation.find((item) => item.id === page)?.label || "Overview"}
          </div>
          <div className="topbar-right">
            <Status state={apiState} />
            <button
              className="icon-button"
              onClick={() => {
                checkBackend();
                loadSkills();
              }}
              title="Refresh backend status and skills"
              aria-label="Refresh"
            >
              <RefreshCw size={16} />
            </button>
          </div>
        </header>

        {error && (
          <div className="error-banner" role="alert">
            <CircleAlert size={18} />
            <span>{error}</span>
            <button onClick={() => setError("")} aria-label="Dismiss error">
              ×
            </button>
          </div>
        )}

        {page === "overview" && (
          <div className="page-content">
            <SectionHeading
              eyebrow="YOUR WORKSPACE"
              title="Organizational knowledge, connected."
              description="A structured memory layer that helps AI agents work with company-specific knowledge and procedures."
              action={
                <button
                  className="button button-primary"
                  onClick={() => changePage("planner")}
                >
                  Open agent planner <ArrowRight size={16} />
                </button>
              }
            />

            <div className="overview-note">
              <div className="overview-note-icon">
                <GitBranch size={20} />
              </div>
              <div>
                <strong>From fragmented information to reusable skills</strong>
                <p>
                  Ingest knowledge, connect relationships, define procedures,
                  and prepare skills for governed agent workflows.
                </p>
              </div>
              <ArrowDownRight className="overview-note-arrow" size={20} />
            </div>

            <div className="section-title-row">
              <h2>Workspace</h2>
              <span className="muted-label">CURRENT MODULES</span>
            </div>

            <div className="module-grid">
              <button
                className="module-card"
                onClick={() => changePage("knowledge")}
              >
                <div className="module-icon"><BookOpen size={19} /></div>
                <div className="module-card-title">
                  <h3>Knowledge base</h3>
                  <ArrowRight size={15} />
                </div>
                <p>Organizational documents, semantic retrieval and connected knowledge.</p>
                <span className="module-link">Explore knowledge</span>
              </button>

              <button
                className="module-card"
                onClick={() => changePage("skills")}
              >
                <div className="module-icon"><FolderOpen size={19} /></div>
                <div className="module-card-title">
                  <h3>Skill library</h3>
                  <ArrowRight size={15} />
                </div>
                <p>Reusable, structured procedures that agents can consume.</p>
                <span className="module-link">
                  {skills.length} registered skills
                </span>
              </button>

              <button
                className="module-card"
                onClick={() => changePage("planner")}
              >
                <div className="module-icon"><Workflow size={19} /></div>
                <div className="module-card-title">
                  <h3>Agent planner</h3>
                  <ArrowRight size={15} />
                </div>
                <p>Validate required inputs and identify missing tools before execution.</p>
                <span className="module-link">Build a plan</span>
              </button>
            </div>

            <div className="section-title-row">
              <h2>Registered skills</h2>
              <button className="text-button" onClick={() => changePage("skills")}>
                View library <ArrowRight size={14} />
              </button>
            </div>

            <SkillTable
              skills={skills.slice(0, 5)}
              loading={loadingSkills}
              onSelect={(id) => {
                setSelectedSkillId(id);
                changePage("skills");
              }}
            />
          </div>
        )}

        {page === "knowledge" && (
          <div className="page-content">
            <SectionHeading
              eyebrow="ORGANIZATIONAL MEMORY"
              title="Knowledge base"
              description="The foundation for grounding agent decisions in company-specific information."
            />

            <div className="knowledge-grid">
              <div className="panel knowledge-panel">
                <div className="module-icon"><BookOpen size={20} /></div>
                <h3>Semantic retrieval</h3>
                <p>
                  Document chunks and embeddings are stored in PostgreSQL with
                  pgvector to support meaning-based search.
                </p>
                <span className="status status-neutral">Backend capability</span>
              </div>
              <div className="panel knowledge-panel">
                <div className="module-icon"><Network size={20} /></div>
                <h3>Knowledge graph</h3>
                <p>
                  Neo4j represents relationships between organizational entities,
                  policies, processes and skills.
                </p>
                <span className="status status-neutral">Backend capability</span>
              </div>
            </div>

            <div className="panel info-panel">
              <h3>How the memory layer works</h3>
              <ol className="numbered-list">
                <li><span>01</span> Ingest organizational documents and structured data.</li>
                <li><span>02</span> Split documents into chunks and generate embeddings.</li>
                <li><span>03</span> Retrieve relevant information using semantic search.</li>
                <li><span>04</span> Use graph relationships to add organizational context.</li>
                <li><span>05</span> Make the relevant knowledge available to downstream skills and agents.</li>
              </ol>
              <p className="subtle-note">
                This screen describes implemented backend capabilities. A live
                search and graph explorer UI has not yet been connected.
              </p>
            </div>
          </div>
        )}

        {page === "skills" && (
          <div className="page-content">
            <SectionHeading
              eyebrow="REUSABLE PROCEDURES"
              title="Skill library"
              description="Browse validated skill definitions and compile them into agent-consumable instructions."
              action={
                <button
                  className="button button-secondary"
                  onClick={loadSkills}
                  disabled={loadingSkills}
                >
                  <RefreshCw size={15} className={loadingSkills ? "spin" : ""} />
                  Refresh
                </button>
              }
            />

            <div className="search-bar">
              <Search size={17} />
              <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Search skills by name or description..."
                aria-label="Search skills"
              />
              <span>{filteredSkills.length} skills</span>
            </div>

            <SkillTable
              skills={filteredSkills}
              loading={loadingSkills}
              onSelect={(id) => {
                setSelectedSkillId(id);
                changePage("skills");
              }}
              selectedId={selectedSkillId}
            />

            {selectedSkillId && (
              <div className="panel detail-panel">
                <div className="detail-heading">
                  <div>
                    <p className="eyebrow">SKILL DEFINITION</p>
                    <h2>{selectedSkill?.name || selectedSkillId}</h2>
                    <p className="muted-text">
                      {selectedSkill?.description || "Loading skill details..."}
                    </p>
                  </div>
                  {selectedSkill?.version && (
                    <span className="version-tag">v{selectedSkill.version}</span>
                  )}
                </div>

                {skillLoading ? (
                  <p className="inline-loading"><LoaderCircle className="spin" size={17} /> Loading skill...</p>
                ) : selectedSkill ? (
                  <>
                    <div className="detail-meta">
                      <div>
                        <span>Skill ID</span>
                        <code>{selectedSkill.skill_id}</code>
                      </div>
                      <div>
                        <span>Risk level</span>
                        <strong>{selectedSkill.risk_level || "Unspecified"}</strong>
                      </div>
                      <div>
                        <span>Status</span>
                        <strong>{selectedSkill.status || "Draft"}</strong>
                      </div>
                      <div>
                        <span>Procedure steps</span>
                        <strong>{selectedSkill.steps?.length ?? 0}</strong>
                      </div>
                    </div>

                    <h3 className="subsection-heading">Procedure</h3>
                    <div className="step-list">
                      {(selectedSkill.steps || []).map((step) => (
                        <div className="step-row" key={`${step.order}-${step.name}`}>
                          <span className="step-number">
                            {String(step.order).padStart(2, "0")}
                          </span>
                          <div className="step-copy">
                            <strong>{step.name.replaceAll("_", " ")}</strong>
                            <p>{step.action}</p>
                          </div>
                          {step.tool_name && (
                            <span className="tool-tag">{step.tool_name}</span>
                          )}
                        </div>
                      ))}
                    </div>

                    <div className="detail-actions">
                      <button
                        className="button button-primary"
                        onClick={() => changePage("planner")}
                      >
                        <Play size={15} /> Plan this skill
                      </button>
                      <button
                        className="button button-secondary"
                        onClick={compileSkill}
                        disabled={compileLoading}
                      >
                        {compileLoading
                          ? <LoaderCircle size={15} className="spin" />
                          : <FileText size={15} />}
                        Compile SKILL.md
                      </button>
                    </div>

                    {compileResult && (
                      <div className="success-banner">
                        <Check size={18} />
                        <div>
                          <strong>Skill compiled successfully</strong>
                          <p>{compileResult.artifact}</p>
                        </div>
                      </div>
                    )}
                  </>
                ) : (
                  <EmptyState
                    title="Skill details unavailable"
                    description="Check that the backend is running and the skill definition is valid."
                  />
                )}
              </div>
            )}
          </div>
        )}

        {page === "planner" && (
          <div className="page-content">
            <SectionHeading
              eyebrow="GOVERNED WORKFLOW"
              title="Agent planner"
              description="Build a structured plan for a skill and check required inputs and tools before any execution."
            />

            <div className="planner-layout">
              <form className="panel planner-form" onSubmit={createPlan}>
                <div className="panel-heading">
                  <div>
                    <h2>Configure a plan</h2>
                    <p>Select a skill and provide its required inputs.</p>
                  </div>
                  <Workflow size={20} />
                </div>

                <label className="field-label" htmlFor="skill-select">Skill</label>
                <div className="select-wrap">
                  <select
                    id="skill-select"
                    value={selectedSkillId}
                    onChange={(event) => setSelectedSkillId(event.target.value)}
                    required
                  >
                    {skills.map((skill) => (
                      <option key={skill.skill_id} value={skill.skill_id}>
                        {skill.name}
                      </option>
                    ))}
                  </select>
                  <ChevronDown size={16} />
                </div>

                {selectedSkill?.description && (
                  <p className="field-hint">{selectedSkill.description}</p>
                )}

                <div className="form-divider" />

                <div className="field-group-heading">
                  <h3>Skill inputs</h3>
                  <span>Required by definition</span>
                </div>

                {selectedSkill?.inputs?.length ? (
                  selectedSkill.inputs.map((field) => (
                    <div className="field-group" key={field}>
                      <label className="field-label" htmlFor={`input-${field}`}>
                        {field.replaceAll("_", " ")}
                      </label>
                      <input
                        id={`input-${field}`}
                        value={inputs[field] ?? ""}
                        onChange={(event) =>
                          setInputs((previous) => ({
                            ...previous,
                            [field]: event.target.value,
                          }))
                        }
                        placeholder={`Enter ${field.replaceAll("_", " ")}`}
                      />
                    </div>
                  ))
                ) : (
                  <p className="field-hint">
                    {selectedSkill
                      ? "This skill does not declare required inputs."
                      : "Loading skill input definitions..."}
                  </p>
                )}

                <div className="form-divider" />

                <label className="field-label" htmlFor="available-tools">
                  Available tools
                </label>
                <input
                  id="available-tools"
                  value={availableTools}
                  onChange={(event) => setAvailableTools(event.target.value)}
                  placeholder="tool_one, tool_two"
                />
                <p className="field-hint">
                  Enter tool names separated by commas. These are supplied to
                  the planner for checking; they are not independently verified
                  integrations.
                </p>

                <button
                  className="button button-primary full-width"
                  type="submit"
                  disabled={planLoading || !selectedSkillId}
                >
                  {planLoading ? (
                    <LoaderCircle size={16} className="spin" />
                  ) : (
                    <Play size={16} />
                  )}
                  {planLoading ? "Building plan..." : "Build execution plan"}
                </button>
              </form>

              <div className="panel plan-panel">
                <div className="panel-heading">
                  <div>
                    <h2>Plan output</h2>
                    <p>Generated by the Company Brain backend.</p>
                  </div>
                  <FileText size={20} />
                </div>

                {!plan ? (
                  <EmptyState
                    icon={Workflow}
                    title="No plan generated"
                    description="Choose a skill and build a plan to see its steps, constraints and missing requirements."
                  />
                ) : (
                  <div className="plan-results">
                    <div className="plan-status-block">
                      <span className="eyebrow">PLANNING STATUS</span>
                      <span className={`plan-status status-${plan.status}`}>
                        {plan.status.replaceAll("_", " ")}
                      </span>
                      <p>
                        Execution started:{" "}
                        <strong>{plan.execution_started ? "Yes" : "No"}</strong>
                      </p>
                    </div>

                    {plan.missing_inputs?.length > 0 && (
                      <div className="requirement-warning">
                        <CircleAlert size={17} />
                        <div>
                          <strong>Missing inputs</strong>
                          <p>{plan.missing_inputs.join(", ")}</p>
                        </div>
                      </div>
                    )}

                    {plan.missing_tools?.length > 0 && (
                      <div className="requirement-warning">
                        <CircleAlert size={17} />
                        <div>
                          <strong>Tools not listed as available</strong>
                          <p>{plan.missing_tools.join(", ")}</p>
                        </div>
                      </div>
                    )}

                    <h3 className="subsection-heading">Planned steps</h3>
                    <div className="step-list">
                      {(plan.steps || []).map((step) => (
                        <div className="step-row" key={`${step.order}-${step.name}`}>
                          <span className="step-number">
                            {String(step.order).padStart(2, "0")}
                          </span>
                          <div className="step-copy">
                            <strong>{step.name.replaceAll("_", " ")}</strong>
                            <p>{step.action}</p>
                            {step.tool_name && (
                              <span className="tool-tag">{step.tool_name}</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    {plan.constraints?.length > 0 && (
                      <>
                        <h3 className="subsection-heading">Constraints</h3>
                        <ul className="constraint-list">
                          {plan.constraints.map((constraint) => (
                            <li key={constraint}>{constraint}</li>
                          ))}
                        </ul>
                      </>
                    )}

                    <div className="governance-note">
                      <ShieldCheck size={18} />
                      <p>
                        {plan.approval_policy ||
                          "This plan must be checked by the governed runtime before execution."}
                      </p>
                    </div>

                    <button
                      className="button button-secondary full-width"
                      onClick={() =>
                        navigator.clipboard?.writeText(
                          JSON.stringify(plan, null, 2)
                        )
                      }
                    >
                      Copy plan JSON
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        <footer className="main-footer">
          <span>Company Brain · Review-III prototype</span>
          <span>Knowledge <span className="footer-separator">/</span> Skills <span className="footer-separator">/</span> Governance</span>
        </footer>
      </main>
    </div>
  );
}

function SkillTable({ skills, loading, onSelect, selectedId }) {
  if (loading && skills.length === 0) {
    return (
      <div className="panel table-state">
        <LoaderCircle className="spin" size={20} />
        Loading skills from the backend...
      </div>
    );
  }

  if (skills.length === 0) {
    return (
      <div className="panel">
        <EmptyState
          title="No skills found"
          description="Check the backend connection or try another search."
        />
      </div>
    );
  }

  return (
    <div className="panel table-panel">
      <div className="table-scroll">
        <table className="skills-table">
          <thead>
            <tr>
              <th>SKILL</th>
              <th>VERSION</th>
              <th>RISK</th>
              <th>STEPS</th>
              <th>STATUS</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {skills.map((skill) => (
              <tr
                key={skill.skill_id}
                className={selectedId === skill.skill_id ? "selected-row" : ""}
              >
                <td>
                  <button
                    className="table-skill-name"
                    onClick={() => onSelect(skill.skill_id)}
                  >
                    <span className="table-file-icon"><FileText size={17} /></span>
                    <span>
                      <strong>{skill.name}</strong>
                      <small>{skill.description}</small>
                    </span>
                  </button>
                </td>
                <td><span className="version-tag">v{skill.version}</span></td>
                <td>
                  <span className={`risk-tag risk-${(skill.risk_level || "unspecified").toLowerCase()}`}>
                    {skill.risk_level || "Unspecified"}
                  </span>
                </td>
                <td>{skill.step_count ?? "—"}</td>
                <td><span className="table-status">{skill.status || "Draft"}</span></td>
                <td>
                  <button
                    className="row-action"
                    onClick={() => onSelect(skill.skill_id)}
                    aria-label={`Open ${skill.name}`}
                  >
                    <ChevronRight size={17} />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
