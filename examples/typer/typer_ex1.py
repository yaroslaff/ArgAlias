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
    aa.alias("show", "get", "sh", "s")
    aa.alias(["employee"], "emp", "e")
    aa.alias(["project"], "proj", "p")

    aa.alias(["employee|project", "create"], "cr", "c")
    aa.alias(["*", "delete"], "del", "d")
    aa.parse()

if __name__ == "__main__":
    resolve_aliases()
    app()
