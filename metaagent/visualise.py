def to_mermaid(wf: dict) -> str:
    lines = ["flowchart TD"]
    # Nodes
    for n in wf.get("nodes", []):
        nid = n["id"]
        kind = n.get("kind", "task")
        lines.append(f"  {nid}[{nid}: {kind}]")
    # Edges
    for e in wf.get("edges", []):
        cond = f" |{e.get('when')}| " if e.get('when') else " "
        lines.append(f"  {e['from']}{cond}--> {e['to']}")
    return "\n".join(lines)
