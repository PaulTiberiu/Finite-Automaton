# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
#from myparser import *

#exercices prise en main

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

auto2=Automate([t1,t2,t3,t4,t5,t6,t]) #creation d'automate version 1
auto1=Automate([t1,t2,t3,t4,t5,t6],[s0,s1,s2]) #creation d'automate version 2

l1=[s0,s1,s2]
succ(l1,'a')
"""
#print(auto)
#auto.show("A_ListeTrans")

#auto1 = Automate.creationAutomate("auto.txt") creation d'automate version 3
print("avec t")
print(auto2)

auto2.removeTransition(t)
print("sans t")
print(auto2)

auto2.removeTransition(t1)
print("sans t1")
print(auto2)

auto2.addTransition(t1)
print("avec t1")
print(auto2)

auto2.removeState(s1)
print(auto2)

auto2.addState(s1)
print(auto2)

auto2.removeState(s1)
print(auto2)

s2=State(0,True,False)#ca va garder la premiere declaration de varbiable
auto2.addState(s2)
print(auto2)
#auto.show("A_ListeTrans")

print(auto1.getListTransitionsFrom(s1))
#auto1.show("A_ListeTrans")
"""

