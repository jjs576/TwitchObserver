import finder
import IRCClient
from multiprocessing import Process, Lock, Queue
import threading

from utils import *
import time

def thread_finder_finduser(input_lock, output_lock, input_queue, output_queue, finder):
    while True:
        streamer_name = ''
        
        input_lock.acquire()
        if not input_queue.empty():
            streamer_name = input_queue.get()
            input_lock.release()
        else:
            input_lock.release()
            break
        
        try:  
            isFound = finder.FindUser(streamer_name)
        except TypeError:
            print_log('(Thread) TypeError')
            input_lock.acquire()
            input_queue.put(streamer_name)
            input_lock.release()

            
        if isFound:
            output_lock.acquire()
            output_queue.put(streamer_name)
            output_lock.release()


def process_finder(lock, channel_queue, target, update_time):
    f = finder.Finder(target)
    
    while True:
        f.RefreshList()
        input_channel_queue = Queue()
        output_channel_queue = Queue()
        input_lock = threading.Lock()
        output_lock = threading.Lock()
        
        for s in f.streamer:
            input_channel_queue.put(s.user_name)
            
        threads = []
        for i in range(10):
            t = threading.Thread(target=thread_finder_finduser, args=(input_lock,output_lock,input_channel_queue,output_channel_queue,f,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
            
        result = []
        while not output_channel_queue.empty():
            result.append(output_channel_queue.get())
        
        resultString = ''
        for r in result:
            resultString = resultString + r + ', '
        resultString = resultString[:-2]
        print_log(f.module_name + ' joined channels : ' + resultString)
        write_log(target, f.module_name + ' joined channels : ' + resultString)

        result.append(target)
        
        channel_queue.put(result)
        time.sleep(update_time)



def process_IRCClient(lock, channel_queue,target):
    i = IRCClient.IRCClient(target)
    i.connect()

    while True:
        if not channel_queue.empty():
            queue_data = channel_queue.get()
            i.join_and_part(queue_data)

        if i.joined:
            i.read_process()
        time.sleep(0.2)
    
    
def run(target, update_time):
    queue = Queue()
    lock = Lock()
    
    procs = []
    
    proc_f = Process(target=process_finder, args=(lock, queue, target, update_time,))
    procs.append(proc_f)
    
    proc_i = Process(target=process_IRCClient, args=(lock, queue, target,))
    procs.append(proc_i)

    for p in procs:
        p.start()
