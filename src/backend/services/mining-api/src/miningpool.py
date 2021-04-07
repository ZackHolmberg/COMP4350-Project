"""a module that contains a class to handle mining requests via a queue"""
import threading
import time
import queue

class MiningPool:
    """
    A class that implements a queue of transactions that are to be mined and two threads.
    the main thread listens for any transaction that is to be put in the mining queuen and
    the worker thread sends the top transaction from the mining queue to be mined.
    """
    DEQUEUE_TIME = 2

    def __init__ (self, receiver, ready_to_mine):
        self._pool = queue.Queue()
        self._mining_thread = threading.Thread(target=self.send_to_mine,\
            kwargs={'self': self, 'receiver': receiver})
        self._mining_thread.daemon = True

        self._send = threading.Condition()
        self._ready_to_mine = ready_to_mine

    def add_to_pool(self, data):
        """
        Adds a transaction to the mining queue

        params:
            data: data to be added to the mining pool
        Returns:
            N/A
        """
        self._pool.put(data)

    def start_thread(self):
        """
        Starts the mining thread

        params:
            N/A
        Returns:
            N/A
        """
        self._mining_thread.start()


    def send_to_mine(*args, **kwargs):
        """
        A method executed in the worker thread to send the top transaction
        from the mining queue to be mined if the pool is not empty

        params:
            self: the caller class instance
            reciever: A method that sends the a transaction to be mined
                      to all the connected clients.

        Returns:
            N/A
        """
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

            except Exception as error:
                print("Receiver produced an error", str(error))

            finally:
                time.sleep(MiningPool.DEQUEUE_TIME)

    def ready_to_mine(self):
        """
        A method to indicate that a transaction is ready to be mined based on the
        worker thread's condition variable.
        """
        with self._send:
            self._ready_to_mine = True
            self._send.notify_all()
