from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from typing import Annotated
from PIL import Image, ImageTk
from country_list import countries_for_language
from functools import reduce
import re

from structure import Collaborator, Department


class Menu(Frame):
    
    def __init__(self, master=None):
       super().__init__(master)
       self.master = master
       self.frames = []
       #self.thispath = os.getcwd()
       self.adding_menu()
    
    def clean_root_space(self):
        for frame in self.frames:
            frame.destroy()
        self.frames = []

    def clean_frame_space(self, current_frame):
        for widget in current_frame.winfo_children():
            widget.destroy()
    


  #------------------------------- COMPANY CONSTRUCTION MENU ----------------------------      
    def adding_menu(self):
        """company construction menu. It provides de interface to add collaborators and departments
            and set relations among them. 
        """
        self.frame1 = Frame(self.master, width = 1100)
        self.frame1.grid(row=0, columnspan=2)
        #self.frame1.config(bd=6, relief='ridge')
        self.frames.append(self.frame1)


        self.frame2 = Frame(self.master)
        self.frame2.grid(row=1, column=0)
        self.frame2.config(bd=4, relief='ridge')
        self.frames.append(self.frame2)

        self.frame3 = Frame(self.master)
        self.frame3.grid(row=1, column=1)
        self.frames.append(self.frame3)

        self.frame4 = Frame(self.master)
        self.frame4.grid(row=2, columnspan=2)
        self.frame4.config(pady = 10)
        self.frames.append(self.frame4)

        textTitle = Label(self.frame1, text='Estructura de la organización', font=("Open Sans", 10, 'bold'))
        textTitle.pack(pady= 5, side='top')

        #----------radio button collaborator/deparment - Frame 2----------------------
        varOption = IntVar()
        
        Label(self.frame2, text= "Selecciona opción: ").pack()
        Radiobutton(self.frame2, text="Añadir colaborador", variable=varOption, value=1, command = lambda: self.add_collaborator_form(self.frame3)).pack()
        Radiobutton(self.frame2, text = "Añadir departamento", variable=varOption, value= 2, command = lambda: self.add_department_form(self.frame3)).pack()
        #Radiobutton(self.frame2, text="Añadir colaborador", variable=varOption, value=1, command = lambda: self.add_collaborator_form(varOption)).pack()
        #Radiobutton(self.frame2, text = "Añadir departamento" ,variable=varOption, value=2, command = lambda: self.add_collaborator_form(varOption)).pack()

        #----------Bottom navigation - options/deparment - Frame 4----------------------

        exitButton = Button(self.frame4, text = "Salir", command = lambda: exit())
        exitButton.grid(row=0, column=0, sticky='N')
        #exitButton.config(pady=10)
    
 #------------------------------- form to add collaborators in a given frame - Frame 3)----------------------------   
    def add_collaborator_form(self, frame):
    #First we add the collaborator with only name, surname and department, then we access de edit collaborator
    #once the instance is already created and we have a id number
        self.clean_frame_space(frame)

        name= StringVar()
        surname1 = StringVar()
        surname2 = StringVar()

        def create_collab_instance(depart_index):
            if name.get() and surname1.get():
                try:
                    collaborator = Department._departments[depart_index].add_collaborator(name.get(),surname1.get(),surname2.get())
                    self.fill_collaborator_form(frame, collaborator)
                except TypeError:
                    pass
            else:
                messagebox.showwarning('Aviso', 'Nombre y apellido son obligatorios')
            
    
        nameLabel = Label(frame, text= "Nombre*")
        nameLabel.grid(row=0, column=0, sticky='W')

        nameEntry = Entry(frame, textvariable= name)
        nameEntry.grid(row=0, column=1, sticky='W')

        surname1Label = Label(frame, text= "Primer apellido*")
        surname1Label.grid(row=0, column=2, sticky='W')

        surname1Entry = Entry(frame, textvariable= surname1)
        surname1Entry.grid(row=0, column=3, sticky='W')

        surname2Label = Label(frame, text= "Segundo apellido")
        surname2Label.grid(row=1, column=2, sticky='W')

        surname2Entry = Entry(frame, textvariable= surname2)
        surname2Entry.grid(row=1, column=3, sticky='W')

        #combox of the departments
         
        departs = [d.name for d in Department._departments]
        depart = StringVar() 

        def depart_index():
            try:
                return departs.index(depart.get())
            except ValueError:
                messagebox.showwarning('Aviso', 'Escoge un departamento, o créalo si no está en la lista')
             
        departsLabel = Label(frame, text="Departamento*")
        departsLabel.grid(row=1, column=0)
        
        comboDeparts = ttk.Combobox(frame, state='readonly', textvariable=depart)
        comboDeparts['values'] = departs
        comboDeparts.grid(sticky='W', row=1, column=1)


        addButton = Button(frame, text="Añadir", command = lambda: create_collab_instance(depart_index()))
        addButton.grid(row=2, columnspan=5, sticky='S')
        addButton.config(pady=5)


        #frame.destroy()

    #---------  once the collaborator is added this form serves to complete information - Frame 3)----------------------------   
    #---------  some options are included to search and navigate through collaborators informations - Frame 3)----------------------------   

    def fill_collaborator_form(self, frame, collab):
        
        self.clean_frame_space(frame)
        
        #First, there is a navigations menu, so that we can select the right collaborator
        def next_collaborator(frame, collab, direction):
            try:
                id = collab._collab_id +1 if direction == "ahead" else collab._collab_id - 1
                self.fill_collaborator_form(frame, Collaborator._collaborators[id - 1])
            except IndexError:
                self.fill_collaborator_form(frame, Collaborator._collaborators[0])


        nameLabel = Label(frame, text=f'{collab.name} {collab.surname1}')
        nameLabel.grid(row=0, columnspan= 2)
        nameLabel.config(bg='white', padx= 10, font=('Open Sans', 9, 'bold'))

        codeLabel = Label(frame, text="Código empleado: ")
        codeLabel.grid(row=0, column=2)
        
        codenumberLabel = Label(frame, text=f'{collab._collab_id}')
        codenumberLabel.grid(row=0, column=3)
                
        leftnavigationButton = Button(frame, text="<", font=('Arial Black', 10, 'bold'), command=lambda: next_collaborator(frame, collab, direction="backwards"))
        leftnavigationButton.grid(row=0, column=4)

        rightnavigationButton = Button(frame, text=">", font=('Arial Black', 10, 'bold'), command=lambda: next_collaborator(frame, collab, direction="ahead"))
        rightnavigationButton.grid(row=0, column=5)

        searchnameLabel = Label(frame, text= "Buscar por nombre")
        searchnameLabel.grid(row=1, column=0)

        #combo of search by person
        people = [f'{person._collab_id}- {person.name} {person.surname1} {person.surname2}' for person in Collaborator._collaborators]
        full_name = StringVar()
        
        def go_to_person(*args):
            try:
                f_name = full_name.get().split("-") #first item of f_name should be the collaborators code
                self.fill_collaborator_form(frame, Collaborator._collaborators[int(f_name[0]) - 1])
            except Exception:
                messagebox.showwarning('Aviso', "Selecciona un valor de la lista")

        #full_name.trace_add('write', callback=go_to_person) 

        searchnameCombo = ttk.Combobox(frame, textvariable= full_name)
        searchnameCombo['values'] = people
        searchnameCombo.bind("<<ComboboxSelected>>", go_to_person)
        searchnameCombo.grid(row=1, column=1)

        #search by code input

        searchidLabel = Label(frame, text="Buscar por código")
        searchidLabel.grid(row=1, column=2)
        searchidLabel.config(padx=10)

        
        collab_code= IntVar()
        collab_code.set(collab._collab_id)

        def go_to_person_by_id(frame):
            try:
                self.fill_collaborator_form(frame, Collaborator._collaborators[collab_code.get()-1])
            except IndexError:
                messagebox.showwarning('Aviso', f'No existe ningún colaborador con código {collab_code.get()}')
            except ValueError:
                messagebox.showwarning('Aviso', 'Introduce un código válido de empleado')
            except Exception:
                messagebox.showwarning('Aviso', 'Introduce un código válido de empleado')
            

        searchidEntry = Entry(frame, textvariable=collab_code)
        searchidEntry.grid(row=1, column=3)
        searchidEntry.config(width=10)

        searchidButton = Button(frame, text="Ir", command=lambda: go_to_person_by_id(frame))
        searchidButton.grid(row=1, column=4, columnspan=3)
        
        #Here are the fields to add/edit the collaborator info
        Label(frame, text="______________________________________________________________________________").grid(row=2,columnspan=5, sticky='N')

        Label(frame, text= "Departamento: ").grid(row=3, column=0)

        departLabel= Label(frame, text=f'{collab._department.name}', font=('Open Sans', 9, 'bold'))
        departLabel.grid(row=3, column=1)
        departLabel.config(bg='white')

        Label(frame, text= "Posición").grid(row=3, column=2)

        pos_in_department = StringVar()
        if collab.position_in_department:
            pos_in_department.set(collab.position_in_department)

        posCombo = ttk.Combobox(frame, textvariable=pos_in_department)
        posCombo['values'] = list(collab._department._positions)
        posCombo.grid(row=3, column=3, columnspan=2)

        def add_position():
            collab.position_in_department = collab._department.create_new_position(pos_in_department.get())
            posCombo['values'] = list(collab._department._positions)
            print(f'{collab.name} es ahora {collab.position_in_department}')

        posButton = Button(frame, text="Confirmar\nnueva", command=add_position)
        posButton.grid(row=3, column=5, columnspan=2)
        posButton.config(height=2, width=10, padx=10)

        titleLabel = Label(frame, text="Título")
        titleLabel.grid(row=4, column=0)

        title_var = StringVar()
        if collab.title:
            title_var.set(collab.title)

        titleEntry = Entry(frame, textvariable=title_var)
        titleEntry.grid(row=4, column=1, columnspan=3, padx=15, sticky='W')
        titleEntry.config(width=70)

        
        coordLabel = Label(frame, text = "Coordinador")
        coordLabel.grid(row=5, column=0)

        manager_var = StringVar()
        if collab._manager:
            manager_var.set(people[collab._manager._collab_id - 1])

        coordCombo = ttk.Combobox(frame, textvariable= manager_var)
        coordCombo['values'] = people
        coordCombo.grid(row=5, column=1)

        statusLabel=Label(frame, text= "Estado")
        statusLabel.grid(row=5, column=2)

        status_var = StringVar()
        if collab.status:
            status_var.set(collab.status)

        statusCombo = ttk.Combobox(frame, textvariable= status_var)
        statusCombo['values'] = list(Collaborator._set_of_status)
        statusCombo.grid(row=5, column=3)


        def add_status():
            collab.update_status(status_var.get())
            statusCombo['values'] = list(Collaborator._set_of_status)
            print(f'{collab.name} tiene ahora el siguiente estado: {collab.status}')

        statButton = Button(frame, text="Confirmar\nnuevo estado", command=add_status)
        statButton.grid(row=5, column=5, columnspan=2)
        statButton.config(height=2, width=10, padx=10)

        #Email updates
        
        emailLabel = Label(frame, text="Email")
        emailLabel.grid(row=6, column=0)

        type_of_email_var = StringVar()
        all_types = list(collab._emails)
        type_of_email_var.set(all_types[0])
        
        email_var = StringVar()
        if type_of_email_var.get():
            email_var.set(collab._emails[type_of_email_var.get()])

        def update_email_value(*args):
            email_var.set(collab._emails[type_of_email_var.get()])

        emailtypeCombo = ttk.Combobox(frame, textvariable=type_of_email_var)
        emailtypeCombo['values'] = all_types
        emailtypeCombo.bind("<<ComboboxSelected>>", update_email_value)
        emailtypeCombo.grid(row=6, column=1)

        emailEntry = Entry(frame, textvariable=email_var)
        emailEntry.grid(row=6, column=2, columnspan=3, padx=15 ,sticky='W')
        emailEntry.config(width=40)

        def save_email():
            email_check = collab.update_email(type_of_email_var.get(), email_var.get())
            if not email_check:
                messagebox.showwarning('Aviso', 'El email no se ha guardado. Verifica el formato')
            all_types = list(collab._emails)
            emailtypeCombo['values'] = all_types

        saveemailButton = Button(frame, text="Guardar", command=save_email)
        saveemailButton.grid(row=6,column=5)

        #Telephone updates

        telephoneLabel = Label(frame, text="Teléfono")
        telephoneLabel.grid(row=7, column=0)

        type_of_telephone_var = StringVar()
        all_types_tel = list(collab._telephones)
        type_of_telephone_var.set(all_types_tel[0])
        
        telephone_var = StringVar()
        if type_of_telephone_var.get():
            telephone_var.set(collab._telephones[type_of_telephone_var.get()])

        def update_telephone_value(*args):
            telephone_var.set(collab._telephones[type_of_telephone_var.get()])

        telephonetypeCombo = ttk.Combobox(frame, textvariable=type_of_telephone_var)
        telephonetypeCombo['values'] = all_types_tel
        telephonetypeCombo.bind("<<ComboboxSelected>>", update_telephone_value)
        telephonetypeCombo.grid(row=7, column=1)

        telephoneEntry = Entry(frame, textvariable=telephone_var)
        telephoneEntry.grid(row=7, column=2, columnspan=3, padx=15, sticky='W')

        def save_telephone():
            telephone_check = collab.update_telephone(type_of_telephone_var.get(), telephone_var.get())
            if not telephone_check:
                messagebox.showwarning('Aviso', 'El teléfono no se ha guardado. Verifica el formato')
            all_types_tel = list(collab._telephones)
            telephonetypeCombo['values'] = all_types_tel

        savetelephoneButton = Button(frame, text="Guardar", command=save_telephone)
        savetelephoneButton.grid(row=7,column=5)

        addresLabel = Label(frame, text="Dirección")
        addresLabel.grid(row=8,column=0)

        adress_var = StringVar()

        adressEntry = Entry(frame, textvariable=adress_var)
        adressEntry.grid(row=8, column=1, columnspan=2, sticky='W')
        adressEntry.config(width=50)

        countryLabel = Label(frame, text="País")
        countryLabel.grid(row=8, column=3)

        country_var = StringVar()
        countries = list(map(lambda country: country[1], countries_for_language('es')))
        
        def dynamic_search(event):
            #pendiente de mejorar la dinámica de autocompletado
            texting_country = "^" + country_var.get().capitalize() + "[A-Za-z.]*"
            print(texting_country)
            countries2 = list(filter(lambda country: re.match(texting_country,country), countries))
            countryCombo['values'] = countries2
            #if len(countries2) == 1:
            #    country_var.set(countries2[0])
            #print(countries2)
            
        countryCombo = ttk.Combobox(frame, textvariable=country_var, state="readonly")
        countryCombo['values'] = countries
        countryCombo.bind("<Any-KeyPress>", lambda event: dynamic_search(event))
        countryCombo.grid(row=8, column=4, columnspan=3)

        stateLabel = Label(frame, text="Estado")
        stateLabel.grid(row=9, column=0)

        state_var = StringVar()

        stateEntry = Entry(frame, textvariable=state_var)
        stateEntry.grid(row=9, column=1)

        cityLabel = Label(frame, text="Ciudad")
        cityLabel.grid(row=9, column=2)

        city_var = StringVar()

        cityEntry = Entry(frame, textvariable=city_var)
        cityEntry.grid(row=9, column=3)

        pcLabel = Label(frame, text="C.P.")
        pcLabel.grid(row=9, column=4)

        pc_var = StringVar()

        pcEntry = Entry(frame, textvariable=pc_var)
        pcEntry.grid(row=9, column=5, columnspan=2)
        #--------------------------- final form buttons------------------------------------------------

        #botones de actualización
        def update_collab_attributes():
            collab.update_information(
                relative_position=pos_in_department.get(),
                title = title_var.get(),
                adress=adress_var.get(),
                country=country_var.get(),
                city=city_var.get(),
                state=state_var.get(),
                postal_code=pc_var.get()
                )

            if status_var.get():
                add_status()
            if manager_var.get():
                m_name = manager_var.get().split("-") #first item of f_name should be the collaborators code
                collab.set_manager(Collaborator._collaborators[int(m_name[0])])
                statusCombo['values'] = list(Collaborator._set_of_status)
            if type_of_email_var and email_var:
                save_email()

            #collab.set_manager(Collaborator._collaborators[index_manager.get()])      
        
        updateButton = Button(frame, text="Guardar datos", command=update_collab_attributes, font=('Open Sans', 9, 'bold'))
        updateButton.grid(row=10, column=1, columnspan=2, pady=10)
        updateButton.config(bg='#696969', fg='white', relief='raised', border=3)

        def start_new_collaborator():
            value = messagebox.askokcancel("Nuevo colaborador", "Si no los has guardado, se perderán los cambios.\n¿Deseas continuar?")
            if value:
                self.add_collaborator_form(frame)

        newcollabButton = Button(frame, text="Nuevo colaborador", command=start_new_collaborator, font=('Open Sans', 9, 'bold'))
        newcollabButton.grid(row=10, column=3, columnspan=2, pady=10)



#------------------------------- form to add a department in a given frame----------------------------   
    def add_department_form(self, frame):
        self.clean_frame_space(frame)

        def update_departments_list():
            return [department.name for department in Department._departments]

        nameLabel = Label(frame, text= "Nombre del departamento")
        nameLabel.grid(row=0, column=0, padx=5)

        department_var= StringVar()

        #departments = [department.name for department in Department._departments]
        nameCombo = ttk.Combobox(frame, textvariable= department_var)
        nameCombo['values'] = update_departments_list()
        nameCombo.grid(row=0, column=1, padx=10)

        dependencyLabel = Label(frame, text= "Dependencia")
        dependencyLabel.grid(row=0, column=2, padx=10)

        dependency_var= StringVar()

        dependencyCombo = ttk.Combobox(frame, textvariable= dependency_var)
        dependencyCombo['values'] = update_departments_list()
        dependencyCombo.grid(row=0, column=3, padx=5)

        def create_or_update_new_department():
            departments = update_departments_list()
            if not department_var.get():
                messagebox.showwarning('Aviso', 'Introduce un departamento')
            elif department_var.get() not in departments:
                    upper_department = list(filter(lambda department: department.name == dependency_var.get(), Department._departments))
                    if len(upper_department) == 1:
                        Department(name=department_var.get(), upper_department= upper_department[0])
                        messagebox.showinfo('Éxito', 
                            f'Se ha creado el departamento {department_var.get()} dependiente de {upper_department[0].name}')
                    else:
                        Department(name=department_var.get())
                        messagebox.showinfo('Éxito', 
                            f'Se ha creado el departamento {department_var.get()}\n Considera introducir una dependencia válida')
            elif department_var.get() in departments and dependency_var.get() in departments:
                selected_department = list(filter(lambda department: department.name == department_var.get(), Department._departments))
                upper_department = list(filter(lambda department: department.name == dependency_var.get(), Department._departments))
                selected_department[0].set_upper_department(upper_department[0]) #update the dependency
                messagebox.showinfo('Excelente', 
                            f'El departamento {department_var.get()} depende ahora {upper_department[0].name}')
            else:
                messagebox.showwarning('Aviso', 
                            'Introduce una dependencia válida')

            nameCombo['values'] = update_departments_list()
            dependencyCombo['values'] = update_departments_list()
            
         
        createButton = Button(frame, text="Crear o actualizar", command=create_or_update_new_department)
        createButton.grid(row=1, column=0, columnspan=2, pady=15)

        def remove_department():
            department = Department.filter_department(department_var.get())

            if department:
                #list(filter(lambda dept: dept.name == department_var.get(), Department._departments))           
                print(f'Se ha seleccionado el departamento {department.name} para eliminar')
                if department.name == 'Otro':
                    messagebox.showwarning('Aviso', 'No se puede eliminar el departament por defecto')
                else:
                    #Default department inherits the collaborators from the deleted one, and its dependencies. 
                    default_deparment = Department.filter_department("Otro")
                    for collab in department.department_collaborators:
                        default_deparment.department_collaborators.add(collab)
                    for dept in department.dependencies:
                        default_deparment.dependencies.add(dept)
                    Department._departments.remove(department)
                    del department
                    nameCombo['values'] = update_departments_list()
                    dependencyCombo['values'] = update_departments_list()
                print(f'Ahora existen los siguientes departamentos: {[i.name for i in Department._departments]}')
            else:
                messagebox.showwarning('Aviso', 'Debes elegir un departamento existente')

        deleteButton = Button(frame, text="Eliminar departamento", command=remove_department)
        deleteButton.grid(row=1, column=2, columnspan=2, pady=15)

        #Create a canva with the view of the general structure

          
        structureCanvas = Canvas(frame, width=1000, height=500, bg='black')    
        structureCanvas.grid(row=2, column=0, columnspan=4)

        ### Drawing the basic structure of the company

        def draw_department(
            row, 
            column,
            nb_columns,
            nb_rows,
            name,
            columnspan=False, 
            screen_width=1000, 
            screen_height = 500, 
            dept_width_pct=0.6,
            dept_height_pct=0.5,
            colour = 'blue'):
            """This function draws a rectanble, representing a department, given the row a colum in which is has to be drawn
            The function receives the following parameters:
            - row: int -> the row where the deparment will be drawns
            - column: int -> the column where the deparment will be drawns
            - columnspan: Boolean -> if True, the department will be drawn between two rows
            - screen_width & screen height -> size of the canvas
            - nb_columns: int -> number of columns
            - nb_rows: int -> number of rows
            - dept_width_pct -> the width of the rectangle in percentage with respecto to the quadrant size
            - dept_height_pct -> the width of the rectangle in percentage with respecto to the quadrant size
            - colour. Colour of the rectanble
            """
            #First, calculate hight and width of the quadrants
            quadrant_base = screen_width / nb_columns
            quadrant_height = screen_height / nb_rows

            ##Second, calculate the initial point, depending on the row and colum
            if not columnspan:
                relative_x = quadrant_base * (1-dept_width_pct) / 2 
                relative_y = quadrant_height * (1-dept_height_pct) / 2
            else:
                relative_x,= quadrant_base * (1 - dept_width_pct/2)
                relative_y = quadrant_height * (1-dept_height_pct) / 2
            
            init_x, init_y = column * quadrant_base + relative_x, row * quadrant_height + relative_y
            rect_base = quadrant_base * dept_width_pct
            rect_height = quadrant_height * dept_height_pct
            end_x, end_y = init_x + rect_base, init_y + rect_height

            structureCanvas.create_rectangle(init_x, init_y, end_x, end_y, fill=colour)
            structureCanvas.create_text(init_x + 5, init_y + rect_height * 0.7, text=name, fill='white', font='Arial')

               
        #number of columns and rows of the grid
        grid_columns = len(list(filter(lambda department: department.level_from_top == 2, Department._departments)))
        grid_rows = max([dept.level_from_top for dept in Department._departments])
        #quadrants_rows = reduce(lambda a, b: max(a.level_from_top,b.level_from_top), list_of_levels)   
        #print(f'El cuadrante tiene {quadrants_columns} columnas y {list_of_levels} filas')

        #Draw the departments depending on general management
        for i , department in enumerate(Department.filter_department("Dirección general").dependencies):
            draw_department(department.level_from_top -1, i, grid_columns, grid_rows, department.name)

        #frame.destroy()
        


if __name__ == '__main__':
    Department.create_basic_structure_of_departments()    

    root = Tk()
    root.title("Diseño de empresa")
    root.resizable(False, False)
    menu_app = Menu(master = root)
    
    root.mainloop()