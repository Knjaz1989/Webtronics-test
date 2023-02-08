import click


@click.group('admin')
def admin_group():
    """ One place to configure all site apps"""


@admin_group.command()
def run():
    pass
