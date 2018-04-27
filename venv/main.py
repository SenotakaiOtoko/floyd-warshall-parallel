import threading
import re
import sys

NUMBER_OF_THREADS = 4

class Graph:
    PLUS_INF = 10 ** 21
    MINES_INF = -10 ** 21

    def __init__(self, path):
        f=open(path, "r")
        matrix = 0

        line = f.readline()
        while line:
            if (not hasattr(self, "nodes_count") and line.upper().find("N=") != -1):
                self.nodes_count = int(line[2:])
                print(self.nodes_count)
                continue
            if (not matrix):
                matrix = line.upper().count("[MATRIX]")
            elif (matrix):
                self.matrix = []
                for i in range(0,self.nodes_count):
                    while (len(line) > 0 and re.match(".*(?:\d+|[NAna]+)+.*", line)):
                        delimiter_index = line.find("\t")
                        edge_length = line[:delimiter_index]
                        if (re.match("\d+", edge_length)):
                            self.matrix.append(int(edge_length))
                        else:
                            self.matrix.append(self.PLUS_INF)
                        line = line[delimiter_index+1:]
                    line = f.readline()
                break
            line = f.readline()
        f.close()
        assert len(self.matrix) == self.nodes_count ** 2
        #print(self.matrix)

class WorkerThread(threading.Thread):
    def __init__(self, thread_idx, graph, graph_lock, rows_per_thread):
        super(WorkerThread, self).__init__()
        self.thread_idx = thread_idx
        self.graph = graph
        self.rows_per_thread = rows_per_thread
        self.graph_lock = graph_lock

    def get_rows(self, k):
        self.k_row = []
        self.graph_lock.acquire(1)
        for i in range(0, self.graph.nodes_count):
            self.k_row.append(self.graph.matrix[k*self.graph.nodes_count + i])
        self.graph_lock.release()

        self.main_rows = []
        right_border = min((self.thread_idx+1)*self.graph.nodes_count*self.rows_per_thread, self.graph.nodes_count**2)
        self.graph_lock.acquire(1)
        print("thread_id:", self.thread_idx)
        for i in range(self.thread_idx*self.graph.nodes_count*self.rows_per_thread, right_border):
            self.main_rows.append(self.graph.matrix[i])
        print(self.main_rows)
        print(len(self.main_rows))
        self.graph_lock.release()
        
    def run(self):
        for i in range(0, self.graph.nodes_count):
            self.get_rows(i)
        """while (1):
            nexturl = self.grab_next_url()
            if nexturl == None: break
            self.retrieve_url(nexturl)"""

    def grab_next_url(self):
        self.url_list_lock.acquire(1)
        if len(self.url_list) < 1:
            nexturl = None
        else:
            nexturl = self.url_list[0]
            del self.url_list[0]
        self.url_list_lock.release()
        return nexturl

    def retrieve_url(self, nexturl):
        text = urlopen(nexturl).read()
        print
        text
        print
        '################### %s #######################' % nexturl


graph=Graph("graphs/3.graph")
graph_lock = threading.Lock()

if (graph.nodes_count < NUMBER_OF_THREADS):
    NUMBER_OF_THREADS = graph.nodes_count
rows_per_thread = int(graph.nodes_count/NUMBER_OF_THREADS)


thread_list = []
for thread_idx in range(0, NUMBER_OF_THREADS):
    new_thread = WorkerThread(thread_idx, graph, graph_lock, rows_per_thread)
    thread_list.append(new_thread)
    new_thread.start()

for thread_idx in range(0, NUMBER_OF_THREADS):
    thread_list[thread_idx].join()



"""
url_list = ['http://linux.org.ru', 'http://kernel.org', 'http://python.org']
url_list_lock = threading.Lock()
workerthreadlist = []
for x in range(0, 3):
    newthread = WorkerThread(url_list, url_list_lock)
    workerthreadlist.append(newthread)
    newthread.start()
for x in range(0, 3):
    workerthreadlist[x].join()
"""