from framework.preguntas import *
from os import listdir

class Quiz:
    def __init__(self,title:str,description:str):
        # Base del quizz
        self.title = title
        self.description = description

        # Preguntas creadas.
        self.questions = []

    def add_question(self, question=Question()):
        """Agrega una nueva pregunta, si no se especifica question crea una nueva."""
        self.questions.append( question )

    def del_question(self,num:int):
        """Borra la pregunta especificada siempre y cuando esta exista"""
        if num >= len(self.questions):  
            raise IndexError

    def mov_question(self,start:int,end:int):
        """Intercambia las preguntas especificadas.""" 
        if len(self.questions) <= start or len(self.questions) <= end:
            raise IndexError
        
        temp = self.questions[end]
        self.questions[end]   = self.questions[start]
        self.questions[start] = temp

    def ls_questions(self,num:int=None):
        """Lista el o las preguntas presentes en el quiz."""
        if num != None:
            if num >= len(self.questions):
                raise IndexError
            print(f"[{num}] {self.questions[num]}") 
        else:
            for i,j in enumerate(self.questions):
                print(f"[{i}] {j}")

    def export(self,output:str):
        """Genera el txt y los pcaps correspondientes."""
        text = f"Quiz Title: {self.title}\nQuiz Description: {self.description}\n\n"
        for i,q in enumerate(self.questions):
            text += q.export(output+str(i))
           
        with open(output+"txt","w") as test:
            test.write( text ) 
        print(text)
