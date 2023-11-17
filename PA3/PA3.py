import sys
import unittest

# First line of input file
NUMBER_OF_TASKS = 0
EXECUTION_TIME = 1
CPU_POWER_1188 = 2
CPU_POWER_918 = 3
CPU_POWER_648 = 4
CPU_POWER_384 = 5
IDLE_POWER = 6
# Lines after first line of input file
NAME_OF_TASK = 0
DEADLINE = 1
WCET_1188 = 2
WCET_918 = 3
WCET_648 = 4
WCET_384 = 5
# For each individual line after the first line
TASK_NAME = 0
TASK_DEADLINE = 1
TASK_EXEC_TIME = 2
TASK_ACTIVE_POWER = 3
TASK_FREQUENCY = 4

CPU_FREQ = ["", "", "1188", "918", "648", "384"] # Empty strings in the first two for alignment 

def accessFile(filePath):
    with open(filePath, 'r') as inFile:
        lines = inFile.readlines() # Read lines from input file
        taskInfo = lines[0].split() # Extract first line
        taskList = [line.split() for line in lines[1:]] # Extract remaining lines after first line
            
        for task in taskList:
            task[DEADLINE] = int(task[DEADLINE])
            task[WCET_1188] = int(task[WCET_1188])
            task[WCET_918] = int(task[WCET_918])
            task[WCET_648] = int(task[WCET_648])
            task[WCET_384] = int(task[WCET_384])

    return (taskInfo, taskList)

def schedule(taskInfo, taskList, scheduler):
    schedule = []
    for task in taskList:
        schedule.append([task[NAME_OF_TASK], task[DEADLINE], task[WCET_1188], CPU_POWER_1188, "1188"])
    
    if scheduler == "RM":
        return calcRM(taskInfo, schedule)
    elif scheduler == "EDF":
        return calcEDF(taskInfo, schedule)
    else:
        print("Invalid scheduler choice.")
        return ""

def calcEnergy(powerConsumed, timeRunning):
    result = ((float(powerConsumed) / 1000.0) * float(timeRunning))
    return round(result, 3)

def scheduleAsArray(schedule):
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
            
    count = 1
    for i in range(len(scheduleArray)):
        energy = calcEnergy(scheduleArray[i][2], executionTimes[i])
        totalEnergy += energy
        totalEnergy = round(totalEnergy, 3)
        result += f"{count} {scheduleArray[i][0]} {scheduleArray[i][1]} {executionTimes[i]} {energy}J\n"
        count += executionTimes[i]
    
    result += f"Total energy consuption during the execution: {totalEnergy}J\n"
    result += f"Percentage of time spent idle: {round((idleTime / len(schedule)) * 100.0, 2)}%\n"
    result += f"Total system execution time: {len(schedule) - idleTime}s\n"
    return result

def calcRM(taskInfo, taskList):
    taskLen = len(taskList)
    utilization = 0
    for task in taskList:
        utilization += task[TASK_EXEC_TIME]/task[DEADLINE]
    if (utilization >= taskLen * (2 ** (1/taskLen) - 1)):
        return ""

    availableTasks = []
    schedule = []
    
    for execStartTime in range(int(taskInfo[EXECUTION_TIME])):
        # Create a list of tasks that are available to be executed at this time based on their deadlines
        for task in taskList:
            if execStartTime == task[TASK_DEADLINE] * (execStartTime // task[TASK_DEADLINE]): # // = division rounded down or is equal to. For example 7 // 3 = 2
                availableTasks.append(task.copy())
        # Find the deadlines
        deadlines = [(task[TASK_DEADLINE]) for task in availableTasks]
        if (deadlines == []):
        # If deadline is empty, then nothing is ran aka IDLE
            schedule.append(["IDLE", "IDLE", taskInfo[IDLE_POWER]])
        else:
            # Find the highest priority deadline
            earliestDeadlineTask = min(availableTasks, key=lambda x: x[TASK_DEADLINE])
            schedule.append([earliestDeadlineTask[TASK_NAME], earliestDeadlineTask[TASK_FREQUENCY], taskInfo[earliestDeadlineTask[TASK_ACTIVE_POWER]]])
            earliestDeadlineTask[TASK_EXEC_TIME] = earliestDeadlineTask[TASK_EXEC_TIME] - 1
        
            # Delete tasks that are done
            if (earliestDeadlineTask[TASK_EXEC_TIME] <= 0):
                availableTasks.remove(earliestDeadlineTask)
    return scheduleAsArray(schedule)


def calcEDF(taskInfo, taskList):
    utilization = 0
    for task in taskList:
        utilization += task[TASK_EXEC_TIME] / task[DEADLINE]
    if (utilization >= 1):
        return ""

    schedule = []
    availableTasks = []

    for execStartTime in range(int(taskInfo[EXECUTION_TIME])):
        # Create a list of tasks that are available to be executed at this time based on their deadlines
        for task in taskList:
            if execStartTime == task[TASK_DEADLINE] * (execStartTime // task[TASK_DEADLINE]):   
                availableTasks.append(task.copy())
                
        if not availableTasks:
            # If no tasks are available, then nothing is ran aka IDLE
            schedule.append(["IDLE", "IDLE", taskInfo[IDLE_POWER]])
        else:
            # Find the highest priority deadline
            earliestDeadlineTask = min(availableTasks, key=lambda x: x[TASK_DEADLINE])
            schedule.append([earliestDeadlineTask[TASK_NAME], earliestDeadlineTask[TASK_FREQUENCY], taskInfo[earliestDeadlineTask[TASK_ACTIVE_POWER]]])
            earliestDeadlineTask[TASK_EXEC_TIME] = earliestDeadlineTask[TASK_EXEC_TIME] - 1

            # Delete tasks that are done
            if earliestDeadlineTask[TASK_EXEC_TIME] <= 0:
                availableTasks.remove(earliestDeadlineTask)

    return scheduleAsArray(schedule)


def scheduleEE(taskInfo, taskList, scheduler):
    taskLog = []
    taskWCETs = []
    lastTask = ""

    # if scheduler == "RM":
        
    # elif scheduler == "EDF":
        
    # else:
    #     print("Invalid scheduler choice.")
    #     return ""
    if scheduler == "RM":
        for task in taskList:
            taskLog.append([task[NAME_OF_TASK], task[DEADLINE], task[WCET_1188], CPU_POWER_1188, "1188"])
            taskWCETs.append(WCET_1188)
            
        runningTask = calcRM(taskInfo, taskLog)
        lastTask = runningTask

        count = 0
        while (runningTask != ""):
            count += 1
            lastTask = runningTask
            idleLocation = 0
            idleDuration = 0

            runningTask = runningTask.split('\n')
            for i in range(len(runningTask)):
                if (runningTask[i].find("IDLE") != -1): # Checking for IDLE 
                    if (int(runningTask[i].split(' ')[3]) > idleDuration): # If is IDLE, then compare the IDLE durations
                        if (runningTask[i-1].split(' ')[2] == "384"): # Use lowest CPU_FREQ
                            continue
                        idleLocation = i - 1
                        idleDuration = int(runningTask[i].split(' ')[3])
            
            for i in range(len(taskLog)):
                if (runningTask[idleLocation].split(' ')[1] == taskLog[i][TASK_NAME]): 
                    taskWCETs[i] = taskWCETs[i] + 1
                    taskLog[i][TASK_EXEC_TIME] = taskList[i][taskWCETs[i]]
                    taskLog[i][TASK_ACTIVE_POWER] = taskWCETs[i]
                    taskLog[i][TASK_FREQUENCY] = CPU_FREQ[taskWCETs[i]]
                    break
            runningTask = calcRM(taskInfo, taskLog)
        return lastTask
    elif scheduler == "EDF":
        for task in taskList:
            taskLog.append([task[NAME_OF_TASK], task[DEADLINE], task[WCET_1188], CPU_POWER_1188, "1188"])
            taskWCETs.append(WCET_1188)
            
        runningTask = calcEDF(taskInfo, taskLog)
        lastTask = runningTask

        count = 0
        while (runningTask != ""):
            count += 1
            lastTask = runningTask
            idleLocation = 0
            idleDuration = 0

            runningTask = runningTask.split('\n')
            for i in range(len(runningTask)):
                if (runningTask[i].find("IDLE") != -1): # Checking for IDLE 
                    if (int(runningTask[i].split(' ')[3]) > idleDuration): # If is IDLE, then compare the IDLE durations
                        if (runningTask[i-1].split(' ')[2] == "384"): # Use lowest CPU_FREQ
                            continue
                        idleLocation = i - 1
                        idleDuration = int(runningTask[i].split(' ')[3])
            
            for i in range(len(taskLog)):
                if (runningTask[idleLocation].split(' ')[1] == taskLog[i][TASK_NAME]): 
                    taskWCETs[i] = taskWCETs[i] + 1
                    taskLog[i][TASK_EXEC_TIME] = taskList[i][taskWCETs[i]]
                    taskLog[i][TASK_ACTIVE_POWER] = taskWCETs[i]
                    taskLog[i][TASK_FREQUENCY] = CPU_FREQ[taskWCETs[i]]
                    break
            runningTask = calcEDF(taskInfo, taskLog)
        return lastTask
    else:
        print("invalid schedule choice")


if __name__ == "__main__":
    (taskInfo, taskList) = accessFile(sys.argv[1])
    outputFile = sys.argv[1].split('.')[0]
    scheduler_choice = sys.argv[2]
    if ("RM" in sys.argv and "EE" in sys.argv):
        output = scheduleEE(taskInfo, taskList, scheduler_choice)
        outputFile += "output_RM_EE"
    elif ("EDF" in sys.argv and "EE" in sys.argv):
        output = scheduleEE(taskInfo, taskList, scheduler_choice)
        outputFile += "output_EDF_EE"
    elif ("RM" in sys.argv):
        output = schedule(taskInfo, taskList, scheduler_choice)
        outputFile += "output_RM"
    elif ("EDF" in sys.argv):
        output = schedule(taskInfo, taskList, scheduler_choice)
        outputFile += "output_EDF"
    else:
        print("The command lines should be in this format: your_program <input_file_name> <EDF or RM> [EE] \n")
        exit()
        
    with open(outputFile + ".txt", 'w') as outFile:
        if (output == ""):
            outFile.write("no possible schedule for input")
        else:
            outFile.write(output)