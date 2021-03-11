# Fire-Safety-System
Fire Safety System model that combines the capabilities of OpenCV machine vision libraries and an evacuation system based on an Arduino microcontroller. 

## Demonstration:
![Demonstration](https://github.com/Brainsoft-Raxat/Fire-Safety-System/blob/main/photo_1.jpg?raw=true)
![](https://github.com/Brainsoft-Raxat/Fire-Safety-System/blob/main/photo_2.jpg?raw=true)

## Details about the system: 
- Fire and human detection features were developed by using computer vision library OpenCV for python and special object detection algorithms. 
- Evacuation system is based on Arduino microcontroller, which controls addressable led strips.
- Both systems work simultaneously and linked with each other.

## Advanatges:
- Unlike conventional systems using smoke detectors, this system will detect fire at the time of ignition.
- Led strips located on the floor indicate the way towards the exit in conditions of heavy smoke. 
- The system always tracks the number of people inside the building during evacuation.
- When fire is detected system saves images of the plan each 10 seconds to track the location of people.

## Disadvantages:
- CCTV cameras have limited viewing angle.
- System is not able to detect smoldering (burning slowly with smoke but not flame)

## Further development:
It would be better to use deep learning and neural networks to implement them in real life situations. There were attempts to use object detection algroithm YOLOv3 along with object tracking algorithm. However, due to lack of knowledge in Deep learning I only managed to train the neural network to detect fire. Human detection feature was already included in neural network. 
