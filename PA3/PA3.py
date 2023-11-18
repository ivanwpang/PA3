import sys

#first row
SYSTEMTIME = 1
#CPU_POWER_1188 = 2
# CPU_POWER_918 = 3
# CPU_POWER_648 = 4
# CPU_POWER_384 = 5
IDLE = 6
#other rows
TASKNAME = 0
DEADLINE = 1
INDEX_WCET1188 = 2
INDEX_WCET918 = 3
INDEX_WCET648 = 4
INDEX_WCET384 = 5
#scheduler format, [taskname, deadline, wcet, cpu power]
#[['w1', 520, 53, 2, '1188'], ['w2', 320, 40, 2, '1188'], ['w3', 500, 104, 2, '1188'], ['w4', 450, 57, 2, '1188'], ['w5', 300, 35, 2, '1188']]
RUNTIME = 2
CPU_POWER = 3 #col 4, given cpu power for given freq
FREQ = 4      #col 5 = freq

def read_file(filePath):
    with open(filePath, 'r') as inFile:
        lines = inFile.readlines() # Read lines from input file
        task_info = lines[0].split() # Extract first line
        tasks = [line.split() for line in lines[1:]] # Extract remaining lines after first line
            
        for task in tasks:
            task[DEADLINE] = int(task[DEADLINE])
            task[INDEX_WCET1188] = int(task[INDEX_WCET1188])
            task[INDEX_WCET918] = int(task[INDEX_WCET918])
            task[INDEX_WCET648] = int(task[INDEX_WCET648])
            task[INDEX_WCET384] = int(task[INDEX_WCET384])
            
    return (task_info, tasks)

def schedule(task_info, tasks, scheduler):
    schedule = []
    for task in tasks:
        schedule.append([task[TASKNAME], task[DEADLINE], task[INDEX_WCET1188], 2, "1188"]) #2nd col is cpu power
    
    if scheduler == "RM":
        return calcRM(task_info, schedule)
    elif scheduler == "EDF":
        return calcEDF(task_info, schedule)
    else:
        print("invalid choice")
        return ""

def calcEnergy(powerConsumed, timeRunning):
    result = ((float(powerConsumed) / 1000.0) * float(timeRunning))
    return round(result, 3)

def calcRM(task_info, tasks):
    #print(tasks)
    n = len(tasks)
    utilization = 0
    for task in tasks:
        utilization += task[RUNTIME]/task[DEADLINE]
    if (utilization >= n * (2 ** (1/n) - 1)):
        return ""

    availableTasks = []
    schedule = []
    
    for execStartTime in range(int(task_info[SYSTEMTIME])):
        #list of tasks ready at this time based of deadline
        for task in tasks:
            if execStartTime == task[DEADLINE] * (execStartTime // task[DEADLINE]):   
                availableTasks.append(task.copy())
                
        if not availableTasks:
            #no tasks availabe so wait
            schedule.append(["IDLE", "IDLE", task_info[IDLE]])
        else:
            #find earliest deadline
            earliestDeadlineTask = min(availableTasks, key=lambda x: x[DEADLINE])
            schedule.append([earliestDeadlineTask[TASKNAME], earliestDeadlineTask[FREQ], task_info[earliestDeadlineTask[CPU_POWER]]])
            earliestDeadlineTask[RUNTIME] = earliestDeadlineTask[RUNTIME] - 1

            #delete when finished
            if earliestDeadlineTask[RUNTIME] <= 0:
                availableTasks.remove(earliestDeadlineTask)

    scheduleArray = []
    scheduleArray.append(schedule[0]) # Starting the array at 0
    executionTimes = [0]
    totalEnergy = 0
    idleTime = 0
    result = ""

    for line in schedule: # Iterating through every line in schedule
        if (scheduleArray[-1] == line): # Checking if the last line is the same as the current line
            executionTimes[-1] += 1 # If same add to execution time
        # If different append to end and increase its execution time
        else: 
            scheduleArray.append(line)
            executionTimes.append(1)
        # Calculate the IDLE time	
        if (line[0] == "IDLE"):
            idleTime = idleTime + 1
            
    currentTime = 0
    for i in range(len(scheduleArray)):
        energy = calcEnergy(scheduleArray[i][2], executionTimes[i])
        totalEnergy += energy
        totalEnergy = round(totalEnergy, 3)
        result += f"{currentTime} {scheduleArray[i][0]} {scheduleArray[i][1]} {executionTimes[i]} {energy}J\n"
        currentTime += executionTimes[i]
    
    result += f"\n"
    result += f"Total energy: {totalEnergy}J\n"
    result += f"Percent idle time: {round((idleTime / len(schedule)) * 100.0, 2)}%\n"
    result += f"System execution time: {len(schedule) - idleTime}s\n"
    return result

def calcEDF(task_info, tasks):
    utilization = 0
    for task in tasks:
        utilization += task[RUNTIME] / task[DEADLINE]
    if (utilization >= 1):
        return ""

    schedule = []
    availableTasks = []

    for execStartTime in range(int(task_info[SYSTEMTIME])):
        #list of tasks ready at this time based of deadline
        for task in tasks:
            if execStartTime == task[DEADLINE] * (execStartTime // task[DEADLINE]):   
                availableTasks.append(task.copy())
                
        if not availableTasks:
            #no tasks availabe so wait
            schedule.append(["IDLE", "IDLE", task_info[IDLE]])
        else:
            #find earliest deadline
            earliestDeadlineTask = min(availableTasks, key=lambda x: x[DEADLINE])
            schedule.append([earliestDeadlineTask[TASKNAME], earliestDeadlineTask[FREQ], task_info[earliestDeadlineTask[CPU_POWER]]])
            earliestDeadlineTask[RUNTIME] = earliestDeadlineTask[RUNTIME] - 1

            #delete when finished
            if earliestDeadlineTask[RUNTIME] <= 0:
                availableTasks.remove(earliestDeadlineTask)

    scheduleArray = []
    scheduleArray.append(schedule[0]) # Starting the array at 0
    executionTimes = [0]
    totalEnergy = 0
    idleTime = 0
    result = ""

    for line in schedule: # Iterating through every line in schedule
        if (scheduleArray[-1] == line): # Checking if the last line is the same as the current line
            executionTimes[-1] += 1 # If same add to execution time
        # If different append to end and increase its execution time
        else: 
            scheduleArray.append(line)
            executionTimes.append(1)
        # Calculate the IDLE time	
        if (line[0] == "IDLE"):
            idleTime = idleTime + 1
            
    currentTime = 0
    for i in range(len(scheduleArray)):
        energy = calcEnergy(scheduleArray[i][2], executionTimes[i])
        totalEnergy += energy
        totalEnergy = round(totalEnergy, 3)
        result += f"{currentTime} {scheduleArray[i][0]} {scheduleArray[i][1]} {executionTimes[i]} {energy}J\n"
        currentTime += executionTimes[i]

    result += f"\n"
    result += f"Total energy: {totalEnergy}J\n"
    result += f"Percent idle time: {round((idleTime / len(schedule)) * 100.0, 2)}%\n"
    result += f"System execution time: {len(schedule) - idleTime}s\n"
    return result

def scheduleEE(task_info, tasks, scheduler):

    CPU_FREQ = ["", "", "1188", "918", "648", "384"] #first 2 rows blank for alignment, used to serach for cpu freq wcet

    taskList = [[task[TASKNAME], task[DEADLINE], task[INDEX_WCET1188], 2, "1188"] for task in tasks]
    taskWCET = [INDEX_WCET1188] * len(tasks)
    
    runningTask = calcRM(task_info, taskList) if scheduler == "RM" else calcEDF(task_info, taskList)
    lastTask = runningTask

    currentTime = 0
    while runningTask != "":
        currentTime += 1
        lastTask = runningTask
        idleLocation = 0
        idleDuration = 0

        runningTask = runningTask.split('\n')

        #find where idles are and duration of idle
        for i in range(len(runningTask)):
            if "IDLE" in runningTask[i]:
                if int(runningTask[i].split(' ')[3]) > idleDuration:
                    if runningTask[i-1].split(' ')[2] == "384": # 384 is the IDLE freq
                        continue
                    idleLocation = i - 1
                    idleDuration = int(runningTask[i].split(' ')[3])

        #during idle time fix task with the highest energy
        for i in range(len(taskList)):
            if runningTask[idleLocation].split(' ')[1] == taskList[i][TASKNAME]:
                taskWCET[i] += 1
                taskList[i][RUNTIME] = tasks[i][taskWCET[i]]
                taskList[i][CPU_POWER] = taskWCET[i]
                taskList[i][FREQ] = CPU_FREQ[taskWCET[i]]
                break

        #run scheduling with updated task info
        runningTask = calcRM(task_info, taskList) if scheduler == "RM" else calcEDF(task_info, taskList)

    return lastTask

def main():
    if len(sys.argv) < 3:
        print("incorrect entry please use:\n")
        print("python your_program.py input.txt <RM or EDF> EE\n")
        sys.exit(1)

    input_file = sys.argv[1]
    scheduler_choice = sys.argv[2]
    output_file = input_file.split('.')[0]

    if "EE" in sys.argv:
        output_file += f"output_{scheduler_choice}_EE"
        task_info, task_list = read_file(input_file)
        output = scheduleEE(task_info, task_list, scheduler_choice)
    elif scheduler_choice in {"RM", "EDF"}:
        output_file += f"output_{scheduler_choice}"
        task_info, task_list = read_file(input_file)
        output = schedule(task_info, task_list, scheduler_choice)
    else:
        print("Invalid scheduler choice.")
        sys.exit(1)

    with open(output_file + ".txt", 'w') as outFile:
        outFile.write("schedule not possible with given input" if output == "" else output)

if __name__ == "__main__":
    main() 