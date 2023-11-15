import unittest

def read_input_file(file_name):
    system_parameters = ()
    tasks = []

    with open(file_name, 'r') as file:
        lines = file.readlines() # Read lines from input file

        # Extract first line or system parameters
        system_params = lines[0].split()
        system_parameters = tuple(map(int, system_params))

        # Extract lines after the first line
        for line in lines[1:]:
            task_data = line.split()
            task_name = task_data[0]
            task_params = list(map(int, task_data[1:]))
            tasks.append((task_name, *task_params))

    return system_parameters, tasks

def schedule_RM(system_parameters, tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x[1])  # Sort tasks based on their periods in ascending order

    schedule = []
    total_energy = 0.0
    current_time = 0
    cpu_freqs = [1188, 918, 648, 384] # Given Frequencies 

    # Scheduling each task
    for task in sorted_tasks:
        task_name, deadline, *wcet_values = task
        wcet_values = list(map(int, wcet_values))

        task_energy = calculate_energy(wcet_values, system_parameters)  # Energy calculations
        total_energy += task_energy

        # Add task to schedule
        schedule.append((current_time, task_name, cpu_freqs[0], wcet_values[0], task_energy))

        # Update current time
        current_time += wcet_values[0]

    return schedule, total_energy



# Energy calculations might be different
def calculate_energy(wcet_values, system_parameters):
    power_consumption = system_parameters[2]
    time_running = wcet_values[0] / system_parameters[2]
    energy_consumed = power_consumption * time_running

    return energy_consumed


def format_and_write_schedule(schedule, output_file):
    with open(output_file, 'w') as f:
        for entry in schedule:
            time_started, task_name, cpu_frequency, duration, energy_consumed = entry
            line = f"{time_started} {task_name} {cpu_frequency} {duration} {energy_consumed:.3f}J\n"
            f.write(line)

def main():
    file_name = "input1.txt"
    system_parameters, tasks = read_input_file(file_name) # Reading input file

    rm_schedule, total_energy_rm = schedule_RM(system_parameters, tasks) # Running RM Schedule

    output_file = "rm_schedule_output.txt" # Output file name
    format_and_write_schedule(rm_schedule, output_file) # Write to output file

    print(f"Total Energy Consumption (RM): {total_energy_rm:.3f}J")

if __name__ == "__main__":
    main()

# FOR TESTING THE FUNCTION THAT READS THE FILE
#############################################################################################################
# class TestInputFileReading(unittest.TestCase):
#     def test_read_input1_file(self):
#         file_name = "input1.txt"  # The name of the provided input file
#         system_parameters, tasks = read_input_file(file_name)

#         # Expected data from the input file
#         expected_system_parameters = (5, 1000, 625, 447, 307, 212, 84)
#         expected_tasks = [
#             ("w1", 520, 53, 66, 89, 141),
#             ("w2", 220, 40, 50, 67, 114),
#             ("w3", 500, 104, 134, 184, 313),
#             ("w4", 200, 57, 74, 103, 175),
#             ("w5", 300, 35, 45, 62, 104),
#         ]

#          # Perform assertions to check if the function reads the file correctly
#         self.assertEqual(system_parameters, expected_system_parameters)
#         self.assertEqual(len(tasks), expected_system_parameters[0])  # Check the number of tasks
#         self.assertEqual(tasks, expected_tasks)
############################################################################################################