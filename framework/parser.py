from framework.preguntas import *
from framework.patrones import *
from framework.quizzes import *
from framework.utils import *
from random import randint
from yaml import safe_load
        
def parse_quiz(title, description, questions):
    res = Quiz(str(title), str(description))

    for i in questions:
        temp = parse_question(**i)
        res.add_question(temp)

    return res

def parse_question(reps, pattern, pcap=None, txt=None):
    res = Question()

    if txt != None:
        res.add_txt(txt)

    for i in range(reps):
        temp = parse_pattern(**pattern)
        res.add_pattern(temp)
        
    return res
            
def parse_pattern(proto, total, period, server, query=None, mods=list()):
    parsed_total  = parse_number(total)
    parsed_period = parse_number(period)


    print(proto,"--",proto.upper()+"Pattern", eval(proto.upper()+"Pattern"))
    print( parsed_total, parsed_period )
    res = eval(proto.upper()+"Pattern")( parsed_total, parsed_period, parse_site(server, parsed_total), parse_site(query, parsed_total))

    for mod in mods:
        res.add_modifier(*parse_modifier(mod))

    return res

def parse_site(site, reps):
    if type(site) == str:
        return [site]*reps
    elif type(site) == dict and "file" in site:
        return Nsequences(site["file"], reps)
    
def parse_modifier(mod):
    return (mod['field'], mod['prob'], parse_number(mod['value']))
    
def parse_number(num):
    if type(num) == int:
        return num
    elif type(num) == list and len(num) == 2:
        return randint(*num)
    else:
        raise ValueError
        

if __name__ == "__main__":
    with open("new_test.yml") as archivo:
        unparsed = safe_load(archivo)
        parsed   = parse_quiz(**unparsed)
        
    for i in parsed.questions:
        print("running")
        i.run()

    a.parsed.export("test")

    print("-----")
    
