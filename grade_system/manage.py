#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == '__main__':
    current_dir = Path(__file__).resolve().parent
    parent_dir = current_dir.parent
    sys.path.insert(0, str(parent_dir))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grade_system.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable?"
        ) from exc
    execute_from_command_line(sys.argv)
