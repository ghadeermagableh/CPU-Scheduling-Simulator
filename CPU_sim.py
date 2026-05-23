"""
CPU Scheduling Simulator
Algorithms: FCFS, SJF (non-preemptive), Priority (non-preemptive), Round Robin (preemptive)
Tie-breaking: SJF -> smallest BT, then AT, then PID
              Priority -> lowest value, then AT, then PID
              RR -> FIFO queue; new arrivals appended as they arrive
"""

from collections import deque


# ─────────────────────────────────────────────────────────────
#  Data helpers
# ─────────────────────────────────────────────────────────────

def make_process(pid, at, bt, priority):
    return {"pid": pid, "at": at, "bt": bt, "priority": priority}

def compute_metrics(pid, at, bt, ct, first_start):
    tat = ct - at
    wt  = tat - bt
    rt  = first_start - at
    return {"pid": pid, "at": at, "bt": bt, "CT": ct, "TAT": tat, "WT": wt, "RT": rt}


# ─────────────────────────────────────────────────────────────
#  Output helpers
# ─────────────────────────────────────────────────────────────

def print_gantt(timeline):
    print("\nGantt Chart:")
    parts = []
    for (start, end, label) in timeline:
        parts.append(f"{start}-{end} {label}")
    print("  " + " | ".join(parts))

def print_table(metrics):
    print(f"\n{'PID':<6}{'AT':<6}{'BT':<6}{'CT':<6}{'TAT':<6}{'WT':<6}{'RT':<6}")
    print("-" * 42)
    for m in metrics:
        print(f"{m['pid']:<6}{m['at']:<6}{m['bt']:<6}{m['CT']:<6}{m['TAT']:<6}{m['WT']:<6}{m['RT']:<6}")

def print_averages(metrics):
    n = len(metrics)
    avg_wt  = sum(m["WT"]  for m in metrics) / n
    avg_tat = sum(m["TAT"] for m in metrics) / n
    avg_rt  = sum(m["RT"]  for m in metrics) / n
    print(f"\nAverages  →  WT: {avg_wt:.2f}  |  TAT: {avg_tat:.2f}  |  RT: {avg_rt:.2f}")


# ─────────────────────────────────────────────────────────────
#  FCFS
# ─────────────────────────────────────────────────────────────

def fcfs(processes):
    procs = sorted(processes, key=lambda p: (p["at"], p["pid"]))
    time, timeline, metrics = 0, [], []

    for p in procs:
        if time < p["at"]:
            timeline.append((time, p["at"], "IDLE"))
            time = p["at"]
        first_start = time
        time += p["bt"]
        timeline.append((first_start, time, p["pid"]))
        metrics.append(compute_metrics(p["pid"], p["at"], p["bt"], time, first_start))

    return timeline, metrics


# ─────────────────────────────────────────────────────────────
#  SJF non-preemptive
# ─────────────────────────────────────────────────────────────

def sjf(processes):
    remaining = sorted(processes, key=lambda p: p["at"])
    time, timeline, metrics = 0, [], []

    while remaining:
        available = [p for p in remaining if p["at"] <= time]
        if not available:
            next_arrival = min(p["at"] for p in remaining)
            timeline.append((time, next_arrival, "IDLE"))
            time = next_arrival
            available = [p for p in remaining if p["at"] <= time]

        # Tie-breaking: smallest BT, then AT, then PID
        chosen = min(available, key=lambda p: (p["bt"], p["at"], p["pid"]))
        remaining.remove(chosen)
        first_start = time
        time += chosen["bt"]
        timeline.append((first_start, time, chosen["pid"]))
        metrics.append(compute_metrics(chosen["pid"], chosen["at"], chosen["bt"], time, first_start))

    return timeline, metrics


# ─────────────────────────────────────────────────────────────
#  Priority non-preemptive
# ─────────────────────────────────────────────────────────────

def priority_scheduling(processes):
    remaining = sorted(processes, key=lambda p: p["at"])
    time, timeline, metrics = 0, [], []

    while remaining:
        available = [p for p in remaining if p["at"] <= time]
        if not available:
            next_arrival = min(p["at"] for p in remaining)
            timeline.append((time, next_arrival, "IDLE"))
            time = next_arrival
            available = [p for p in remaining if p["at"] <= time]

        # Tie-breaking: lowest priority number, then AT, then PID
        chosen = min(available, key=lambda p: (p["priority"], p["at"], p["pid"]))
        remaining.remove(chosen)
        first_start = time
        time += chosen["bt"]
        timeline.append((first_start, time, chosen["pid"]))
        metrics.append(compute_metrics(chosen["pid"], chosen["at"], chosen["bt"], time, first_start))

    return timeline, metrics


# ─────────────────────────────────────────────────────────────
#  Round Robin preemptive
# ─────────────────────────────────────────────────────────────

def round_robin(processes, quantum=2):
    procs = sorted(processes, key=lambda p: (p["at"], p["pid"]))
    remaining_bt = {p["pid"]: p["bt"] for p in procs}
    first_start   = {}
    ct             = {}

    queue   = deque()
    time    = 0
    arrived = set()
    timeline = []
    idx     = 0   # pointer into sorted arrival list

    # Enqueue all processes that arrive at time 0
    while idx < len(procs) and procs[idx]["at"] <= time:
        queue.append(procs[idx])
        arrived.add(procs[idx]["pid"])
        idx += 1

    while queue or idx < len(procs):
        if not queue:
            # CPU idle: jump to next arrival
            next_arr = procs[idx]["at"]
            timeline.append((time, next_arr, "IDLE"))
            time = next_arr
            while idx < len(procs) and procs[idx]["at"] <= time:
                queue.append(procs[idx])
                arrived.add(procs[idx]["pid"])
                idx += 1

        current = queue.popleft()
        pid = current["pid"]

        if pid not in first_start:
            first_start[pid] = time

        run = min(quantum, remaining_bt[pid])
        timeline.append((time, time + run, pid))
        time += run
        remaining_bt[pid] -= run

        # Enqueue newly arrived processes BEFORE re-queuing current (if not finished)
        while idx < len(procs) and procs[idx]["at"] <= time:
            queue.append(procs[idx])
            arrived.add(procs[idx]["pid"])
            idx += 1

        if remaining_bt[pid] > 0:
            queue.append(current)   # re-queue at back
        else:
            ct[pid] = time

    metrics = []
    for p in procs:
        metrics.append(compute_metrics(p["pid"], p["at"], p["bt"], ct[p["pid"]], first_start[p["pid"]]))

    return timeline, metrics


# ─────────────────────────────────────────────────────────────
#  Run one dataset through all algorithms
# ─────────────────────────────────────────────────────────────

def run_dataset(name, processes, quantum=2):
    algos = [
        ("FCFS",     lambda ps: fcfs(ps)),
        ("SJF",      lambda ps: sjf(ps)),
        ("Priority", lambda ps: priority_scheduling(ps)),
        (f"RR(q={quantum})", lambda ps: round_robin(ps, quantum)),
    ]

    print("\n" + "=" * 60)
    print(f"  DATASET {name}")
    print("=" * 60)

    for algo_name, func in algos:
        print(f"\n{'─'*60}")
        print(f"  Algorithm: {algo_name}")
        print(f"{'─'*60}")
        timeline, metrics = func(processes)
        print_gantt(timeline)
        print_table(metrics)
        print_averages(metrics)


# ─────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    dataset_A = [
        make_process("P1", 0, 7, 2),
        make_process("P2", 2, 4, 1),
        make_process("P3", 4, 1, 3),
        make_process("P4", 5, 4, 2),
        make_process("P5", 6, 3, 1),
    ]

    dataset_B = [
        make_process("P1", 0, 20, 3),
        make_process("P2", 1,  2, 1),
        make_process("P3", 2,  1, 2),
        make_process("P4", 3,  3, 1),
        make_process("P5", 4,  2, 2),
        make_process("P6", 6,  1, 1),
    ]

    run_dataset("A", dataset_A, quantum=2)
    run_dataset("B", dataset_B, quantum=2)

