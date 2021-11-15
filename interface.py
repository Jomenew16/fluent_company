from tkinter import *
from tkinter import ttk
#from department import Department
from collaborator import Collaborator

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

  #------------------------------- company construction menu ----------------------------      
    def adding_menu(self):
        """company construction menu. It provides de interface to add collaborators and departments
            and set relations among them. 
        """
        self.frame1 = Frame(self.master, width = 1100)
        self.frame1.grid(row=0, columnspan=2)
        self.frame1.config(bd=10, relief='ridge')
        self.frames.append(self.frame1)


        self.frame2 = Frame(self.master)
        self.frame2.grid(row=1, column=0)
        self.frames.append(self.frame2)

        self.frame3 = Frame(self.master)
        self.frame3.grid(row=1, column=1)
        self.frames.append(self.frame3)

        textTitle = Label(self.frame1, text='Añadir o editar colaboradores', font=("Open Sans", 10, 'bold'))
        textTitle.pack(pady= 5, side='top')

        #----------radio button collaborator/deparment----------------------
        varOption = IntVar()
        
        Label(self.frame2, text= "Selecciona opción: ").pack()
        Radiobutton(self.frame2, text="Añadir colaborador", variable=varOption, value=1, command = lambda: self.add_collaborator_form(self.frame3)).pack()
        Radiobutton(self.frame2, text = "Añadir departamento", variable=varOption, value= 2, command = lambda: self.add_department_form(self.frame3)).pack()
        #Radiobutton(self.frame2, text="Añadir colaborador", variable=varOption, value=1, command = lambda: self.add_collaborator_form(varOption)).pack()
        #Radiobutton(self.frame2, text = "Añadir departamento" ,variable=varOption, value=2, command = lambda: self.add_collaborator_form(varOption)).pack()

    
 #------------------------------- form to add collaborators in a given frame----------------------------   
    def add_collaborator_form(self, frame):
    #First we add the collaborator with only name and surname, the we access de edit collaborator
    #once the instance is already created and we have a id number
        self.clean_frame_space(frame)

        name= StringVar()
        surname1 = StringVar()
        surname2 = StringVar()

        def create_collab_instance():
            Collaborator(name.get(),surname1.get(),surname2.get())
    
        nameLabel = Label(frame, text= "Nombre")
        nameLabel.grid(row=0, column=0, sticky='W')

        nameEntry = Entry(frame, textvariable= name)
        nameEntry.grid(row=0, column=1, sticky='W')

        surname1Label = Label(frame, text= "Primer apellido")
        surname1Label.grid(row=0, column=3, sticky='W')

        surname1Entry = Entry(frame, textvariable= surname1)
        surname1Entry.grid(row=0, column=4, sticky='W')

        surname2Label = Label(frame, text= "Segundo apellido")
        surname2Label.grid(row=1, column=3, sticky='W')

        surname2Entry = Entry(frame, textvariable= surname2)
        surname2Entry.grid(row=1, column=4, sticky='W')

        addButton = Button(frame, text="Añadir collaborador", command = create_collab_instance)
        addButton.grid(row=2, columnspan=4, sticky='S')


        #frame.destroy()

#------------------------------- form to add a department s in a given frame----------------------------   
    def add_department_form(self, frame):
        self.clean_frame_space(frame)
        Label(frame, text= f'La opción seleccionada es departamento').pack()

        #frame.destroy()
        




if __name__ == '__main__':
    
    #When the app initialites main department instances are created by default
    #departments_name={"Dirección general", "Talento", "Operaciones", "Administración"}
#
    #for department in departments_name:
    #    Department(department)        
    #
    #print(Department.departments)

    root = Tk()
    root.title("Diseño de empresa")
    root.resizable(False, False)
    menu_app = Menu(master = root)
    
    root.mainloop()