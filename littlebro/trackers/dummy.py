import importlib
from time import time
from littlebro.trackers.base import BaseTracker
from littlebro.backends.base import InvalidBackendError
from littlebro import BACKEND_CLASSES

class DummyTracker(BaseTracker):
    """
    Saves tracking events synchronously into either a regular or Mongo DB table.
    Primarily used for testing.
    """
    def __init__(self, *args, **kwargs):
        BaseTracker.__init__(self, *args, **kwargs)
        
    def track_event(self, event, params={}, collection=None):
        try:
            backend = 'littlebro.backends.%s' % BACKEND_CLASSES[self.backend]
            mod_path, cls_name = backend.rsplit('.', 1)
            mod = importlib.import_module(mod_path)
            backend_cls = getattr(mod, cls_name)
        except (AttributeError, ImportError, ValueError, KeyError), e:
            raise InvalidBackendError(
                'Could not find a backend named %s' %  e)
        
        backend = backend_cls()
        backend.save(event, time(), params, collection)