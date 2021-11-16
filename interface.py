from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk

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
    #First we add the collaborator with only name and surname, the we access de edit collaborator
    #once the instance is already created and we have a id number
        self.clean_frame_space(frame)

        name= StringVar()
        surname1 = StringVar()
        surname2 = StringVar()

        def create_collab_instance(depart_index):
            collaborator = Collaborator(name.get(),surname1.get(),surname2.get(), Department.departments[depart_index])
            self.clean_frame_space(frame)
            self.fill_collaborator_form(frame, collaborator)
    
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
         
        departs = [d.name for d in Department.departments]
        depart = StringVar() 

        def depart_index():
            return departs.index(depart.get())
             
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
        
        #First navigation functionalities
        def previous_collaborator(frame, collab):
            try:
                id = collab.collab_id - 1
                self.fill_collaborator_form(frame, Collaborator.collaborators[id])
            except IndexError:
                self.fill_collaborator_form(frame, Collaborator.collaborators[0])
        
        def next_collaborator(frame, collab):
            try:
                id = collab.collab_id + 1
                self.fill_collaborator_form(frame, Collaborator.collaborators[id])
            except IndexError:
                self.fill_collaborator_form(frame, Collaborator.collaborators[0])


        nameLabel = Label(frame, text=f'{collab.name} {collab.surname1}')
        nameLabel.grid(row=0, column= 0)
        nameLabel.config(bg='white', padx= 10, font=('Open Sans', 9, 'bold'))

        codeLabel = Label(frame, text="Código empleado: ")
        codeLabel.grid(row=0, column=1)
        
        codenumberLabel = Label(frame, text=f'{collab.collab_id}')
        codenumberLabel.grid(row=0, column=2)
                
        leftnavigationButton = Button(frame, text="<", font=('Arial Black', 10, 'bold'), command=lambda: previous_collaborator(frame, collab))
        leftnavigationButton.grid(row=0, column=3)

        rightnavigationButton = Button(frame, text=">", font=('Arial Black', 10, 'bold'), command=lambda: next_collaborator(frame, collab))
        rightnavigationButton.grid(row=0, column=4)

#------------------------------- form to add a department s in a given frame----------------------------   
    def add_department_form(self, frame):
        self.clean_frame_space(frame)
        Label(frame, text= f'La opción seleccionada es departamento').pack()

        #frame.destroy()
        




if __name__ == '__main__':
    
    #When the app initialites main department instances are created by default
    departments_name={"Dirección general", "Talento", "Operaciones", "Administración"}

    for department in departments_name:
        Department(department)        
    
    #print(Department.departments)

    root = Tk()
    root.title("Diseño de empresa")
    root.resizable(False, False)
    menu_app = Menu(master = root)
    
    root.mainloop()