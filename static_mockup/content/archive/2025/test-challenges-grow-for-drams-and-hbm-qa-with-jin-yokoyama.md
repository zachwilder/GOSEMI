---
title: "Test Challenges Grow for DRAMs and HBM – Q&A with Jin Yokoyama"
slug: test-challenges-grow-for-drams-and-hbm-qa-with-jin-yokoyama
date: 
category: "Q&A"
author: ""
excerpt: "Posted  in Q&A"
original_url: "https://www.gosemiandbeyond.com/test-challenges-grow-for-drams-and-hbm/"
---

Posted  in [Q&A](https://www.gosemiandbeyond.com/category/qa/)

# Test Challenges Grow for DRAMs and HBM – Q&A with Jin Yokoyama

*This article is adapted with permission from a Q&A with Advantest’s ***Jin Yokoyama***, senior director and memory product marketing manager, with Mark LaPedus from *[Semiecosystem](https://marklapedus.substack.com/)*. The original article can be viewed *[here](https://marklapedus.substack.com/p/test-challenges-grow-for-drams-and)*.*

**Q. In general, how do we test the latest DRAMs? Isn’t there a test flow involved here? Can you briefly describe the basic test flow for DRAMs and each step?******

A. Typically, for DRAM devices, the test flow starts with wafer-level test. At the wafer level, our test systems apply memory test algorithms at varying speeds to test DRAM performance. The DRAM device is then tested again after it is assembled into a package. The final test stage runs tests at operational speed to confirm whether the device processes data correctly and meets end-use requirements.

 

**Q. Over the years, DRAMs have become more complex. What are some of the technology trends that you see with current and future leading-edge DRAMs?**

A. We see myriad trends emerging as DRAM technology evolves. DRAM devices are playing a critical role across a variety of applications, including artificial intelligence (AI)/high-performance computing (HPC), data centers, smartphones, AI PCs, and video game consoles.****

The growth of AI, specifically, has led to an increase in demand for DRAM devices with higher per-pin speed, higher bandwidth, and low latency. Meanwhile, data centers and AI edge applications require devices to integrate new industry standards for speed and power consumption, including GDDR7, LPDDR6, and HBM4. These devices must also have lower output levels to maintain accuracy and higher operational efficiency to reduce cost.

We also see the trend of miniaturization and the shrinking of bit cells. There is a shift in size to 3,000 devices under test (DUTs) per 300mm wafer, leading to higher density that makes DRAM devices more vulnerable to defects. This means that these devices will likely require more tests and screening to meet demands for quality and reliability. Further densification of tester resources and technology will be necessary to accommodate device miniaturization trends.

**Q. What are some of the test challenges with the latest DRAMs?**

A. The increasing speed of these devices certainly presents a challenge in the test process. Speed performance requirements for at-speed interface testing on DRAM devices are increasing from 4.5 Gbps to over 10 Gbps, requiring high-performance test equipment to run test algorithms at high operational speeds.

We also need test systems that can test more devices in parallel to maintain lower costs. This requires highly specialized probe card technology that can handle high-speed testing. Massive levels of parallelism will be vital, as the industry trends toward requiring only one touchdown per wafer. Miniaturizing DRAM devices also makes them more susceptible to defects, requiring more thorough testing in the form of burn-in test at the wafer and package levels. Moreover, thermal requirements for DRAM devices continue to rise alongside demands for higher power and bandwidth capacity, and the complexity of integrating DRAM in 2.5D/3D packaging poses its own set of unique test challenges.

In the DRAM market, where high bandwidth and high performance continue to increase, Advantest recently introduced a next-generation ultra-high-speed solution, the T5801. This cutting-edge platform is engineered to support the latest advancements in high-speed memory technologies – including GDDR7, LPDDR6, and DDR6 – critical to meeting the growing demands of AI, HPC, and edge applications.

**Q. What are some of the technology trends and challenges that you are seeing with HBM?**

****A. AI and HPC devices are demanding higher and higher processing speeds to power advanced applications like large-language models (LLMs). HBM consists of multiple DRAM chips stacked vertically. This structure allows for faster and more efficient data transfer with a smaller footprint, which is why HBM plays a key role in data centers. Of course, these HBM devices are incredibly complex and pose various challenges during testing. With multiple DRAM ICs stacked on top of each other, these devices are extremely dense and produce a lot of heat, which poses a risk to the structure of the device. Test systems must be equipped with the proper thermal-management capabilities and refined handler/probe equipment needed to monitor potential hotspots and dissipate heat.

The density of device circuitry and the number of DRAM devices stacked is increasing with each generation of HBM, moving from 8 stacks to 12, 16 and even 24. This has led to longer test times, especially as HBM migrates much faster than traditional memory technology transitions by generation. Higher interface speeds and higher bandwidth of HBM devices also mean high test speed and an increased load on peripheral circuits, requiring high-speed probing technology. Moreover, increases in power supply and current capacity require scalability.

The 2.5D/3D packaged structure of HBM devices also poses significant challenges, requiring thorough testing before the devices are packaged together. More and more manufacturers are looking to utilize die-level test, i.e., testing individual die after the wafer has been diced, to ensure that the DRAM ICs function properly before they are stacked into an HBM device and packaged, increasing overall yield and reliability. “Known-good die” or KGD testing, as it’s sometimes called, helps to prevent manufacturers from assembling packages containing defective die. If even one die in a stack is defective, then the entire package must be disposed of at great cost to the manufacturer.

******Q. Are there any test challenges when the industry migrates to HBM4?**

A. The greatest challenge we will see is the rising complexity of HBM4 devices. HBM4-based logic wafers are being made at leading-edge logic foundries for use in high-performance data centers to power AI edge applications. This will make the supply chain more complex, and the requirements and manufacturing and testing processes for DRAM manufacturers, foundries, and SoCs will also become more complex as a result. So, more advancements will have to be made in test process optimization in the future to support the next generation of HBM.

  end .post_content