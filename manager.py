#!/usr/bin/env python3
import click

from apps.cli import site_group
from apps.admin.cli import admin_group
from database.cli import db_group


@click.group()
def main_group():
    pass


main_group.add_command(site_group)
main_group.add_command(admin_group)
main_group.add_command(db_group)


if __name__ == "__main__":
    main_group()


