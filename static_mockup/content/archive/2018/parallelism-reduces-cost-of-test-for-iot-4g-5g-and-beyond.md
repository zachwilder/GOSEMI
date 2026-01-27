---
title: "Parallelism Reduces Cost of Test for IoT, 4G, 5G, and Beyond"
slug: parallelism-reduces-cost-of-test-for-iot-4g-5g-and-beyond
date: 
category: "Top Stories"
author: ""
excerpt: "Posted  in Top Stories"
original_url: "https://www.gosemiandbeyond.com/parallelism-reduces-cost-of-test-for-iot-4g-5g-and-beyond/"
---

Posted  in [Top Stories](https://www.gosemiandbeyond.com/category/topstories/)

# Parallelism Reduces Cost of Test for IoT, 4G, 5G, and Beyond

*By Dieter Ohnesorge, Product Manager for RF Solutions*

**Introduction**

The proliferation of the Internet of Things and the move from 4G to 5G is bringing about pressing test problems. The challenges will increase as billions of IoT devices incorporate GPS, Bluetooth, WLAN, NB-IoT, LTE-A, LTE-M, and other connectivity technologies and as smartphones begin connecting with 5G networks. Applications extend from M2M communications to fixed and mobile wireless access in smart cities. Venues for deployment will extend from factories and vehicles to stadiums and airports.

Transceiver chips for such applications include an increasing number of bands and RF ports carrying high-quality signals. The result can be longer test times leading to increasing cost of test.

**Parallel test flow**

Many transceivers have architectures that support testing paths and bands in parallel to reduce the cost of test with test techniques that are closer to mission mode, with the test mimicking real-life operation. For example, while you are making a phone call in your car, your smartphone is connected to a cell tower but also to your hands-free Bluetooth connection. You are also likely navigating by GPS and may use a WLAN connection to download a video for your kids to watch. All these functions are taking place in parallel, and an effective production-test strategy should come as close as possible to applying these mission-mode parallel operations.

Traditional “serial” test-flow techniques, based on a fanout RF architecture with shared stimulus and measurement resources, cannot cost-effectively test complex devices. For an LTE-A transceiver with carrier aggregation, a serial test approach would need to test the various uplink and downlink channels sequentially in a series of RF stimulus and baseband measurement operations followed by baseband stimulus and RF measurement operations—leading to long test times.

An alternative is the parallel test flow, enabled by an architecture incorporating independent RF subsystems with truly parallel stimulus and measurement ports. A parallel test flow can speed the test of multiple ports in a single device and can also support multisite test.

**WSRF LTE-A/RF combo device test example**

The parallel test technique is enabled by instruments such as the V93000 Wave Scale RF (WSRF) card, which offers test-processor-based synchronization and parallel mission-mode test capability. WSRF can simultaneously test multiple transceiver channels in parallel, thereby improving multisite efficiency (MSE) and significantly reducing test time.

The WSRF includes four independent RF subsystems on each card, with 32 truly parallel stimulus and measurement RF ports per card. Each RF subsystem includes an embedded arbitrary waveform generator and digitizer. The WSRF supports 16x multisite test with native ATE resources and includes embedded RF calibration standards.

For less demanding IoT applications, the WSRF scales down to one RF subsystem for use in an A-Class V93000 system. The WSRF can scale down for IoT, enabling it to perform quad-site testing based on one-fourth of a card using just one RF subsystem. At the other end of the spectrum, you may need four WSRF cards to cover the different needs for both sub-6-GHz and mmWave frequencies.

A concept study involving an LTE-A RF transceiver/RF combo device with 802.11ac support and a 3G/4G front-end module showed that the WSRF resulted in test-time improvements of up to 50% as compared with the PSRF, the predecessor to the WSRF.

Figure 1 (not to scale) depicts receive-channel, transmit-channel, and other tests performed serially (top) and the same tests using a mission-mode parallel technique (bottom). Parallel mission-mode test coupled with test-processor-based synchronization can provide a 40% to 60% test-time reduction. Figure 2 provides specific test-time-reduction values for testing parameters such as gain and EVM in single- and quad-site formats, showing MSE and test-time improvement. The results are based on similar setups and sample rates, with the patterns used being the same.

Figure 1. A serial test technique (top) cannot cost-effectively test complex devices, whereas a parallel mission-mode test (bottom) can result in a 50% test-time reduction.

 

Figure 2. This overview shows multisite efficiencies (MSE) and test-time improvements for parallel vs. serial receiver tests.

**
Testing 802.11ax**

Test of 802.11ax devices offers another example of the benefits of parallel test flow. The successor to 802.11ac, 802.11ax offers an expected fourfold increase in user throughput. Designed to improve overall spectral efficiency in dense deployment scenarios, 802.11ax incorporates multiuser MIMO on the downlink and uplink. It operates in both the 2.4-GHz and 5-GHz ISM bands.

These characteristics impose significant ATE challenges. Multiuser MIMO places more demands on RF/analog resources, resulting in longer test times. ATE RF and baseband instruments (AWGs and digitizers) must accommodate the standard’s 160-MHz bandwidth, and the 1024 QAM modulation scheme demands improved phase noise and linearity.

An eight-site test of an 802.11ax transceiver operating in the 5-GHz band with 4×4 MIMO demonstrates how Wave Scale technology and SmarTest 8 software can test over 4,000 test items, including transmitter, receiver, power-detection, DC, and functional test parameters. The Wave Scale technology includes the Wave Scale RF plus the Wave Scale MX, which includes 16 AWGs, 16 digitizers, 64 PMUs, a hardware sequencer, a real-time signal-processing unit, and a large waveform memory.

Complementing the Wave Scale cards, SmarTest 8 protocol-aware software works directly with user-defined register files and generates a protocol-aware sequence using device-setup APIs with no additional conversion required. The software supports the easy-to-implement flexibleA-Class parallel programming required for concurrent testing. An automated bursting capability works with any type of test, including DC, RF, and digital, and runs as fast as tests based on flat patterns, eliminating the need for manual test-time-reduction efforts, thereby providing an early throughput advantage.

In the 802.11ax example, the Wave Scale instruments powered by SmarTest 8 can test four transmitters concurrently in about 23 ms, vs. 80 ms for a serial-measurement approach, resulting in a test-time reduction of about 70%.

**Moving to 5G**

5G chips are appearing on the market and can be expected to find their way into 5G handsets and infrastructure equipment in the coming months as 5G deployments roll out. Such devices will increasingly need to rely on parallel test flows to handle the complexities of 5G while continuing to provide backwards compatibility with 3G and 4G technologies, and as they continue to support WLAN, GPS, ZigBee, Bluetooth, and various IoT connectivity applications.

With respect to 5G, new smartphones and other devices will achieve high peak speeds, and 5G will rely heavily on eMBB (enhanced mobile broadband). eMBB will provide not only improved data rates but also broadband everywhere, including in vehicles extending to high-speed trains. Coupled with carrier aggregation, eMBB provides a further example of the benefit for having a parallel test flow that goes hand in hand with test-time reduction and lower COT.

The Wave Scale cards, available now, stand ready to help customers keep pace with the parallel test demands of current and next-generation semiconductor devices.

  end .post_content

![](../images/parallelism-reduces-cost-of-test-for-iot-4g-5g-and-beyond-1.png)


![](../images/parallelism-reduces-cost-of-test-for-iot-4g-5g-and-beyond-2.png)
