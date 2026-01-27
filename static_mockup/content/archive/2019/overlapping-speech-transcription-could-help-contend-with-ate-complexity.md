---
title: "Overlapping Speech Transcription Could Help Contend with ATE Complexity"
slug: overlapping-speech-transcription-could-help-contend-with-ate-complexity
date: 
category: "Top Stories"
author: ""
excerpt: "Posted  in Top Stories"
original_url: "https://www.gosemiandbeyond.com/overlapping-speech-transcription-could-help-contend-with-ate-complexity/"
---

Posted  in [Top Stories](https://www.gosemiandbeyond.com/category/topstories/)

# Overlapping Speech Transcription Could Help Contend with ATE Complexity

*By Keith Schaub, Vice President of Business Development for US Applied Research & Technology, Advantest America Inc.*

**Introduction**

Increasingly complex chipsets are driving corresponding increases in semiconductor test system hardware and software. Artificial intelligence offers innovative, ingenious opportunities to mitigate the challenges that test engineers and test-system operators face and to improve security and traceability. Advantest, which fields thousands of test systems worldwide that test billions of devices per year, is studying several ways in which AI can help.

Initial work has involved facial recognition and overlapping speech transcription (the latter being the focus of this article), both of which can reduce the need for a mouse and keyboard interface. With a mouse and keyboard, operators can leave themselves logged in when other operators take over, creating security vulnerabilities and making it difficult, for example, to trace which operator was on duty during a subsequently detected yield-limiting event. A voice-recognition system could facilitate identifying which operators gave which commands.

**Industrial cocktail-party problem**

Implementing a voice-recognition system in a test lab or production floor presents its own challenges, with air-cooled systems’ fans whirring and multiple teams of engineers and operators conversing—creating an industrial version of the cocktail-party problem.

To address this problem, Advantest has developed fast, multi-speaker transcription system that accurately transcribes speech and labels the speakers.

The three main steps in the transcription process include speaker separation, speaker labeling, and transcription. For the first step, a real-time GPU-based TensorFlow implementation of the deep-clustering model recently developed by Mitsubishi1 separates the mixed-source audio into discrete individual-speaker audio streams. A matrix of audio-frequency domain vectors obtained by the short-time Fourier Transform (STFT) serves as the input to this model. The model learns feature transformations called embeddings using an unsupervised, auto-associative, deep network structure followed by a traditional k-means clustering method (recent implementations have shown significant improvements over traditional spectral methods) that output the clusters used to generate single-speaker audio.

The second step involves an implementation of Fisher Linear Semi-Discriminant Analysis (FLD)2 for an accurate diarization process to label the speakers for each audio stream that the clustering model generated in the separation step. The third and final step makes use of the Google Cloud speech-to-text API to transcribe the audio streams, assigning a speaker based on the diarization step.

*Figure 1: This system-flow diagram illustrates the steps in the overlapping speech-transcription process, from the audio input to the labeling of the speakers.* 

Figure 1 illustrates the system flow of the entire process. During the first step, the clustering separates the audio. The spectrogram of the mixed and separated audio (Figure 2) makes it easy to visualize the separation taking place.

*Figure 2: A view of the spectrogram of the mixed and separated audio helps illustrate how the separation takes place. * 

**Testing the model**

We tested the model on the TED-LIUM Corpus Release 3,3 which is a collection of TED Talk audio and time-aligned transcriptions. To measure the system accuracy, we compared our system-generated transcriptions to the ground-truth transcriptions using Word Error Rate (WER), denoted by the proportion of word substitutions, insertions, and deletions incurred by the system. Our system demonstrated a WER of 26% versus a ground-truth WER of approximately 14%. Overall, the generated transcripts were largely intelligible, as shown by the following example:

- Actual Audio

“Most recent work, what I and my colleagues did, was put 32 people who were madly in love into a function MRI brain scanner, 17 who were. . .”

- System Transcription

“Most recent work but I am my colleagues did was put 32 people who are madly in love into a functional MRI brain scanner 17 Hoover.”

As shown, the results are largely readable, even with the current word error rate.

Often, the audio output from the Separation Step contains many artifacts, which lead to outputs readily understood by humans but that are more difficult for current speech-to-text converters. Thus, we get an output like this:

- Actual Audio

“Brain just like with you and me. But, anyway, not only does this person take on special meaning, you focus your attention on them…”

- System Transcription

“Brain, it’s like with your and name. But anyway, I don’t leave something special meeting. I’m still get your attention from you a Grande, AZ them…”

Thus, when the clustering algorithm becomes unstable, the transcription is also erroneous. However, many of these errors can likely be fixed in future work.

Overall, overlapping speech has presented a daunting problem for many applications including automated transcription and diarization. But recent innovations in learned-embeddings for speaker segmentations make it possible to produce accurate, real-time transcription of overlapping speech. The clustering model is the most computationally expensive step, but because it is implemented in TensorFlow and it is GPU-optimized, the system can run in real time. In short, recent research in learned embeddings allows for higher accuracy transcription of overlapping speaker audio.

Nevertheless, implementations of such systems are currently very limited due to relatively low accuracy, which we believe is likely the result of the clustering model using binary (discrete) masks1 to output the audio of each speaker. We will investigate continuous masking to further improve the audio quality well enough to be used for live transcription for live events.

**Virtual engineering assistant for ATE**

Ultimately, we envision AI techniques such as overlapping speech transcription to be useful in developing an AI-based engineering assistant for ATE, as outlined in a presentation at the 2018 International Test Conference. In the high-decibel environment of the test floor, overlapping speech transcription could help solve the cocktail-party problem, allowing the virtual assistant—a test engineering equivalent of Iron Man J.A.R.V.I.S—to respond to one particular engineer or operator.

Overlapping speech transcription is just one way of interacting with such an assistant. At Advantest, we have also experimented with facial recognition, using software that can create what is essentially a “face fingerprint” from one image, eliminating the need of traditional networks for thousands of images for training. We have found that the technology performs well at a variety of angles (photographing the subject from 30 degrees left or right, for example) and at a variety of distances (image sizes). Eventually, such technology might enable the virtual assistant to proactively intervene when recognizing a look of frustration on an engineer’s face and intuiting what information may be helpful in solving the problem at hand.

Beyond speech-transcription and facial-recognition capabilities, a virtual engineering assistant would embody a wealth of highly specialized domain knowledge, with many cognitive agents offering expertise extending from RF device test to load-board design. Such an assistant would be well versed in test-system features that might only be occasionally required over the long lifetime of expensive equipment with a steep learning curve. Ultimately, such an assistant could exhibit intuition, just as do game-playing AI machines that have mastered “perfect information” games like checkers and chess and have become competitive at games like poker, with imperfect information and the ability to bluff. Although computers haven’t traditionally thought to be intuitive, it might turn out that intuition evolves from deep and highly specialized knowledge of a specific domain.

**References**

1. Hershey, John R., et al., “Deep Clustering: Discriminative Embeddings for Segmentation and Separation,” *2016 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 2016. [https://ieeexplore.ieee.org/document/7471631](https://ieeexplore.ieee.org/document/7471631)

2. Giannakopoulos, Theodoros, and Sergios Petridis, “Fisher Linear Semi-Discriminant Analysis for Speaker Diarization,” *IEEE Transactions on Audio, Speech, and Language Processing*, vol. 20, no. 7, 2012, pp. 1913-1922. [https://ieeexplore.ieee.org/document/6171836](https://ieeexplore.ieee.org/document/6171836)

3. Hernandez, François, et al., “TED-LIUM 3: Twice as Much Data and Corpus Repartition for Experiments on Speaker Adaptation,” *Speech and Computer Lecture Notes in Computer Science*, 2018, pp. 198-208. [https://arxiv.org/abs/1805.04699](https://arxiv.org/abs/1805.04699)

Did you enjoy this article? [Subscribe](https://visitor.r20.constantcontact.com/manage/optin?v=001y_Bo5goCBKQ5mpCMPMk9NZ99QMnLrLlllSx9KsYRBGtAwx3BUnAXKOaTpnrPkps9ENqJ2xavSS4iHZoRcF3vbOUMslAszWh5o0QemBpi7ixX88dplnKCbCc1wBocZnWqQunAJgFjTckoqFGgqvpIFXY1CeP37TR15PDr8yiOViQ%3D) to GOSEMI AND BEYOND

  end .post_content

![](../images/overlapping-speech-transcription-could-help-contend-with-ate-complexity-1.png)


![](../images/overlapping-speech-transcription-could-help-contend-with-ate-complexity-2.png)
