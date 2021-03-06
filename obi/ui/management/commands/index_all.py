from optparse import make_option

from django.core.management.base import BaseCommand

from ui.utils import index_databases, index_journals


class Command(BaseCommand):
    help = 'index the database list and journal titles list'
    option_list = BaseCommand.option_list + (
        make_option('--no-clear', action="store_true", default=False,
                    help='Do not clear out the solr index.'),
        )

    def handle(self, *args, **options):
        index_databases(options.get('no-clear', None))
        index_journals(options.get('no-clear', None))
