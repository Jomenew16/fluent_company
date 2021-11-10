from collaborator import Collaborator


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

    

