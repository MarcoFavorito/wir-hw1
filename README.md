# wir-hw1

Repository for the homework 1 of the class "Web Information Retrieval", using the software MG4J.

#### repo structure
- **src**: the source code of the homework;
- **data**: contains the [Cranfield Dataset](http://www.diag.uniroma1.it/~fazzone/Teaching/WebIR_2016_2017/Homework_1__2016_2017/Cranfield_DATASET.zip);  
- **libs** : all the libraries (`.jar`), including MG4J classes. **NOTICE:** there is also a `jar` called `homework.jar`, provided by the tutor, where there are some utils;  
- **resources**: some useful resources provided by the tutor.

#### setup
First of all, clone this repository:
```
git clone https://github.com/MarcoFavorito/wir-hw1.git
```
If you want to use MG4J from the command line, you have to set some environment variables. The script `set-my-classpath.sh` will help you. Use it as the following:
```
# Go with your terminal in the repository path
# Enable execution right for the script
chmod +x set-my-classpath.sh
. ./set-my-classpath.sh libs
```


#### links:  
 - [Class website](https://piazza.com/uniroma1.it/spring2017/1018570/home)
 - [MG4J official site](http://mg4j.di.unimi.it/)
