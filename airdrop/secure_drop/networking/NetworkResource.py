import threading
from abc import ABC
from typing import List


class NetworkResource(ABC):
    def __init__(self):
        super().__init__()
        self._should_stop: bool = False
        self._should_stop_lock: threading.Lock = threading.Lock()
        self.__threads: List[threading.Thread] = []
        self.__threads_lock: threading.Lock = threading.Lock()

    def start(self):
        with self.__threads_lock:
            for thread in self.__threads:
                thread.start()

    def stop(self):
        with self._should_stop_lock:
            self._should_stop = True
        with self.__threads_lock:
            for thread in self.__threads:
                if thread.is_alive():
                    thread.join()

    def _add_thread(self, thread: threading.Thread):
        with self.__threads_lock:
            self.__threads.append(thread)
