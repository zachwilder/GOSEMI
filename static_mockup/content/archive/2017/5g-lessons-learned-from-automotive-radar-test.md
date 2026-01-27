---
title: "5G Lessons Learned from Automotive Radar Test"
slug: 5g-lessons-learned-from-automotive-radar-test
date: 
category: "Top Stories"
author: ""
excerpt: "Posted  in Top Stories"
original_url: "https://www.gosemiandbeyond.com/5g-lessons-learned-from-automotive-radar-test/"
---

Posted  in [Top Stories](https://www.gosemiandbeyond.com/category/topstories/)

# 5G Lessons Learned from Automotive Radar Test

*By Roger McAleenan, Director, Millimeter-Wave Test Solutions, Advantest America*

Situated between microwave and infrared waves, the millimeter-wave spectrum is the band of spectrum between 30 gigahertz (GHz) and 300GHz. It is used for high-speed wireless communications and is widely considered as the means to bring 5G into the future by allocating more bandwidth to deliver faster, higher-quality video, and multimedia content and services. Automotive radar is the entry point into millimeter wave for testing purposes.

Automotive radar has been evolving for the past several years, with Tier One companies producing and developing designs for a variety of different applications. As automotive is considered one of the key vertical markets for 5G technology – others include mobile broadband, healthcare wearables, augmented and virtual reality (AR/VR), and smart homes – radar systems in vehicles can provide valuable insight into the other millimeter-wave applications.

The 5G standard promises new levels of speed and capacity for mobile and wireless communications with greatly improved flexibility and latency compared to 3G and 4G/LTE technologies. However, its unique chip structures will create new challenges for test and measurement. By understanding the limits of test equipment, systems and hardware, we can better address the practical aspects associated with delivering on the promise of this technology.

**Test and measurement challenges
**From a measurement perspective, 5G and auto radar have functional characteristics in common that need to be measured, such as signal blockage, radiation interference and beamwidth selection. Another aspect is loss of signal penetration, an area where radar has an advantage over optical techniques that can be confounded by rain or snow. The band assigned to automotive radar, 76-81GHz provides greater accuracy in range resolution, and is sandwiched between point-to-point (P2P) bands on each side.**
**

The challenges to be addressed in 5G test are similar to those associated with automotive radar, as well. Challenges in millimeter-wave applications include:

- Handling multiple port devices economically
- Providing features and testing optimized for characterization and production
- Over-the-air environment due to packages with integrated antennas
- High-port-count switching/multiplexing (4×4, 8×8, etc.), often in the same device
- High levels of device features on a die– MCU + memory  + radio + high-speed digital

Multiple antennas improve power efficiency since more energy is pointed where it needs to be, and with steering, multiple targets can be tracked. This provides improvements to the capabilities and applications expand broadly to “surround” safety features, vehicle-vehicle coordination/communication.  The increased complexity in devices extends up to multiple combinations of transmit and receive.  This functionality will significantly improve vehicle-to-animal/human/object recognition and avoidance, as well as tracking more targets simultaneously.

Transceiver design is important, and they can be optimized as required as a low- or zero-intermediate frequency (IF) design. Automotive and 5G radios look nearly the same, with the similar IP blocks, e.g., phase shifters, local oscillators, RF amplifiers and mixers (Figure 1). The primary distinction is 5G radios’ modulation capability. Both may include up and down conversions, but for 5G, the market is looking for information bandwidth increase. This is actually pretty difficult from a test perspective because it requires elaborate analog equipment like high-performance oscilloscopes. This aspect is still a work in progress.

**Figure 1. Transceiver design in automotive and 5G systems is highly similar.**

Four main millimeter issues and considerations must be addressed in auto radar. This applies to 5G as well in that these four problems – rain attenuation, Fresnel zone, path loss, and ground reflection – are all problematic, whether you’re driving a car or the equipment is on a tower. Figure 2 shows all the areas in which radar is being used in cars, and further underscores the challenges associated with effective testing of these systems from a system level perspective.

**Figure 2. Radar zones in vehicles continue to multiply as automated content increases.**

One way to address some of the operational millimeter challenges is through beamforming. This is a technique that focuses the radar transmitter and receiver in a particular direction. Beamforming can be passive or active, although the former is limited in its effectiveness. Active RF beamforming, the increasingly preferred approach, will be gamechanging: it enables tracking multiple objects, both moving and static (people, vehicles, buildings, etc.) at various speeds, simultaneously. This allows auto radar to actively steer the beam toward objects and track them independently. Because the beam can be positioned with so many possibilities, testing in this way is currently a rhetorical question, although several automakers are working on solutions. For 5G, the beams would normally point either to other towers or to individual handsets and be able to track them. Basestations will have antenna arrays that can be steered to track people with 5G handsets – this will be an essential success factor in achieving the information bandwidth promise.

**Test lessons learned**

Advantest’s automated test equipment has been deployed for testing automotive radar for more than four years, testing from 18GHz to 81GHz, including wireless gigabit (WiGig) test in the 60GHz range, which may also be applicable to 5G.

At the moment, the focus remains on device test, but this is changing. Millimeter-wave applications provide an ideal opportunity to move away from component-level test and more toward higher-level models and end-to-end system-level testing. Figure 3 highlights the growing trends associated with system-level test. With that noted, here are some key lessons learned from Advantest’s work in the auto radar space, using its proven V93000 test platform.

**Figure 3. Demand and opportunity for system-level testing is on the rise.**

1. Power accuracy is critical. This will be very important to understand and address because, as we move closer to built-in self test (BIST), the device must be able to measure accurately the power it’s generating. Right now, we’re still learning how to get RF CMOS and BIST working together to give an accurate power measurement.
2. Metrology is difficult. Given the various connectors and waveguides that must be navigated, there are few reliable ways to perform accurate metrology of fixtures, connectors, loadboards, and other components. Also, there is the issue of system degradation – every time a new part is tested, it degrades slightly due to the materials used, and over time, the sockets or membranes that begin to deteriorate. In addition, when something finally needs to be changed out on the test system, recalibration must be performed, and that can cause a slight change in measurement results when combined with the degradation issue.
3. Limits need to be established. As devices grow more complex and better – and as efforts are made to extend radar range – two key factors come into play:

Phase noise – This key parameter on RF signals affects performance of radio systems in various ways. It’s important to understand at what point phase noise begins to impact performance    and the cost-benefit.
Noise figure – This measure of the degradation of the signal-to-noise ratio, caused by components in an RF signal chain, is essential to making radar more effective. The key question in this regard is, what’s the smallest signal I can see (relates to dynamic range)?
4. Millimeter “anything” is expensive. Currently, there are significant costs associated with millimeter-wave technology that will likely decline over the next few years. In the meantime, some chipmakers are trying to implement millimeter-wave technology for smaller end products, such as radar distance measuring devices, but they can’t build them because they can’t figure out how to test them economically on a small scale. The solution may rely on future technology that is still being developed.
5. Test engineering knowledge is scarce. This is perhaps the most critical factor of all – hence, saving it for last. The number of engineers working in millimeter technology is relatively small, and companies wanting to enter the space can’t simply materialize engineers versed in radar technology to help them with product development – particularly when the primary emphasis in most engineering programs is digital technology, rather than analog/RF. This means that talent is expensive, which can put a real damper on what companies are able to do. We need competent engineers to be trained that are strongly motivated and passionate about millimeter-wave.

**Summary**

Automotive radar technology is here now, and while it’s currently being seen primarily in premium-brand vehicles, the goal is to bring down the unit cost so that it becomes standard equipment throughout the automotive industry. To do this, a number of challenges must be addressed, including solving of the complexities associated with testing. Advantest is strongly committed to this market and in taking a leading role in finding these solutions and applying them to other millimeter-wave applications as the market continues to grow – including the fast-emerging 5G.

  end .post_content

![](../images/5g-lessons-learned-from-automotive-radar-test-1.png)


![](../images/5g-lessons-learned-from-automotive-radar-test-2.png)


![](../images/5g-lessons-learned-from-automotive-radar-test-3.png)
