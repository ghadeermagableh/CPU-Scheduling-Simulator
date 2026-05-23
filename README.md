# CPU Scheduling Simulator and Analysis

**Course:** Operating Systems (Project 1)  

---

## 1. Algorithms and Tie-Breaking Rules

This simulator implements four fundamental CPU scheduling algorithms. To ensure deterministic results and handle edge cases where multiple processes are eligible, the following rules are applied.

### Algorithms Implemented

| Algorithm | Type | Description |
|---|---|---|
| **FCFS** (First-Come First-Served) | Non-preemptive | Allocates CPU in order of arrival |
| **SJF** (Shortest Job First) | Non-preemptive | Selects process with smallest burst time |
| **Priority Scheduling** | Non-preemptive | Selects process with highest priority (lowest number) |
| **Round Robin (RR)** | Preemptive | Fixed time quantum q=2; unfinished processes go to back of queue |

### Tie-Breaking Rules

- **SJF:** Smallest Burst Time → Smallest Arrival Time → Smallest PID
- **Priority:** Lowest Priority Value → Smallest Arrival Time → Smallest PID
- **Idle Periods:** If no process is in the ready queue, CPU stays IDLE until next arrival
- **Ready Queue (RR):** FIFO queue — newly arrived processes are appended as they arrive

---

## 2. Outputs for Dataset A

### Gantt Charts

FCFS:     0-7 P1 | 7-11 P2 | 11-12 P3 | 12-16 P4 | 16-19 P5
SJF:      0-7 P1 | 7-8 P3  | 8-11 P5  | 11-15 P2 | 15-19 P4
Priority: 0-7 P1 | 7-11 P2 | 11-14 P5 | 14-18 P4 | 18-19 P3
RR (q=2): 0-2 P1 | 2-4 P2  | 4-6 P1   | 6-7 P3   | 7-9 P2  | 9-11 P4 | 11-13 P5 | 13-15 P1 | 15-17 P4 | 17-18 P5 | 18-19 P1

### Average Metrics — Dataset A

| Algorithm | Avg Wait Time (WT) | Avg Turnaround Time (TAT) | Avg Response Time (RT) |
|---|---|---|---|
| FCFS | 5.80 | 9.60 | 5.80 |
| SJF | 4.80 | 8.60 | 4.80 |
| Priority | 6.60 | 10.40 | 6.60 |
| RR (q=2) | 6.80 | 10.60 | 2.20 |

---

## 3. Outputs for Dataset B

### Gantt Charts

FCFS:     0-20 P1 | 20-22 P2 | 22-23 P3 | 23-26 P4 | 26-28 P5 | 28-29 P6
SJF:      0-20 P1 | 20-21 P3 | 21-22 P6 | 22-24 P2 | 24-26 P5 | 26-29 P4
Priority: 0-20 P1 | 20-22 P2 | 22-25 P4 | 25-26 P6 | 26-27 P3 | 27-29 P5
RR (q=2): 0-2 P1  | 2-4 P2   | 4-5 P3   | 5-7 P1   | 7-9 P4   | 9-11 P5 | 11-12 P6 | 12-14 P1 | 14-15 P4 | ... | 27-29 P1
### Average Metrics — Dataset B

| Algorithm | Avg Wait Time (WT) | Avg Turnaround Time (TAT) | Avg Response Time (RT) |
|---|---|---|---|
| FCFS | 17.17 | 22.00 | 17.17 |
| SJF | 16.17 | 21.00 | 16.17 |
| Priority | 17.33 | 22.17 | 17.33 |
| RR (q=2) | **5.17** | **10.00** | **2.83** |

---

## 4. Comparison and Reflection

The analysis of both datasets reveals distinct performance trade-offs between the scheduling policies.

**Dataset A (mixed arrivals):** SJF proved the most efficient by minimizing average waiting time (4.80) and turnaround time (8.60). However, Round Robin provided the best responsiveness with an average response time of 2.20.

**Dataset B (stress test):** The results highlight the **convoy effect** in non-preemptive algorithms. Because P1 has a long burst time of 20, it forces all subsequent short jobs to wait — resulting in high average wait times of approximately 16–17. Round Robin (q=2) effectively mitigated this by preempting P1, allowing short jobs to finish significantly earlier and reducing average wait time to **5.17**.

> **Key takeaway:** SJF is optimal for throughput. Round Robin is essential for fairness and interactive responsiveness in systems with high-variance workloads.
