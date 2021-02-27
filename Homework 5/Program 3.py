import time

def timer(func):

    def wrapper(*args, **kwargs):
        start = time.time()
        print("test")
        end = time.time()
        print(end - start)
    return wrapper

@timer
def dec_func(*args, **kwargs):
    print("time")
