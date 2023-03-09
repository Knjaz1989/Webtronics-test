import click

from settings import config


@click.group("site")
def site_group():
    """Work with server"""


@site_group.command()
@click.option(
    '-h', '--host',
    default='0.0.0.0',
    help="IP address or local domain name to run server on")
@click.option(
    '-p', '--port',
    default=8000,
    help="Server port")
@click.option(
    '-l', '--log-level',
    default=config.DEBUG_SERVER,
    help="Logging level. One of: [critical|error|warning|info|debug|trace]")
def run(
        host: str = None,
        port: int = None,
        log_level: str = None):
    """Run server"""
    import uvicorn

    app_name = 'apps.server:app'

    uvicorn.run(
        app_name,
        host=host,
        port=port,
        log_level=log_level,
        reload=True
    )
