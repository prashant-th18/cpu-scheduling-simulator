from src.utils.test import processes
import src.utils.table as table
import src.utils.graph as graph


def run(processes):
    """
        First Come First Serve

    """
    print("running fcfs...")

    gantt = []  # Empty Array

    # Initialisation
    total_turnaround_time = 0
    total_completion_time = 0
    total_waiting_time = 0
    total_response_time = 0

    proc = sorted(processes, key=lambda proc: proc.arrival_time)  # Sorted on the basis of Arrival Time
    print(proc)

    # Calculating info about all processes
    for i in range(len(proc)):
        # Calculate for each
        proc[i].completion_time = total_completion_time + proc[i].burst_time
        proc[i].turnaround_time = proc[i].completion_time - proc[i].arrival_time
        proc[i].waiting_time = proc[i].turnaround_time - proc[i].burst_time
        proc[i].response_time = max(0, total_completion_time - proc[i].arrival_time)

        gantt.append((proc[i].p_id, (total_completion_time, proc[i].burst_time)))
        # Appende a Tuple of 'id' and tuple of 'total_completion_time' and 'burst time'

        # Update total
        total_completion_time += proc[i].burst_time
        total_turnaround_time += proc[i].turnaround_time
        total_waiting_time += proc[i].waiting_time
        total_response_time += proc[i].response_time

    return {
        'name': 'FCFS',
        'avg_turnaround_time': total_turnaround_time / len(proc),
        'avg_waiting_time': total_waiting_time / len(proc),
        'avg_response_time': total_response_time / len(proc),
        'processes': proc,
        'gantt': gantt
    }


# If this file is executed directly -> run temporary test-cases
def main():
    result = run(processes)
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    print("Avg Waiting Time: {}".format(result['avg_waiting_time']))
    table.plot(result['processes'])
    graph.plot_gantt(result)


if __name__ == '__main__':
    main()
