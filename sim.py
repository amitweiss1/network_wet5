import random
import heapq
import time

# Parameters
arrival_rate = 2.0  # lambda
service_rate = 5.0  # mu
simulation_time = 10  # Total simulation time
load_balancer_buffer_size = 1000 #N

# Set random seed for reproducibility
current_seed = int(time.time())
random.seed(current_seed)

# Events
ARRIVAL = 1
DEPARTURE = 2

# State variables
current_time = 0.0
counter_current_message_in_system = 0
queue = []
server_busy = False
event_list = []

# Statistics
num_in_queue = 0
total_wait_time = 0.0
num_customers_served = 0

# Schedule the first arrival

heapq.heappush(event_list, (random.expovariate(arrival_rate), ARRIVAL))

while current_time < simulation_time:
    event_time, event_type = heapq.heappop(event_list)
    current_time = event_time
    
    if event_type == ARRIVAL:
        if counter_current_message_in_system < load_balancer_buffer_size:
            counter_current_message_in_system += 1
        else:
            print("Load balancer buffer is full")
            continue
        if not server_busy:
            server_busy = True
            service_time = random.expovariate(service_rate)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            queue.append(current_time)
        next_arrival = current_time + random.expovariate(arrival_rate)
        heapq.heappush(event_list, (next_arrival, ARRIVAL))
    elif event_type == DEPARTURE:
        counter_current_message_in_system -= 1  # Message is leaving the system
        num_customers_served += 1
        if queue:
            arrival_time = queue.pop(0)
            wait_time = current_time - arrival_time
            total_wait_time += wait_time
            service_time = random.expovariate(service_rate)
            heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
        else:
            server_busy = False

# Results
print(f"Simulation seed: {current_seed}")
print(f"Number of customers served: {num_customers_served}")
print(f"Average wait time: {total_wait_time / num_customers_served if num_customers_served > 0 else 0}")
