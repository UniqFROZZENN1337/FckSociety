# FckSociety
SSH self-spreading worm

This is self-spreading worm through SSH. Warning its ILLEGAL in most of countries. Educational uses only.
It takes 4 steps.


#Step 1
_______________________
Scanning random ips with port 22 to check is there any SSH. It is done by nmap.


#Step 2
_______________________
Ips from step 1, which have already been verified, attacked by bruteforce. It is done by hydra.


#Step 3
_______________________
Credentials from step 2 needed to be verifed again, because hydra causes a lot of false positive results. They should be checked at this step.


#Step 4
_______________________
Copy itself to new machine through SSH. Attacking speed grow linear.

Development of this program now under step 2.


#How to start
_______________________
It is easy for use. Use install.sh to install dependencies and then just run main.py


#Also TODO
_______________________
Normal logging system.
Transfer data through redis.
Genetic algorithm.
