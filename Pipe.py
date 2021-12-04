from multiprocessing import Pipe, Event
import threading


class Connection:

    flag = None
    conn = None
    event1 = None
    event2 = None
    callback = None

    def __init__(self, conn, flag, event1, event2):
        self.conn = conn
        self.flag = flag
        self.event1 = event1
        self.event2 = event2

    def send(self, msg):
        self.conn.send(msg)
        if self.flag:
            self.event1.set()
        else:
            self.event2.set()

    def setCallback(self, callback):
        self.callback = callback

    def recv(self):
        return self.conn.recv()

    def receive(self):
        while True:
            if self.flag:
                self.event2.wait()
            else:
                self.event1.wait()
            data = self.conn.recv()
            self.callback(data)

    def startReceive(self):
        t = threading.Thread(target=self.receive)
        t.daemon = True
        t.start()


def PipeImpl() -> tuple[Connection, Connection]:
    _conn1, _conn2 = Pipe()
    event1 = Event()
    event2 = Event()
    conn1 = Connection(_conn1, True, event1, event2)
    conn2 = Connection(_conn2, False, event1, event2)
    return (conn1, conn2)
