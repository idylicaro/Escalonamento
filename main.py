def sort_func(e):
    return e.time_process


class Task:
    def __init__(self, period, time_process, arrival, name, quantum=None):
        self.period = period
        self.time_process = time_process
        self.arrival = arrival
        self.name = name
        self.quantum = quantum
        self.quantum_execute_cycle_time = 0

    def execute(self):
        self.time_process -= 1
        if self.quantum is not None:
            self.quantum_execute_cycle_time += 1


class EscalatorSRTN:
    def __init__(self, tasks, static_tasks, X):
        self.tasks: [Task] = tasks
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = self.tasks[0]

    def execute(self):
        for i in range(0, self.total_time, 1):
            print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i, self.current_task.time_process))
            self.kill_task()
            self.verify_arrival(i)
            self.preempt()
            self.current_task.execute()
            self.tasks.sort(key=sort_func)

    def preempt(self):
        self.tasks.sort(key=sort_func)
        self.current_task = self.tasks[0]

    def kill_task(self):
        for task in self.tasks:
            if task.time_process == 0:
                self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time)))


class EscalatorRR:
    def __init__(self, tasks, static_tasks, X):
        self.tasks: [Task] = tasks
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = self.tasks[0]

    def execute(self):
        for i in range(0, self.total_time, 1):
            print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i, self.current_task.time_process))
            self.kill_task()
            self.current_task = self.tasks[0]
            self.preempt()
            self.verify_arrival(i)
            self.current_task.execute()

    def preempt(self):
        if self.current_task.quantum_execute_cycle_time == self.current_task.quantum:
            self.tasks.append(self.tasks.pop(0))
            self.current_task = self.tasks[0]

    def kill_task(self):
        for task in self.tasks:
            if task.time_process == 0:
                self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum))


def main():
    X = int(input('Qual a duração: '))

    tasks = [Task(10, 4, 0, 'A', 5), Task(20, 8, 0, 'B', 5), Task(30, 12, 0, 'C', 5)]
    static_tasks = [Task(10, 4, 0, 'A', 5), Task(20, 8, 0, 'B', 5), Task(30, 12, 0, 'C', 5)]

    # SRTN
    # escalator = EscalatorSRTN(tasks, static_tasks, X)
    # escalator.execute()
    # ROUND ROBIN
    escalator = EscalatorRR(tasks, static_tasks, X)
    escalator.execute()


if __name__ == "__main__":
    main()
