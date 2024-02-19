import uuid
import threading
from concurrent.futures import ThreadPoolExecutor

class WindowExecutor(ThreadPoolExecutor):
    def __init__(self, max_workers: int, logging = False):
        super().__init__(max_workers)
        self.lock = threading.Lock()
        self.futures = []
        self.logging = logging

    def log(self, *args):
        if self.logging: print(*args)

    def submit(self, fn, *args, **kwargs):
        with self.lock:
            id = uuid.uuid4().hex[:2]

            if len(self.futures) >= self._max_workers:
                #Max workers, discard first cancellable future
                for fut in self.futures:
                    if fut.cancel(): 
                        self.log("Cancelled:", fut.id)
                        fut.discard()
                    else:
                        self.log("Failed cancel:", fut.id)

            future = super().submit(fn, *[*args, id], **kwargs)
            discard = lambda f: f in self.futures and self.futures.remove(future)
            setattr(future,'id', id)
            setattr(future,'discard', lambda: discard(future))

            self.log("Added", future.id)

            future.add_done_callback(discard)
            self.futures.append(future)
            
            self.log([f'{f.id}' for f in self.futures], self._work_queue.qsize())

            return future