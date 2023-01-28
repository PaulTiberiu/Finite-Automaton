# -*- coding: utf-8 -*-
"""
Code modifiable.
"""
from automate import Automate
from state import State
from transition import Transition
from myparser import *


#automate = Automate.creationAutomate("exempleAutomate.txt")
#automate.show("exempleAutomate")

#s1= State(1, False, False)
#s2= State(2, False, False)

#print (s1==s2)
#print (s1!=s2)

s0=State(0,True,False)
s1=State(1,False,False)
s2=State(2,False,True)

t1=Transition(s0,"a",s0)
t2=Transition(s0,"b",s1)
t3=Transition(s1,"a",s2)
t4=Transition(s1,"b",s2)
t5=Transition(s2,"a",s0)
t6=Transition(s2,"b",s1)
t=Transition(s0,"a",s1)
t7=Transition(s2,"b",s0)
t8=Transition(s2,"a",s1)
t9=Transition(s0,"b",s1)

auto2=Automate([t1,t2,t3,t4,t5,t6,t]) #creation d'automate version 1
auto1=Automate([t1,t2,t3,t4,t5,t6],[s0,s1,s2]) #creation d'automate version 2


print(auto2.succElem(s0,'a'))#premiere fonction teste
print("")
#test ex3 question 1
print("test q1")
l1=[s0,s1]
print(auto2.succ(l1,'a'))

#test ex3 question 2
print("")
print("test q2")
print(Automate.accepte(auto2,"abb"))
print(Automate.accepte(auto2,"a"))
print(Automate.accepte(auto2,""))

#test ex3 question 3
print("")
print("test q3")
print(Automate.estComplet(auto2,"ab"))
auto3=Automate([t1,t2,t3])
print(Automate.estComplet(auto3,"ab"))
#test ex3 question 4
print("")
print("test q4")
s3=State(3,True,False)
auto4=Automate([t1,t2,t3,t4,t5,t6],[s0,s1,s2,s3])
print(Automate.estDeterministe(auto4))
print(Automate.estDeterministe(auto2))
print(Automate.estDeterministe(auto3))
#test ex3 question 5
print("")
print("test q5")
print(Automate.completeAutomate(auto3,"ab"))
#test ex4

print("")
print("test ex4")

auto5=Automate([t1,t2,t3,t4,t5,t6,t7,t8,t9])
#print(Automate.determinisation(auto5))
print(Automate.estDeterministe(auto5))
print("")

t10=Transition(s0,"a",s2)
t11=Transition(s1,"a",s2)
t12=Transition(s0,"b",s1)
t13=Transition(s0,"b",s0)
t14=Transition(s2,"b",s0)
auto6=Automate([t10,t11,t12,t13,t14],[s0,s1,s2])
auto6=Automate.determinisation(auto6)
print(auto6)
print("test   ",Automate.estDeterministe(auto6))
#test ex5 q1
print("")
print("test ex5 q1")
auto3=Automate.complementaire(auto3,"ab")
print(auto3)
#test ex5 q2
print("")
print("test ex5 q2")
print("")
auto10=Automate.creationAutomate("exdeterminisation.txt")
auto11=Automate.creationAutomate("exdeterminisation2.txt")
auto10.show("lqlq")
auto11.show("lala")
auto12=Automate.intersection(auto10,auto11)
auto12.show("all")
#test ex5 q2
print("")
print("test ex5.2.1")
print("")
"""
auto10.show("lqlq")
auto11.show("lala")
auto12=Automate.concatenation(auto10,auto11)
auto12.show("all")
"""
