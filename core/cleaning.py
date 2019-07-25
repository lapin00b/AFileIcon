import shutil

import sublime

from . import settings

from .utils import path
from .utils.logging import log, dump, message
from .utils.overlay import with_ignored_overlay


@with_ignored_overlay
def clean_all():
    message("Cleaning up")

    def handler(function, path, excinfo):
        if handler.success:
            handler.success = False
            log("Error during cleaning")
        dump(path)

    handler.success = True

    shutil.rmtree(path.overlay_cache_path(), onerror=handler)
    shutil.rmtree(path.overlay_path(), onerror=handler)

    if handler.success:
        message("Cleaned up successfully")

    return handler.success


def revert():
    settings.clear_listener()

    try:
        clean_all()
    except Exception as error:
        dump(error)
    finally:
        settings.add_listener()
