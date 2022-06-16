from src.utils.test import processes
import src.utils.table as table
import src.utils.graph as graph


def run(process):
    """
        Shortest Remaining Time First

    """

    print('running srtf...')

    gantt = []

    # Initialisation
    total_turnaround_time = 0
    total_completion_time = 0
    total_waiting_time = 0
    total_response_time = 0

    n = len(process)
    proc = sorted(process, key=lambda k: k.arrival_time)  # Sorted on the basis of Arrival Time

    li = []
    burst_array = []
    for i in range(n):
        burst_array.append(proc[i].burst_time)

    j = 0  # Tells the index of next process which will get inserted in 'li'
    pre = -1  # Index of the current process which is executed
    pre_comp = 0  # Point of time from where current process is getting executed
    count = 0  # How many process till now have been executed completely
    start = []  # Used to tell whether process with index 'j' had executed earlier or not
    for i in range(n):
        start.append(False)

    while count != n:
        flag = False
        while j < n and total_completion_time >= proc[j].arrival_time:
            flag = True
            li.append([j, proc[j].burst_time])
            j += 1

        if flag:
            li = sorted(li, key=lambda k: k[1])

        elem = li.pop(0)
        index = elem[0]

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

        inside = False
        while elem[1] > 0 and not inside:
            elem[1] -= 1
            total_completion_time += 1
            while j < n and proc[j].arrival_time <= total_completion_time:
                inside = True
                li.append([j, proc[j].burst_time])
                j += 1

        if elem[1] != 0:
            li.append(elem)
        else:
            proc[index].completion_time = total_completion_time
            proc[index].turnaround_time = proc[index].completion_time - proc[index].arrival_time
            proc[index].waiting_time = proc[index].turnaround_time - proc[index].burst_time

            # gantt.append((proc[index].p_id, (total_completion_time, proc[index].burst_time)))
            proc[index].burst_time = 0

            # Updating total
            total_turnaround_time += proc[index].turnaround_time
            total_waiting_time += proc[index].waiting_time

            count += 1

            if count != n and len(li) == 0:
                gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))
                total_completion_time = proc[j].arrival_time
                li.append([j, proc[j].burst_time])
                index = j
                pre = j
                pre_comp = total_completion_time
                j += 1

        li = sorted(li, key=lambda b: b[1])

    if total_completion_time != pre_comp:
        gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))

    for i in range(n):
        proc[i].burst_time = burst_array[i]

    return {
        'name': 'SRTF',
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
