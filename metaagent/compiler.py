import json, yaml, os
from .models import AgentSpec

def load_spec(path: str) -> AgentSpec:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AgentSpec(**data)

def compile_to_workflow(spec: AgentSpec) -> dict:
    # Normalize spec to a canonical, machine-oriented structure
    wf = {
        "name": spec.agent.name,
        "description": spec.agent.description,
        "nodes": [n.model_dump(by_alias=True) for n in spec.workflow.nodes],
        "edges": [e.model_dump(by_alias=True) for e in spec.workflow.edges],
        "policies": spec.policies.model_dump(),
        "tools": [t.model_dump() for t in spec.tools],
    }
    return wf

def save_json(obj: dict, out_path: str):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
