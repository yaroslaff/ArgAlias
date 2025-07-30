import typer
from argalias import ArgAlias

def common_handler(entity: str, command: str, name: str):
    typer.echo(f"{entity.capitalize()} {command}: {name}")

app = typer.Typer()

@app.command()
def employee(command: str, name: str):
    "Manage employees"
    common_handler("employee", command, name)

@app.command()
def project(command: str, name: str):
    "Manage projects"
    common_handler("project", command, name)

def resolve_aliases():
    aa = ArgAlias()
    aa.alias(["get", "sh", "s"], "show", prefix="*")
    aa.alias(["emp", "e"], "employee")
    aa.alias(["proj", "p", "pr"], "project")

    aa.alias(["cr", "c"], "create", prefix=["employee|project"])
    aa.alias(["del", "d"], ["delete"], prefix="**")

    aa.parse()


if __name__ == "__main__":
    resolve_aliases()
    app()
