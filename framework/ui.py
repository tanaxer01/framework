from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit import PromptSession

from framework.preguntas import *
from framework.patrones import *
from framework.quizzes import *
from framework.parser import *

import sys
import os

class Interface:
    EXIT = ["quit", "exit", "e"]
    RET  = ["return", "back", "b"]

    def exit_program(self):
        ans = confirm("Salir del programa?")
        if ans:
            print("\nExiting program!")
            sys.exit()

    def _clear():
        os.system('clear')

class MainInterface (Interface):
    def __init__(self,title,desc): 
        self.q = Quiz(title,desc)
        self.template_dir = "."
        self.pcap_dir = "."
        self.txt_dir  = "."
        
    def run(self): 
        completer = WordCompleter(["add","clear","delete","question","show","template","export"])
        session = PromptSession()

        while True:
            try:
                command = session.prompt("[quiz] >>> ", completer=completer, complete_style=CompleteStyle.READLINE_LIKE)
            except KeyboardInterrupt:
                self.exit_program()
            try:
                command = command.split(" ")
                if command[0] in self.EXIT:
                    self.exit_program()
                    return
                elif command[0] in self.RET:
                    break
                elif command[0] in ["add","a"]:
                    self._add(command)
                elif command[0] in ["delete","del","d"]:
                    self._del(command)
                elif command[0] in ["show","s"]:
                    self._show(command)
                elif command[0] in ["template","temp","t"]:
                    self._templates(command)
                elif command[0] in ["question", "q"]:
                    self._question(command)
                elif command[0] in ["export","e"]:
                    self._export(command)
                elif command[0] == "clear":
                    Interface._clear()
                else: 
                    print("ERROR - cmd not found")
            except Exception as e:
                print(f"ERROR - {e} --",e)

    def _add(self,command): 
        self.q.add_question()
        self._question(["q","-1"])

    def _del(self,command): 
        self.q.del_question( int(command[1]) ) 

    def _show(self,command): 
        if len(command) == 1:
            print(f"Title: {self.q.title}\nDescription: {self.q.description}")  
            self.q.ls_questions()
        else:
            self.q.ls_questions(int(command[1]))
            
    def _templates(self,command): 
        if len(command) == 1:
            files = os.listdir( self.template_dir )
            for i,j in enumerate(files):
                print(i,j)
        else:
            files = os.listdir( self.template_dir )
            with open( self.template_dir + "/" + files[int(command[1])] ) as archivo:
                unparsed = safe_load(archivo)
                
                print(unparsed)
                parsed = parse_question(**unparsed)

            self.q.add_question( parsed )

    def _question(self,command): 
        if len(self.q.questions) == 0 or int(command[1]) >= len(self.q.questions):
            print("ERROR - Question not found")
            return
        elif len(command) == 1:
            print("ERROR - No se ha seleccionado una pregunta")
            return
        iface = QuestionInterface( self.q.questions[int(command[1])] )
        iface.template_dir = self.template_dir
        iface.pcap_dir = self.pcap_dir
        iface.txt_dir  = self.txt_dir
        
        iface.run()

    def _export(self,command): 
        if len(command) == 1:
            print(">>> export [nombre del txt]")
            return
        self.q.export(command[1])

class QuestionInterface (Interface):
    def __init__(self, question):
        self.q = question

    def run(self):
        completer = WordCompleter(["add","delete","show","move","pcap","txt","run"])
        session = PromptSession()

        while True:
            try: 
                command = session.prompt("[question] >>> ", completer=completer, complete_style=CompleteStyle.READLINE_LIKE)
            except KeyboardInterrupt:
                self.exit_program() 
            try:
                command = command.split(" ")
                if command[0] in self.EXIT:
                    self.exit_program() 
                elif command[0] in self.RET:
                    break
                elif command[0] in ["add","a"]:
                    self._add(command)
                elif command[0] in ["delete","del","d"]:
                    self._del(command)                   
                elif command[0] in ["show","s","ls"]:
                    self._show(command)
                elif command[0] in ["move", "mov"]:
                    self._mov(command)
                elif command[0] in ["modify","mod"]:
                    self._mod(command)
                elif command[0] in ["txt","t"]:
                    self._txt(command)
                elif command[0] in ["pcap","p"]:
                    self._pcap(command)
                elif command[0] in ["list","ls","l"]:
                    self._list(command)
                elif command[0] in ["run","r"]:
                    self._run(command)
                else: 
                    print("ERROR - cmd not found")
            except Exception as e:
                print(f"ERROR - {e} --",e)

    def _add(self,command):
        print("INTERACTIVE ADD")
        proto = int(input("1. protocolo: (1-icmp, 2-dns) "))
        if proto == 1:
            proto = ICMPPattern
        elif proto == 2:
            proto = DNSPattern
        else:
            print("ERROR - proto no exite")
            return

        total = int(input("2. cantidad de paquetes: "))
        delay = int(input("3. periodo del patron: "))

        server = input("4. ip del servidor: ")
        qry    = None
        if proto == DNSPattern:
            qry = input("5. url a preguntar: ")
        
        temp = proto(total,delay,[server]*total,[qry]*total)
        self.q.add_pattern(temp)

    def _del(self,command):
        self.q.del_pattern( int(command[1]) )

    def _show(self,command): 
        if len(command) == 1:
            print(f"pcap: {self.q.pcap_name}\ntxt: {self.q.txt_name}")
            self.q.ls_patterns()
            return

        self.q.ls_patterns(int(command[1]))

    def _mov(self,command):
        self.q.mov_pattern(int(command[1]),int(command[2]))

    def _mod(self,command):
        if len(self.q.patterns) == 0 or int(command[1]) >= len(self.q.patterns):
            print("ERROR - Pattern not found")
            return

        iface = PatternInterface( self.q.patterns[int(command[1])] )
        iface.txt_dir = self.txt_dir
        
        iface.run()

    def _txt(self,command):
        if len(command) == 1:
            print(f"--> Pregunta importada: {self.q.txt_name}")

        elif command[1] == "-l":
            files = os.listdir( self.txt_dir )
            for i in files:
                print(i)
        elif command[1].isnumeric():
            files = os.listdir( self.txt_dir ) 
            print(f"[+] pregunta {files[int(command[1])]} agregada")
            
            self.q.add_txt(self.txt_dir+"/"+files[ int(command[1]) ]) 

    def _pcap(self,command):
        if len(command) == 1:
            print(f"--> Pcap importado: {self.q.pcap_name}")

        elif command[1] == "-l":
            files = os.listdir( self.pcap_dir )
            for i in files:
                print(i)

        elif command[1].isnumeric():
            files = os.listdir( self.pcap_dir ) 
            print(f"[+] Pcap {files[int(command[1])]} agregado")
            
            self.q.add_pcap(self.pcap_dir+"/"+files[ int(command[1]) ]) 
        
    def _run(self,command):
        print("RUNNING sim")
        self.q.run()

class PatternInterface (Interface):
    def __init__(self, pattern):
        self.p = pattern

    def run(self):
        completer = WordCompleter(["add","delete","list","show","run"])
        session = PromptSession()

        while True:
            try:
                command = session.prompt("[packet] >>> ", completer=completer, complete_style=CompleteStyle.READLINE_LIKE) 
            except KeyboardInterrupt:
                self.exit_program()  

            try:
                command = command.rstrip().split(" ")
                if command[0] in self.EXIT:
                    self.exit_program()  
                    return
                elif command[0] in self.RET:
                    break
                elif command[0] in ["add","a"]:
                    self._add(command)
                elif command[0] in ["delete","del","d"]:
                    self._del(command)
                elif command[0] in ["list", "ls", "l"]:
                    self._list(command)
                elif command[0] in ["show","s"]:
                    self._show(command)
                elif command[0] in ["run","r"]:
                    self._run(command)
                else: 
                    print("ERROR - cmd not found")
            except Exception as e:
                print(f"ERROR - {e}")

    def _add(self,command):
        """Usa el metodo `add_modifiers` para agregar un modificador al patrón."""
        def constVal(val):
            while True:
                yield val

        def randVal(mi,ma):
            while True:
                val = randint(mi,ma)
                yield val

        field = input("Campo a modificar: ")
        prob  = float(input("Probabilidad de modificar un paquete (0<=p<=1): ")) % 1 
  
        rand = confirm("Utilizar valor random al modificar un pkt?")
        if rand:
            mi = int(input("Valor mínimo: "))
            ma = int(input("Valor maximo: "))

            func = randVal(mi,ma) 
        else:
            val = int(input("Valor: "))
            func = constVal( val )
                
        self.p.add_modifier(field,prob,func)

    def _del(self,command):
        if len(command) != 2:
            print("ERROR - no cuadra el numero de argumentos")
        self.p.del_modifier(int(command[1])) 

    def _show(self,command):
        if len(command) == 1:
            self.p.ls_modifiers()
        else:
            self.p.ls_modifiers(int(command[1]))

    def _list(self,command):
        if len(self.p.packets) == 0:
            print("No hay paquetes generados.")
            return
        
        for i in self.p.packets:
            print(i.summary())     
    
    def _run(self,command):
        self.p.run()
