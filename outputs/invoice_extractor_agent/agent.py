from typing import Any, Dict, List
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
        r"Total[:\s]+([0-9]+(?:\.[0-9]{2})?)",
        text,
        flags=re.IGNORECASE,
    )
    # Capture supplier up to end-of-line only (no bleed into next lines)
    supplier_match = re.search(
        r"Supplier[:\s]+([^\r\n]+)",
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
        res_load_pdf = TOOLS['builtin.pdf_read'](path=self.ctx['inputs']['pdf_path'])
        self.ctx['load_pdf'] = res_load_pdf
        res_extract_fields = TOOLS['builtin.regex'](text=self.ctx['load_pdf']['text'])
        self.ctx['extract_fields'] = res_extract_fields
        res_validate = TOOLS['builtin.schema'](obj=self.ctx['extract_fields']['fields'])
        self.ctx['validate'] = res_validate
        return self.ctx