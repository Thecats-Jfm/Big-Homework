#这里要作为一个自动机的核心
import threading
import time
from functools import wraps
def A():
    pass
def B():
    pass
def C():
    pass
INITIAL_STATE_ID = 0
DEBUG = True

def log(func):
    @wraps(func)
    def wrapper():
        print("Start of %s."%func.__name__)
        func()
        print("End of %s."%func.__name__)
    return wrapper
def StandBy():
    global state_id
    state_id = int(input())


state={0:StandBy,1:A,2:B,3:C}
state_id = INITIAL_STATE_ID
while __name__ == "__main__":
    now_state = state[state_id]
    if(state_id==-1):
        print('exit')
        exit
    if(DEBUG):
        now_state = log(now_state)
    thread_local = threading.Thread(target=now_state)
    thread_local.start()
    thread_local.join()
    print("Next:",state_id)
