# 🤖 AgentFoundry

**AgentFoundry** is a meta-agent framework that reads human-defined specifications and forges executable agents from them.
It demonstrates how structured reasoning, deterministic workflows, and modular tool bindings can be composed into auditable, real-world automation aligning with the principles of *Building Effective Agents*.

---

## 🚀 Overview

AgentFoundry transforms **YAML based agent specifications** into two main artifacts:

1. **Compiled Workflows** → canonical JSON + Mermaid diagrams.
2. **Runnable Agents** → generated Python packages (`agent.py`, `run.py`) that execute those workflows end-to-end.

This project is designed as a reproducible prototype for evaluating structured, safe, and composable meta-agent systems.

---

## ⚙️ Quick Start

### 1. Setup Environment

```bash
# Create and activate a virtual environment
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Compile a Spec → Workflow

```bash
python -m metaagent.cli compile examples/invoice_extractor.yaml --out outputs/
```

**Outputs:**

```
outputs/invoice_extractor.workflow.json
outputs/invoice_extractor.mmd
```

View the `.mmd` file at [https://mermaid.live](https://mermaid.live).

### 4. Generate Runnable Agents (Bonus)

```bash
python -m metaagent.cli generate examples/invoice_extractor.yaml --out outputs/
python outputs/invoice_extractor_agent/run.py --pdf_path sample_invoice.txt
```

### 5. Multi-Agent Demonstrations

```bash
# Support triage system
python -m metaagent.cli generate examples/support_triage.yaml --out outputs/
python outputs/support_triage_agent/run.py --support_path sample_support.txt

# Data enrichment workflow
python -m metaagent.cli generate examples/data_enricher.yaml --out outputs/
python outputs/data_enricher_agent/run.py --csv_path sample_data.csv
```

---

## 📁 Project Structure

```
AgentFoundry/
├── metaagent/
│   ├── cli.py             # CLI for compile & generate commands
│   ├── compiler.py        # YAML → JSON workflow compiler
│   ├── generator.py       # Workflow → runnable agent generator
│   ├── models.py          # Pydantic models for spec validation
│   ├── visualise.py       # Mermaid diagram generation
│   └── __init__.py
│
├── examples/              # Example YAML specs
│   ├── invoice_extractor.yaml
│   ├── support_triage.yaml
│   └── data_enricher.yaml
│
├── outputs/               # Compiled workflows and generated agents
├── sample_invoice.txt
├── sample_support.txt
├── sample_data.csv
├── requirements.txt
└── README.md
```

---

## 🧩 Example Output

### SupportTriage Agent

```json
{
  "inputs": {"support_path": "sample_support.txt"},
  "load_msg": {"text": "Hello, I have a billing issue with my last invoice. Thanks!"},
  "classify": {"label": "billing"},
  "make_reply": {
    "reply": "Hi, this looks like a billing question. Our team will assist shortly."
  }
}
```

### DataEnricher Agent

```json
{
  "inputs": {"csv_path": "sample_data.csv"},
  "read_csv": {"rows": [{"id": "123", "name": "Widget A"}]},
  "enrich_first": {"status": 200, "json": {"id": 42, "info": "mocked"}},
  "validate": {"ok": true}
}
```

---

## 🧱 Core Technologies

| Component       | Technology                               |
| --------------- | ---------------------------------------- |
| Language        | Python 3.10+                             |
| Validation      | Pydantic v2                              |
| Parsing         | PyYAML                                   |
| CLI             | Click                                    |
| Code Generation | Jinja2 Templates                         |
| Visualization   | Mermaid Flowcharts                       |
| Platform        | Cross-platform (Windows / Linux / macOS) |

---

## 🧠 Design Principles

* **Deterministic:** The same spec always yields the same workflow and agent.
* **Composable:** Workflows are built from typed nodes (`task`, `evaluator`, etc.).
* **Auditable:** Generated agents are readable, structured, and testable.
* **Extensible:** New tool types can be added with minimal code changes.
* **Safe:** No hidden network or LLM calls; all behavior is explicit.

---

## 🧭 Roadmap

* [ ] Router node type with conditional branching (`when:` clauses)
* [ ] Parallel execution and dependency graph scheduling
* [ ] CI/CD testing for generated agents
* [ ] Optional LLM-based spec ingestion
* [ ] Built-in metrics dashboard for execution telemetry

---

## 🪶 License

Released under the **MIT License** for educational and research use.
© 2025 Oke Iyanuoluwa Enoch

