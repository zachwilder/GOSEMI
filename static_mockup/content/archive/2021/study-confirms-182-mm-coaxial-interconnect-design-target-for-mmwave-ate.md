---
title: "Study Confirms 1.82-mm Coaxial-Interconnect Design Target for mmWave ATE"
slug: study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate
date: 
category: "Top Stories"
author: ""
excerpt: "Posted  in Top Stories"
original_url: "https://www.gosemiandbeyond.com/study-confirms-1-85-mm-coaxial-interconnect-design-target-for-mmwave-ate/"
---

Posted  in [Top Stories](https://www.gosemiandbeyond.com/category/topstories/)

# Study Confirms 1.82-mm Coaxial-Interconnect Design Target for mmWave ATE

*This article is a condensed version of an article published March 12, 2021, in *Microwave Journal*. Adapted with permission. Read the original article at *[https://www.microwavejournal.com/articles/35583-development-and-verification-of-a-185-mm-coaxial-interconnect-for-mmwave-ate](https://www.microwavejournal.com/articles/35583-development-and-verification-of-a-185-mm-coaxial-interconnect-for-mmwave-ate)*.*

*By Jose Moreira, Senior Staff Engineer, SOC R&D, Advantest*

The adoption of mmWave frequencies for applications such as 5G and WiGig creates new challenges for the ATE industry, including the need for a reliable blind-mate interconnection between the printed-circuit-board (PCB) test fixture and ATE measurement instrumentation. An ATE system requires multiple types of interconnects (**Figure 1**). Spring-pin interconnects predominate for power and digital. RF and mmWave signals require coaxial interconnects, due mainly to the isolation requirements, not just the frequency range. The ATE must also automatically mate to the PCB test fixture without any kind of manual interaction. 

*Figure 1: This depiction of Advantest’s V93000 ATE system top-side shows the different interconnects for digital, power, RF, and mmWave.*

A key requirement is interconnect reliability; for mmWave ATE applications, the interconnect must support 20,000 insertions while guaranteeing ATE system specifications. A reliability study demonstrates that a blind-mate 1.85-mm coaxial interconnect achieves this design target with a significant margin.

Figure 2 shows the bottom side of a mmWave ATE test fixture and the different mating interconnects. For the spring-pin-based interconnect, a plated via connects to the spring pin tip and to a PCB signal trace, which is then routed to the DUT. A coaxial mating connector handles RF and mmWave signals. A coaxial cable from the coaxial interconnect in the test fixture connects to another connector close to the DUT socket. Unlike a PCB signal trace, the coaxial cable provides layout flexibility and, more importantly, significantly lower loss, since even a thin coaxial cable is less lossy than the best PCB signal trace.1 

*Figure 2: This view of the bottom-side of an Advantest V93000 ATE test fixture shows the mating connectors and signal routing.*

**1.85-mm interconnect design**

Reference [2] describes the development of a 1.85-mm blind-mating interconnect design (Figure 3), which provides mode-free operation to 70 GHz with no interconnect failure for 20,000 docking cycles. The IEEE 287 standard-compliant3 1.85-mm female interface on the nonmating side of the interconnect uses off-the-shelf 1.85-mm cable assemblies to connect the blind-mating interface to the ATE measurement instrumentation and to the connector in the PCB test fixture close to the DUT. 

*Figure 3: The blind-mating spring-loaded 1.85-mm interconnect requires mode-free operation to 70 GHz with a guaranteed 20,000 docking cycles.*

Figure 4 shows the 1.85-mm blind mating connector pairs implemented on the ATE system and DUT test fixture sides. The system supports a maximum of 64 mmWave interconnects. The connector interface is spring-loaded on the male, ATE interface side and designed to self-align as the interface is mated. The mating action is part of the test fixture docking process to the ATE system. The ATE interconnect interface (Figure 2) comprises several interconnects apart from the 1.85-mm blind-mate connectors, all of which require a large docking force and, in turn, require special care with the mechanical design of the entire docking interface. This blind-mating interconnect requires a constant specific pressure on the entire mating surface to achieve the required 70-GHz frequency bandwidth. If this pressure is not correct or homogenous, effects like in-band resonances will appear in the interconnect frequency response.

*Figure 4. This illustration depicts 1.85-mm blind mating connector pairs implemented on the ATE system and DUT test-fixture sides.*

**Reliability measurement procedure**

Unfortunately, no clear guidelines have been published for evaluating the reliability of a blind-mate interconnection. Using the IEEE 287 standard3 as a guide and considering available resources, we developed a reliability test plan using a set of 14 connectors. Ten connectors were used for a docking cycle test to the maximum number of 60,000 insertion cycles. We measured S-parameters after every 300 cycles and removed the connectors to perform optical and mechanical measurements after every 6,000 cycles. Due to measurement resource limitations, we tested only two interconnects in parallel.

To eliminate the possibility that individuals in a pair become adapted to each other across the test run, after every 6,000 cycles, we exchanged the female of the pair between the two connectors being tested in parallel. Otherwise, measured reliability results could be significantly better than what you would find in a real application, where different test fixtures connect to different ATE systems through the lifetime of the connector.

Two other connectors were stressed to 60,000 cycles; in this case, only contact resistance measurements were performed every 300 cycles. Similarly, the same physical measurements and female connector exchange were performed every 6,000 cycles, as previously described.

Finally, the remaining two connectors in the measurement set were subjected to an accelerated life test, where they were left in a climatic chamber for 72 hours at 85°C and 85% humidity followed by the 60,000-docking-cycle test, with S-parameters measured every 300 cycles.

**Measurement results**

Our reliability testing strategy generated an enormous amount of data, which is summarized below and discussed in detail in Reference [4]. 

The S-parameter measurement setup consisted of an Anritsu MS4647B VNA and a 4-port extension MN4697B as well as Megaphase RF Orange 1.85-mm measurement cables. The VNA was used without calibration, so the loss shown includes both the coaxial cables’ and the VNA’s intrinsic loss. We employed this approach because our objective is to measure variations of interconnect performance over an increasing number of docking cycles, not the intrinsic connector performance. 

Figure 5 shows the interior of one connector pair before the test, at 30,000 cycles, and at 60,000 cycles, showing degradation of the socket side in the female of the pair. 

*Figure 5: These successive images depict the interior of the connector pairs at different numbers of cycles.*

Figure 6 shows the measured S-parameters after 60,000 insertion cycles. Since S-parameter measurements were performed every 300 cycles, the graph contains 200 overlaid plots. After cycle 54,000, a resonance appeared in the measured insertion loss around 20 GHz, revealing a failure of the interconnect, even though it continued working at higher mmWave frequencies. The cause for the failures was a crack in one of the socket fingers. This is the same mechanism seen with all failed connector pairs—not surprising since finite-element mechanical simulation shows this point has the highest mechanical stress during connector mating.4

*Figure 6. After cycle 54,000, a resonance appears in the measured insertion loss at around 20 GHz.*

Figure 7 shows the measured |S11| and |S21| parameters for a connector with no resonance failures during the entire 60,000-cycle test. This measurement was done with a fully calibrated VNA before the start of the test and after the entire 60,000 cycles. The results show even after 60,000 cycles, measured insertion and return loss are still acceptable.

*Figure 7. This diagram shows the measured |S11| and |S21|** for a connector with no resonance failures during the entire 60,000-cycle test.*

**Additional considerations**

Although from a test and measurement perspective, electrical performance is the critical metric, the IEEE 287 standard defines several mechanical metrics, including the connector socket’s withdrawal and insertion forces.3 Another important metric is concentricity, the difference between the center of the inner and outer diameters of the socket and pin. In addition, computed tomography (CT) provides additional information regarding connector reliability. **Figure 8** compares the surface of the original connector at cycle 0 to the connector’s surface at cycles 12,000 to 60,000 by visualizing the deviation in microns of the connector surface compared to cycle 0. Resolution is in the range of single-digit microns. 

*Figure 8: CT scans performed on one of the interconnect female connectors at different stages of the cycle testing show successive deviations.*

And finally, it is worth noting that the 1.85-mm connector standard offers many advantages for the blind-mate interface. For example, the long length of mechanical engagement of the adapter housing protects the center conductor while acting as an electromagnetic interference shield. A recent *Microwave Journal* article,5 on which this article is based, provides more information on the connector, mechanical metrics, concentricity, and CT scanning as well as additional details on our connector reliability test plan and on the mechanical finite-element simulations we used to confirm the specific failure mechanism we detected.

**Conclusion**

Our reliability study of a blind mate 1.85 mm coaxial interconnect for ATE mmWave applications shows that the target of 20,000 insertions was achieved with a significant margin, since all the connectors in the study failed above 40,000 cycles, excluding the connectors that had the accelerated life procedure performed. 

**Acknowledgments**

We thank Kosuke Miyao, Andy Richter, Marc Moessinger, and Matthias Feyerabend from Advantest; the Advantest failure-analysis lab in Gunma, Japan; and Eric Gebhard from Signal Microwave. We also thank Professor Sven Simon and Peter Gaenz from the Department of Parallel Systems at the Stuttgart University for the CT scan measurements.

**References**

1. J. Moreira and H. Werkmann, Automated Testing of High-Speed Interfaces, Artech House, Second Edition, 2016.
2. B. Rosas, J. Moreira, and D. Lam, “Development of a 1.85 mm Coaxial Blind Mating Interconnect for ATE Applications,” IEEE International Microwave Symposium, 2017.
3. “IEEE Standard for Precision Coaxial Connectors (DC to 110 GHz),” IEEE 287-2007, September 2007.
4. A. J. Rodrigues Mendes, Reliability Evaluation of a 1.85 mm Blind Mating Coaxial Interconnect for mmWave ATE Applications, Master of Science Thesis, Instituto Superior Técnico, University of Lisbon, 2020. fenix.tecnico.ulisboa.pt/downloadFile/845043405507284/Final_Thesis_Antonio_81353.pdf.
5. Moreira, Jose, et al., “Development and Verification of a 1.85 mm Coaxial Interconnect for mmWave ATE,” Microwave Journal, March 12, 2021. https://www.microwavejournal.com/articles/35583-development-and-verification-of-a-185-mm-coaxial-interconnect-for-mmwave-ate

**Captions**

*Figure 1: This depiction of Advantest’s V93000 ATE system top-side shows the different interconnects for digital, power, RF, and mmWave.*

*Figure 2: This view of the bottom-side of an Advantest V93000 ATE test fixture shows the mating connectors and signal routing.*

*Figure 3: The blind-mating spring-loaded 1.85-mm interconnect requires mode-free operation to 70 GHz with a guaranteed 20,000 docking cycles.*

*Figure 4. This illustration depicts 1.85-mm blind mating connector pairs implemented on the ATE system and DUT test-fixture sides.*

*Figure 5: These successive images depict the interior of the connector pairs at different numbers of cycles.*

*Figure 6. After cycle 54,000, a resonance appears in the measured insertion loss at around 20 GHz.*

*Figure 7. This diagram shows the measured |S**11**| and |S**21**| for a connector with no resonance failures during the entire 60,000-cycle test.*

*Figure 8: CT scans performed on one of the interconnect female connectors at different stages of the cycle testing show successive deviations.*

  end .post_content

![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-1.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-2.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-3.jpg)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-4.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-5.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-6.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-7.png)


![](../images/study-confirms-182-mm-coaxial-interconnect-design-target-for-mmwave-ate-8.jpg)
