from src.utils.test import processes
import src.utils.table as table
import src.utils.graph as graph


def run(process):
    """
        Priority Scheduling (Preemptive)

    """

    print('running priority preemptive...')

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
    j = 0
    pre = -1
    pre_comp = 0
    count = 0  # How many process till now have been executed completely
    start = []  # Used to tell whether process wil index 'j' had executed earlier or not
    for i in range(n):
        start.append(False)

    while count < n:
        flag = False
        while j < n and total_completion_time >= proc[j].arrival_time:
            flag = True
            # print(j, proc[j].__dict__)
            li.append([j, [proc[j].priority, proc[j].burst_time]])
            j += 1

        # print(li)

        if flag == True:
            li = sorted(li, key=lambda k: k[1][0])

        index = li[0][0]

        # print(total_completion_time, li)
        if pre != -1 and pre != index:
            gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))
            pre_comp = total_completion_time
            pre = index
        elif pre == -1:
            pre = index
            pre_comp = total_completion_time

        if start[index] == False:
            start[index] = True
            # Response Time
            proc[index].response_time = total_completion_time - proc[index].arrival_time
            total_response_time += proc[index].response_time

        # Check whether this index process will be executed fully first and then a new process will come
        # or, in between a new process will come
        fully = False
        if j == n:
            fully = True
        else:
            t1 = proc[j].arrival_time - total_completion_time
            t2 = proc[index].burst_time
            if t2 <= t1:
                fully = True

        if fully == True:
            # Process with index 'index' will be executed fully
            proc[index].completion_time = total_completion_time + proc[index].burst_time
            proc[index].turnaround_time = proc[index].completion_time - proc[index].arrival_time
            proc[index].waiting_time = proc[index].turnaround_time - proc[index].burst_time

            # gantt.append((proc[index].p_id, (total_completion_time, proc[index].burst_time)))
            proc[index].burst_time = 0

            # Updating total
            total_completion_time = proc[index].completion_time
            total_turnaround_time += proc[index].turnaround_time
            total_waiting_time += proc[index].waiting_time

            li.pop(0)  # First element popped
            count += 1  # A process fully executed
            if count != n:
                if len(li) == 0:
                    total_completion_time = proc[j].arrival_time

        else:
            # Find how much it will run
            how_much = proc[j].arrival_time - total_completion_time
            # remaining = proc[j].burst_time - how_much

            proc[index].burst_time -= how_much

            li[0][1][1] = proc[index].burst_time

            # Updating total
            total_completion_time += how_much

    if total_completion_time != pre_comp:
        gantt.append((proc[pre].p_id, (pre_comp, total_completion_time - pre_comp)))

    for i in range(n):
        proc[i].burst_time = burst_array[i]

    return {
        'name': 'PR-P',
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
