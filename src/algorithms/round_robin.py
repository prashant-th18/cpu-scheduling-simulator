from src.utils.test import processes
import src.utils.table as table
import src.utils.graph as graph


def run(process, quantum=3):
    """
        Round Robin

    """

    print('running round robin...')

    gantt = []

    # Initialisation
    total_turnaround_time = 0
    total_completion_time = 0
    total_waiting_time = 0
    total_response_time = 0

    n = len(process)

    proc = sorted(processes, key=lambda l: l.arrival_time)

    queue = []
    burst_array = []
    for i in range(n):
        burst_array.append(proc[i].burst_time)

    j = 1  # Tells the index of next process which will get inserted in 'queue'
    pre = -1  # Index of the current process which is executed
    pre_comp = 0  # Point of time from where current process is getting executed
    count = 0  # How many process till now have been executed completely
    start = []  # Used to tell whether process with index 'j' had executed earlier or not
    for i in range(n):
        start.append(False)

    queue.append([0, proc[0].burst_time])

    while count != n:

        cur_elem = queue.pop(0)  # First element retrieved and popped
        index = cur_elem[0]

        if pre != -1 and pre != index:
            gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))
            pre_comp = total_completion_time
            pre = index
        elif pre == -1:
            pre = index
            pre_comp = total_completion_time

        if not start[index]:
            start[index] = True
            # Response Time
            proc[index].response_time = total_completion_time - proc[index].arrival_time
            total_response_time += proc[index].response_time

        cur_burst = cur_elem[1]
        for i in range(min(cur_burst, quantum)):
            total_completion_time += 1
            while j < n and proc[j].arrival_time <= total_completion_time:
                queue.append([j, proc[j].burst_time])
                j += 1

        cur_burst -= min(cur_burst, quantum)
        if cur_burst == 0:
            proc[index].completion_time = total_completion_time
            proc[index].turnaround_time = proc[index].completion_time - proc[index].arrival_time
            proc[index].waiting_time = proc[index].turnaround_time - proc[index].burst_time

            # gantt.append((proc[index].p_id, (total_completion_time, proc[index].burst_time)))
            proc[index].burst_time = 0

            # Updating total
            total_turnaround_time += proc[index].turnaround_time
            total_waiting_time += proc[index].waiting_time

            count += 1

            if count != n and len(queue) == 0:
                gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))
                total_completion_time = proc[j].arrival_time
                queue.append([j, proc[j].burst_time])
                index = j
                pre = j
                pre_comp = total_completion_time
                j += 1
        else:
            queue.append([index, cur_burst])

    if total_completion_time != pre_comp:
        gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))

    for i in range(n):
        proc[i].burst_time = burst_array[i]

    return {
        'name': 'ROUND-RB',
        'avg_turnaround_time': total_turnaround_time / len(process),
        'avg_waiting_time': total_waiting_time / len(process),
        'avg_response_time': total_response_time / len(process),
        'processes': proc,
        'gantt': gantt
    }

def main():

    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    print("Avg Turnaround Time: {}".format(result['avg_turnaround_time']))
    print("Avg Response Time: {}".format(result['avg_response_time']))
    table.plot(result['processes'])
    graph.plot_gantt(result)


if __name__ == '__main__':
    main()