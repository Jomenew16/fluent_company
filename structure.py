
class Person:
    def __init__(self, name, surname1, surname2) -> None:
        self.name = name
        self.surname1 = surname1
        self.surname2 = surname2
        self.adress: str
        self.emails = {
            "trabajo": str,
            "personal": str 
        }
        self.telephone = {
            "trabajo": str,
            "personal": str
        }
        self.users = []


    def create_user(self):
        "Make the person a user of the system"
        print("se ha creado un usuario")
        #user = User(user_name, email, password) #Class to be defined
        #self.users.append(user)


#-------------------------------------Collaborator class (inheritance from person)---------------------


class Collaborator(Person):
    
    collaborators = []

    def __init__(self, name, surname1,surname2 = "", department= None, status = "en activo", title = "No especificado") -> None:
        super().__init__(name,surname1,surname2)
        self.department = department #department class
        self.decisions = []
        self.status = status
        self.manager: Collaborator #In principle, only one maneger per collaborator. We will later see if that's realistic
        self.collaborators.append(self)
        self.collab_id = self.collaborators.index(self)
        self.title = title
        print(f'{self.name} {self.surname1} se ha incorporado al departamento {self.department.name}')
        print(f'Ahora el equipo lo forman {[collaborator.name for collaborator in self.collaborators]}')
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



#-------------------------------------Department class (related to Collaborator)---------------------


class Department:

    departments = []

    def __init__(self, name) -> None:
        self.name = name
        self.departments.append(self)
        self.department_collaborators = set()
        self.positions = {"head of department", "deputy of department", "team manager"}
        print(f"Se ha creado el nuevo departmento {name}")
        print(f'Ahora existen los siguientes departamentos: {[i.name for i in self.departments]}')


    def add_collaborator(self, name, surname):
        new_collaborator = Collaborator(name, surname, self)
        self.department_collaborators.add(new_collaborator)
        print(f"se ha añadido a {name} en el departamento {self.name}")
        print(f'Ahora trabajan las siguientes personas en el departament')
        print([i.name for i in self.department_collaborators])

    def create_new_position(self, position):
        self.positions.add(position)

    def assign_position_to_collaborator(self, collab:Collaborator, position):
        if position in self.positions:
            collab.position_in_department = position
            
        else:
            print("La posición no existe en el departmento")
    