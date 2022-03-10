from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Array, Manager

NPHIL = 5
K = 100

class Table():
    def __init__(self, NPHIL, manager):
        self.nphil = manager.list([False]*NPHIL)
        self.neaten = manager.list([0]*NPHIL)
        self.current_phil = None
        #self.eating = Value('i',0)
        self.mutex = Lock()
        self.freefork = Condition(self.mutex)
        
    def wants_eat(self):
        self.mutex.acquire()
        self.freefork.wait_for(self.freefork_condition)
        self.nphil[self.current_phil] = True
        self.neaten[self.current_phil] += 1
        #self.eating.value += 1
        self.mutex.release()
        
        
    def wants_think(self):
        self.mutex.acquire()
        self.nphil[self.current_phil] = False
        #self.eating.value -= 1
        self.freefork.notify_all()
        self.mutex.release()
        
        
    def freefork_condition(self):
        return (not self.nphil[(self.current_phil-1)%NPHIL]) and (not self.nphil[(self.current_phil+1)%NPHIL])
        
       
    def set_current_phil(self, index):
        self.mutex.acquire()
        self.current_phil = index
        self.mutex.release()
        

def philosopher_task(num:int, table: Table):
    table.set_current_phil(num)
    for i in range(K):
        print (f"Philosofer {num} thinking")
        print (f"Philosofer {num} wants to eat")
        table.wants_eat()
        print (f"Philosofer {num} eating")
        table.wants_think()
        print (f"Philosofer {num} stops eating")
        
def main():
    manager = Manager()
    table = Table(NPHIL, manager)
    philosofers = [Process(target=philosopher_task, args=(i,table)) \
                   for i in range(NPHIL)]
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()
    for i in range(NPHIL):
    	print(f"philosopher {i} has eaten {table.neaten[i]} times")
if __name__ == '__main__':
    main()
