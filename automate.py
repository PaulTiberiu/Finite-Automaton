# -*- coding: utf-8 -*-
#Iordache Paul-Tiberiu
#Audigier Roman
import itertools
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        
        successeurs = []
        for state in listStates:
        	successeurs= successeurs+ [stateDest for stateDest in self.succElem(state,lettre) if stateDest not in successeurs]

        return successeurs
        #ou bien:
        """
        successeurs = []
        j = 0
        for i in range(0, len(listStates)):
            for t in self.getListTransitionsFrom(listStates[i]):
                if t.etiquette == lettre and t.stateDest not in successeurs:
                    successeurs.append(t.stateDest)
        return successeurs
        """


    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        liste=auto.getListInitialStates()
        if liste ==[]:
        	return False
        for lettre in mot:
        	liste=auto.succ(liste,lettre)
        for final in liste:
        	if final in auto.getListFinalStates():
        		return True
        return False
        
    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        for state in auto.listStates:
            chaineetiquette = ""
            for transition in auto.listTransitions:
                if state == transition.stateSrc:
                    chaineetiquette=chaineetiquette+transition.etiquette
            for a in alphabet:
                if (a not in chaineetiquette):
                    return False
                
            for l in chaineetiquette:
                if l not in alphabet:
                    return False

        return True
            
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        alphabet = auto.getAlphabetFromTransitions()
       	a = auto.listStates
       	c = auto.getListInitialStates()
       	if(len(c)==0 or len(c)>=2):
       		return False
       		
       	for i in a:
       		for j in alphabet:
       			b=auto.succElem(i,j)
       			if(len(b)>=2):
       				return False
       	return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        auto2 = copy.deepcopy(auto)
        if(Automate.estComplet(auto2, alphabet) != True):
        	a = auto2.listStates
        	poubelle = State(len(a),False,False)
        	for i in a:
        		for j in alphabet:
        			b = auto2.succElem(i, j)
        			if(b == []):
        				t = Transition(i,j,poubelle)
        				auto2.addTransition(t)
        return auto2
        
    @staticmethod
    def determinisation(auto) :
        """Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if Automate.estDeterministe(auto) == False:
            # On va creer l'etat initial et on l'ajoute a l'automate resultat
            compteID = 0#compteur de nombre d'etats
            listeInit = auto.getListInitialStates()
            etatInitial: State = State(
                compteID, True, False, str(set(listeInit)))#set donne l'ensemble et il range dans l'ordre les etats,str(set(listeInit))) etant le label(le nom)de notre etat

            # Le nouvel etat initial est final si au moins un des etats de la liste listeInit est final
            for etat in listeInit:
                if etat.fin:
                    etatInitial.fin = True
                    break

            # On va creer l'automate resultat avec notre etat initial
            autoRes = Automate([], [etatInitial], "")

            # On va recuperer l'alphabet de l'automate
            alphabet = auto.getAlphabetFromTransitions()

            # On va creer notre dico ID de l'ensemble d'etats
            dicoListe = {0: listeInit}

            # Ensemble des etats dont on doit calculer les transitions crees
            aTraiterEns = {etatInitial}
            # Ensemble des etats deja vu, donc a ne pas recalculer
            deja_vu = set()#on va avoir un ensemble vide
            # Pour stocker tous les nouveaux états à calculer
            tempEtats = set()
            # Un etat temporaire pour nos calculs
            etatTemp: State = etatInitial

            # Tant qu'on a des nouveaux etats a traiter
            while aTraiterEns != set():
                for aTraiterEtat in aTraiterEns:
                    for lettre in alphabet:
                        # Liste des successeurs
                        listeSucc = auto.succ(
                            dicoListe[aTraiterEtat.id], lettre)
                        # Creation du label de l'etat
                        labelEtat = str(set(listeSucc))
                        for etat in autoRes.listStates:
                            # On regarde si l'etat avec le label correspondant existe deja
                            if etat.label == labelEtat:
                                etatTemp = etat#on garde l'etat pcq il est deja ete cree(pas besoin de le faire) et on ajoute une transition
                                break
                        if etatTemp.label != labelEtat:
                            # Si le label est different c'est qu'il n'a pas ete fait
                            compteID += 1
                            # On incremente l'ID et on va creer l'etat
                            etatTemp: State = State(
                                compteID, False, False, str(set(listeSucc)))
                            dicoListe[compteID] = listeSucc
                            # On stocke la liste des etats correspondants a l'ID dans notre dictionnaire
                            for etat in listeSucc:
                                # On rend l'etat final s'il contient au moins un etat final
                                if etat.fin:
                                    etatTemp.fin = True
                                    break
                        if str(etatTemp) != "set()":
                            autoRes.addTransition(Transition(
                                aTraiterEtat, lettre, etatTemp))
                            # On va creer la transition de l'etat aTraiter a l'etat suivant
                            tempEtats.add(etatTemp)
                            # On ajoute le nouvel etat a notre ensemble des successeurs a calculer
                # | = Union pour les set!
                deja_vu = deja_vu | aTraiterEns
                # Les ensembles qu'on a traite deviennent deja vu
                aTraiterEns = tempEtats - deja_vu
                # Les prochains etats a calculer sont les successeurs
                # moins ceux deja visites
                tempEtats = set()

            return autoRes
        return auto

       			 
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        if Automate.estComplet(auto, alphabet):
            if Automate.estDeterministe(auto):
                lis = auto.listStates
                lfs = auto.getListFinalStates()
                for i in lis:
                    if i not in lfs:
                        i.fin = True
                for j in lfs:
                    j.fin = False
            else:
                auto=Automate.determinisation(auto)
                lis = auto.listStates
                lfs = auto.getListFinalStates()
                for i in lis:
                    if i not in lfs:
                        i.fin = True
                for j in lfs:
                    j.fin = False
        else:
            if Automate.estDeterministe(auto):
                auto=Automate.completeAutomate(auto, alphabet)
                lis = auto.listStates
                lfs = auto.getListFinalStates()
                for i in lis:
                    if i not in lfs:
                        i.fin = True
                for j in lfs:
                    j.fin = False
            else:
                auto=Automate.determinisation(auto)
                auto=Automate.completeAutomate(auto, alphabet)
                lis = auto.listStates
                lfs = auto.getListFinalStates()
                for i in lis:
                    if i not in lfs:
                        i.fin = True
                for j in lfs:
                    j.fin = False
        return auto
              
   #a revoir pour les explications
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        
        T = []
        done = []
        # On concatene les etats initiaux de auto1 et auto2 avec itertools. to_do liste de listes
        to_do = list(itertools.product(
            auto0.getListInitialStates(), auto1.getListInitialStates()))
	#to_do liste a 2 dimensions
        Dico = dict()

        i = 0

        alphabet = auto0.getAlphabetFromTransitions()

        while to_do != []:
            for l in alphabet:
                # Est ce qu'un des deux etats du couple a-t-il une transition vers un autre etat avec la lettre l
                if auto0.succElem(to_do[0][0], l) != [] and auto1.succElem(to_do[0][1], l) != []:
                    # Si oui on nomme ce couple todo
                    todo = to_do[0]
                    # On concatene les listes d'etats vers lesquels le couple peut se diriger
                    succ = list(itertools.product(auto0.succElem(
                        to_do[0][0], l), auto1.succElem(to_do[0][1], l)))#succ est une liste de couples vers lesquels todo peut se diriger,donc une liste de listes des etats
                    # On parcours cette liste via couple
                    for couple in succ:
                        # Est-ce que le couple todo est dans le dico ?
                        #on fait le str pcq les labels sont de type string donc l'id de notre dico
                        if str(todo) in Dico:
                            # Est-ce que le couple de successeurs vers lesquels le couple todo peut se diriger est dans le dico ?
                            if str(couple) in Dico:
                                # Si oui on ajoute alors les transitions du couple vers les etats de l'autre couple
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                # Si non, on cree l'etat et on ajoute ses transitions
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                # Puis on ajoute finalement le couple vers lequel le couple todo pouvait se diriger
                                Dico[str(couple)] = s
                                i += 1
                        else:
                            # Si non, on cree l'etat todo et on l'ajoute au dico
                            s = State(
                                i, todo[0].init and todo[1].init, todo[0].fin and todo[1].fin)
                            Dico[str(todo)] = s
                            i += 1
                            # Ici on recommence pour verifier si le couple vers lequel vont todo est deja dans Dico puis on ajoute les transitions.
                            if str(couple) in Dico:
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                Dico[str(couple)] = s
                                i += 1
                        # Si le couple vers lequel va todo n'est pas dans la liste to_do et n'est pas fini, alors on l'ajoute a to_do puis on va la traiter.
                        if couple not in to_do and couple not in done:
                            to_do.append(couple)
            done.append(to_do[0])
            to_do.remove(to_do[0])

        return Automate(T)



#??? jsp si ca marche bien(supplementaire)
    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        T = []
        done = []
        # On concatene les états initiaux de auto1 et auto2
        to_do = list(itertools.product(
            auto0.getListInitialStates(), auto1.getListInitialStates()))

        Dico = dict()

        i = 0

        alphabet = auto0.getAlphabetFromTransitions()

        while to_do != []:
            for l in alphabet:
                # Est ce qu'un des deux états du couple à-t-il une transition vers un autre état avec la lettre l
                if auto0.succElem(to_do[0][0], l) != [] and auto1.succElem(to_do[0][1], l) != []:
                    # Si oui on nomme ce couple todo
                    todo = to_do[0]
                    # On concatène les listes d'états vers lesquels le couple peut se diriger
                    succ = list(itertools.product(auto0.succElem(
                        to_do[0][0], l), auto1.succElem(to_do[0][1], l)))
                    # On parcours cette liste via couple
                    for couple in succ:
                        # Est-ce que ce couple est dans le dico ?
                        if str(todo) in Dico:
                            # Est-ce que la liste des états vers lesquels le couple peut se diriger est dans le dico ?
                            if str(couple) in Dico:
                                # Si oui on ajoute alors les transitions du couple vers les états de l'autre couple
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                # Sinon, on crée l'état et on ajoute ses transitions
                                s = State(
                                    i, couple[0].init or couple[1].init, couple[0].fin or couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                # Puis on ajoute finalement le couple vers lequel le couple todo pouvait se diriger
                                Dico[str(couple)] = s
                                i += 1
                        else:
                            # Si non, on crée l'état todo et on l'ajoute au dico
                            s = State(
                                i, todo[0].init or todo[1].init, todo[0].fin or todo[1].fin)
                            Dico[str(todo)] = s
                            i += 1
                            # Ici on recommence pour verifier si le couple vers lequel vont todo est déjà dans Dico puis on ajoute les transitions.
                            if str(couple) in Dico:
                                T.append(Transition(
                                    Dico[str(todo)], l, Dico[str(couple)]))
                            else:
                                s = State(
                                    i, couple[0].init and couple[1].init, couple[0].fin and couple[1].fin)
                                T.append(Transition(Dico[str(todo)], l, s))
                                Dico[str(couple)] = s
                                i += 1
                        # Si le couple vers lequel va todo n'est pas dans la liste to_do et n'est pas fini, alors on l'ajoute à to_do puis on va la traiter.
                        if couple not in to_do and couple not in done:
                            to_do.append(couple)
            done.append(to_do[0])
            to_do.remove(to_do[0])

        return Automate(T)
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        auto3 = copy.deepcopy(auto1)
        auto2bis = copy.deepcopy(auto2)

        final = False
		#on regarde si l'un des etats eset initial et final (donc accepte le mot vide) car ca veut dire que le 2eme automate doit etre initial.
        for a in auto3.getListInitialStates():
            if a in auto3.getListFinalStates():
                final = True
                break

        for s in auto3.getListFinalStates():
            s.fin = False

        i = len(auto3.listStates)

        for j in auto2bis.listStates:
            j.id = str(i)
            j.label = str(i)
            i += 1
            auto3.addState(j)

        for t in auto2bis.listTransitions:
            auto3.addTransition(t)

        listInitialAuto2 = auto2bis.getListInitialStates()

        for s in auto1.listStates:
            for l in auto1.getAlphabetFromTransitions():
                for sf in auto1.succElem(s, l):
                    if sf.fin:
                        for si in listInitialAuto2:
                            if final == True:
                                auto3.addTransition(Transition(s, l, si))
                            else:
                                si.init = False
                                auto3.addTransition(Transition(s, l, si))

        return auto3
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return




