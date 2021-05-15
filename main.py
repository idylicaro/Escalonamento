def sort_func(e):
    return e.time_process

class Task:
    def __init__(self, periodo, time_process, arrival, name):
        self.periodo = periodo
        self.time_process = time_process
        self.arrival = arrival
        self.name = name
    
    def execute(self, time):
        self.time_process -= time
    

    
        

class Escalator:
    def __init__(self, tasks, static_tasks, X):
      self.tasks:[Task] = tasks
      self.static_tasks:[Task] = static_tasks
      self.total_time = X
      self.current_task: Task = self.tasks[0]

    def execute(self):
        for i in range(0,self.total_time):
            print("Task: {} || Time: {}".format(self.current_task.name, i))
            self.kill_task()
            self.verify_arrival(i)
            self.preempt()
            self.current_task.execute(i)
            self.tasks.sort(key=sort_func)

    def preempt(self):
        if self.current_task.time_process > 0:
            self.tasks.append(self.current_task)
        self.tasks.sort(key=sort_func)
        self.current_task = self.tasks[0]         

    def kill_task(self):
        for task in self.tasks:
            if task.time_process == 0:
                self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if task.periodo == current_time:
                self.tasks.append(task)


def main():
  
  X = int(input('Qual a duração: '))
  tasks = [Task(10,4,0,'A'),Task(20,8,0,'B'),Task(30,12,0,'C')]
  #preenchendo lista com o processo adicionado pelo usuário
  escalator = Escalator(tasks,tasks,X)
  escalator.execute()
   
if __name__ == "__main__":
    main()