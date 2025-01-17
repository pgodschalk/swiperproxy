# From <http://code.activestate.com/recipes/574454-thread-pool-mixin-class-for-use-with-socketservert/>
# By Michael Palmer, 2008-07-20
# PSF license

# This class creates a Queue where incoming requests are stored. A
# number of threads, defined by 'numThreads' then get requests off of
# this queue and handle them. The original code limited the request
# queue to the number of threads; this limitation has been removed.
from SocketServer import ThreadingMixIn
from Queue import Queue
import threading, socket
import time


class ThreadPoolMixIn(ThreadingMixIn):
    '''
    use a thread pool instead of a new thread on every request
    '''
    allow_reuse_address = True  # seems to fix socket.error on server restart
    last_time = 0
    reqs = {}

    def serve_forever(self, numThreads = 20):
        '''
        Handle one request at a time until doomsday.
        '''
        self.numThreads = numThreads

        # set up the request pool
        self.requests = Queue()

        for x in range(self.numThreads):
            t = threading.Thread(target = self.process_request_thread)
            t.setDaemon(1)
            t.start()

        # server main loop
        while True:
            self.handle_request()

        self.server_close()


    def process_request_thread(self):
        '''
        obtain request from queue instead of directly from server socket
        '''
        while True:
            ThreadingMixIn.process_request_thread(self, *self.requests.get())

    def handle_request(self):
        '''
        simply collect requests and put them on the queue for the workers.
        '''
        try:
            request, client_address = self.get_request()
        except socket.error:
            return

        if self.verify_request(request, client_address):
            self.requests.put((request, client_address))
