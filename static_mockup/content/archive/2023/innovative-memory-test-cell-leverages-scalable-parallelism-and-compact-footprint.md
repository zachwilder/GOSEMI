---
title: "Innovative Memory Test Cell Leverages Scalable Parallelism and Compact Footprint for Final Test"
slug: innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint
date: 
category: "Top Stories"
author: ""
excerpt: "Posted  in Top Stories"
original_url: "https://www.gosemiandbeyond.com/innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint-for-final-test/"
---

Posted  in [Top Stories](https://www.gosemiandbeyond.com/category/topstories/)

# Innovative Memory Test Cell Leverages Scalable Parallelism and Compact Footprint for Final Test

*By Zain Abadin, Sr. Director, Device Interface and Handling*,* and Masahito Kondo,* *Integrated Test Cell Solution Lead, Advantest*

Products ranging from datacenter servers to automobiles require more and faster memory ICs, which must be thoroughly yet cost-effectively tested. As these chips evolve to provide ever higher levels of performance and quality, they are placing increasing demands on the test floor. An effective test solution must meet final-test requirements presented by the increasing bit densities, the power consumption, and the faster interface speeds of evolving memory devices. The solution will include automated test equipment (ATE) as well as a test handler that conveys devices under test to the ATE, establishes the proper test temperature, and sorts tested devices into bins according to their pass/fail status.

An effective approach to memory test requires a shift away from the memory-test paradigm that has dominated test floors for the past two decades. ATE and test handler companies have regularly increased parallelism, but each doubling in device capacity has been accompanied by a double-digit increase in test-system size. A way forward beyond 512 devices under test (DUTs) in parallel requires thinking beyond the handler or ATE individually to consider the configuration and performance of the entire test cell. Key points to address include the impact of system downtime; the effect of a big, heavy test cell and its footprint; and the test complexity that results from device variation and requirements for testing at multiple temperatures.

A successful memory-test-cell concept will maximize productivity while controlling cost of test through several features:

- Scalability would enable customers to configure their test cells based on current test requirements while retaining the ability to scale up when necessary.
- A single test cell would support efficient device evaluation at the R&D stage while offering the flexibility to be repurposed for production.
- At any level of scalability, the test cell would efficiently utilize floor space and optimize overall operating efficiency.
- Innovative software would apply artificial intelligence (AI) processing and analysis for tracking handler health and scheduling preventive maintenance.
- For installations with more than one test cell, independent asynchronous test-cell operation would allow partial production test to continue even during maintenance on one cell.

**Fully integrated test cell’s compact design saves floor space **

Advantest is now offering these features in a new minimal-footprint memory-test-cell family called inteXcell. The inteXcell infrastructure currently integrates T5835 memory tester modules, which incorporate full testing functionality for any memory ICs with operating speeds to 5.4Gbps, including next-generation memories ranging from NAND flash devices to DDR-DRAM and LPDDR-DRAM in BGA, CSP, QFP, and other packages. Throughput can reach 36,500 DUTs per hour.

TC5835 features include an enhanced programmable power supply to assist with testing advanced mobile memories, a real-time DQS vs. DQ (strobe vs. data) function to improve yield, a timing training function that is indispensable for high-speed memory tests, and test time reduction and defect-analysis functions based on various device data patterns. In addition to working with the TC5835, the inteXcell platform is designed to work with future memory-test solutions as well.

The inteXcell tester section consists of three units (Figure 1). The first, the AC rack, operates on 220VAC and delivers power to the test cell. Second, the server rack implements the system-controller, test-processor, and handler-controller functions. Third, as many as four test heads can test up to 1,536 devices in parallel. These three units have been designed to fit together into compact test configurations, eliminating the wasted space that can result when trying to integrate separately developed test-cell units. Consequently, inteXcell occupies one-third the floor space a conventional test cell would require.

** **

*Figure 1. The inteXcell tester section comprises an AC rack, a server rack, and up to four test heads.*

**From engineering to mass production**

With inteXcell, ICs can be tested on the same platform from R&D through mass production. Figure 2 shows the scalable parallelism that inteXcell deployments can achieve. At the right, a base inteXcell can test 384 devices in parallel for initial engineering work. That cell can subsequently be repurposed for production. As production volumes increase, inteXcell’s scalable parallelism enables the addition of another test cell, providing a total test capacity of 768 devices in parallel. Moving from right to left in Figure 2, the addition of a third inteXcell brings capacity to 1,152 devices in parallel, while adding a fourth brings total capacity to 1,536 devices in parallel.

*Figure 2. The inteXcell’s scalable parallelism provides flexibility for customers.*

**Reducing downtime**

The inteXcell handler unit incorporates a new, compact chamber structure to provide an efficient and highly accurate thermal-test environment over an operating temperature range of -40°C to 125°C or, optionally, from -55 to 150°C.  New functions such as an automatic position correction capability and a one-touch type replacement kit also improve maintainability and reduce downtime.

In addition, new HM360 status-monitoring software comprehensively manages maintenance and temperature data for the handler unit, making it possible to develop predictive maintenance notifications using AI analysis. Sensors might detect, for example, that a handler pick-and-place mechanism is not achieving optimum vacuum levels. By monitoring deterioration in the vacuum performance, an AI algorithm could determine the optimum time to schedule maintenance. As illustrated on the far left of Figure 2, in a four-cell installation, production can continue at 75% capacity when one cell is taken offline for maintenance.

**Minimizing need for operator intervention **

The production efficiency of the test process is further improved by the optimization of the test cell’s automated guided vehicle (AGV) or overhead hoist transport (OHT) function, which minimizes operator intervention. As shown in Figure 3a, a traditional flow involves obtaining untested devices from the virgin-device lot stock area and conveying them to a high-temperature test stage. The output of this stage will be either a failed device or one that requires further test. In the latter case, the device is conveyed to the cold test stage. The output will be either a failed device or a good device that has passed both hot and cold tests. As Figure 3a illustrates, this process involves eight operator access points requiring a complex scheduler/dispatcher.

**(a)**

**(b)**

 

*Figure 3. Whereas a traditional test cell requires eight operator accesses for a two-temperature test, inteXcell reduces that number to four and eliminates the need for one lot stock area.*

In contrast, inteXcell simplifies the test flow by completing both hot and cold tests with one lot input, as shown in Figure 3b. This approach eliminates the need to establish and access a lot stock area for parts that have passed the hot test, cutting the number of operator access points to four.

**Conclusion**

Advantest’s inteXcell platform is the first fully integrated and unified test solution to combine broad test coverage with high-throughput handling in a highly flexible system architecture. The new test cells have a compact structure that enables up to 384 simultaneous measurements per cell while using only one-third of the floor space occupied by conventional test systems. inteXcell’s scalable parallelism enables customers to choose the test capacity they need. In addition, each cell employs an independent asynchronous testing capability and AI-based performance tracking, enabling inteXcell to be configured from one to four testers, resulting in high equipment utilization, and streamlined cell-based maintenance. A four-test-cell implementation can test up to 1,536 devices in parallel with high speed and high accuracy. The inteXcell platform is expected to begin shipping to customers in the second quarter of 2023.

  end .post_content

![](../images/innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint-1.png)


![](../images/innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint-2.png)


![](../images/innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint-3.png)


![](../images/innovative-memory-test-cell-leverages-scalable-parallelism-and-compact-footprint-4.png)
