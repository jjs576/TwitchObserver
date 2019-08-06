import time

folder = './log/'

def print_log(message):
    t = time.strftime('[%Y/%m/%d %H:%M:%S] ', time.localtime(time.time()))
    print(t + message)

def write_log(user_name,message):
    t = time.localtime(time.time())
    file_date = time.strftime('%Y%m%d_',t)
    message_date = time.strftime('[%Y/%m/%d %H:%M:%S] ', t)
    
    f= open(folder + file_date + user_name + '.txt','a')
    f.write(message_date + message + '\n')
    f.close()

def binary_search(arr, value):
    low = 0
    high = len(arr)-1
    while (low <= high):
        mid = (low+high)//2
        
        if arr[mid] > value:
            high = mid - 1
        elif arr[mid] < value:
            low = mid + 1
        else:
            return mid
    return -1

def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args,**kwargs)
        end_time = time.time()
        print('WorkingTime[{0}] : {1:0.2f} sec'.format(original_fn.__name__, end_time - start_time))
        return result
    return wrapper_fn

