
from department import Department
from person import Person

class Collaborator(Person):
    
    collaborators = []

    def __init__(self, name, surname1,surname2, department: Department = None, status = "en activo", title = "No especificado") -> None:
        super.__init__(name,surname1,surname2)
        self.department = department #department class
        self.decisions = []
        self.status = status
        self.manager: Collaborator #In principle, only one maneger per collaborator. We will later see if that's realistic
        self.collaborators.append(self)
        self.collab_id = self.collaborators.index(self)
        self.title = title
        self.position_in_department: str #head of department, deputy... The idea is having a general view with simple relative positions

    def set_manager(self, manager):
        self.manager = manager
    
    def edit_collaborator(self):
        pass

    
    def request_decision(self):
        "The collaborator initiates a decision making process"
        #a new decision class is created including the requester and the responsible of decision making
        self.decisions.append(Decision(self,responsible, urgency, importance)) 
        print(f"se inicia un proceso de decisión por parte de {self.name}")
    
    def edit_decision(self):
        "The collaborator initiates a decision making process"
        print(f"modificación de una decisión por parte de {self.name}")