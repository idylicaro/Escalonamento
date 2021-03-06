def sort_func_by_time(e):
    return e.time_process


def sort_func_by_priority(e):
    return e.priority


def sort_func_by_period(e):
    return e.period


class Task:
    def __init__(self, period, time_process, arrival, name, quantum=None, priority=None):
        self.period = period
        self.time_process = time_process
        self.arrival = arrival
        self.name = name
        self.quantum = quantum
        self.quantum_execute_cycle_time = 0
        self.priority = priority

    def execute(self):
        self.time_process -= 1
        if self.quantum is not None:
            self.quantum_execute_cycle_time += 1


class EscalatorSRTN:
    def __init__(self, static_tasks, X):
        self.tasks: [Task] = []
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = None

    def execute(self):
        print("\n ================\n SRTN \n ================ \n")
        for i in range(0, self.total_time, 1):
            if self.current_task and self.current_task.time_process >= 0:
                print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i,
                                                                 self.current_task.time_process))
            self.kill_task()
            self.verify_arrival(i)
            self.preempt()
            self.current_task.execute()

    def preempt(self):
        if len(self.tasks) != 0:
            self.tasks.sort(key=sort_func_by_time)
            self.current_task = self.tasks[0]

    def kill_task(self):
        if len(self.tasks) != 0:
            for task in self.tasks:
                if task.time_process == 0:
                    self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if task.arrival == current_time:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time)))
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time)))


class EscalatorRR:
    def __init__(self, static_tasks, X):
        self.tasks: [Task] = []
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = None

    def execute(self):
        print("\n ================\n ROUND ROBIN \n ================ \n")
        for i in range(0, self.total_time, 1):
            if self.current_task and self.current_task.time_process >= 0:
                print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i,
                                                                 self.current_task.time_process))

            self.kill_task()
            self.verify_arrival(i)
            if len(self.tasks) != 0:
                self.current_task = self.tasks[0]
            self.preempt()
            if self.current_task is not None:
                self.current_task.execute()

    def preempt(self):
        if len(self.tasks) != 0:
            if self.current_task.quantum_execute_cycle_time == self.current_task.quantum:
                self.tasks[0].quantum_execute_cycle_time = 0
                self.tasks.append(self.tasks.pop(0))
                self.current_task = self.tasks[0]

    def kill_task(self):
        if len(self.tasks) != 0:
            for task in self.tasks:
                if task.time_process == 0:
                    self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if task.arrival == current_time:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum))
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum))


class EscalatorPriority:
    def __init__(self, static_tasks, X):
        self.tasks: [Task] = []
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = None

    def execute(self):
        print("\n================\n Priority scheduler \n================\n")
        for i in range(0, self.total_time, 1):
            if self.current_task and self.current_task.time_process >= 0:
                print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i,
                                                                 self.current_task.time_process))

            self.kill_task()
            self.verify_arrival(i)
            if len(self.tasks) != 0:
                self.current_task = self.tasks[0]
            self.preempt()
            if self.current_task is not None:
                self.current_task.execute()

    def preempt(self):
        if len(self.tasks) != 0:
            self.tasks.sort(key=sort_func_by_priority)
            self.current_task = self.tasks[0]

    def kill_task(self):
        if len(self.tasks) != 0:
            for task in self.tasks:
                if task.time_process == 0:
                    self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if task.arrival == current_time:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum, task.priority))
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum, task.priority))


class EscalatorMotonic:
    def __init__(self, static_tasks, X):
        self.tasks: [Task] = []
        self.static_tasks: [Task] = static_tasks
        self.total_time = X
        self.current_task: Task = None

    def execute(self):
        print("\n================\n Motonic scheduler \n================\n")
        for i in range(0, self.total_time, 1):
            if self.current_task and self.current_task.time_process >= 0:
                print("Task: {} || Time: {} || Value: {}".format(self.current_task.name, i,
                                                                 self.current_task.time_process))

            self.kill_task()
            self.verify_arrival(i)
            if len(self.tasks) != 0:
                self.current_task = self.tasks[0]
            self.preempt()
            if self.current_task is not None:
                self.current_task.execute()

    def preempt(self):
        if len(self.tasks) != 0:
            self.tasks.sort(key=sort_func_by_period)
            self.current_task = self.tasks[0]

    def kill_task(self):
        if len(self.tasks) != 0:
            for task in self.tasks:
                if task.time_process == 0:
                    self.tasks.remove(task)

    def verify_arrival(self, current_time):
        for task in self.static_tasks:
            if task.arrival == current_time:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum, task.priority))
            if (current_time % task.period) == 0 and current_time != 0:
                self.tasks.append(
                    Task(task.period, task.time_process, task.arrival, task.name + "-{}".format(current_time),
                         task.quantum, task.priority))


def main():
    X = int(input('Qual a dura????o: '))

    tasks = []  # [Task(10, 4, 0, 'A', 5), Task(20, 8, 0, 'B', 5), Task(30, 12, 0, 'C', 5)]
    static_tasks = [Task(10, 4, 0, 'A', 5), Task(20, 8, 0, 'B', 5), Task(30, 12, 0, 'C', 5)]

    # SRTN
    # escalator = EscalatorSRTN(static_tasks, X)
    # escalator.execute()
    # ROUND ROBIN
    # escalator = EscalatorRR(
    #     [Task(10, 4, 0, 'A', 5, 0), Task(20, 8, 0, 'B', 5, 5), Task(30, 12, 0, 'C', 5, 10)], 101)
    # escalator.execute()
    # Priority
    # escalator = EscalatorPriority(
    #     [Task(3, 1, 0, 'A', 5, 2), Task(6, 3, 0, 'B', 5, 1), Task(9, 5, 0, 'C', 5, 0), Task(15, 8, 0, 'D', 5, 3)], 31)
    # escalator.execute()
    escalator = EscalatorMotonic(
         [Task(100, 20, 0, 'A', 5, 2), Task(150, 40, 0, 'B', 5, 1), Task(350, 100, 0, 'C', 5, 0)], 361)
    escalator.execute()

if __name__ == "__main__":
    main()
