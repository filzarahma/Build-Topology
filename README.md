# Build-Topology

This project implements a **Network Topology** using Mininet. It allows users to create and manage a network topology with routers and hosts, configure routing, and test connectivity and bandwidth.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Network Topology](#network-topology)
4. [How to Use](#how-to-use)
5. [Test Cases](#test-cases)
6. [Code Description](#code-description)
7. [Dependencies](#dependencies)
8. [Example Usage](#example-usage)
9. [Acknowledgments](#acknowledgments)
10. [Output Example](#output-example)

---

## Project Overview

The Network Topology project enables users to:

1. **Create a Network Topology** with routers and hosts.
2. **Configure Routing** between different network segments.
3. **Test Connectivity** between network nodes.
4. **Simulate Traffic** and measure bandwidth.

This system uses **Mininet** to create and manage the network topology.

---

## Features

1. **Add Routers and Hosts**  
   Users can add routers and hosts with specified IP addresses and MAC addresses.

2. **Configure Links**  
   Links between nodes can be configured with specified bandwidth.

3. **Routing Configuration**  
   Configure routing tables for routers to enable communication between different network segments.

4. **Connectivity Testing**  
   Test connectivity between nodes using ping.

5. **Traffic Simulation**  
   Simulate traffic between hosts using iperf.

---

## Network Topology

The network topology consists of:

-   **4 Routers** (r1, r2, r3, r4)
-   **2 Hosts** (h1, h2)
-   **Links** with specified bandwidths

---

## How to Use

### Step 1: Clone the Repository

```bash
git clone https://gitclone.com/github.com/filzarahma/Build-Topology-dengan-Mininet.git
```

### Step 2: Run the Python Script

The project is intended to be run using **Mininet** on a **Linux** system. If you are using Windows, you can use **WSL2** or a virtual machine like **VirtualBox**.

1. Ensure Mininet is installed on your system:

```bash
sudo apt install mininet
```

2. Navigate to the project directory.
3. Run the script:

```bash
sudo python Mininet.py
```

or

```bash
sudo python3 Mininet.py
```

### Step 3: Follow Interactive CLI

The system offers an interactive CLI for managing the network topology.

---

## Test Cases

Below are the predefined test cases to verify system functionality:

1. **Test Connectivity**  
   Test connectivity between all nodes using ping.

2. **Simulate Traffic**  
   Simulate traffic between hosts using iperf.

---

## Code Description

-   **`Mininet.py`**: Contains the implementation of the network topology, routing configuration, and testing functions.

### Key Functions:

-   **`run`**: Sets up the network topology and starts the Mininet CLI.
-   **`test_connectivity`**: Tests connectivity between nodes using ping.
-   **`test_traffic`**: Simulates traffic between hosts using iperf.

---

## Dependencies

This project requires:

-   **Mininet**
-   **Python 2.7 or 3.x**

No external libraries are needed.

---

## Example Usage

### Run the Script

```bash
sudo python Mininet.py
```

or

```bash
sudo python3 Mininet.py
```

### Test Connectivity

```plaintext
*** Running connectivity test
*** Testing connectivity:
...
```

### Simulate Traffic

```plaintext
*** Running traffic simulation
...
```

---

## Acknowledgments

This project demonstrates a basic **network topology** using Mininet. It serves as an excellent resource for learning network simulation and configuration.

Feel free to use this project for educational purposes or extend it for more advanced use cases. Feedback and contributions are welcome! 😊

---

## Output Example

Below is an example output of the network topology:

![Output Example](/docs/screenshots/OuputExample.png)
