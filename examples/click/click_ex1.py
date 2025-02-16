import click
from argalias import ArgAlias

def common_handler(entity, command, name):
    click.echo(f"{entity.capitalize()} {command}: {name}")

@click.group()
def cli():
    pass

@click.command()
@click.argument('command')
@click.argument('name')
def employee(command, name):
    "Manage employees"
    common_handler("employee", command, name)

@click.command()
@click.argument('command')
@click.argument('name')
def project(command, name):
    "Manage projects"
    common_handler("project", command, name)

cli.add_command(employee)
cli.add_command(project)


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
    cli()
