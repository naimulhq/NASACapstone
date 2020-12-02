# NASA Capstone
Group Members: <br/>
* Naimul Hoque
* Rishit Arora
* Oles Bober
* Edwin Varela
* Abel Semma

Professor and TA: <br/>
* Professor Yogananda Isukapalli
* TA Boning Dong

Nasa Mentors: <br/>
* John Karasinski
* Melodie Yashar

# External Behavior Specification

**Purpose:** The Astronaut Procedure Tracker is designed to help an individual perform a specific task by tracking each step using various cameras and sensors. Utilizing concepts such as computer vision and machine learning, our system will help an individual assemble a PhantomX Pan Tilt Robotic Turret. The system will keep track of each step the individual is on, and validate to ensure that it is being done correctly. If a person has not completed a specific step, or has completed a step incorrectly, the system must be able to notify the user about the issue before moving on. The assembly of the robotic turret will be split into ‘stages’. Each stage corresponds to a significant portion of the robotic turret. Additionally, screws will be stored in a container or bag with a QR Code to differentiate each screw.

**Nvidia Jetson Nano:** The following development kit is well known for computer vision and machine learning applications. The development kit will be interfacing with various sensors and cameras using specific protocols. 

**Raspberry Pi Camera (1):** The Nvidia Jetson Nano comes with four USB ports. These ports will be utilized to interface with two different cameras. Our goal is to have two different cameras on a table oriented in different angles to capture visual data. The Jetson will be on the table as well.

**GoPro Wifi Camera(1):** Since an individual might be moving around for extended periods of time, we decided to attach a camera onto the individual’s waist or head which will communicate through Wifi. As a result, there is no need to keep the Jetson on the person and instead, have only a camera attached.

**LCD Display or Monitor:** Our system needs to find a way to communicate with the individual about what task they are currently working on and if it is being done properly. We will use either an LCD Display or Monitor as our output device. Not only should the output device show the task being worked on but should put the feed from the camera with a bounding box on the tools and parts needed for that specific step.

# Identification of Roles (Roles are tentative for now)
**Rishit Arora**
* Communication between Cameras and Sensors with the Nvidia Jetson Nano using common Networking Protocols (Interface / Data Transmission)
* Figuring out Image Detection using different Open-Source Object Detection packages (ML / AI Training) <br/>
**Oles Bober**
* Hardware assembler, Interface / Data Transmission <br/>
**Naimul Hoque**
* Team Leader.
* ML/AI Training
* QR Code Integration <br/>
**Edwin Varela**
* ML/AI training.
* QR Code  <br/>
**Abel Semma**
* Work with Python GUI frameworks to create the User Interface
* Work with Edwin and Naimul on the AI/ML training to integrate our systems <br/>

Hardware Assembly

**ML / AI Training -**  This individual(s) is responsible for creating a custom dataset for different tools that will be used in the assembly process. Responsible for utilizing different software packages to train a model and use the model for object detection purposes.

**Interface / Data Transmission -** This individual(s) is responsible for determining how to use the Nvidia Jetson TX2 to interface with different sensors and cameras using different protocols such as UART and I2C.

**QR Code Integration -** This individual(s) is responsible for generating QR Codes that are used to differentiate components that make up the assembly of the Robotic Turret. Responsible for using Computer Vision to detect and decode April Tags.

**User Interface -** This individual(s) is responsible for designing a user interface that allows  the user to choose a specific procedure and lets them view the current step that is being performed.

**LCD/Monitor Configuration -** The individual(s) is responsible for figuring out how to interface the Monitor or LCD Display with the Jetson. In addition, this individual(s) will be working with the User Interface to determine how to put the live feed on display.

**PCB Design:** This individual(s) is responsible for designing and printing the necessary circuit boards for the project. Have not determined if this will be necessary.
