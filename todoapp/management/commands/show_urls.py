# todoapp/management/commands/show_urls.py

from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Displays all registered routes'

    def handle(self, *args, **kwargs):
        resolver = get_resolver()
        for pattern in resolver.url_patterns:
            self.print_patterns(pattern)

    def print_patterns(self, pattern, prefix=''):
        if hasattr(pattern, 'url_patterns'):
            for sub_pattern in pattern.url_patterns:
                self.print_patterns(sub_pattern, prefix + pattern.pattern.regex.pattern)
        else:
            self.stdout.write(f"{prefix}{pattern.pattern.regex.pattern} -> {pattern.callback}")
