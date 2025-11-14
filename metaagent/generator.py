# metaagent/generator.py
import os
from typing import Any, Dict
from jinja2 import Template

AGENT_TEMPLATE = """from typing import Any, Dict, List
import csv, re

# ---------- Built-in tool implementations (MVP) ----------
def pdf_read(path: str) -> Dict[str, Any]:
    # Treat input as plain text for the MVP
    with open(path, "r", encoding="utf-8") as f:
        return {"text": f.read()}

def regex_extract(text: str) -> Dict[str, Any]:
    # Real regex parsing for "Total:" and "Supplier:"
    # Handles:
    #   Supplier: ABC Ltd
    #   Total: 123.45
    total_match = re.search(
        r"Total[:\\s]+([0-9]+(?:\\.[0-9]{2})?)",
        text,
        flags=re.IGNORECASE,
    )
    # Capture supplier up to end-of-line only (no bleed into next lines)
    supplier_match = re.search(
        r"Supplier[:\\s]+([^\\r\\n]+)",
        text,
        flags=re.IGNORECASE,
    )

    total = float(total_match.group(1)) if total_match else 0.0
    supplier = supplier_match.group(1).strip() if supplier_match else "Unknown"

    return {"fields": {"total": total, "supplier": supplier}}

def schema_validate(obj: dict) -> Dict[str, Any]:
    # MVP: accept everything; stub for future schema checks
    return {"ok": True}

def classify_text(text: str) -> Dict[str, Any]:
    t = (text or "").lower()
    if "bill" in t or "invoice" in t or "payment" in t:
        return {"label": "billing"}
    if "refund" in t or "return" in t:
        return {"label": "returns"}
    return {"label": "general"}

def reply_template(label: str) -> Dict[str, Any]:
    replies = {
        "billing": "Hi, this looks like a billing question. Our team will assist shortly.",
        "returns": "Thanks for reaching out. Here’s how to start a return...",
        "general": "Thanks for your message! We’ll get back to you soon.",
    }
    return {"reply": replies.get(label, replies["general"])}

def http_get(url: str) -> Dict[str, Any]:
    # MVP: do not hit the network; return a mock
    return {"status": 200, "json": {"id": 42, "info": "mocked"}}

def csv_read(path: str) -> Dict[str, Any]:
    rows: List[dict] = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return {"rows": rows}

# Registry keyed by TOOL TYPE
TOOLS = {
    "builtin.pdf_read": pdf_read,
    "builtin.regex": regex_extract,
    "builtin.schema": schema_validate,
    "builtin.classify": classify_text,
    "builtin.reply_template": reply_template,
    "builtin.http_get": http_get,
    "builtin.csv_read": csv_read,
}

class GeneratedAgent:
    def __init__(self):
        self.ctx: Dict[str, Any] = {"inputs": {}}

    def run(self, **inputs):
        self.ctx["inputs"].update(inputs)
        {{body}}
        return self.ctx
"""

def _tool_type_for(tool_id: str, workflow: dict) -> str:
    """
    Look up the tool 'type' (e.g., 'builtin.pdf_read') for a given tool 'id'
    (e.g., 'pdf_reader'). Falls back to the id if not found.
    """
    for t in workflow.get("tools", []):
        if t.get("id") == tool_id:
            return t.get("type", tool_id)
    return tool_id

def _render_arg(value: Any) -> str:
    """
    Convert a spec value into Python code for a function argument.
    Supports:
      - {{inputs.X}}  -> self.ctx['inputs']['X']
      - {{nodeY.key}} -> self.ctx['nodeY']['key']
      - literals -> repr(value)
    """
    if isinstance(value, str) and value.startswith("{{") and value.endswith("}}"):
        inner = value[2:-2].strip()
        if inner.startswith("inputs."):
            key = inner.split(".", 1)[1]
            return f"self.ctx['inputs']['{key}']"
        if "." in inner:
            node_ref, out_key = inner.split(".", 1)
            return f"self.ctx['{node_ref}']['{out_key}']"
        return repr(value)
    return repr(value)

def generate_agent_package(workflow: dict, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)

    # Naive linear execution in node order (MVP)
    lines = []
    for n in workflow.get("nodes", []):
        nid = n["id"]
        tool_type = _tool_type_for(n["tool"], workflow)

        # Build args
        args_src = []
        for k, v in (n.get("inputs") or {}).items():
            args_src.append(f"{k}={_render_arg(v)}")

        call = f"res_{nid} = TOOLS['{tool_type}']({', '.join(args_src)})"
        assign = f"self.ctx['{nid}'] = res_{nid}"
        lines.append(call)
        lines.append(assign)

    # IMPORTANT: use real newlines, not escaped "\\n"
    body = "\n        ".join(lines) if lines else "pass"
    rendered = Template(AGENT_TEMPLATE).render(body=body)

    # Write agent.py
    with open(os.path.join(out_dir, "agent.py"), "w", encoding="utf-8") as f:
        f.write(rendered)

    # Minimal run script
    run_py = """from agent import GeneratedAgent
import argparse, json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf_path", type=str, required=False, help="Path to input file")
    parser.add_argument("--support_path", type=str, required=False, help="Path to support text")
    parser.add_argument("--csv_path", type=str, required=False, help="Path to CSV")
    args = parser.parse_args()

    agent = GeneratedAgent()
    ctx = agent.run(
        pdf_path=args.pdf_path,
        support_path=args.support_path,
        csv_path=args.csv_path
    )
    print(json.dumps(ctx, indent=2))
"""
    with open(os.path.join(out_dir, "run.py"), "w", encoding="utf-8") as f:
        f.write(run_py)
