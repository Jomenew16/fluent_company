class Collaborator(Person):
    def __init__(self, name, surname, department) -> None:
        super.__init__(name,surname)
        self.department = department #department class
        self.collaborators = [] #list of all collaborators. 
        self.decisions = []
        self.manager: Collaborator #In principle, only one maneger per collaborator. We will later see if that's realistic

    def set_manager(self, manager):
        self.manager = manager
    
    def request_decision(self):
        "The collaborator initiates a decision making process"
        #a new decision class is created including the requester and the responsible of decision making
        self.decisions.append(Decision(self,responsible, urgency, importance)) 
        print(f"se inicia un proceso de decisión por parte de {self.name}")
    
    def edit_decision(self):
        "The collaborator initiates a decision making process"
        print(f"modificación de una decisión por parte de {self.name}")