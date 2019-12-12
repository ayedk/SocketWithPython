
import socket
import sys
import ast
from threading import *
from socketserver import *
import os
import threading
import time
threads=[]

HOST = '127.0.0.1'  
PORT = 5004        
SIZE = 2048


lock = threading.Lock()



class ClientThread(Thread):
    def __init__(self,ip,port,connexion):
            Thread.__init__(self) 
            self.ip = ip 
            self.port = port
            self.connexion=connexion
            print ("*****************New socket thread launched *****************")

    
    
    def run(self):


        def SignInParticipant(IP):
            File1=open('participant.txt','r')
            data=File1.readlines()
            File1.close()

            File3=open('participant.txt','w')
            File3.write('       '+str(len(data)+1)+'                      '+str(IP)+'    \n')
            File3.close()
        

        def ParticipantExists(IP):

                f=open('participant.txt','a')
                f.close()
                f=open('participant.txt','r')
                lines=f.readlines()
                Exists =False
                for participant in lines:
                    List= participant.split()
                    if (IP==List[1]):
                        Exists=True
                f.close()
                return Exists 


        def SearchID(ip):
            File1=open('participant.txt','r')
            for participant in File1:
                L= participant.split()
                if (L[1] == ip):
                    return(L[0])

        def EnvoyerBien(self):
            f = open("bien.txt",'r')
            data = f.read()
            f.close()
            self.connexion.sendto(data.encode(),(self.ip,self.port))
        
        def Changeprix(ref,prix):
            f = open("bien.txt","r")
            lines=f.readlines()
            f.close()
            pos=0
            for report in lines:
                pos+=1
                L=report.split()
                if(L[0]==ref):
                    break
            L[3] = prix
            lines[pos-1]='   '+str(L[0])+'                  '+str(L[1])+'                    '+str(L[2])+'                 '+str(L[3])+'                 '+str(L[4])+'                 \n'
            lock.acquire()
            f = open("bien.txt","w")
            f.writelines(lines)
            lock.release()
            f.close()

        def ChangerEtat(ref,id):
            f = open("bien.txt","r")
            lines=f.readlines()
            f.close()
            pos=0
            for report in lines:
                pos+=1
                L=report.split()
                if(L[0]==ref):
                    break
            L[2] = 'Vendu'
            L[4] = id
            lines[pos-1]='   '+str(L[0])+'                  '+str(L[1])+'                    '+str(L[2])+'                 '+str(L[3])+'                 '+str(L[4])+'                 \n'
            lock.acquire()
            f = open("bien.txt","w")
            f.writelines(lines)
            lock.release()
            f.close()


        def SearchCurrentPrice(ref):
            f = open('bien.txt','r')
            lines=f.readlines()
            f.close()
            for report in lines:
                L=report.split()
                if(L[0]==ref):
                    return int(L[3])

        EnvoyerBien(self)
        if ((ParticipantExists(self.ip)==False)):
                SignInParticipant(self.ip)
        
        def SearchEtat(ref):
            f = open('bien.txt','r')
            lines=f.readlines()
            f.close()
            for report in lines:
                L=report.split()
                if(L[0]==ref):
                    return str(L[2])


        def Ajoterfacture(id,tot):
            f = open('facture.txt','a')
            f.close()
            f = open('facture.txt','r')
            lines=f.readlines()
            f.close()
            pos=0
            exist = False
            for report in lines:
                pos+=1
                L=report.split()
                if(L[0]==id):
                    exist = True
                    break
            if(exist == False):
                f = open('facture.txt','a')
                f.write('       '+str(id)+'                      '+str(tot)+'    \n')
                f.close()
            else:
                L[1] = tot
                lines[pos-1]='       '+str(L[0])+'                      '+str(L[1])+'    \n'
                f = open("facture.txt","w")
                f.writelines(lines)
                f.close()

        def EnvoyerFacture(self,id,prix):
            s = prix*0.2 + prix
            f = open('bien.txt','r')
            lines=f.readlines()
            f.close()
            tot = 0
            for report in lines:
                L=report.split()
                if(L[4]==id):
                    tot+=int(L[3])*0.2 + int(L[3])
            Ajoterfacture(id,tot)
            data = 'operation effectuée avec succès \n' + "prix de l'objet acheté " +str(s)+'\n'+ "prix total à payer"+str(tot)
            self.connexion.sendto(data.encode(),(self.ip,self.port))

        while(1):
            (data,addr) = self.connexion.recvfrom(SIZE)
            ref = str(data.decode())
            (data,addr) = self.connexion.recvfrom(SIZE)
            prix = int(data.decode())
            if (prix>SearchCurrentPrice(ref) and SearchEtat(ref) == 'Disponible'):
                Changeprix(ref,prix)
                time.sleep(10)
                crprix = SearchCurrentPrice(ref)
                id = SearchID(self.ip)
                if (crprix == prix):
                    ChangerEtat(ref,id)
                    EnvoyerFacture(self,id,prix)
                    f = open("hist"+str(ref)+".txt","a")
                    f.write('       '+str(id)+'                      '+str(prix)+'                    succes'+'\n')
                    f.close()
                else:
                    f = open("hist"+str(ref)+".txt","a")
                    f.write('       '+str(id)+'                      '+str(prix)+'                    echec'+'\n')
                    f.close()
                    EnvoyerBien(self)
            EnvoyerBien(self)


                

            

def Servermenu():
    while(True):
        print('Donner votre choix\n<0> Ajouter bien\n<1> Consulter la liste des biens\n<2> Consulter la facture d’un acheteur\n'+
        '<3> Consulter l’historique des proposions\n')
        x = int(input())
        if(x == 0):
            rep = "oui"
            File1 = open('bien.txt', 'a')
            while (rep != "non"):
                print("donner la reference de l'objet")
                ref = input()
                print("donner la prix de l'objet")
                prix = int(input())
                File1.write('   '+ref+'                  '+str(prix)+'                    '+'Disponible'+'                 '+str(prix)+'                 '+str(0)+'                 \n')
                print("Ajouter un autre bien ?!")
                rep = input()
            File1.close()
        if(x == 1):
            File1 = open('bien.txt', 'r')
            lines = File1.readlines()
            for line in lines:
                print(str(line))
            File1.close()
        if(x == 2):
            File1 = open('facture.txt', 'r')
            lines = File1.readlines()
            for line in lines:
                print(str(line))
            File1.close()
        if(x == 2):
            File1 = open('facture.txt', 'r')
            lines = File1.readlines()
            for line in lines:
                print(str(line))
            File1.close()
        if(x == 3):
            a = int(input("donner reference de l'objet"))
            File1 = open('hist'+str(a)+'.txt', 'r')
            lines = File1.readlines()
            for line in lines:
                print(str(line))
            File1.close()




def Serveur():
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind(('127.0.0.1', 5004))
    mysocket.listen(3)

    while True :
        print('waiting')
        (client, (ip,port)) = mysocket.accept()
        newthread = ClientThread(ip,port,client)
        newthread.start()
        threads.append(newthread)
    


def main():
    print("Donner votre choix :\n 1_Lancer le serveur\n 2_Consulter les fichiers\n")
    x = int(input())
    if(x == 1):
        Serveur()
    if(x == 2):
        Servermenu()


main()
