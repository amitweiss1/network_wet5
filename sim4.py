import random
import heapq
import time
import sys
from collections import deque

# Parameters
simulation_time = 0.0 # Total simulation time
servers_num = 0     # number of servers
arrival_rate = 0.0    # lambda
probabilities = []  # P
queue_lens = []     # Q
services_rate = []  #mu

# output Params
num_of_customers_served = 0     # A
num_of_dump = 0                 # B
time_finish_last_served = 0.0     #Tend
avg_time_waiting_for_served = 0.0 # Tw
avg_time_served_per_mesg = 0.0    #Ts

# Events
ARRIVAL = 1
DEPARTURE = 2

def parse_args():
  global simulation_time, servers_num, arrival_rate
  global probabilities, queue_lens, services_rate

  # sys.argv[0] is the script name
  print("Script name:", sys.argv[0])

  # Other arguments
  if len(sys.argv) < 7:
      raise("Not enought args")
  
  servers_num = (int)(sys.argv[2])                 #M
  if (servers_num < 1):
      raise("M must be >= 1")

  if (len(sys.argv) != 3*servers_num + 4):
      raise("Not proper number of args")
  
  simulation_time = float(sys.argv[1])             #T
  for i in range(servers_num):
      probabilities.append(float(sys.argv[3+i]))   #P
  if (sum(probabilities) != 1):
      raise("Sum of all probabilities must be 1")

  arrival_rate = float(sys.argv[servers_num+3])    #lambda

  for i in range(servers_num):
      queue_lens.append(int(sys.argv[servers_num+4+i]))   #Q

  for i in range(servers_num):
      services_rate.append(float(sys.argv[2*servers_num+4+i]))   #Q

parse_args()

# Set random seed for reproducibility
current_seed = int(time.time())
random.seed(current_seed)

# State variable
current_time = 0.0
event_list = []       # list of 3-tuple: (time, server number for DEP, event type)
servers_busy = [False] * servers_num
servers_queue = [deque() for _ in range(servers_num)]
total_wait_time = 0.0
total_serve_time = 0.0

# Schedule the first arrival
heapq.heappush(event_list, (random.expovariate(arrival_rate), -1, ARRIVAL))

while current_time < simulation_time:
    event_time, chosen_server, event_type = heapq.heappop(event_list)
    current_time = event_time
    
    if event_type == ARRIVAL:

        # choose server
        indices = list(range(len(probabilities)))
        chosen_server = random.choices(indices, weights=probabilities, k=1)[0]

        # check if there is room for mesg in chosen server
        if len(servers_queue[chosen_server]) < queue_lens[chosen_server]:
            if not servers_busy[chosen_server]:
                servers_busy[chosen_server] = True
                service_time = random.expovariate(services_rate[chosen_server])
                total_serve_time += service_time
                heapq.heappush(event_list, (current_time + service_time, chosen_server, DEPARTURE))
            else:
                servers_queue[chosen_server].append(current_time)
        else:
            num_of_dump += 1
            # print("Server number " + str(chosen_server) + " is full with " + str(queue_lens[chosen_server]) + "messages, so message will be dump")

        next_arrival = current_time + random.expovariate(arrival_rate)
        heapq.heappush(event_list, (next_arrival, -1, ARRIVAL))

    elif event_type == DEPARTURE:

        num_of_customers_served += 1
        time_finish_last_served = current_time

        if len(servers_queue[chosen_server]) > 0:
            arrival_time = servers_queue[chosen_server].popleft()  # for FIFO
            wait_time = current_time - arrival_time
            total_wait_time += wait_time
            service_time = random.expovariate(services_rate[chosen_server])
            total_serve_time += service_time
            heapq.heappush(event_list, (current_time + service_time, chosen_server, DEPARTURE))
        else:
            servers_busy[chosen_server] = False

# Results
avg_time_waiting_for_served = total_wait_time / num_of_customers_served if num_of_customers_served > 0 else 0
avg_time_served_per_mesg =  total_serve_time / num_of_customers_served if num_of_customers_served > 0 else 0
# print(f"Simulation seed: {current_seed}")
# print(f"Number of customers served: {num_of_customers_served}")
# print(f"Number of dump messages: {num_of_dump}")
# print(f"Time of last message finish process: {round(time_finish_last_served, 4)}")
# print(f"Average wait time: {round(avg_time_waiting_for_served, 4)}")
# print(f"Average serve time: {round(avg_time_served_per_mesg, 4)}")

# for submission
print(f"{num_of_customers_served} {num_of_dump} {round(time_finish_last_served, 4)} {round(avg_time_waiting_for_served, 4)} {round(avg_time_served_per_mesg, 4)}")