import random
import math
import sys
from queue_o import SimulationQueue
from queue_k import SimulationQueue_M_M_1_K
from packet import Packet
from simulation_config import Config
import matplotlib.pyplot as plt 


def question1():
    lambda1 = 75
    random_numbers = []
    # Generate 1000 random numbers
    for i in range(1000):
        x = - (1 / lambda1) * math.log(1 - random.uniform(0, 1))
        random_numbers.append(x)
    # Mean
    mean = sum(random_numbers) / len(random_numbers)
    # Variance
    variance = sum([(x - mean) ** 2 for x in random_numbers]) / len(random_numbers)
    # Print results
    print("--------------------------------------------------")
    print("-------------------QUESTION 1---------------------")
    print("--------------------------------------------------")
    print("Expected mean", 1/lambda1)
    print("Mean:", mean)
    print("--------------------------------------------------")
    print("Expected variance", 1/lambda1**2)
    print("Variance:", variance)


def question3():
    # Print the header
    print("--------------------------------------------------") 
    print("-------------------QUESTION 3---------------------")
    print("--------------------------------------------------")
    # Initialize variables
    x_axis = []
    y_axis_E_N = []
    y_axis_Idle = []
    E_N_list = []
    Idle_list = []
    y_axis_E_N.append(E_N_list)
    y_axis_Idle.append(Idle_list)
    List_K = ["K is infinite", "green"]
    # Start a loop for every value of rho
    for i in range(35, 95, 10):
        i /= 100
        print("p = ", i)
        x_axis.append(i)
        #Run the simulation
        Idle_counter, E_N, N_a, N_d, N_o = simulator_M_M_1(i)
        #Updarte the lists for the graph
        E_N_list.append(E_N)
        Idle_list.append(Idle_counter)
        #Print the results
        print("Idle: ", Idle_counter)
        print("E[N]: ", E_N)
        print("N_a: ", N_a)
        print("N_d: ", N_d)
        print("N_o: ", N_o)
        print("--------------------------------------------------")
    y_axis_E_N.append(E_N_list)
    y_axis_Idle.append(Idle_list)
    #Plot the graph
    graph(x_axis, y_axis_E_N, 'Average number in the system E[N]', 'M_M_1 simulation', [List_K], "E_N_M_M_1.png")
    graph(x_axis, y_axis_Idle, 'Idle queue probability', 'M_M_1 simulation', [List_K], "P_idle_M_M_1.png")


def question4():
    # Print the header
    print("--------------------------------------------------") 
    print("-------------------QUESTION 4---------------------")
    print("--------------------------------------------------")
    # Run the simulation for rho = 1.2
    Idle_counter, E_N, N_a, N_d, N_o = simulator_M_M_1(1.2)
    # Print the results
    print("Idle: ", Idle_counter)
    print("E[N]: ", E_N)
    print("N_a: ", N_a)
    print("N_d: ", N_d)
    print("N_o: ", N_o)


def question6():
    # Print the header
    print("--------------------------------------------------") 
    print("-------------------QUESTION 6---------------------")
    print("--------------------------------------------------")
    # Initialize variables
    x_axis = []
    y_axis_E_N = []
    y_axis_P_loss = []

    K = [10, 25, 50]
    colors = ["red", "green", "blue", "black"]
    K_colors = []
    #Start a loop for every value of K
    for k in K:
        print("-------------------- K =", k,"----------------------")
        text = "K = " + str(k)
        K_colors.append([text, colors.pop(0)])
        # Initialize lists to store the results of the loop
        E_N_list = []
        P_loss_list = []
        for i in range(60, 150, 10):
            i /= 100
            if k == K[0]:
                x_axis.append(i)
            # Run the simulation
            E_N, P, N_a, N_d, N_o, Idle_counter = simulator_M_M_1_K(i, k)
            # Print the results
            print("Idle: ", Idle_counter)
            print("E[N]: ", E_N)
            print("P_loss: ", P)
            print("N_a: ", N_a)
            print("N_d: ", N_d)
            print("N_o: ", N_o)
            # Update the lists for the graph
            E_N_list.append(E_N)
            P_loss_list.append(P)
            print("--------------------------------------------------")
        # Update the lists for the graph for every value of K
        y_axis_E_N.append(E_N_list)
        y_axis_P_loss.append(P_loss_list)
    # Plot the graph
    graph(x_axis, y_axis_E_N, 'Average number in the system E[N]', 'M_M_1_K simulation', K_colors, "E_N_M_M1_K.png")
    graph(x_axis, y_axis_P_loss, 'Probability of losing a packet', 'M_M_1_K simulation', K_colors, "P_loss_M_M_1_K.png")


def simulator_M_M_1_K(p, k):
    # Initialize variables
    Length = Config.Length
    C = Config.C
    lambda1 = p * C / Length
    T = Config.T
    DES = []

    queue = SimulationQueue_M_M_1_K(k)
    # Generate observers
    observer_generator(lambda1, T, DES)
    # Generate arrivals
    generate_packets(lambda1, T, DES)
    #Process events
    return process_events_M_M_1_K(Length, C, DES, queue)


def generate_packets(lambda1, T, DES):
    arrival_time = 0
    # Generate arrivals until T is reached
    while arrival_time <= T:
        time = - (1 / lambda1) * math.log(1 - random.uniform(0, 1))
        arrival_time += time
        if arrival_time > T:
            break
        # Add the arrival to the DES
        DES.append(Packet("A", arrival_time))


def process_events_M_M_1_K(Length, C, DES, queue):
    # Initialize variables
    N_a = 0
    N_d = 0
    N_o = 0
    E_N = 0
    Idle_counter = 0
    last_departure = 0
    departures = []
    DES = sorted(DES, key=lambda packet: packet._arrival_time)
    index = 0
    while index != len(DES):
        # Get the next event
        if departures:
            # If the next event is an arrival and the next departure is before the arrival, process the departure
            if DES[index]._arrival_time > departures[0]._arrival_time:
                element = departures.pop(0)
                index -= 1
            else:
                element = DES[index]
        else:
            element = DES[index]
        # Process an arrival
        if element.event_type == "A":
            N_a += 1
            # If the queue is not full, enqueue the packet
            if (queue.is_full() == False):
                queue.enqueue(element)
                # Generate a departure for the packet
                length = - (Length) * math.log(1 - random.uniform(0, 1))
                service_time = length / C
                packet = Packet("A", element._arrival_time, length, service_time)
                packet.departure(last_departure)
                last_departure = packet._departure
                # Add the departure to the DES
                departures.append(Packet("D", packet._departure))
        # Process a departure
        elif element.event_type == "D":
            N_d += 1
            queue.dequeue()
        # Process an observer
        elif element.event_type == "O":
            N_o += 1
            # If the queue is empty, increment the idle counter
            if queue.size() == 0:
                Idle_counter += 1
            # Else, update the average number of packets in the system
            else:
                E_N += queue.size()
        index += 1
    # Process the remaining departures
    while departures:
        departures.pop(0)
        N_d += 1
        queue.dequeue()
    # Calculate the results
    Idle_counter /= N_o
    E_N /= N_o
    P_loss = 1 - (N_d / N_a)

    return E_N, P_loss, N_a, N_d, N_o, Idle_counter


def simulator_M_M_1(p):
    # Initialize variables
    Length = Config.Length
    C = Config.C
    lambda1 = p * C / Length
    T = Config.T
    # Generate events
    DES = events_generator_M_M_1(Length, C, lambda1, T)
    #Process the DES
    return simulation(DES)


def simulation(DES):
    # Initialize variables
    N_a = 0
    N_d = 0
    N_o = 0
    E_N = 0
    Idle_counter = 0
    queue = SimulationQueue()
    # Process events
    for element in DES:
        # Process an arrival
        if element.event_type == "A":
            N_a += 1
            queue.enqueue(element)
        # Process a departure
        elif element.event_type == "D":
            N_d += 1
            queue.dequeue()
        # Process an observer
        elif element.event_type == "O":
            N_o += 1
            # If the queue is empty, increment the idle counter
            if queue.size() == 0:
                Idle_counter += 1
            # Else, update the average number of packets in the system
            else:
                E_N += queue.size()
    # Calculate the results
    Idle_counter /= N_o
    E_N /= N_o

    return Idle_counter, E_N, N_a, N_d, N_o


def events_generator_M_M_1(Length, C, lambda1, T):
    # Initialize variables
    packets = []
    DES = []
    arrival_time = 0
    last_departure = 0
    # Initialize arrivals and departures
    while arrival_time <= T:
        # Generate arrivals until T is reached
        time = - (1 / lambda1) * math.log(1 - random.uniform(0, 1))
        arrival_time += time
        if arrival_time > T:
            break
        DES.append(Packet("A", arrival_time))
        # Generate departures
        lenght = - (Length) * math.log(1 - random.uniform(0, 1))
        service_time = lenght / C
        packet = Packet("A", arrival_time, lenght, service_time)
        packet.departure(last_departure)
        last_departure = packet._departure
        # Add the departure to the DES
        DES.append(Packet("D", packet._departure))
        #Store the packet
        packets.append(packet)
    
    # Initialize observers
    observer_generator(lambda1, T, DES)

    # Sort events by arrival time
    DES = sorted(DES, key=lambda packet: packet._arrival_time)

    return DES


def observer_generator(lambda1, T, DES):
    observer_time = 0
    # Generate observers until T is reached
    while observer_time <= T:
        x = - (1 / (5 * lambda1)) * math.log(1 - random.uniform(0, 1))
        observer_time += x
        if observer_time <= T:
            DES.append(Packet("O", observer_time))


def graph(x_values, y_values, y_text, title, K_colors, output_file):
    # Plot the graph
    for element, k_color in zip(y_values, K_colors):
        plt.plot(x_values, element, marker='o', linestyle='-', color=k_color[1], label=k_color[0])

    # Set labels and title
    plt.xlabel('Traffic intensity p')
    plt.ylabel(y_text)
    plt.title(title)
    plt.legend()
    # save the graph in the output file
    plt.savefig(output_file)
    plt.close()
#Code necessary to run the program
functions = {
    'question1': question1,
    'question3': question3,
    'question4': question4,
    'question6': question6
}

if __name__ == '__main__':
    print(sys.argv)
    func = functions[sys.argv[1]]
    args = sys.argv[6:]

    sys.exit(func(*args))






