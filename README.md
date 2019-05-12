# social robot
a social robot is an autonomous robot that interacts and communicates with humans or other autonomous physical agents by following social behaviors and rules attached to its role.

this project deals with creation of such a social robot from scratch. currently the repo includes the code for design and implementation of the software side of the project.  

refer to [the final project report]() for more details on the hardware side and the exact implementation details.

## overview
the project makes use of several python modules, as well as android packages. to set up a basic working environment you can run the install script provided within the project. 

## achievement
this project was my mini-project(a.k.a design project) for junior year(3rd year) in my college and it **won the best computer science project award.**

## installation

if your system doesn't have any python3.x yet, then do install it first before going forward.  

on  your linux/mingw terminal, assuming that you're at the root of this project:  
```bash
chmod +x ./install.sh
./install.sh
```
this installs all the python modules and sets the environment.  

the best possible way to install the android packages is to open up the android project ```./code/AndroidUSBCam``` in Android Studio and let it automatically sync the project.

## how to use this project?

### training a model
```bash
cd ./code/classification
```
the dataset needs to be collected and it should be present in the directory ```code```, with the name ```dataset```. After that we have to expand the dataset, for that run:  
```bash
python3 generate_dataset.py
```
after the dataset is generated in the folder ```make_dataset/filtered_dataset```, we start the training process by:  
```bash
python3 constants.py
python3 training.py
```
after training we get an svm trained model. copy that model to the directory named ```server``` in the root of the project.  
***we collected nearly 5000 images of different daily objects and do note that the dataset generation and the training process can take nearly 1 full day or more to complete***  

### setting up the android app
a minimum of sdk23 needs to be installed in your system. the project used ndk10 specifically to run the native scripts. make sure that these kits are downloaded from withing android studio.  

after that open up the android project from ```./code/AndroidUSBCam``` and sync and install the necessary packages.  

after building the app, make sure that your change the variable ```URL``` to the ip address of your system. the ip address of your system could be found out by running the ```ip addr``` command in the terminal.  
```java
public static final String URL = "your ip address";
```

now rebuild the project and install it to your phone.

### setting up the arduino ide
download and install the arduino IDE. for linux 64 use  this link ```https://www.arduino.cc/download_handler.php?f=/arduino-1.8.7-linux64.tar.xz```.  
after untarring the tar file, open up the arduino IDE(with sudo privileges obviously) and run the code at ```./code/arduinoIDECode/firmata_code.c``` in the IDE, into the arduino connected via USB to your system.

### running the server
open up a terminal and do the following:  
```bash
cd ./code/server/
```
then become super user by running the ```su``` command in terminal.  
after that run:  
```bash
python3 server.py
```
and thats it. we are done with the software side.

### presentation and report
the report and presentation are available in the ```./presentation``` and ```./report``` directories.  
if you want to edit and compile the project, then look into the ```tex``` files in the compile directory.
