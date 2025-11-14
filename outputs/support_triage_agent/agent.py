from typing import Any, Dict, List
import csv

# ---------- Built-in tool stubs (MVP) ----------
def pdf_read(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return {"text": f.read()}

def regex_extract(text: str) -> Dict[str, Any]:
    # TODO: replace with real regex; MVP returns dummy parse
    return {"fields": {"total": 0.00, "supplier": "ACME Ltd"}}

def schema_validate(obj: dict) -> Dict[str, Any]:
    # MVP: accept everything
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
        res_load_msg = TOOLS['builtin.pdf_read'](path=self.ctx['inputs']['support_path'])
        self.ctx['load_msg'] = res_load_msg
        res_classify = TOOLS['builtin.classify'](text=self.ctx['load_msg']['text'])
        self.ctx['classify'] = res_classify
        res_make_reply = TOOLS['builtin.reply_template'](label=self.ctx['classify']['label'])
        self.ctx['make_reply'] = res_make_reply
        return self.ctx