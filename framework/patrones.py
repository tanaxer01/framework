from scapy.all import IP, UDP, ICMP, DNS, DNSQR, sr
from random import random
from time import sleep

# TODO - Agregar IPTABLES & HTTPPattern

class Pattern:
    def __init__(self, total:int, period:int, dst,qry = None):
        # Caracteristicas del patrón.
        self.total  = total
        self.period = period

        # Info del destinatario.
        self.dst = dst[0]
        self.dst_arr = dst

        if qry != None:
            self.qry = qry[0]
            self.qry_arr = qry

        # Modificadores & paquetes.
        self.packets   = list()
        self.modifiers = list()

    def __str__(self):
        return f"<< Pattern --> {self.dst} | {self.total} Pkts - {self.period} Period >>"

    def packet(self, num:int):
        """Retorna el paquete que se enviara en este patrón."""
        if num >= len(self.dst_arr):
            raise IndexError("indice exede el numero de paquetes del patrón.")

        return IP(dst = self.dst_arr[num])

    def add_modifier(self, field:str, prob:float, value):
        """Agrega un modificador al arreglo."""
        if not hasattr(self.packet(0), field):
            raise Exception
        if prob > 1.0:
            raise Exception

        self.modifiers.append({ 'field': field, 'prob': prob, 'value': value })

    def del_modifier(self, num:int):
        """Borra un modificador del paquete."""
        if num > len(self.modifiers):
            raise ValueError
        
        self.modifiers.pop(num)

    def ls_modifiers(self):
        """Muestra todos los modificadores del patrón."""
        print("modifiers:")
        for i,j in enumerate(self.modifiers):
            print(f"[{i}] {j}")

    def run(self):
        """Genera el tráfico del patrón y almacena los paquetes en `self.packets`."""
        for i in range(self.total):
            #Genera el paquete a mandar.
            pkt = self.packet(i)

            #Aplica las modificaciones.
            for mod in self.modifiers:
                if random() <= mod['prob']:
                    if type(mod["value"])== list:
                        pkt.setfieldval(mod["field"], random.randint(mod["value"][0],mod["value"][1]))
                    else:
                        pkt.setfieldval(mod["field"], mod["value"] )

            result = sr(pkt, verbose=False)
            for j in result[0][0]:
                self.packets.append(j)

            sleep(self.period)
            
class ICMPPattern(Pattern):
    def __str__(self):
        return f"<< ICMP Pattern --> {self.dst} | {self.total} Pkts - {self.period} Period >>"

    def packet(self, num:int):
        """Adorna la función packet de `Pattern` para que envíe un paquete ICMP."""
        return super().packet(num)/ICMP(id = num)

class DNSPattern(Pattern):
    def __init__(self,total:int,period:int,dst,qry):
        if qry == None:
            raise Exception
        super().__init__(total,period,dst,qry)
    
    def __str__(self):
        return f"<< DNS Pattern --> {self.dst} ? {self.qry} | {self.total} Pkts - {self.period} Period >>"

    def packet(self, num:int):
       """Adorna la función packet de `Pattern` para que envíe un paquete DNS."""
       return super().packet(num)/UDP(dport=53)/DNS(id=num, qd=DNSQR(qname=self.qry_arr[num]))
