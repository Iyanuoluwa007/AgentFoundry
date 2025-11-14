from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field, model_validator

NodeKind = Literal["task", "router", "evaluator"]

class AgentInfo(BaseModel):
    name: str
    description: Optional[str] = ""

class IOParam(BaseModel):
    name: str
    type: str

class Tool(BaseModel):
    id: str
    type: str
    config: Dict = Field(default_factory=dict)

class Node(BaseModel):
    id: str
    kind: NodeKind
    tool: str
    inputs: Dict = Field(default_factory=dict)
    outputs: List[str] = Field(default_factory=lambda: ["result"])
    on_error: Dict = Field(default_factory=dict)
    timeout: int = 30
    retry: int = 0

class Edge(BaseModel):
    from_: str = Field(alias="from")
    to: str
    when: Optional[str] = None

class WorkflowSpec(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

class Policies(BaseModel):
    pii_redaction: bool = False
    allow_network: bool = False

class AgentSpec(BaseModel):
    agent: AgentInfo
    tools: List[Tool]
    workflow: WorkflowSpec
    policies: Policies = Policies()

    @model_validator(mode="after")
    def validate_graph(self):
        tool_ids = {t.id for t in self.tools}
        node_ids = {n.id for n in self.workflow.nodes}

        # Tool references
        for n in self.workflow.nodes:
            if n.tool not in tool_ids:
                raise ValueError(f"Node '{n.id}' references unknown tool '{n.tool}'")

        # Edge references
        for e in self.workflow.edges:
            if e.from_ not in node_ids or e.to not in node_ids:
                raise ValueError(f"Edge {e.from_}->{e.to} references unknown nodes")

        # Simple cycle check via DFS (optional, minimal)
        graph = {n.id: [] for n in self.workflow.nodes}
        for e in self.workflow.edges:
            graph[e.from_].append(e.to)

        visited, stack = set(), set()

        def dfs(u: str):
            if u in stack:
                raise ValueError("Cycle detected in workflow graph")
            if u in visited:
                return
            stack.add(u)
            for v in graph.get(u, []):
                dfs(v)
            stack.remove(u)
            visited.add(u)

        for n in node_ids:
            if n not in visited:
                dfs(n)

        return self
