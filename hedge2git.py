from datetime import datetime

import click

import _helpers
from hedgedoc.core import hedgedoc


@click.command()
@click.option(
    '--pull', '--download', 'pull',
    is_flag=True, default=False, show_default=True,
    help='Fetch and merge the latest changes.',
)
# @click.option(
#     '--pull-type', '--download-type', metavar='PULL_TYPE',
#     type=click.Choice(['append', 'overwrite'], case_sensitive=False),
#     default='append', show_default=True,
#     help='Choose the pulling type: append, overwrite.',
# )
@click.option(
    '--push', '--upload', 'push', metavar='COMMENT',
    is_flag=False, flag_value=datetime.now().strftime('Pushed at %Y-%m-%d %H:%M:%S'),
    default=None, show_default=True,
    help='Push changes.',
)
@click.option(
    '--overwrite', 'overwrite',
    is_flag=True, default=False, show_default=True,
    help='Remove unexisting notes during --pull/--push',
)
@click.option(
    '--refresh-history', 'refresh_history',
    is_flag=True, default=False, show_default=True,
    help='Refresh the browsing history.',
)
@click.option(
    '--refresh-alias', 'refresh_alias',
    is_flag=True, default=False, show_default=True,
    help='Refresh the alias of each note based on the tags.',
)
@click.option(
    '--dry-run', 'dry_run', is_flag=True,
    help='Show the files to be pulled/pushed without actually pulling/pushing them.',
)
def hedge2git(**actions: str | bool):
    """
    Sync hedgedoc via Git registries. Use .env to configure repository, access token, etc.
    """
    _helpers.validate(**actions)

    if actions['pull']:
        _helpers.pull(overwrite=actions['overwrite'], dry_run=actions['dry_run'])  # type: ignore

    if (comment := actions['push']) is not None:
        _helpers.push(comment, overwrite=actions['overwrite'], dry_run=actions['dry_run'])  # type: ignore

    if actions['refresh_history']:
        hedgedoc.refresh_history()
    if actions['refresh_alias']:
        hedgedoc.refresh_alias()  # type: ignore


if __name__ == '__main__':
    hedge2git()
