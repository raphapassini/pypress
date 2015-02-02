import os
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from docutils.core import publish_parts
from core.models import Entry


class Command(BaseCommand):
    args = '<rst_dir rst_dir ...>'
    help = 'Convert all rst and md files inside a directory into a Entry'

    def handle(self, *args, **options):
        for path in args:
            filenames = self.get_files_from_path(path)
            for filename in filenames:
                name, extension = os.path.splitext(filename)
                if extension != '.rst':
                    continue

                self.stdout.write('Processing: {}'.format(filename))
                with open(filename) as file:
                    content = file.read()
                    parts = publish_parts(
                        content, writer_name='html')
                    author = User.objects.get(username='root')

                    try:
                        Entry.objects.get(title=parts['title'])
                    except Entry.DoesNotExist:
                        Entry(
                            author=author, title=parts['title'],
                            body=parts['body']).save()

    def get_files_from_path(self, path):
        f = []
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                f.append(os.path.join(dirpath, filename))
        return f
