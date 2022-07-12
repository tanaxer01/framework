#from scapy.utils import wrpcap, rdpcap
from scapy.all   import *
from random import randint, shuffle
from framework.patrones import *
from framework.utils import *
from os import listdir
from re import findall

class Question:
    def __init__(self):
        # Tráfico a generar en la captura. 
        self.patterns  = list()
        self.pcap_name = None
        self.pcap      = None

        # Información de la pregunta. 
        self.txt_name = None
        self.txt = None

        # Información adicional
        self.start_time = 0
        self.end_time   = 0

    def __str__(self):
        return f"<< Question | txt = {self.txt_name} | pcap = {self.pcap_name} | patterns = [ "+" ".join([ str(i) for i in self.patterns ]) +" ] >>"

    def add_pattern(self, pattern):
        self.patterns.append(pattern)
        
    def del_pattern(self, num:int):
        if num >= len(self.patterns):
            raise IndexError

        del self.patterns[num]

    def ls_patterns(self):
        print("preguntas:")
        for i,j in enumerate(self.patterns):
            print(f"[{i}] {j}")

    def mov_pattern(self, start:int, end:int):
        """Intercambiar los patrones especificados."""
        if len(self.patterns) <= start or len(self.patterns) <= end:
            raise IndexError

        temp = self.patterns[end]
        self.patterns[end]   = self.patterns[start]
        self.patterns[start] = temp
                            
    def add_txt(self, txt_name:str):
        """Especifica que txt debe utilizar la pregunta al ser exportada."""
        try:
            with open(txt_name,"r") as question:
                self.txt_name = txt_name
                self.txt = question.read()
        except IOError:
            raise FileNotFoundError

    def add_pcap(self, pcap_name, shuffle = False):
        """Especifica que .pcap se utilizara como ruido en la pregunta""" 
        packets = [ pkt for pkt in rdpcap(pcap_name) ]
        
        start = packets[0].time
        for pkt in packets:
            pkt.time -= start

        if shuffle:
            timestamps = [ i.time for i in packets ]
            shuffle(packets)

            for i,j in zip(packets,timestamps):
                i.time = j

        self.pcap_name = pcap_name
        self.pcap = packets    

    def run(self):
        """Genera el tráfico de todos los patrones en el orden que se encuentran."""
        for i in self.patterns:
            i.run()

        self.start_time = self.patterns[0].packets[0].time
        if self.pcap != None and self.start_time > self.pcap[0].time:
            self.start_time = self.pcap[0]

        self.end_time   = self.patterns[-1].packets[-1].time
        if self.pcap != None and self.end_time < self.pcap[0].time:
            self.end_time = self.pcap[0]

    def export(self,output:str):
        if self.patterns == list():
            raise FileNotFoundError("txt file not imported")

        if sum([ len(i.packets) for i in self.patterns ]) == 0:
            self.run()

        temp = []
        for p in self.patterns:
            temp += [ Ether()/i for i in p.packets ]
       
        if self.pcap != None:
            first = self.pcap[0].time
            for pkt in self.pcap:
                pkt.time += self.start_time - first
            
            temp += self.pcap
            temp = sorted( temp, key= lambda x:x.time)

        wrpcap(output+".pcap", temp) 

        text = "GROUP\npick:1\n\n"
        for num, pattern in enumerate(self.patterns):
            curr = self.txt

            print(curr)
            print(findall("(?<={{).*?(?=}})",curr))
            for i in findall("(?<={{).*?(?=}})",curr): 
                curr = curr.replace("{{"+i+"}}", str(eval(i)) )  
            
            text += curr + "\n"
            
        text += "\nEND_GROUP\n\n"
        
        return text
