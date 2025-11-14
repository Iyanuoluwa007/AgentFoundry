import os, click
from .compiler import load_spec, compile_to_workflow, save_json
from .visualise import to_mermaid
from .generator import generate_agent_package

@click.group()
def cli():
    """MetaAgent CLI"""
    pass

@cli.command()
@click.argument("spec_path")
@click.option("--out", default="outputs", help="Output directory")
def compile(spec_path, out):
    """Compile a YAML spec into a normalized workflow JSON and Mermaid diagram."""
    os.makedirs(out, exist_ok=True)
    spec = load_spec(spec_path)
    wf = compile_to_workflow(spec)
    base = os.path.splitext(os.path.basename(spec_path))[0]
    wf_path = os.path.join(out, f"{base}.workflow.json")
    save_json(wf, wf_path)

    mmd_path = os.path.join(out, f"{base}.mmd")
    with open(mmd_path, "w", encoding="utf-8") as f:
        f.write(to_mermaid(wf))

    click.echo(f"Compiled: {wf_path}\nMermaid:  {mmd_path}")

@cli.command()
@click.argument("spec_path")
@click.option("--out", default="outputs", help="Output directory for generated agent package")
def generate(spec_path, out):
    """Generate a runnable Python agent package from a YAML spec."""
    os.makedirs(out, exist_ok=True)
    spec = load_spec(spec_path)
    wf = compile_to_workflow(spec)
    base = os.path.splitext(os.path.basename(spec_path))[0]
    out_dir = os.path.join(out, f"{base}_agent")
    generate_agent_package(wf, out_dir)
    click.echo(f"Generated agent package: {out_dir}\nRun it with: python {out_dir}/run.py --pdf_path path/to/input.txt")

if __name__ == "__main__":
    cli()
