import numpy as np

# Number of processes and resources
P = 5
R = 3

# Resource allocation, maximum resource requirements, and available resources
allocation = np.array([[0, 1, 0],
                       [2, 0, 0],
                       [3, 0, 2],
                       [2, 1, 1],
                       [0, 0, 2]])

max_resources = np.array([[7, 5, 3],
                          [3, 2, 2],
                          [9, 0, 2],
                          [2, 2, 2],
                          [4, 3, 3]])

available = np.array([3, 3, 2])

# Calculate the need matrix
need = max_resources - allocation

def is_safe(available, allocation, need):
    work = available.copy()
    finish = np.zeros(P, dtype=bool)
    safe_sequence = []

    for k in range(P):
        deadlock = True
        for i in range(P):
            if not finish[i]:
                flag = 0
                for j in range(R):
                    if need[i][j] > work[j]:
                        flag = 1
                        break

                if flag == 0:
                    safe_sequence.append(i)
                    for y in range(R):
                        work[y] += allocation[i][y]
                    finish[i] = True
                    deadlock = False

        if deadlock:
            break

    if np.all(finish):
        return True, safe_sequence
    else:
        return False, None

def request_resources(process_id, request, available, allocation, need):
    if np.any(request > need[process_id]):
        print(f"Process {process_id}: Request exceeds the maximum claim.")
        return False

    if np.any(request > available):
        print(f"Process {process_id}: Request exceeds available resources.")
        return False

    # Temporarily allocate resources and check if the state is safe
    available -= request
    allocation[process_id] += request
    need[process_id] -= request

    if is_safe(available, allocation, need):
        print(f"Process {process_id}: Request granted. System remains in a safe state.")
        return True
    else:
        print(f"Process {process_id}: Request denied. System would be in an unsafe state.")
        # Revert the temporary allocation
        available += request
        allocation[process_id] -= request
        need[process_id] += request
        return False

# Test case 1: Granting a request (safe state)
request = np.array([1, 0, 2])
process_id = 1
print(f"Request by process {process_id}: {request}")
print(f"Initial Available: {available}")
print(f"Initial Need Matrix: \n{need}")
result = request_resources(process_id, request, available, allocation, need)
print(f"Resulting Available: {available}")
print(f"Resulting Need Matrix: \n{need}\n")

# Test case 2: Denying a request (unsafe state)
request = np.array([3, 5, 1])
process_id = 0
print(f"Request by process {process_id}: {request}")
print(f"Initial Available: {available}")
print(f"Initial Need Matrix: \n{need}")
result = request_resources(process_id, request, available, allocation, need)
print(f"Resulting Available: {available}")
print(f"Resulting Need Matrix: \n{need}\n")


