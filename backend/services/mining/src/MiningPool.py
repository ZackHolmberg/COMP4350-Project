import threading
import time

class MiningPool:
    DEQUEUE_TIME = 5

    def __init__ (self, receiver):
        self._pool = []
        self._lock = threading.Lock()
        self._mining_thread = threading.Thread(target=self.sendToMine, kwargs={'self': self, 'receiver': receiver})
        self._mining_thread.daemon = True
    

    def addToPool(self, data):
        self._lock.acquire()
        self._pool.append(data)
        self._lock.release()

    def start_thread(self):
        self._mining_thread.start()


    def sendToMine(*args, **kwargs):
        self = kwargs["self"]
        receiver = kwargs["receiver"]

        while True:
            print("Thread called ")

            try:
                if len(self._pool) > 0:
                    self._lock.acquire()
                    last_transaction = self._pool.pop()
                    self._lock.release()
                    
                    receiver(last_transaction)

            except Exception as e:
                print("Receiver produced an error")
                
            finally:
                time.sleep(MiningPool.DEQUEUE_TIME)

    
