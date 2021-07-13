# NASA Capstone

**Website Link:** https://sites.google.com/view/projectargus/ <br/>

**Group Members:** <br/>
* Naimul Hoque
* Rishit Arora
* Abel Semma
* Oles Bober
* Edwin Varela

**Professor and TA:** <br/>
* Professor Yogananda Isukapalli
* TA Boning Dong

**Nasa Mentors:** <br/>
* John Karasinski
* Melodie Yashar

# Background and Overview

NASA astronauts perform maintenance and assembly procedures, which contain many complicated steps that are difficult to follow. As a result, astronauts are required to contact ground control for guidance. This poses a significant issue for future space exploration missions that require traveling to farther locations. For example, as astronauts prepare to head towards Mars, communication delay with ground control could take up to 20 minutes. With the help of NASA's Ames Research Center, Project Argus utilizes Machine Learning and Computer Vision concepts to develop a system that can track and validate each step of a procedure performed by an astronaut.

# Project Specification

**Nvidia Jetson Nano:** This development kit is the brains of the entire system. The Jetson Nano will be running our GUI and using various protocols to capture data from our cameras and perform inferencing on the data for part detection and stage validation purposes. Jetson Nano will also be used to train our object detection models. 

**Camera:** To collect our data, we will be using a single camera. We would either use a USB Camera that is connected to the Jetson or a Go Pro Camera which communicates with the Jetson using a transmission protocol.

**PhantomX Robotic Turret:** To test out our system, we will be assembling a PhantomX Robotic Turret. This turret contains various parts of all shapes and sizes that our system will be responsible for validating.

# Roles 

**Naimul Hoque** - Team Leader


**Rishit Arora** - Wireless Interface Design


**Abel Semma** - User Interface Design


**Oles Bober** - Model Training/Procedure Design


**Edwin Varela** - Model Training/Procedure Design


# Installation and Setup Guide. (NOT IMPLEMENTED)

To set up our project on your Jetson Nano, you will need to run the following commands:
```
mkdir ProjectArgus
cd ProjectArgus
git clone https://github.com/naimulhq/NASACapstone
cd NASACapstone
./install.sh
```


