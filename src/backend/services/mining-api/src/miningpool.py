import queue
import threading
import time


class MiningPool:
    DEQUEUE_TIME = 2

    def __init__(self, receiver, ready_to_mine):
        self._pool = queue.Queue()
        self._mining_thread = threading.Thread(
            target=self.send_to_mine, kwargs={"self": self, "receiver": receiver}
        )
        self._mining_thread.daemon = True

        self._send = threading.Condition()
        self._ready_to_mine = ready_to_mine

    def add_to_pool(self, data):
        self._pool.put(data)

    def start_thread(self):
        self._mining_thread.start()

    def send_to_mine(*args, **kwargs):
        self = kwargs["self"]
        receiver = kwargs["receiver"]

        while True:
            try:
                if not self._pool.empty():
                    last_transaction = self._pool.get()

                    with self._send:
                        while not self._ready_to_mine:
                            self._send.wait()

                        self._ready_to_mine = False
                    receiver(last_transaction)

            except Exception as e:
                print("Receiver produced an error", str(e))

            finally:
                time.sleep(MiningPool.DEQUEUE_TIME)

    def ready_to_mine(self):
        with self._send:
            self._ready_to_mine = True
            self._send.notify_all()
