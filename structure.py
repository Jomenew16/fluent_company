import re
from tkinter import messagebox


class Person:
    def __init__(self, name, surname1, surname2) -> None:
        self.name = name
        self.surname1 = surname1
        self.surname2 = surname2
        self.adress: str = None
        self.postal_code: str = None
        self.city: str= None
        self.state: str= None
        self.country: str = None
        self._emails = {
            "trabajo": "",
            "personal": "" 
        }
        self._telephones = {
            "trabajo": "",
            "personal": ""
        }
        self.users = []

    def update_email(self, key, value) -> bool:
        #Verify if the provided email matches with a usual patron, else, return false
        email_pattern = "^[A-Za-z.]+@[a-z.]+\.[a-z]+$"
        match = re.match(email_pattern, value)
        if match:
            self._emails[key] = value
            print(f'Se ha añadido el email {value} del tipo {key}')
        return match

    def update_telephone(self, key, value) -> bool:
        #Verify if the provided email matches with a usual patron, else, return false
        telephone_pattern = "^\+?[0-9]+$" #+ is allowed for international code
        match = re.match(telephone_pattern, value)
        if match:
            self._telephones[key] = value
            print(f'Se ha añadido el teléfono {value} del tipo {key}')
        return match

    def create_user(self):
        "Make the person a user of the system"
        print("se ha creado un usuario")
        #user = User(user_name, email, password) #Class to be defined
        #self.users.append(user)


#-------------------------------------Collaborator class (inheritance from person)---------------------


class Collaborator(Person):
    
    _collaborators = []
    _set_of_status = {"en activo", "de baja", "comisión de servicio", "ex-colaborador"}

    def __init__(self, name, surname1, surname2 = "", department= None, status = "en activo", title = "No especificado") -> None:
        super().__init__(name,surname1,surname2)
        self._department = department #department class
        self.decisions = []
        self.status = status
        self.position_in_department: str = "No especificado" #one of the relative positions exising on each department
        self._manager: Collaborator = None #In principle, only one maneger per collaborator. We will later see if that's realistic
        self._reports = [] #the reports of each manager
        self._collaborators.append(self)
        self._collab_id = self._collaborators.index(self) + 1
        self.title = title
        print(f'{self.name} {self.surname1} se ha incorporado al departamento {self._department.name}')
        print(f'Ahora el equipo lo forman {[collaborator.name for collaborator in self._collaborators]}')
        self.position_in_department: str #head of department, deputy... The idea is having a general view with simple relative positions

    def set_manager(self, manager):
        self._manager = manager
        manager._reports.append(self)
        print(f'El manager de {self.name} es ahora {self._manager.name}')
        print(f'{manager.name} tiene ahora estas personas a su cargo {[mnger.name for mnger in manager._reports]}')
    
    def update_information(self, relative_position, title, adress, country, city, state, postal_code):
        #validate some info

        #postal_code is a 5 digits code
        pc_pattern = "\d{5}"
        if re.match(pc_pattern, postal_code) or postal_code==None:
            self.postal_code = postal_code
        else:
            messagebox.showwarning('Aviso', 'El código postal no tiene un formato válido')

        #Validations to be added    
        self.position_in_department = relative_position
        self.title = title
        self.adress = adress
        self.country = country
        self.city = city
        self.state = state 
        
        print(f'''Se han actualizado los siguientes datos\nPosición interna: {self.position_in_department}
        \nTítulo: {self.title}
        \nEstado: {self.status}''')

    def update_status(self, status):
        "Creates a new status if it doesn't exist, or updates it with the new parameter"
        self._set_of_status.add(status)
        self.status = status
        print(f'se ha creado un nuevo estado {status}')
        print(f'Ahora existen estas posiciones {self._set_of_status}')
        
    
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

    _departments = []

    def __init__(self, name, upper_department = None) -> None:
        self.name = name
        self.upper_department: Department = upper_department
        self.dependencies = set() #departments depending on this one
        self.level_from_top: int = 0
        self._departments.append(self)
        self._department_id = self._departments.index(self) + 1
        self.department_collaborators = set()
        self._positions = {"head of department", "deputy of department", "team manager"}
        print(f"Se ha creado el nuevo departmento {name}")
        if upper_department:
            self.set_dependencies()
            print(f'{name} depende de {self.upper_department.name}')
        print(f'Ahora existen los siguientes departamentos: {[i.name for i in self._departments]}')

    def set_dependencies(self):
        self.upper_department.dependencies.add(self)
    
    def set_upper_department(self, upper_department):
        self.upper_department = upper_department
        self.set_dependencies()

    def check_department_structure(self):
        "Goes through all the departments and checks their dependencies and level o hierarchy"
        def get_top_department(dept):
            if not dept.upper_department:
                dept.level_from_top = 1
                print(f'top deparment es {dept.name}')
                print(type(dept))
                return dept
            else:
                return get_top_department(dept.upper_department)

        def set_levels(top_dept):
            for department in top_dept.dependencies:
                department.level_from_top = top_dept.level_from_top + 1
                print(f'El nivel del departmento {department.name} es {department.level_from_top}')
                if len(department.dependencies) != 0:
                    set_levels(department)
                else:
                    pass
            
            #if len(top_dept.dependencies) == 0 and end==True:
            #    pass
            #else:
            #    for department in top_dept.dependencies:
            #        cont +=1
            #        end = True if cont == len(top_dept.dependencies) else False
            #        department.level_from_top = top_dept.level_from_top + 1
            #        print(f'El nivel del departmento {department.name} es {department.level_from_top}')
            #        return set_levels(department, cont, end)

        top_department = get_top_department(self)
        set_levels(top_department)
        for department in self._departments:
            print(f'El nivel de {department.name} es {department.level_from_top}')
        
        #return get_top_department(self)
        #test
        
            


    def add_collaborator(self, name, surname1, surname2):
        new_collaborator = Collaborator(name, surname1, surname2, self)
        self.department_collaborators.add(new_collaborator)
        print(f"se ha añadido a {name} en el departamento {self.name}")
        print(f'Ahora trabajan las siguientes personas en el departament')
        print([i.name for i in self.department_collaborators])
        return new_collaborator

    def create_new_position(self, position):
        self._positions.add(position)
        print(f'se ha creado la posición {position}')
        print(f'Ahora existen estas posiciones {self._positions}')
        return position
    
    def remove_position(self, position):
        "Removes one of the relative positions in de deparment"
        #This function wasn't test nor implemented
        self._positions.remove(position)
        print(f'se ha eliminado la posición {position}')
        print(f'Ahora existen estas posiciones {self._positions}')
        

    def assign_position_to_collaborator(self, collab:Collaborator, position):
        if position in self.positions:
            collab.position_in_department = position
            
        else:
            print("La posición no existe en el departmento")
    