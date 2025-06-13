import random
import heapq
import time
import matplotlib.pyplot as plt

def generate_graph(values, label):
    plt.clf()  # Clear the current figure

    x = list(range(10, 101, 10))  # T values: 10, 20, ..., 100
    y = values

    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    plt.xlabel("T (Simulation Time)")
    plt.ylabel(label)
    plt.title(f"{label} as a function of Simulation Time")
    plt.grid(True)
    plt.savefig(f"{label}_graph.png")  # Saves the figure to a file

def calc_errorX(x, therotical):
  return (abs((therotical - x))/therotical) * 100

# Parameters
arrival_rate = 2.0  # lambda
service_rate = 5.0  # mu
load_balancer_buffer_size = 1000 #N

# Events
ARRIVAL = 1
DEPARTURE = 2

wait_for_all_T = [] #10 different x per T index
served_for_all_T = [] #10 different x per T index

for simulation_time in range(10, 101, 10):
    
    wait_for_gen_x = [] #20 different values for generating x
    served_for_gen_x = [] #20 different values for generating x

    for i in range(20):
        
      ### start simulation

      # Set random seed for reproducibility
      current_seed = time.time_ns() % (2**32)  # keep seed in 32-bit range
      random.seed(current_seed)

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

                  if not server_busy:
                      server_busy = True
                      service_time = random.expovariate(service_rate)
                      heapq.heappush(event_list, (current_time + service_time, DEPARTURE))
                  else:
                      queue.append(current_time)

              else:
                  print("Load balancer buffer is full")

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
      avg_wait_time = total_wait_time / num_customers_served if num_customers_served > 0 else 0
      # print(f"Simulation T: {simulation_time}")
      # print(f"range 1-20 : {i}")
      # print(f"Simulation seed: {current_seed}")
      # print(f"Number of customers served: {num_customers_served}")
      # print(f"Average wait time: {avg_wait_time}")


      ### end simulation

      wait_for_gen_x.append(avg_wait_time)
      served_for_gen_x.append(num_customers_served)
    
    avg_wait = sum(wait_for_gen_x) / len(wait_for_gen_x)
    avg_served = sum(served_for_gen_x) / len(served_for_gen_x)
    wait_for_all_T.append(calc_errorX(avg_wait, ((2/3)/arrival_rate)))
    served_for_all_T.append(calc_errorX(avg_served, (simulation_time*arrival_rate)))

generate_graph(wait_for_all_T, "avg_wait_time")
generate_graph(served_for_all_T, "num_customers_served")
