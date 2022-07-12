from framework.preguntas import *
from framework.patrones import *
from framework.quizzes import *
from framework.utils import *
from random import randint
from yaml import safe_load

class Parser:
    def __init__(self, archivo):
        quiz = safe_load(archivo)
        self.parsed = self.parse_quiz(**quiz)
        
    def parse_quiz(self, title, description, questions):
        res = Quiz(str(title), str(description))

        for i in questions:
            temp = self.parse_question(**i)
            res.add_question(temp)

        return res

    def parse_question(self, reps, pattern, pcap=None, txt=None):
        res = Question()

        if txt != None:
            res.add_txt(txt)

        for i in range(reps):
            temp = self.parse_pattern(**pattern)
            res.add_pattern(temp)
            
        return res
            
    def parse_pattern(self, proto, total, period, server, query=None, mods=list()):
        parsed_total  = self.parse_number(total)
        parsed_period = self.parse_number(period)
        
        res = eval(proto.upper()+"Pattern")( parsed_total, parsed_period, self.parse_site(server, parsed_total), self.parse_site(query, parsed_total))

        for mod in mods:
            res.add_modifier(*self.parse_modifier(mod))

        return res

    def parse_site(self, site, reps):
        if type(site) == str:
            return [site]*reps
        elif type(site) == dict and "file" in site:
            return Nsequences(site["file"], reps)
    
    def parse_modifier(self, mod):
            return (mod['field'], mod['prob'], self.parse_number(mod['value']))
    
    def parse_number(self, num):
        if type(num) == int:
            return num
        elif type(num) == list and len(num) == 2:
            return randint(*num)
        else:
            raise ValueError
        

if __name__ == "__main__":
    with open("framework/new_test.yml") as archivo:
        a = Parser(archivo)
    #a = Parser("./framework/new_test.yml")
    #print("-----")
    #quiz = a.parse_quiz()
    #print(">", quiz.title, quiz.description )

    #a.parsed.ls_questions()
    for i in a.parsed.questions:
        print("running")
        i.run()

    a.parsed.export("test")

    print("-----")
    
