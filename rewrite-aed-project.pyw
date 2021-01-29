import sys
import os
import re # Usado para verificar certos campos (e-mail, nome, etc.) com expressões regulares (regex)
import cryptocode # Usado para encriptar informações gerais (primeiros e últimos nomes)
import hashlib # Usado para encriptar informações confidenciais (e-mails e passwords) com a função SHA256
import shutil # Usado para copiar ficheiros de um directório para outro
import traceback # Usado para facilitar o debugging
import datetime # Usado para determinar a data em que cada receita foi criada
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from functools import partial # Usado para acionar eventos com argumentos customizados
from PySide2 import QtWidgets, QtGui # Usado para centrar a janela no ecrã
from PIL import ImageTk, Image # Usado para converter imagens em formato PGM/PPM
from threading import Thread
# pip install cryptocode
# pip install PySide2
# pip install Pillow

def CreatePath():
    if not os.path.exists(os.getcwd() + "\\data"): os.mkdir(os.getcwd() + "\\data")
    if not os.path.exists(os.getcwd() + "\\data\\user"): os.mkdir(os.getcwd() + "\\data\\user")
    if not os.path.exists(os.getcwd() + "\\data\\images"): os.mkdir(os.getcwd() + "\\data\\images")
    if not os.path.exists(os.getcwd() + "\\data\\recipes"): os.mkdir(os.getcwd() + "\\data\\recipes")
    if not os.path.exists(os.getcwd() + "\\data\\categories"): os.mkdir(os.getcwd() + "\\data\\categories")

def MD5Checksum(img):
    if img == 1:
        if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
            md5hash = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\default.jpg").tobytes())
            return str(md5hash.hexdigest())
        else:
            messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar")
            os._exit(0)
    elif img == 2:
        if os.path.exists(os.getcwd() + "\\data\\images\\default_recipes.jpg"):
            md5hash = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\default_recipes.jpg").tobytes())
            return str(md5hash.hexdigest())
        else:
            messagebox.showerror("Erro", "O ficheiro 'data\images\default_recipes.jpg' está em falta\nO programa irá fechar")
            os._exit(0)
    elif img == 3:
        iconsList = []
        if os.path.exists(os.getcwd() + "\\data\\images\\favIcon.png"):
            if os.path.exists(os.getcwd() + "\\data\\images\\favIcon2.png"):
                if os.path.exists(os.getcwd() + "\\data\\images\\heartIcon.png"):
                    if os.path.exists(os.getcwd() + "\\data\\images\\heartIcon2.png"):
                        md5hash1 = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\favIcon.png").tobytes())
                        md5hash2 = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\favIcon2.png").tobytes())
                        md5hash3 = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\heartIcon.png").tobytes())
                        md5hash4 = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\heartIcon2.png").tobytes())
                        iconsList.append(str(md5hash1.hexdigest()))
                        iconsList.append(str(md5hash2.hexdigest()))
                        iconsList.append(str(md5hash3.hexdigest()))
                        iconsList.append(str(md5hash4.hexdigest()))
                        return iconsList
                    else:
                        messagebox.showerror("Erro", "O ficheiro 'data\\images\\heartIcon2.png' está em falta\nO programa irá fechar")
                        os._exit(0)
                else:
                    messagebox.showerror("Erro", "O ficheiro 'data\\images\\heartIcon.png' está em falta\nO programa irá fechar")
                    os._exit(0)
            else:
                messagebox.showerror("Erro", "O ficheiro 'data\\images\\favIcon2.png' está em falta\nO programa irá fechar")
                os._exit(0)
        else:
            messagebox.showerror("Erro", "O ficheiro 'data\\images\\favIcon.png' está em falta\nO programa irá fechar")
            os._exit(0)

def GetImageChecksum(path):
    if os.path.exists(path):
        md5hash = hashlib.md5(Image.open(path).tobytes())
        return str(md5hash.hexdigest())

def CenterWindow(target):
    target.update_idletasks()
    if not QtWidgets.QApplication.instance(): app = QtWidgets.QApplication([])
    else: app = QtWidgets.QApplication.instance()
    screen_width = QtGui.QGuiApplication.primaryScreen().availableGeometry().width()
    screen_height = QtGui.QGuiApplication.primaryScreen().availableGeometry().height()
    size = tuple(int(_) for _ in target.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - size[0] / 2
    y = screen_height / 2 - size[1] / 2
    target.geometry("+%d+%d" % (x, y))

def ShowPassword(origin, target):
    if int(origin.var.get()) == 0: target["show"] = "*"
    else: target["show"] = ""

def ChangeTextColor(target, color, event):
    target.config(fg = color)

def ChangeBackgroundColor(target, color, event):
    if target["bg"] != "#a8a8a8": target.config(bg = color)

def EncryptSHA256(data):
    EncryptedData = \
        hashlib.sha256(data.encode()).hexdigest()
    return EncryptedData

def EncryptString(data, key):
    return cryptocode.encrypt(data, key)

def DecryptString(data, key):
    return cryptocode.decrypt(data, key)

class MainProgram:
    def __init__(self, master):
        def MainProgram_CustomClose():
            self.UpdateLeaveTimeStamp()
            self.master.destroy()
            os._exit(0)

        # [Initial configuration]
        self.master = master
        self.loggedInUserInformation = [False]
        self.master.geometry("850x500")
        CenterWindow(self.master)
        self.master.title("Projeto AED")
        self.master.resizable(False, False)
        self.MainProgram_Authentication()
        self.master.protocol("WM_DELETE_WINDOW", MainProgram_CustomClose)

    def ClearWindowWidgets(self, target):
        widgetsList = target.winfo_children()
        for widget in widgetsList:
            if widget.winfo_children():
                widgetsList.extend(widget.winfo_children())
        for widget in widgetsList: widget.destroy()

    def ExitProgram(self):
        self.exitPrompt = messagebox.askquestion ("Sair", "Tem a certeza que prentende sair do programa?", icon = "warning", parent = self.master)
        if self.exitPrompt == "yes":
            self.UpdateLeaveTimeStamp()
            os._exit(0)

    def MainProgram_Authentication(self):
        if self.loggedInUserInformation[0]:
            self.logoutPrompt = messagebox.askquestion ("Terminar sessão", "Tem a certeza que prentende terminar sessão?", icon = "warning", parent = self.master)
            if self.logoutPrompt == "yes":
                self.UpdateLeaveTimeStamp()
                self.loggedInUserInformation[0] = False
                self.MainProgram_Authentication()
        else:
            self.ClearWindowWidgets(self.master)
            self.master.withdraw()
            self.newWindow = Toplevel(self.master)
            self.app = Login(self.newWindow)

    def MainProgram_FrontPage(self):
        def SwitchTabs(a, b):
            self.tabControl.select(a)
            existingButtons = [self.editProfile, self.usersRecipes, self.allRecipes, self.usersFavourite, self.usersNotifications]
            for button in existingButtons:
                if button != b: button.config(bg = "#f0f0f0")
            b.config(bg = "#a8a8a8")
            if a == 0: self.MainProgram_EditProfile()
            if a == 1: self.MainProgram_UsersRecipesPage()
            if a == 2: self.MainProgram_AllRecipesPage()
            if a == 3: self.MainProgram_UsersFavorites()
            if a == 4: self.MainProgram_Notifications()

        def UpdateFiltersList():
            self.globalCategoriesList = []
            self.filtersCategoriesList = ["Qualquer"]
            self.isAtLeastOneCategoryAvailable = False
            CreatePath()
            if os.path.exists(os.getcwd() + "\\data\\categories\\categories.txt"):
                with open(os.getcwd() + "\\data\\categories\\categories.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.globalCategoriesList.append(line.strip())
                            self.filtersCategoriesList.append(line.strip())
                            self.isAtLeastOneCategoryAvailable = True
                    if not self.isAtLeastOneCategoryAvailable:
                        messagebox.showerror("Erro", "O ficheiro de categorias não tem conteúdo\nO programa irá fechar", parent = self.master)
                        os._exit(0)
            else:
                messagebox.showerror("Erro", "O ficheiro de categorias não tem conteúdo\nO programa irá fechar", parent = self.master)
                os._exit(0)

        def CreateAdminCategoriesWindow():
            def AdminCategoriesCustomClose():
                self.adminCatWindow.destroy()
                self.master.update()
                self.master.grab_set()

            def SaveModifications():
                with open(os.getcwd() + "\\data\\categories\\categories.txt", "w", encoding="utf-8") as f:
                    for i in range(self.categoriesListbox.size()):
                        f.write(self.categoriesListbox.get(i).strip()+"\n")
                UpdateFiltersList()
                try:
                    self.searchByCategoryDropdown["value"] = self.filtersCategoriesList
                    self.usersRecipesSearchByCategoryDropdown["value"] = self.filtersCategoriesList
                except: pass
                messagebox.showinfo("Sucesso", "As alterações foram guardadas", parent = self.adminCatWindow)

            def AddCategoryAdmin():
                def AddNewCategoryAdmin():
                    if self.catgoryIngredientsText.get().lower().strip().replace(" ", ""):
                        self.addIsAlreadyPresent = False
                        for i in range(self.categoriesListbox.size()):
                            if self.catgoryIngredientsText.get().lower().strip() == self.categoriesListbox.get(i).lower().strip():
                                self.addIsAlreadyPresent = True
                        if not self.addIsAlreadyPresent:
                            with open(os.getcwd() + "\\data\\categories\\categories.txt", "a", encoding = "utf-8") as f:
                                self.categoriesListbox.insert("end", self.catgoryIngredientsText.get().strip())
                                AddNewCategoryClose()
                        else: messagebox.showerror("Erro", "A categoria introduzida já existe", parent = self.addNewCategoryWindowAdmin)
                    else: messagebox.showerror("Erro", "A categoria introduzida é inválida", parent = self.addNewCategoryWindowAdmin)

                def AddNewCategoryClose():
                    self.addNewCategoryWindowAdmin.destroy()
                    self.adminCatWindow.update()
                    self.adminCatWindow.grab_set()

                # [Layout] - Add ingredient window
                self.addNewCategoryWindowAdmin = Toplevel(self.master)
                self.addNewCategoryWindowAdmin.geometry("250x100")
                CenterWindow(self.addNewCategoryWindowAdmin)
                self.addNewCategoryWindowAdmin.title("Adicionar Categoria")
                self.addNewCategoryWindowAdmin.resizable(False, False)
                self.addNewCategoryWindowAdmin.grab_set()
                self.addNewCategoryWindowAdmin.protocol("WM_DELETE_WINDOW", AddNewCategoryClose)

                # [Layout] - Add new ingredient textbox
                self.categoryAddLabel = Label(self.addNewCategoryWindowAdmin, text = "Nome da categoria:")
                self.categoryAddLabel.place(x = 60, y = 10)
                self.catgoryIngredientsText = Entry(self.addNewCategoryWindowAdmin, width = 35)
                self.catgoryIngredientsText.place(x = 18, y = 35)
                self.catgoryIngredientsText.focus_force()

                # [Layout] - Add new ingredient button
                self.recipeIngredientsButton = ttk.Button(self.addNewCategoryWindowAdmin, text = "Adicionar", command = AddNewCategoryAdmin)
                self.recipeIngredientsButton.place(x = 85, y = 65)

            def RemoveCategoryAdmin():
                try:
                    self.selectedIngredientAdmin = self.categoriesListbox.curselection()[0]
                    if self.categoriesListbox.size() > 1: self.categoriesListbox.delete(self.selectedIngredientAdmin)
                    else: messagebox.showerror("Erro", "Tem de haver pelo menos 1 categoria presente na lista!", parent = self.adminCatWindow)
                except:
                    messagebox.showerror("Erro", "Selecione uma categoria para remover", parent = self.adminCatWindow)

            def EditCategoryAdmin():
                def EditNewCategoryClose():
                    self.editNewCategoryWindow.destroy()
                    self.adminCatWindow.update()
                    self.adminCatWindow.grab_set()

                def UpdateCategory():
                    if self.categoryTextAdmin.get().lower().strip().replace(" ", ""):
                        self.editIsAlreadyPresent = False
                        for i in range(self.categoriesListbox.size()):
                            if self.categoryTextAdmin.get().lower().strip() == self.categoriesListbox.get(i).lower().strip():
                                self.editIsAlreadyPresent = True

                        if self.categoryTextAdmin.get().lower().strip() == self.categoriesListbox.get(self.selectedCategoryAdmin).lower().strip():
                            self.editIsAlreadyPresent = False

                        if not self.editIsAlreadyPresent:
                            self.categoriesListbox.delete(self.selectedCategoryAdmin)
                            self.categoriesListbox.insert(self.selectedCategoryAdmin, self.categoryTextAdmin.get().strip())
                            EditNewCategoryClose()
                        else: messagebox.showerror("Erro", "A categoria introduzida já existe", parent = self.editNewCategoryWindow)
                    else: messagebox.showerror("Erro", "A categoria introduzida é inválida", parent = self.editNewCategoryWindow)

                try:
                    self.selectedCategoryAdmin = self.categoriesListbox.curselection()[0]

                    # [Layout] - Edit ingredient window
                    self.editNewCategoryWindow = Toplevel(self.master)
                    self.editNewCategoryWindow.geometry("250x100")
                    CenterWindow(self.editNewCategoryWindow)
                    self.editNewCategoryWindow.title("Editar Ingrediente")
                    self.editNewCategoryWindow.resizable(False, False)
                    self.editNewCategoryWindow.grab_set()
                    self.editNewCategoryWindow.protocol("WM_DELETE_WINDOW", EditNewCategoryClose)

                    # [Layout] - Edit ingredient textbox
                    self.categoryEditLabel = Label(self.editNewCategoryWindow, text = "Nome do ingrediente:")
                    self.categoryEditLabel.place(x = 60, y = 10)
                    self.categoryTextAdmin = Entry(self.editNewCategoryWindow, width = 35)
                    self.categoryTextAdmin.insert("end",self.categoriesListbox.get(self.selectedCategoryAdmin).strip())
                    self.categoryTextAdmin.place(x = 18, y = 35)
                    self.categoryTextAdmin.focus_force()

                    # [Layout] - Edit ingredient button
                    self.editCategoryButtonAdmin = ttk.Button(self.editNewCategoryWindow, text = "Editar", command = UpdateCategory)
                    self.editCategoryButtonAdmin.place(x = 85, y = 65)
                except: messagebox.showerror("Erro", "Selecione uma categoria para editar", parent = self.adminCatWindow)

            def UpdateListboxCatgoriesAdmin():
                self.categoriesListbox.delete(0,"end")
                with open(os.getcwd() + "\\data\\categories\\categories.txt", "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        self.categoriesListbox.insert("end", line.strip())

            # [Initial configuration]
            self.adminCatWindow=Toplevel(self.master)
            self.adminCatWindow.geometry("300x300")
            CenterWindow(self.adminCatWindow)
            self.adminCatWindow.title("Admin - Categorias")
            self.adminCatWindow.resizable(False, False)
            self.adminCatWindow.grab_set()
            self.adminCatWindow.protocol("WM_DELETE_WINDOW", AdminCategoriesCustomClose)

            # [Layout] - Title
            self.adminCatTitle=Label(self.adminCatWindow, text="Área de Admin - Categorias", font=("Helvetica 15 bold"))
            self.adminCatTitle.pack(side = TOP, anchor=CENTER, pady=20)

            # [Layout] - Label Frame
            self.categoriesLabelFrame=LabelFrame(self.adminCatWindow, height="200", width="270", text="Categorias")
            self.categoriesLabelFrame.place(x=10,y=70)

            # [Layout] - Show categories
            self.categoriesListbox=Listbox(self.categoriesLabelFrame)
            self.categoriesListbox.place(x=10,y=10)
            UpdateListboxCatgoriesAdmin()

            # [Layout] - Add categories
            self.categoriesAddButton=ttk.Button(self.categoriesLabelFrame, text="Adicionar", command=AddCategoryAdmin)
            self.categoriesAddButton.place(x=150,y=20)

            # [Layout] - Remove categories
            self.categoriesRemoveButton=ttk.Button(self.categoriesLabelFrame, text="Remover", command=RemoveCategoryAdmin)
            self.categoriesRemoveButton.place(x=150,y=60)

            # [Layout] - Edit categories
            self.categoriesEditButton=ttk.Button(self.categoriesLabelFrame, text="Editar", command=EditCategoryAdmin)
            self.categoriesEditButton.place(x=150,y=100)

            # [Layout] - Save all
            self.categoriesSaveButton=ttk.Button(self.categoriesLabelFrame, text="Guardar alterações", command=SaveModifications)
            self.categoriesSaveButton.place(x=150,y=140)

        def CreateAdminUsersWindow():
            def AdminUserWindowCustomClose():
                self.adminUsersWindow.destroy()
                self.master.update()
                self.master.grab_set()

            def ChangeUserType():
                try:
                    self.selectedUserAdmin = self.usersListbox.curselection()[0]
                    with open(os.getcwd() + "\\data\\user\\users_info.txt", "w", encoding="utf-8") as f: pass
                    for i in range(len(self.saveUsersState["lines"])):
                        if i == int(self.usersListbox.get(self.selectedUserAdmin).split("|")[0]):
                            if self.saveUsersState["lines"][i]["type"] == "Administrador": builtString = self.saveUsersState["lines"][i]["email"] + EncryptSHA256("user")[:10] + ";" + self.saveUsersState["lines"][i]["content"].split(";")[1] + ";" + self.saveUsersState["lines"][i]["content"].split(";")[2]
                            else: builtString = self.saveUsersState["lines"][i]["email"] + EncryptSHA256("admin")[:10] + ";" + self.saveUsersState["lines"][i]["content"].split(";")[1] + ";" + self.saveUsersState["lines"][i]["content"].split(";")[2]
                            with open(os.getcwd() + "\\data\\user\\users_info.txt", "a", encoding="utf-8") as f: f.write(builtString)
                        else:
                            with open(os.getcwd() + "\\data\\user\\users_info.txt", "a", encoding="utf-8") as f: f.write(self.saveUsersState["lines"][i]["content"])
                    UpdateListboxUsersAdmin()
                except: messagebox.showerror("Erro", "Selecione um utilizador para alterar", parent = self.adminUsersWindow)

            def UpdateListboxUsersAdmin():
                self.saveUsersState = { "lines": [] }
                self.countHelper = 0
                self.usersListbox.delete(0, END)
                with open(os.getcwd() + "\\data\\user\\users_info.txt", "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        user = {}
                        user["content"] = line
                        user["email"] = line.split(";")[0][:-10]
                        user["index"] = self.countHelper
                        user["type"] = "Administrador"
                        if line.split(";")[0][-10:] == EncryptSHA256("user")[:10]:
                            user["type"] = "Utilizador"
                        self.countHelper += 1
                        self.saveUsersState["lines"].append(user)

                for i in range(len(self.saveUsersState["lines"])):
                    if self.saveUsersState["lines"][i]["email"] != EncryptSHA256(self.loggedInUserInformation[1]):
                        self.usersListbox.insert("end", str(self.saveUsersState["lines"][i]["index"]) + " | " + DecryptString(self.saveUsersState["lines"][i]["content"].split(";")[2], self.saveUsersState["lines"][i]["content"].split(";")[0][:-10]) + " | " + str(self.saveUsersState["lines"][i]["type"]))

            # [Initial configuration]
            self.adminUsersWindow=Toplevel(self.master)
            self.adminUsersWindow.geometry("390x280")
            CenterWindow(self.adminUsersWindow)
            self.adminUsersWindow.title("Admin - Utilizadores")
            self.adminUsersWindow.resizable(False, False)
            self.adminUsersWindow.grab_set()
            self.adminUsersWindow.protocol("WM_DELETE_WINDOW", AdminUserWindowCustomClose)

            # [Layout] - Title
            self.adminUsersTitle=Label(self.adminUsersWindow, text="Área de Admin - Utilizadores", font=("Helvetica 15 bold"))
            self.adminUsersTitle.pack(side = TOP, anchor=CENTER, pady=20)

            # [Layout] - Label Frame
            self.usersLabelFrame=LabelFrame(self.adminUsersWindow, height="200", width="370", text="Utilizadores")
            self.usersLabelFrame.place(x=10,y=70)

            # [Layout] - Show users
            self.usersListbox=Listbox(self.usersLabelFrame, width="57", height="7")
            self.usersListbox.place(x=10,y=10)

            UpdateListboxUsersAdmin()

            # [Layout] - Change type
            self.usersChageTypeButton=ttk.Button(self.usersLabelFrame, text="Alterar tipo", command=ChangeUserType)
            self.usersChageTypeButton.place(x=145, y=140)

        def OpenLoadingScreen():
            def StopLoadingScreenWindowClose(): pass

            # [Initial configuration]
            self.master.withdraw()
            self.loadingScreen=Toplevel(self.master)
            self.loadingScreen.geometry("250x100")
            CenterWindow(self.loadingScreen)
            self.loadingScreen.title("A carregar...")
            self.loadingScreen.resizable(False, False)
            self.loadingScreen.grab_set()
            self.loadingScreen.protocol("WM_DELETE_WINDOW", StopLoadingScreenWindowClose)
            self.loadingLabel = Label(self.loadingScreen, text = "A carregar receitas...")
            self.loadingLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        OpenLoadingScreen()
        Thread(target=self.MainProgram_LoadRecipesToDictionary, args=()).start()

        # [Configuration] - Control variables
        self.hasUserGoneToPage0 = False
        self.hasUserGoneToPage1 = False
        self.hasUserGoneToPage2 = False
        self.hasUserGoneToPage3 = False
        self.hasUserGoneToPage4 = False

        UpdateFiltersList()

        # [Layout] - Admin menu
        if self.loggedInUserInformation[3] == "admin":
            self.master.geometry("850x518")
            self.adminBar = Menu(self.master)
            self.adminMenu = Menu(self.adminBar, tearoff = 0)
            self.adminMenu.add_command(label = "Categorias", command = CreateAdminCategoriesWindow)
            self.adminMenu.add_command(label = "Utilizadores", command = CreateAdminUsersWindow)
            self.adminBar.add_cascade(label = "Admin", menu = self.adminMenu)
            self.master.configure(menu = self.adminBar)
        else: self.master.geometry("850x500")

        # [Layout] - Sidebar > Profile Picture
        self.possiblePaths = [EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpeg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".png"]
        self.wasPhotoFound = False
        for path in self.possiblePaths:
            if os.path.exists(os.getcwd() + "\\data\\images\\" + path):
                self.profilePicture = Label(self.master)
                self.profilePicture.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\" + path).resize((70, 70)))
                self.profilePicture["image"] = self.profilePicture.image
                self.profilePicture.place(x = 60, y = 20)
                self.wasPhotoFound = True
                break
        if not self.wasPhotoFound:
            if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
                if MD5Checksum(1) == "28c17e68aa44166d1c8e716bd535676a":
                    self.profilePicture = Label(self.master)
                    self.profilePicture.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\default.jpg").resize((70, 70)))
                    self.profilePicture["image"] = self.profilePicture.image
                    self.profilePicture.place(x = 60, y = 20)
                else:
                    messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar", parent = self.master)
                    os._exit(0)
            else:
                messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar", parent = self.master)
                os._exit(0)

        # [Layout] - Sidebar > User's first and last name
        self.displayName = self.loggedInUserInformation[2].strip().split(" ")[0] + " " + self.loggedInUserInformation[2].strip().split(" ")[-1]
        self.usersName = Label(self.master, text = self.displayName)
        self.usersName.place(x = 50, y = 110)

        # [Layout] - Sidebar > User's type
        if self.loggedInUserInformation[3] == "admin": self.loggedInUserInformation[3] = "administrator"
        self.usersType = Label(self.master, text = self.loggedInUserInformation[3])
        self.usersType.place(x = 50, y = 130)

        # [Layout] - Sidebar > Edit user's profile button
        self.editProfile = Button(self.master, text = "Editar perfil", height = 2, width = 25, cursor="hand2")
        self.editProfile["command"] = partial(SwitchTabs, 0, self.editProfile)
        self.editProfile.place(x = 0, y = 170)
        self.editProfile.bind("<Enter>", partial(ChangeBackgroundColor, self.editProfile, "lightgray"))
        self.editProfile.bind("<Leave>", partial(ChangeBackgroundColor, self.editProfile, "#f0f0f0"))

        # [Layout] - Sidebar > User's recipes button
        self.usersRecipes = Button(self.master, text = "Minhas receitas", height = 2, width = 25, cursor="hand2")
        self.usersRecipes["command"] = partial(SwitchTabs, 1, self.usersRecipes)
        self.usersRecipes.place(x = 0, y = 215)
        self.usersRecipes.bind("<Enter>", partial(ChangeBackgroundColor, self.usersRecipes, "lightgray"))
        self.usersRecipes.bind("<Leave>", partial(ChangeBackgroundColor, self.usersRecipes, "#f0f0f0"))

        # [Layout] - Sidebar > All recipes button
        self.allRecipes = Button(self.master, text = "Receitas", height = 2, width = 25, cursor="hand2")
        self.allRecipes["command"] = partial(SwitchTabs, 2, self.allRecipes)
        self.allRecipes.place(x = 0, y = 260)
        self.allRecipes.bind("<Enter>", partial(ChangeBackgroundColor, self.allRecipes, "lightgray"))
        self.allRecipes.bind("<Leave>", partial(ChangeBackgroundColor, self.allRecipes, "#f0f0f0"))

        # [Layout] - Sidebar > User's favourites button
        self.usersFavourite = Button(self.master, text = "Favoritos", height = 2, width = 25, cursor="hand2")
        self.usersFavourite["command"] = partial(SwitchTabs, 3, self.usersFavourite)
        self.usersFavourite.place(x = 0, y = 305)
        self.usersFavourite.bind("<Enter>", partial(ChangeBackgroundColor, self.usersFavourite, "lightgray"))
        self.usersFavourite.bind("<Leave>", partial(ChangeBackgroundColor, self.usersFavourite, "#f0f0f0"))

        # [Layout] - Sidebar > User's notifications button
        self.usersNotifications = Button(self.master, text = "Notificações", height = 2, width = 25, bg = "#a8a8a8", cursor="hand2")
        self.usersNotifications["command"] = partial(SwitchTabs, 4, self.usersNotifications)
        self.usersNotifications.place(x = 0, y = 350)
        self.usersNotifications.bind("<Enter>", partial(ChangeBackgroundColor, self.usersNotifications, "lightgray"))
        self.usersNotifications.bind("<Leave>", partial(ChangeBackgroundColor, self.usersNotifications, "#f0f0f0"))

        # [Layout] - Sidebar > Logout button
        self.logoutUser = Button(self.master, text = "Terminar sessão", height = 2, width = 25, cursor="hand2", command = self.MainProgram_Authentication)
        self.logoutUser.place(x = 0, y = 395)
        self.logoutUser.bind("<Enter>", partial(ChangeBackgroundColor, self.logoutUser, "lightgray"))
        self.logoutUser.bind("<Leave>", partial(ChangeBackgroundColor, self.logoutUser, "#f0f0f0"))

        # [Layout] - Sidebar > Exit button
        self.exitMainProgram = Button(self.master, text = "Sair", height = 2, width = 25, cursor="hand2", command = self.ExitProgram)
        self.exitMainProgram.place(x = 0, y = 440)
        self.exitMainProgram.bind("<Enter>", partial(ChangeBackgroundColor, self.exitMainProgram, "lightgray"))
        self.exitMainProgram.bind("<Leave>", partial(ChangeBackgroundColor, self.exitMainProgram, "#f0f0f0"))

        # [Layout] - Tabs (notebook)
        self.tabControl = ttk.Notebook(self.master)
        self.tabEditProfile = Frame(self.tabControl, width = 649, height = 500)
        self.tabUsersRecipes = Frame(self.tabControl, width = 649, height = 500)
        self.tabAllRecipes = Frame(self.tabControl, width = 649, height = 500)
        self.tabUsersFavourite = Frame(self.tabControl, width = 649, height = 500)
        self.tabUsersNotifications = Frame(self.tabControl, width = 649, height = 500)
        self.tabControl.add(self.tabEditProfile)
        self.tabControl.add(self.tabUsersRecipes)
        self.tabControl.add(self.tabAllRecipes)
        self.tabControl.add(self.tabUsersFavourite)
        self.tabControl.add(self.tabUsersNotifications)
        self.tabControl.select(4)
        self.tabControl.place(x = 200, y = -23)

    def MainProgram_LoadRecipesToDictionary(self):
        def AppendToGlobalDict(i):
            self.data = {}
            self.currDir = os.getcwd()
            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\id.txt", "r") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["id"] = line.strip()

            self.data["index"] = str(self.currentDictId)
            self.currentDictId += 1

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\author.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["email"] = DecryptString(line.strip(), "auth")

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\name.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["titulo"] = DecryptString(line.strip(), "auth")

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\description.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["descricao"] = DecryptString(line.strip(), "auth")

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\procedure.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["procedimento"] = DecryptString(line.strip(), "auth")

            self.data["ingredientes"] = []
            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir+ "\\data\\recipes")[i] + "\\ingredients.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["ingredientes"].append(DecryptString(line.strip(), "auth"))

            self.data["categorias"] = []
            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\categories.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["categorias"].append(DecryptString(line.strip(), "auth"))

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\views\\nviews.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["views"] = line.strip()

            # self.data["viewed_by"]
            # with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\views\\whoviewed.txt", "r", encoding = "utf-8") as f:
            #     for line in f:
            #         if line.strip().replace(" ", ""):
            #             self.data["viewed_by"].appendl(line.strip())

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\likes\\nlikes.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["likes"] = line.strip()

            # self.data["liked_by"]
            # with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\likes\\wholiked.txt", "r", encoding = "utf-8") as f:
            #     for line in f:
            #         if line.strip().replace(" ", ""):
            #             self.data["liked_by"].appendl(line.strip())

            self.data["rating"] = 0.0
            self.auxSumRating, self.auxQuantRating = 0, 0
            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\rating.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.auxSumRating += int(line.split(";")[1])
                        self.auxQuantRating += 1
                    if self.auxQuantRating > 0: self.data["rating"] = float(self.auxSumRating / self.auxQuantRating)

            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\time.txt", "r", encoding = "utf-8") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["tempo_confecao"] = line.strip()

            self.data["data"] = "01/01/2021"
            with open(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\date.txt", "r") as f:
                for line in f:
                    if line.strip().replace(" ", ""):
                        self.data["data"] = DecryptString(line, "auth")

            self.data["path"] = self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i]

            self.data["imgpath"] = self.currDir + "\\data\\images\\default_recipes.jpg"
            if os.path.exists(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.jpg"):
                self.data["imgpath"] = self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.jpg"
            elif os.path.exists(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.png"):
                self.data["imgpath"] = self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.png"
            elif os.path.exists(self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.jpeg"):
                self.data["imgpath"] = self.currDir + "\\data\\recipes\\" + os.listdir(self.currDir + "\\data\\recipes")[i] + "\\picture.jpeg"

            self.globalRecipesDict["recipes"].append(self.data)
        self.currentDictId = 0
        self.globalRecipesDict = { "recipes":[] }
        self.shouldTheNoRecipesCardBeDisplayed = False
        if len(os.listdir(os.getcwd() + "\\data\\recipes")) > 0:
            for i in range(len(os.listdir(os.getcwd() + "\\data\\recipes")) - 1, -1, -1):
                if os.path.isdir(os.getcwd() + "\\data\\recipes\\" + os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                    if "-" in str(os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                        if len(os.listdir(os.getcwd() + "\\data\\recipes\\" + os.listdir(os.getcwd() + "\\data\\recipes")[i])) > 0:
                            AppendToGlobalDict(i)
        else: self.shouldTheNoRecipesCardBeDisplayed = True
        self.loadingScreen.destroy()
        self.master.deiconify()
        self.master.update()
        self.MainProgram_Notifications()

    def MainProgram_EditProfile(self):
        def UpdateProfile():
            self.listUsers=[]
            self.wasAccountFoundEdit = False
            with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                for line in f.readlines():
                    if line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10] == EncryptSHA256(self.loggedInUserInformation[1]):
                        self.wasAccountFoundEdit = True
                        self.isEditSaveReady = True
                        self.wasImageEdited = False
                        if self.editNameEntry.get().replace(" ", ""):
                            if self.editNameEntry.get().count(" ") >= 1:
                                self.isNameAcceptable = True
                                for i in range(len(self.editNameEntry.get().split(" "))):
                                    if len(self.editNameEntry.get().split(" ")[i]) < 2: self.isNameAcceptable = False
                                if self.isNameAcceptable:
                                    if re.compile(r"^[^\W\d_]+(-[^\W\d_]+)?$", re.U).match(self.editNameEntry.get().replace(" ", "")):
                                        if len(self.editNameEntry.get()) <= 55:
                                            self.passWordToSave = line.strip().split(";")[1]
                                            if self.oldPasswordEntry.get():
                                                if EncryptSHA256(self.oldPasswordEntry.get()) == line.strip().split(";")[1]:
                                                    if len(self.editPasswordEntry.get()) >= 8:
                                                        self.passWordToSave = EncryptSHA256(self.editPasswordEntry.get())
                                                        try: shutil.copy2(self.profilePictureEdit.imgpath, os.getcwd() + "\\data\\images\\" + line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10][:15] + os.path.splitext(self.profilePictureEdit.imgpath)[1])
                                                        except: pass
                                                        self.listUsers.append(line.strip().split(";")[0] + ";" + self.passWordToSave + ";" + EncryptString(" ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" ")))), line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10]))
                                                        self.loggedInUserInformation[2] = " ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" "))))
                                                    else:
                                                        self.isEditSaveReady = False
                                                        messagebox.showerror("Erro", "A nova palavra-passe escolhida tem de ter 8 ou mais caracteres", parent = self.master)
                                                else:
                                                    self.isEditSaveReady = False
                                                    messagebox.showerror("Erro", "A antiga palavra-passe não está correta", parent = self.master)
                                            elif self.editPasswordEntry.get():
                                                if len(self.oldPasswordEntry.get()) >= 8:
                                                    if EncryptSHA256(self.oldPasswordEntry.get()) == line.strip().split(";")[1]:
                                                        self.passWordToSave = EncryptSHA256(self.editPasswordEntry.get())
                                                        try: shutil.copy2(self.profilePictureEdit.imgpath, os.getcwd() + "\\data\\images\\" + line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10][:15] + os.path.splitext(self.profilePictureEdit.imgpath)[1])
                                                        except: pass
                                                        self.listUsers.append(line.strip().split(";")[0] + ";" + self.passWordToSave + ";" + EncryptString(" ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" ")))), line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10]))
                                                        self.loggedInUserInformation[2] = " ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" "))))
                                                    else:
                                                        self.isEditSaveReady = False
                                                        messagebox.showerror("Erro", "A antiga palavra-passe não está correta", parent = self.master)
                                                else:
                                                    self.isEditSaveReady = False
                                                    messagebox.showerror("Erro", "A nova palavra-passe escolhida tem de ter 8 ou mais caracteres", parent = self.master)
                                            else:
                                                try: shutil.copy2(self.profilePictureEdit.imgpath, os.getcwd() + "\\data\\images\\" + line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10][:15] + os.path.splitext(self.profilePictureEdit.imgpath)[1])
                                                except: pass
                                                self.listUsers.append(line.strip().split(";")[0] + ";" + self.passWordToSave + ";" + EncryptString(" ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" ")))), line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10]))
                                                self.loggedInUserInformation[2] = " ".join(self.editNameEntry.get().split(" ")[i].capitalize() for i in range(len(self.editNameEntry.get().split(" "))))
                                        else:
                                            self.isEditSaveReady = False
                                            messagebox.showerror("Erro", "O campo de nome não pode exceder os 55 caracteres", parent = self.master)
                                    else:
                                        self.isEditSaveReady = False
                                        messagebox.showerror("Erro", "O campo de nome não pode conter caracteres especiais nem números", parent = self.master)
                                else:
                                    self.isEditSaveReady = False
                                    messagebox.showerror("Erro", "O nome introduzido é inválido", parent = self.master)
                            else:
                                self.isEditSaveReady = False
                                messagebox.showerror("Erro", "Introduza, pelo menos, o primeiro e último nome", parent = self.master)
                        else:
                            self.isEditSaveReady = False
                            messagebox.showerror("Erro", "O nome introduzido é inválido", parent = self.master)
                    else: self.listUsers.append(line.strip())
            if not self.wasAccountFoundEdit:
                messagebox.showerror("Erro", "Ocorreu um erro inesperado\nO programa vai fechar", parent = self.master)
                os._exit(0)

            if self.isEditSaveReady:
                with open(os.getcwd() + "\\data\\user\\users_info.txt", "w") as f:
                    for i in range(len(self.listUsers)):
                        f.write(self.listUsers[i]+"\n")
                messagebox.showinfo("Sucesso", "Foram feitas as alterações", parent = self.master)
                self.updatedDisplayName = self.loggedInUserInformation[2].strip().split(" ")[0] + " " + self.loggedInUserInformation[2].strip().split(" ")[-1]
                self.usersName["text"] = self.updatedDisplayName
                self.ClearWindowWidgets(self.tabUsersRecipes)
                self.ClearWindowWidgets(self.tabAllRecipes)
                self.ClearWindowWidgets(self.tabUsersFavourite)
                self.hasUserGoneToPage1, self.hasUserGoneToPage2, self.hasUserGoneToPage3 = False, False, False
                self.shouldRecipesBeLoaded = True
                if self.wasImageEdited:
                    self.profilePicture.imgpath = self.path
                    self.profilePicture.image = ImageTk.PhotoImage(Image.open(self.profilePicture.imgpath).resize((70, 70)))
                    self.profilePicture["image"] = self.profilePicture.image

        def ChangeAvaImage(origin):
            self.imageCheckEdit, self.path = False, filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
            if self.path:
                try:
                    Image.open(self.path).verify()
                    self.imageCheckEdit = True
                except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem", parent = self.master)
                if self.imageCheckEdit:
                    try:
                        if Image.open(self.path).size[0] == Image.open(self.path).size[1]:
                            if Image.open(self.path).size[0] >= 50:
                                if os.stat(self.path).st_size <= 5000000:
                                    self.wasImageEdited = True
                                    origin.imgpath = self.path
                                    origin.image = ImageTk.PhotoImage(Image.open(origin.imgpath).resize((70, 70)))
                                    origin["image"] = origin.image
                                else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb", parent = self.master)
                            else: messagebox.showerror("Erro", "A imagem é inferior a 50x50px", parent = self.master)
                        else: messagebox.showerror("Erro", "A largura e altura da imagem não são iguais", parent = self.master)
                    except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema", parent = self.master)
                    except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.master)

        if not self.hasUserGoneToPage0:
            self.hasUserGoneToPage0 = True

            # [Layout] - Title
            self.titlePerfilLabel=Label(self.tabEditProfile, text="Editar Perfil")
            self.titlePerfilLabel.pack(side=TOP, pady="20")
            self.titlePerfilLabel.config(font = ('Helvetica 15 bold'))

            # [Layout] - Fieldset
            self.editPerfilLabelFrame= LabelFrame(self.tabEditProfile, height="400", width="400")
            self.editPerfilLabelFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

            # [Layout] - User Avatar
            self.possiblePaths = [EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpeg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".png"]
            self.wasPhotoFound = False
            for path in self.possiblePaths:
                if os.path.exists(os.getcwd() + "\\data\\images\\" + path):
                    self.profilePictureEdit = Label(self.editPerfilLabelFrame)
                    self.profilePictureEdit.imgpath = os.getcwd() + "\\data\\images\\" + path
                    self.profilePictureEdit.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\" + path).resize((70, 70)))
                    self.profilePictureEdit["image"] = self.profilePictureEdit.image
                    self.profilePictureEdit.place(x = 158, y = 10)
                    self.wasPhotoFound = True
                    break
            if not self.wasPhotoFound:
                if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
                    if MD5Checksum(1) == "28c17e68aa44166d1c8e716bd535676a":
                        self.profilePictureEdit = Label(self.editPerfilLabelFrame)
                        self.profilePictureEdit.imgpath = os.getcwd() + "\\data\\images\\default.jpg"
                        self.profilePictureEdit.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\default.jpg").resize((70, 70)))
                        self.profilePictureEdit["image"] = self.profilePictureEdit.image
                        self.profilePictureEdit.place(x = 158, y = 10)
                    else:
                        messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar", parent = self.master)
                        os._exit(0)
                else:
                    messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar", parent = self.master)
                    os._exit(0)

            # [Layout] - Button edit avatar
            self.editAvaButton=ttk.Button(self.editPerfilLabelFrame, text="Alterar imagem", command=partial(ChangeAvaImage, self.profilePictureEdit))
            self.editAvaButton.place(x=150 ,y=100)
            self.editAvaLabel=Label(self.editPerfilLabelFrame, text = ".jpg .jpeg ou .png", wraplength = 140, justify = LEFT, font=(None, 8))
            self.editAvaLabel.place(x=250 , y=105)

            # [Layout] - Edit Name
            self.editNameLabel=Label(self.editPerfilLabelFrame, text="Nome")
            self.editNameLabel.place(x=74,y=150)
            self.editNameEntry=Entry(self.editPerfilLabelFrame, width="30")
            self.editNameEntry.insert(END, self.loggedInUserInformation[2])
            self.editNameEntry.place(x=130,y=150)

            # [Layout] - Edit Email
            self.editEmailLabel=Label(self.editPerfilLabelFrame, text="Email", state = DISABLED)
            self.editEmailLabel.place(x=76,y=200)
            self.editEmailEntry=Entry(self.editPerfilLabelFrame, width="30")
            self.editEmailEntry.insert(END, self.loggedInUserInformation[1])
            self.editEmailEntry["state"] = DISABLED
            self.editEmailEntry.place(x=130,y=200)

            # [Layout] - Old password
            self.oldPasswordLabel=Label(self.editPerfilLabelFrame, text="Password Antiga")
            self.oldPasswordLabel.place(x=20,y=250)
            self.oldPasswordEntry=Entry(self.editPerfilLabelFrame, width="30", show="*")
            self.oldPasswordEntry.place(x=130,y=250)

            # [Layout] - New Password
            self.editPasswordLabel=Label(self.editPerfilLabelFrame, text="Password Nova")
            self.editPasswordLabel.place(x=26,y=300)
            self.editPasswordEntry=Entry(self.editPerfilLabelFrame, width="30", show="*")
            self.editPasswordEntry.place(x=130,y=300)

            # [Layout] - Update Button
            self.editProfileButton=ttk.Button(self.editPerfilLabelFrame, text="Atualizar", command=UpdateProfile)
            self.editProfileButton.place(x=155,y=350)

    def MainProgram_UsersRecipesPage(self):
        def UsersRecipesApplyFilters():
            self.usersRecipesPageFilters.clear()
            self.usersRecipesPageFilters.extend([self.usersRecipesSearchByTitleText.get(), self.usersRecipesSearchByIngredientText.get(), self.usersRecipesSearchByCategoryDropdown.get(), self.usersRecipesOrderByDropdown.get()])
            self.MainProgram_ShowRecipeCards("UsersRecipes", self.usersRecipesPageFilters)

        if not self.hasUserGoneToPage1:
            self.hasUserGoneToPage1 = True
            self.usersRecipesPageFilters = []

            # [Layout] - Filters fieldset
            self.usersRecipesFilterPanel = LabelFrame(self.tabUsersRecipes, text = "Filtros de Pesquisa", width = "640", height = "135", bd = "2")
            self.usersRecipesFilterPanel.place(x = 5, y = 5)

            # [Layout] - Search by title filter
            self.usersRecipeSearchByTitleLabel = Label(self.usersRecipesFilterPanel, text = "Pesquisar por título:")
            self.usersRecipeSearchByTitleLabel.place(x = 5, y = 5)
            self.usersRecipesSearchByTitleText = Entry(self.usersRecipesFilterPanel, width = "25")
            self.usersRecipesSearchByTitleText.place(x = 8, y = 30)
            self.usersRecipesSearchByTitleClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesSearchByTitleText))
            self.usersRecipesSearchByTitleClearButton.place(x = 165, y = 27)

            # [Layout] - Search by ingredient filter
            self.usersRecipesSearchByIngredientLabel = Label(self.usersRecipesFilterPanel, text = "Pesquisar por ingrediente:")
            self.usersRecipesSearchByIngredientLabel.place(x = 5, y = 55)
            self.usersRecipesSearchByIngredientText = Entry(self.usersRecipesFilterPanel, width = "25")
            self.usersRecipesSearchByIngredientText.place(x = 8, y = 80)
            self.usersRecipesSearchByIngredientClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesSearchByIngredientText))
            self.usersRecipesSearchByIngredientClearButton.place(x = 165, y = 77)

            # [Layout] - Search by category filter
            self.usersRecipesSearchByCategoryLabel = Label(self.usersRecipesFilterPanel, text = "Ordernar por categoria:")
            self.usersRecipesSearchByCategoryLabel.place(x = 225, y = 5)
            self.usersRecipesSearchByCategoryDropdown = ttk.Combobox(self.usersRecipesFilterPanel, value = self.filtersCategoriesList, width = "25")
            self.usersRecipesSearchByCategoryDropdown.place(x = 228, y = 30)
            self.usersRecipesSearchByCategoryDropdown.current(0)
            self.usersRecipesSearchByCategoryDropdownClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesSearchByCategoryDropdown))
            self.usersRecipesSearchByCategoryDropdownClearButton.place(x = 405, y = 28)

            # [Layout] - Order by filter
            self.usersRecipesOrderByLabel = Label(self.usersRecipesFilterPanel, text = "Ordernar por:")
            self.usersRecipesOrderByLabel.place(x = 225, y = 55)
            self.usersRecipesOrderByList = ["Mais recentes", "Mais antigos", "Mais vistos", "Menos vistos", "Mais gostados", "Menos gostados", "Maior rating", "Menor rating"]
            self.usersRecipesOrderByDropdown = ttk.Combobox(self.usersRecipesFilterPanel, value = self.usersRecipesOrderByList, width = "25")
            self.usersRecipesOrderByDropdown.place(x = 228, y = 80)
            self.usersRecipesOrderByDropdown.current(0)
            self.usersRecipesOrderByDropdownClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesOrderByDropdown))
            self.usersRecipesOrderByDropdownClearButton.place(x = 405, y = 78)

            # [Layout] - Clear filters button
            self.usersRecipesClearAllFiltersButton = ttk.Button(self.usersRecipesFilterPanel, text = "Limpar todos os filtros", width = "25", command = partial(self.MainProgram_GlobalFunctions, "ClearAllFilters", 2))
            self.usersRecipesClearAllFiltersButton.place(x = 468, y = 28)

            # [Layout] - Apply filters button
            self.usersRecipesApplyAllFiltersButton = ttk.Button(self.usersRecipesFilterPanel, text = "Aplicar filtros", width = "25", command = UsersRecipesApplyFilters)
            self.usersRecipesApplyAllFiltersButton.place(x = 468, y = 78)

            # [Layout] - Recipes fieldset
            self.usersRecipesPanel = LabelFrame(self.tabUsersRecipes, text = "Minhas Receitas", width = "640", height = "345", bd = "2")
            self.usersRecipesPanel.place(x = 5, y = 150)

            # [Layout] - Create recipe button
            self.usersCreateRecipeButton = Button(self.usersRecipesPanel, text = "Criar receita", relief = "groove", width = "50", height = "1", command = partial(self.MainProgram_AddRecipe, "UsersRecipes", self.usersRecipesPageFilters))
            self.usersCreateRecipeButton.place(x = 140, y = 10)

        self.MainProgram_ShowRecipeCards("UsersRecipes", self.usersRecipesPageFilters)

    def MainProgram_AllRecipesPage(self, *args):
        def AllRecipesApplyFilters():
            self.allRecipesPageFilters.clear()
            self.allRecipesPageFilters.extend([self.searchByTitleText.get(), self.searchByIngredientText.get(), self.searchByCategoryDropdown.get(), self.orderByDropdown.get()])
            self.MainProgram_ShowRecipeCards("AllRecipes", self.allRecipesPageFilters)

        if not self.hasUserGoneToPage2:
            self.hasUserGoneToPage2 = True
            self.allRecipesPageFilters = []

            # [Layout] - Filters fieldset
            self.filterPanel = LabelFrame(self.tabAllRecipes, text = "Filtros de Pesquisa", width = "640", height = "135", bd = "2")
            self.filterPanel.place(x = 5, y = 5)

            # [Layout] - Search by title filter
            self.searchByTitleLabel = Label(self.filterPanel, text = "Pesquisar por título:")
            self.searchByTitleLabel.place(x = 5, y = 5)
            self.searchByTitleText = Entry(self.filterPanel, width = "25")
            self.searchByTitleText.place(x = 8, y = 30)
            self.searchByTitleClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.searchByTitleText))
            self.searchByTitleClearButton.place(x = 165, y = 27)

            # [Layout] - Search by ingredient filter
            self.searchByIngredientLabel = Label(self.filterPanel, text = "Pesquisar por ingrediente:")
            self.searchByIngredientLabel.place(x = 5, y = 55)
            self.searchByIngredientText = Entry(self.filterPanel, width = "25")
            self.searchByIngredientText.place(x = 8, y = 80)
            self.searchByIngredientClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.searchByIngredientText))
            self.searchByIngredientClearButton.place(x = 165, y = 77)

            # [Layout] - Search by category filter
            self.searchByCategoryLabel = Label(self.filterPanel, text = "Ordernar por categoria:")
            self.searchByCategoryLabel.place(x = 225, y = 5)
            self.searchByCategoryDropdown = ttk.Combobox(self.filterPanel, value = self.filtersCategoriesList, width = "25")
            self.searchByCategoryDropdown.place(x = 228, y = 30)
            self.searchByCategoryDropdown.current(0)
            self.searchByCategoryDropdownClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.searchByCategoryDropdown))
            self.searchByCategoryDropdownClearButton.place(x = 405, y = 28)

            # [Layout] - Order by filter
            self.orderByLabel = Label(self.filterPanel, text = "Ordernar por:")
            self.orderByLabel.place(x = 225, y = 55)
            self.orderByList = ["Mais recentes", "Mais antigos", "Mais vistos", "Menos vistos", "Mais gostados", "Menos gostados", "Maior rating", "Menor rating"]
            self.orderByDropdown = ttk.Combobox(self.filterPanel, value = self.orderByList, width = "25")
            self.orderByDropdown.place(x = 228, y = 80)
            self.orderByDropdown.current(0)
            self.orderByDropdownClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.orderByDropdown))
            self.orderByDropdownClearButton.place(x = 405, y = 78)

            # [Layout] - Clear filters button
            self.clearAllFiltersButton = ttk.Button(self.filterPanel, text = "Limpar todos os filtros", width = "25", command = partial(self.MainProgram_GlobalFunctions, "ClearAllFilters", 1))
            self.clearAllFiltersButton.place(x = 468, y = 28)

            # [Layout] - Apply filters button
            self.applyAllFiltersButton = ttk.Button(self.filterPanel, text = "Aplicar filtros", width = "25", command = AllRecipesApplyFilters)
            self.applyAllFiltersButton.place(x = 468, y = 78)

            # [Layout] - Recipes fieldset
            self.recipesPanel = LabelFrame(self.tabAllRecipes, text = "Receitas", width = "640", height = "345", bd = "2")
            self.recipesPanel.place(x = 5, y = 150)

            # [Layout] - Create recipe button
            self.createRecipeButton = Button(self.recipesPanel, text = "Criar receita", relief = "groove", width = "50", height = "1", command = partial(self.MainProgram_AddRecipe, "AllRecipes", self.allRecipesPageFilters))
            self.createRecipeButton.place(x = 140, y = 10)

        self.MainProgram_ShowRecipeCards("AllRecipes", self.allRecipesPageFilters)

    def MainProgram_UsersFavorites(self):
        def UsersFavoritesApplyFilters():
            self.usersFavoritesPageFilters.clear()
            self.usersFavoritesPageFilters.extend([self.usersFavoritesSearchByTitleText.get(), self.usersFavoritesSearchByIngredientText.get(), self.usersFavoritesSearchByCategoryDropdown.get(), self.usersFavoritesOrderByDropdown.get()])
            self.MainProgram_ShowRecipeCards("UsersFavorites", self.usersFavoritesPageFilters)

        if not self.hasUserGoneToPage3:
            self.hasUserGoneToPage3 = True
            self.usersFavoritesPageFilters = []

            # [Layout] - Filters fieldset
            self.usersFavoritesFilterPanel = LabelFrame(self.tabUsersFavourite, text = "Filtros de Pesquisa", width = "640", height = "135", bd = "2")
            self.usersFavoritesFilterPanel.place(x = 5, y = 5)

            # [Layout] - Search by title filter
            self.usersFavoritesSearchByTitleLabel = Label(self.usersFavoritesFilterPanel, text = "Pesquisar por título:")
            self.usersFavoritesSearchByTitleLabel.place(x = 5, y = 5)
            self.usersFavoritesSearchByTitleText = Entry(self.usersFavoritesFilterPanel, width = "25")
            self.usersFavoritesSearchByTitleText.place(x = 8, y = 30)
            self.usersFavoritesSearchByTitleClearButton = ttk.Button(self.usersFavoritesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersFavoritesSearchByTitleText))
            self.usersFavoritesSearchByTitleClearButton.place(x = 165, y = 27)

            # [Layout] - Search by ingredient filter
            self.usersFavoritesSearchByIngredientLabel = Label(self.usersFavoritesFilterPanel, text = "Pesquisar por ingrediente:")
            self.usersFavoritesSearchByIngredientLabel.place(x = 5, y = 55)
            self.usersFavoritesSearchByIngredientText = Entry(self.usersFavoritesFilterPanel, width = "25")
            self.usersFavoritesSearchByIngredientText.place(x = 8, y = 80)
            self.usersFavoritesSearchByIngredientClearButton = ttk.Button(self.usersFavoritesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersFavoritesSearchByIngredientText))
            self.usersFavoritesSearchByIngredientClearButton.place(x = 165, y = 77)

            # [Layout] - Search by category filter
            self.usersFavoritesSearchByCategoryLabel = Label(self.usersFavoritesFilterPanel, text = "Ordernar por categoria:")
            self.usersFavoritesSearchByCategoryLabel.place(x = 225, y = 5)
            self.usersFavoritesSearchByCategoryDropdown = ttk.Combobox(self.usersFavoritesFilterPanel, value = self.filtersCategoriesList, width = "25")
            self.usersFavoritesSearchByCategoryDropdown.place(x = 228, y = 30)
            self.usersFavoritesSearchByCategoryDropdown.current(0)
            self.usersFavoritesSearchByCategoryDropdownClearButton = ttk.Button(self.usersFavoritesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersFavoritesSearchByCategoryDropdown))
            self.usersFavoritesSearchByCategoryDropdownClearButton.place(x = 405, y = 28)

            # [Layout] - Order by filter
            self.usersFavoritesOrderByLabel = Label(self.usersFavoritesFilterPanel, text = "Ordernar por:")
            self.usersFavoritesOrderByLabel.place(x = 225, y = 55)
            self.usersFavoritesOrderByList = ["Mais recentes", "Mais antigos", "Mais vistos", "Menos vistos", "Mais gostados", "Menos gostados", "Maior rating", "Menor rating"]
            self.usersFavoritesOrderByDropdown = ttk.Combobox(self.usersFavoritesFilterPanel, value = self.usersFavoritesOrderByList, width = "25")
            self.usersFavoritesOrderByDropdown.place(x = 228, y = 80)
            self.usersFavoritesOrderByDropdown.current(0)
            self.usersFavoritesOrderByDropdownClearButton = ttk.Button(self.usersFavoritesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersFavoritesOrderByDropdown))
            self.usersFavoritesOrderByDropdownClearButton.place(x = 405, y = 78)

            # [Layout] - Clear filters button
            self.usersFavoritesClearAllFiltersButton = ttk.Button(self.usersFavoritesFilterPanel, text = "Limpar todos os filtros", width = "25", command = partial(self.MainProgram_GlobalFunctions, "ClearAllFilters", 3))
            self.usersFavoritesClearAllFiltersButton.place(x = 468, y = 28)

            # [Layout] - Apply filters button
            self.usersFavoritesApplyAllFiltersButton = ttk.Button(self.usersFavoritesFilterPanel, text = "Aplicar filtros", width = "25", command = UsersFavoritesApplyFilters)
            self.usersFavoritesApplyAllFiltersButton.place(x = 468, y = 78)

            # [Layout] - Recipes fieldset
            self.usersFavoritesPanel = LabelFrame(self.tabUsersFavourite, text = "Receitas favoritas", width = "640", height = "345", bd = "2")
            self.usersFavoritesPanel.place(x = 5, y = 150)

            # [Layout] - Create recipe button
            self.usersFavoritesCreateRecipeButton = Button(self.usersFavoritesPanel, text = "Criar receita", relief = "groove", width = "50", height = "1", command = partial(self.MainProgram_AddRecipe, "UsersFavorites", self.usersFavoritesPageFilters))
            self.usersFavoritesCreateRecipeButton.place(x = 140, y = 10)

        self.MainProgram_ShowRecipeCards("UsersFavorites", self.usersFavoritesPageFilters)

    def MainProgram_Notifications(self):
        def DismissNotification(index):
            self.UpdateLeaveTimeStamp()
            self.MainProgram_ShowRecipeDetails(self.globalRecipesDict["recipes"][int(index)]["index"], self.globalRecipesDict["recipes"][int(index)]["path"] , "UsersNotifications")
            self.hasUserGoneToPage4 = False
            self.ClearWindowWidgets(self.tabUsersNotifications)
            self.MainProgram_Notifications()

        if not self.hasUserGoneToPage4:
            self.hasUserGoneToPage4 = True

            # [Layout] - Notifications Title
            self.notificationsTitle=Label(self.tabUsersNotifications, text="Notificações " + "(0)", font=("Helvetica 15 bold"))
            self.notificationsTitle.pack(side = TOP, anchor=CENTER, pady=20)

            # [Layout] - Recipes fieldset
            self.notificationsPanel = LabelFrame(self.tabUsersNotifications, text = "Notificações", width = "640", height = "345", bd = "2")
            self.notificationsPanel.pack(anchor=CENTER)

            self.notificationsFrame = Frame(self.notificationsPanel, width = 625, height = 280)
            self.notificationsFrame.place(x = 5, y = 10)
            self.notificationsCanvas = Canvas(self.notificationsFrame, width = 605, height=300)
            self.notificationsCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.notificationsCanvasScrollbar = ttk.Scrollbar(self.notificationsFrame, orient = VERTICAL, command = self.notificationsCanvas.yview)
            self.notificationsCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.notificationsCanvas.configure(yscrollcommand = self.notificationsCanvasScrollbar.set)
            self.notificationsCanvas.bind('<Configure>', lambda e: self.notificationsCanvas.configure(scrollregion = self.notificationsCanvas.bbox("all")))
            self.notificationsSecondFrame = Frame(self.notificationsCanvas)
            self.notificationsCanvas.create_window((0, 0), window = self.notificationsSecondFrame, anchor = NW)

            CreatePath()
            if str(MD5Checksum(2)) != "8b53223e6b0ba3a1564ef2a5397bb03e":
                messagebox.showerror("Erro", "A foto padrão das receitas não foi reconhecida\nO programa irá fechar", parent = self.master)
                os._exit(0)

            # Check if leave timestamp exists
            self.shouldTheNoNotificationsCardBeDisplayed = True
            self.whatCategoriesShouldBeDisplayed = []
            if os.path.exists(os.getcwd() + "\\data\\user\\" + EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".txt"):
                # Check if user has any favorited recipes
                    self.doesUserHaveAnyFavoritedRecipes = False
                    if len(os.listdir(os.getcwd() + "\\data\\recipes")) > 0:
                        for i in range(len(os.listdir(os.getcwd() + "\\data\\recipes"))):
                            if os.path.isdir(os.getcwd() + "\\data\\recipes\\" + os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                                if "-" in str(os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                                    self.wasRecipeFavorited = False
                                    with open(os.getcwd() + "\\data\\recipes\\" + str(os.listdir(os.getcwd() + "\\data\\recipes")[i]) + "\\favoritedby.txt", "r") as f:
                                        for line in f:
                                            if line.strip():
                                                if line.strip() == EncryptSHA256(self.loggedInUserInformation[1]):
                                                    self.doesUserHaveAnyFavoritedRecipes = True
                                                    self.shouldTheNoNotificationsCardBeDisplayed = False
                                                    self.wasRecipeFavorited = True
                                    if self.wasRecipeFavorited:
                                        with open(os.getcwd() + "\\data\\recipes\\" + str(os.listdir(os.getcwd() + "\\data\\recipes")[i]) + "\\categories.txt", "r") as f:
                                            for line in f:
                                                if line.strip():
                                                    self.doesCategoryExistAlready = False
                                                    for category in self.whatCategoriesShouldBeDisplayed:
                                                        if category == line.strip():
                                                            self.doesCategoryExistAlready = True
                                                    if not self.doesCategoryExistAlready:
                                                        self.whatCategoriesShouldBeDisplayed.append(DecryptString(line.strip(), "auth"))
                        if not self.doesUserHaveAnyFavoritedRecipes: self.shouldTheNoNotificationsCardBeDisplayed = True
                    else: self.shouldTheNoNotificationsCardBeDisplayed = True
            else: self.shouldTheNoNotificationsCardBeDisplayed = True
            if len(self.whatCategoriesShouldBeDisplayed) <= 0: self.shouldTheNoNotificationsCardBeDisplayed = True
            if not self.shouldTheNoNotificationsCardBeDisplayed:
                with open(os.getcwd() + "\\data\\user\\" + EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".txt", "r") as f:
                    for line in f:
                        if line.strip():
                            self.userLeaveTime = datetime.datetime.strptime(line.strip(), '%Y-%m-%d %H:%M:%S.%f')
                if self.userLeaveTime:
                    self.quantNotifications = 0
                    for i in range(len(self.globalRecipesDict["recipes"])):
                        # Check if the current recipe has the same categories as the one the user has previously favorited
                        self.shouldRecipeBeShown = False
                        for j in range(len(self.globalRecipesDict["recipes"][i]["categorias"])):
                            for category in self.whatCategoriesShouldBeDisplayed:
                                if self.globalRecipesDict["recipes"][i]["categorias"][j] == category:
                                    self.shouldRecipeBeShown = True
                                    break
                            if self.shouldRecipeBeShown: break
                        if self.shouldRecipeBeShown:
                            if datetime.datetime.strptime(self.globalRecipesDict["recipes"][i]["data"], '%Y-%m-%d %H:%M:%S.%f') > self.userLeaveTime:
                                self.quantNotifications += 1

                                self.allNotificationsCard = Frame(self.notificationsSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                                self.allNotificationsCard.pack(pady = 3)

                                self.allNotificationsPictureCanvas = Canvas(self.allNotificationsCard, width = "65", height = "65")
                                self.allNotificationsPictureCanvas.place(x = 10, y = 5)
                                self.allNotificationsPictureCanvas.imgpath = self.globalRecipesDict["recipes"][i]["imgpath"]
                                self.allNotificationsPictureCanvas.image = ImageTk.PhotoImage(Image.open(self.allNotificationsPictureCanvas.imgpath).resize((65, 65)))
                                self.allNotificationsPictureCanvas.create_image(32.5, 32.5, image = self.allNotificationsPictureCanvas.image, anchor = CENTER)

                                self.allnotificationsName = Label(self.allNotificationsCard, text = "Título: " + self.globalRecipesDict["recipes"][i]["titulo"])
                                self.allnotificationsName.place(x = 90, y = 5)

                                self.allRecipesNotificationTime = Label(self.allNotificationsCard, text = "Tempo de confeção: " + self.globalRecipesDict["recipes"][i]["tempo_confecao"].split(";")[0] + "h " + self.globalRecipesDict["recipes"][i]["tempo_confecao"].split(";")[1] + "min")
                                self.allRecipesNotificationTime.place(x = 90, y = 30)

                                self.recipeNotificationLikes = Label(self.allNotificationsCard, text = "Likes: " + self.globalRecipesDict["recipes"][i]["likes"])
                                self.recipeNotificationLikes.place(x = 90, y = 55)

                                self.recipeNotificationRating = Label(self.allNotificationsCard, text = "Rating: " + str(self.globalRecipesDict["recipes"][i]["rating"]))
                                self.recipeNotificationRating.place(x = 150, y = 55)

                                self.allRecipesNotificationsCreator = Label(self.allNotificationsCard, text = "Criado por: " + self.MainProgram_GlobalFunctions("GetUserNameFromEmail", self.globalRecipesDict["recipes"][i]["email"]) + ", " + str(datetime.datetime.strptime(self.globalRecipesDict["recipes"][i]["data"], '%Y-%m-%d %H:%M:%S.%f').strftime("%d/%m/%Y")))
                                self.allRecipesNotificationsCreator.place(x = 220, y = 55)

                                self.notificationRecipesSeeMore = Button(self.allNotificationsCard, text = "Ver notificação", command = partial(DismissNotification, self.globalRecipesDict["recipes"][i]["index"]))
                                self.notificationRecipesSeeMore.place(x = 480, y = 27)
                    if self.quantNotifications == 0: self.shouldTheNoNotificationsCardBeDisplayed = True
                    self.notificationsTitle["text"] = "Notificações (" + str(self.quantNotifications) + ")"
                else: self.shouldTheNoNotificationsCardBeDisplayed = True

            if self.shouldTheNoNotificationsCardBeDisplayed:
                self.noRecipesFoundCardNotification = Frame(self.notificationsSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                self.noRecipesFoundCardNotification.pack(pady = 3)
                self.noRecipesNotification = Label(self.notificationsSecondFrame, text = "Não tem nenhumas notificações!")
                self.noRecipesNotification.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    def MainProgram_GlobalFunctions(self, func, *arg):
        def ClearFilters(a):
            if str(type(a)) == "<class 'tkinter.Entry'>": a.delete(0, END)
            else: a.current(0)

        def ClearAllFilters(a):
            if a == 1:
                self.orderByDropdown.current(0)
                self.searchByCategoryDropdown.current(0)
                self.searchByIngredientText.delete(0, END)
                self.searchByTitleText.delete(0, END)
            elif a == 2:
                self.usersRecipesOrderByDropdown.current(0)
                self.usersRecipesSearchByCategoryDropdown.current(0)
                self.usersRecipesSearchByIngredientText.delete(0, END)
                self.usersRecipesSearchByTitleText.delete(0, END)
            elif a == 3:
                self.usersFavoritesOrderByDropdown.current(0)
                self.usersFavoritesSearchByCategoryDropdown.current(0)
                self.usersFavoritesSearchByIngredientText.delete(0, END)
                self.usersFavoritesSearchByTitleText.delete(0, END)

        def ResetScrollRegion(target):
            target.configure(scrollregion = target.bbox("all"))

        def GetUserNameFromEmail(email):
            returnName = ""
            with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                for line in f:
                    if line.strip():
                        if line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10] == EncryptSHA256(email):
                            returnName = DecryptString(line.strip().split(";")[2], line.strip().split(";")[0][0:len(line.strip().split(";")[0]) - 10])
            return returnName

        if func == "ClearFilters":
            ClearFilters(list(arg)[0])
        elif func == "ClearAllFilters":
            ClearAllFilters(list(arg)[0])
        elif func == "ResetScrollRegion":
            ResetScrollRegion(list(arg)[0])
        elif func == "GetUserNameFromEmail":
            return GetUserNameFromEmail(list(arg)[0])

    def MainProgram_AddRecipe(self, page, filters):
        self.newRecipeWindow = Toplevel(self.master)
        self.app = Recipe(self.newRecipeWindow, page, filters)

    def MainProgram_ShowRecipeDetails(self, id = 0, path = "", page = "", filters = []):
        def RecipeDetailsCustomClose():
            self.recipeDetailsWindow.destroy()
            self.master.update()
            self.MainProgram_ShowRecipeCards(page, filters)

        def VerifyUserLike():
            self.hasUserLikedThisRecipe = False
            if os.path.getsize(path + "\\likes\\wholiked.txt") > 0:
                with open(path + "\\likes\\wholiked.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip():
                            if line.strip() == EncryptSHA256(self.loggedInUserInformation[1]):
                                self.hasUserLikedThisRecipe = True
            return self.hasUserLikedThisRecipe

        def LikeRecipe():
            self.currentLikes = 0
            if VerifyUserLike():
                self.likeImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\heartIcon2.png").resize((20, 20)))
                self.likeButton.currentImg = "heartIcon2.png"
                self.likeButton["image"] = self.likeImage

                self.userLikedList = []
                with open(path + "\\likes\\wholiked.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip():
                            if line.strip() != EncryptSHA256(self.loggedInUserInformation[1]):
                                self.userLikedList.append(line.strip())
                with open(path + "\\likes\\wholiked.txt", "w", encoding = "utf-8") as f:
                    for like in self.userLikedList:
                        if like.replace(" ", ""): f.write(like + "\n")

                with open(path + "\\likes\\nlikes.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.currentLikes = int(line.strip()) - 1
            else:
                self.likeImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\heartIcon.png").resize((20, 20)))
                self.likeButton.currentImg = "heartIcon.png"
                self.likeButton["image"] = self.likeImage

                with open(path + "\\likes\\wholiked.txt", "a", encoding = "utf-8") as f: f.write(EncryptSHA256(self.loggedInUserInformation[1]) + "\n")
                with open(path + "\\likes\\nlikes.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.currentLikes = int(line.strip()) + 1
            with open(path + "\\likes\\nlikes.txt", "w", encoding = "utf-8") as f: f.write(str(self.currentLikes))
            UpdateLikes()

        def UpdateLikes():
            self.currentRecipeLikes = 0
            with open(path + "\\likes\\nlikes.txt", "r", encoding = "utf-8") as f:
                for line in f.readlines():
                    if line.strip().replace(" ", ""):
                        self.currentRecipeLikes = line.strip()
            self.likesLabel["text"] = "Likes: " + str(self.currentRecipeLikes)
            self.globalRecipesDict["recipes"][int(id)]["likes"] = str(self.currentRecipeLikes)

        def VerifyUserFavorite():
            self.hasUserFavoritedThisRecipe = False
            with open(path + "\\favoritedby.txt", "r", encoding = "utf-8") as f:
                for line in f.readlines():
                    if line.strip():
                        if line.strip() == EncryptSHA256(self.loggedInUserInformation[1]):
                            self.hasUserFavoritedThisRecipe = True
            return self.hasUserFavoritedThisRecipe

        def FavoriteRecipe():
            if VerifyUserFavorite():
                self.favImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\favIcon2.png").resize((20, 20)))
                self.favButton.currentImg = "favIcon2.png"
                self.favButton["image"] = self.favImage
                self.usersFavoritedList = []
                with open(path + "\\favoritedby.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip():
                            if line.strip() != EncryptSHA256(self.loggedInUserInformation[1]):
                                self.usersFavoritedList.append(line.strip())

                with open(path + "\\favoritedby.txt", "w", encoding = "utf-8") as f:
                    for favorite in self.usersFavoritedList:
                        if favorite.replace(" ", ""): f.write(favorite + "\n")
            else:
                self.favImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\favIcon.png").resize((20, 20)))
                self.favButton.currentImg = "favIcon.png"
                self.favButton["image"] = self.favImage
                with open(path + "\\favoritedby.txt", "a", encoding = "utf-8") as f: f.write(EncryptSHA256(self.loggedInUserInformation[1]) + "\n")

        def RateRecipe():
            self.hasUserRatedThisRecipe = False
            self.recipeRatesList = []
            with open(path + "\\rating.txt", "r", encoding = "utf-8") as f:
                for line in f.readlines():
                    if line.strip():
                        self.isThisTheLoggedInUser = False
                        if line.strip().split(";")[0] == EncryptSHA256(self.loggedInUserInformation[1]):
                            self.hasUserRatedThisRecipe = True
                            self.isThisTheLoggedInUser = True
                        if not self.isThisTheLoggedInUser: self.recipeRatesList.append(line.strip())
                        else: self.recipeRatesList.append(EncryptSHA256(self.loggedInUserInformation[1]) + ";" + str(self.ratingSpinBox.get()))
            if not self.hasUserRatedThisRecipe: self.recipeRatesList.append(EncryptSHA256(self.loggedInUserInformation[1]) + ";" + str(self.ratingSpinBox.get()))
            with open(path + "\\rating.txt", "w", encoding = "utf-8") as f:
                for rate in self.recipeRatesList:
                    if rate.replace(" ", ""): f.write(rate + "\n")
            UpdateRating()
            UpdateUserRating()

        def UpdateRating():
            self.averageRatingLabelVar = 0.0
            self.ratingsSum, self.quantRatings = 0, 0
            with open(path + "\\rating.txt", "r", encoding = "utf-8") as f:
                for line in f.readlines():
                    if line.strip().replace(" ", ""):
                        self.ratingsSum += int(line.split(";")[1])
                        self.quantRatings += 1
                if self.quantRatings > 0: self.averageRatingLabelVar = float(self.ratingsSum / self.quantRatings)
            self.averageRatingLabel["text"] = "Rating: " + str(float("{:.2f}".format(self.averageRatingLabelVar))) + " de 5.0"
            self.globalRecipesDict["recipes"][int(id)]["rating"] = str(float("{:.2f}".format(self.averageRatingLabelVar)))

        def UpdateUserRating():
            self.userGivenRating = "Nenhuma"
            with open(path + "\\rating.txt", "r", encoding = "utf-8") as f:
                for line in f.readlines():
                    if line.strip():
                        if line.strip().split(";")[0] == EncryptSHA256(self.loggedInUserInformation[1]):
                            self.userGivenRating = str(float(line.strip().split(";")[1]))
            self.usersRatingLabel["text"] = "A sua avaliação: " + self.userGivenRating

        def AddComment():
            if str(self.commentArea.get("1.0", END)).strip().replace(" ", ""):
                if len(str(self.commentArea.get("1.0", END)).strip()) <= 100:
                    self.wasAnyCommentIdFound = False
                    if len(os.listdir(path + "\\comments")) > 0:
                        for i in range(len(os.listdir(path + "\\comments"))):
                            if os.path.isfile(path + "\\comments\\" + os.listdir(path + "\\comments")[i]):
                                if "-" in str(os.listdir(path + "\\comments")[i]):
                                    self.savedCommentId = int(os.listdir(path + "\\comments")[i][:-4].split("-")[-1]) + 1
                                    self.wasAnyCommentIdFound = True
                            else:
                                if i == (len(os.listdir(path + "\\comments")) - 1) and not self.wasAnyCommentIdFound: self.savedCommentId = 1
                    else: self.savedCommentId = 1
                    with open(path + "\\comments\\comment-id-" + str(self.savedCommentId) + ".txt", "w", encoding = "utf-8") as f:
                        f.write(str(self.savedCommentId) + ";" + EncryptSHA256(self.loggedInUserInformation[1]) + ";" + EncryptString(self.loggedInUserInformation[2], "auth") + ";" + EncryptString(str(datetime.datetime.now()), "auth") + ";" + EncryptString(str(self.commentArea.get("1.0", END)).strip(), "auth"))
                else: messagebox.showerror("Erro", "O comentário não deve exceder os 100 caracteres", parent = self.recipeDetailsWindow)
            else: messagebox.showerror("Erro", "O comentário deve ter conteúdo", parent = self.recipeDetailsWindow)
            UpdateComments()

        def UpdateComments():
            def ShowNoCommentsCard():
                self.allComments = Frame(self.commentsSecondFrame, width = "355", height = "75", highlightbackground = "black", highlightthickness = 1)
                self.allComments.pack(pady = 3)
                self.commentText=Label(self.allComments, wraplength = 310, justify = LEFT, text="Não existem comentários para esta receita")
                self.commentText.place(x=60,y=25)

            self.ClearWindowWidgets(self.commentsLabelFrame)

            # [Layout] - Recipe interaction - users comments
            self.commentsFrame = Frame(self.commentsLabelFrame, width = 390, height = 380)
            self.commentsFrame.place(x = 5, y = 10)
            self.commentsCanvas = Canvas(self.commentsFrame, width = 355, height = 380)
            self.commentsCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.commentsCanvasScrollbar = ttk.Scrollbar(self.commentsFrame, orient = VERTICAL, command = self.commentsCanvas.yview)
            self.commentsCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.commentsCanvas.configure(yscrollcommand = self.commentsCanvasScrollbar.set)
            self.commentsCanvas.bind('<Configure>', lambda e: self.commentsCanvas.configure(scrollregion = self.commentsCanvas.bbox("all")))
            self.commentsSecondFrame = Frame(self.commentsCanvas)
            self.commentsCanvas.create_window((0, 0), window = self.commentsSecondFrame, anchor = NW)

            if len(os.listdir(path + "\\comments")) > 0:
                for i in range(len(os.listdir(path + "\\comments")) -1, -1, -1):
                    if os.path.isfile(path + "\\comments\\" + os.listdir(path + "\\comments")[i]):
                        if "-" in str(os.listdir(path + "\\comments")[i]):
                            with open(path + "\\comments\\" + os.listdir(path + "\\comments")[i], "r", encoding = "utf-8") as f:
                                for line in f.readlines():
                                    if line.strip():
                                        self.allComments = Frame(self.commentsSecondFrame, width = "355", height = "75", highlightbackground = "black", highlightthickness = 1)
                                        self.allComments.pack(pady = 3)

                                        self.commentedBy = DecryptString(line.strip().split(";")[2], "auth")
                                        self.creatorComment=Label(self.allComments, text="Autor: " + self.commentedBy)
                                        self.creatorComment.place(x=3,y=3)

                                        self.commentDate = DecryptString(line.strip().split(";")[3], "auth")
                                        self.commentDateObject = datetime.datetime.strptime(self.commentDate, '%Y-%m-%d %H:%M:%S.%f')
                                        self.dateComment=Label(self.allComments, text=str(self.commentDateObject.strftime("%d/%m/%Y %H:%M")))
                                        self.dateComment.place(x=250,y=3)

                                        separator = ttk.Separator(self.allComments, orient='horizontal')
                                        separator.place(relx=0, rely=0.37, relwidth=1)

                                        self.commentContent = DecryptString(line.strip().split(";")[4], "auth")
                                        self.commentText=Label(self.allComments, wraplength = 300, justify = LEFT, text="Mensagem: " + self.commentContent)
                                        self.commentText.place(x=3,y=30)

                                        if EncryptSHA256(self.loggedInUserInformation[1]) == line.strip().split(";")[1] or self.loggedInUserInformation[3] == "administrator":
                                            self.removeCommentButton=Button(self.allComments, text="X", width="2", relief="groove", command = partial(RemoveComment, line.strip().split(";")[0]))
                                            self.removeCommentButton.place(x=320,y=35)
            else: ShowNoCommentsCard()

            # [Layout] - Recipe interaction - comment textbox
            self.commentArea = Text(self.commentsLabelFrame, width = "62", height = "5", wrap = WORD, font = ('TkDefaultFont'))
            self.commentArea.place(x = 5, y = 415)
            self.addCommentIcon = ttk.Button(self.commentsLabelFrame, text = "Comentar", command = AddComment)
            self.addCommentIcon.place(x = 150, y = 505)

        def RemoveComment(id):
            self.wasTheIdFound = False
            if len(os.listdir(path + "\\comments")) > 0:
                for i in range(len(os.listdir(path + "\\comments"))):
                    if os.path.isfile(path + "\\comments\\" + os.listdir(path + "\\comments")[i]):
                        if "-" in str(os.listdir(path + "\\comments")[i]):
                            if int(os.listdir(path + "\\comments")[i][:-4].split("-")[-1]) == int(id):
                                self.wasTheIdFound = True
                                break
            else: messagebox.showerror("Erro", "Ocorreu um erro ao remover comentário", parent = self.recipeDetailsWindow)
            if not self.wasTheIdFound: messagebox.showerror("Erro", "Ocorreu um erro ao remover comentário", parent = self.recipeDetailsWindow)
            else: os.remove(path + "\\comments\\comment-id-" + str(id) + ".txt")
            UpdateComments()

        if id == 0 or path == "":
            messagebox.showerror("Erro", "Ocorreu um erro ao tentar carregar as informações desta receita", parent = self.master)
        else:
            # [Initial configuration]
            self.recipeDetailsWindow = Toplevel(self.master)
            self.recipeDetailsWindow.geometry("840x600")
            CenterWindow(self.recipeDetailsWindow)
            self.recipeDetailsWindow.title("Receita")
            self.recipeDetailsWindow.resizable(False, False)
            self.recipeDetailsWindow.grab_set()
            self.recipeDetailsWindow.focus_force()
            self.recipeDetailsWindow.protocol("WM_DELETE_WINDOW", RecipeDetailsCustomClose)

            # [Layout] - Recipe information fieldset
            self.recipeInformation = LabelFrame(self.recipeDetailsWindow, width = "420", height = "365", text = "Informação da receita")
            self.recipeInformation.place(x = 10, y = 10)

            try:
                # Before designing the window increment the file views.txt of the chosen recipe
                self.hasUserViewedThisRecipe = False
                if os.path.getsize(path + "\\views\\whoviewed.txt") > 0:
                    with open(path + "\\views\\whoviewed.txt", "r", encoding = "utf-8") as f:
                        for line in f.readlines():
                            if line.strip():
                                if line.strip() == EncryptSHA256(self.loggedInUserInformation[1]):
                                    self.hasUserViewedThisRecipe = True

                if not self.hasUserViewedThisRecipe:
                    self.currentViews = 0
                    with open(path + "\\views\\whoviewed.txt", "a", encoding = "utf-8") as f: f.write(EncryptSHA256(self.loggedInUserInformation[1]) + "\n")
                    with open(path + "\\views\\nviews.txt", "r", encoding = "utf-8") as f:
                        for line in f.readlines():
                            if line.strip().replace(" ", ""):
                                self.currentViews = int(line.strip()) + 1
                    with open(path + "\\views\\nviews.txt", "w", encoding = "utf-8") as f: f.write(str(self.currentViews))

                # [Layout] - Recipe title
                self.recipeDetailsNameVar = ""
                with open(path + "\\name.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeDetailsNameVar = DecryptString(line, "auth")
                self.recipeDetailsName = Label(self.recipeInformation, text = self.recipeDetailsNameVar, wraplength = 280, justify = LEFT)
                self.recipeDetailsName.place(x = 5, y = 5)
                self.recipeDetailsName.config(font = ('Helvetica 12 bold'))

                # [Layout] - Recipe picture
                self.recipeDetailsPictureCanvas = Canvas(self.recipeInformation, width = "110", height = "110")
                self.recipeDetailsPictureCanvas.place(x = 295, y = 5)
                CreatePath()
                if os.path.exists(path + "\\picture.jpg"):
                    self.recipeDetailsPictureCanvas.imgpath = path + "\\picture.jpg"
                elif os.path.exists(path + "\\picture.png"):
                    self.recipeDetailsPictureCanvas.imgpath = path + "\\picture.png"
                elif os.path.exists(path + "\\picture.jpeg"):
                    self.recipeDetailsPictureCanvas.imgpath = path + "\\picture.jpeg"
                else:
                    self.recipeDetailsPictureCanvas.imgpath = os.getcwd() + "\\data\\images\\default_recipes.jpg"
                self.recipeDetailsPictureCanvas.image = ImageTk.PhotoImage(Image.open(self.recipeDetailsPictureCanvas.imgpath).resize((110, 110)))
                self.recipeDetailsPictureCanvas.create_image(55, 55, image = self.recipeDetailsPictureCanvas.image, anchor = CENTER)

                # [Layout] - Recipe description
                self.recipeDetailsDescriptionLabel = Label(self.recipeInformation, text = "Descrição da receita")
                self.recipeDetailsDescriptionLabel.place(x = 5, y = 55)
                self.recipeDetailsDescriptionText = Text(self.recipeInformation, font = ('TkDefaultFont'), wrap = WORD, width = "45", height = "4")
                self.recipeDetailsDescriptionText.place(x = 8, y = 80)
                self.recipeDetailsDescriptionTextVar = ""
                with open(path + "\\description.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeDetailsDescriptionTextVar += line
                self.recipeDetailsDescriptionText.insert(END, DecryptString(self.recipeDetailsDescriptionTextVar, "auth"))
                self.recipeDetailsDescriptionText.config(state = DISABLED)

                # [Layout] - Recipe procedure
                self.recipeDetailsPreparationModeLabel = Label(self.recipeInformation, text = "Preparação")
                self.recipeDetailsPreparationModeLabel.place(x = 5, y = 150)
                self.recipeDetailsPreparationModeText = Text(self.recipeInformation, font = ('TkDefaultFont'), wrap = WORD, width = "45", height = "7")
                self.recipeDetailsPreparationModeText.place(x = 8, y = 175)
                self.recipeDetailsPreparationModeTextVar = ""
                with open(path + "\\procedure.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeDetailsPreparationModeTextVar += line
                self.recipeDetailsPreparationModeText.insert(END, DecryptString(self.recipeDetailsPreparationModeTextVar, "auth"))
                self.recipeDetailsPreparationModeText.config(state = DISABLED)

                # [Layout] - Recipe ingredients
                self.recipeDetailsIngredientsLabel = Label(self.recipeInformation, text = "Ingredientes")
                self.recipeDetailsIngredientsLabel.place(x = 290, y = 150)
                self.recipeDetailsIngredientsList = Listbox(self.recipeInformation, font = ('TkDefaultFont'), width="19", height = "7")
                with open(path + "\\ingredients.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeDetailsIngredientsList.insert(END, DecryptString(line, "auth"))
                self.recipeDetailsIngredientsList.place(x = 290, y = 175)

                # [Layout] - Recipe cooking time
                self.recipeCookingTimeVar = "Tempo de confeção: "
                with open(path + "\\time.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeCookingTimeVar += line.split(";")[0] + "h " + line.split(";")[1] + "min"
                self.recipeCookingTime = Label(self.recipeInformation, text = self.recipeCookingTimeVar)
                self.recipeCookingTime.place(x = 5, y = 295)

                self.categoriesContent = ", ".join(self.globalRecipesDict["recipes"][int(id)]["categorias"])
                self.recipeCategoriesContent = Label(self.recipeInformation, text = "Categorias: " + self.categoriesContent)
                self.recipeCategoriesContent.place(x = 5, y = 320)

                # [Layout] - Recipe statistics fieldset
                self.recipeStatistics = LabelFrame(self.recipeDetailsWindow, width = "420", height = "100", text = "Estatísticas")
                self.recipeStatistics.place(x = 10, y = 380)

                # [Layout] - Recipe statistics - average rating
                self.averageRatingLabel = Label(self.recipeStatistics, text = "Rating: 0.0")
                self.averageRatingLabel.place(x = 10, y = 5)
                UpdateRating()

                # [Layout] - Recipe statistics - likes
                self.likesLabel = Label(self.recipeStatistics, text = "Likes: 0")
                self.likesLabel.place(x = 10, y = 30)
                UpdateLikes()

                # [Layout] - Recipe statistics - views
                self.viewsLabelVar = 0
                with open(path + "\\views\\nviews.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.viewsLabelVar = line
                self.viewsLabel = Label(self.recipeStatistics, text = "Visualizações: " + str(self.viewsLabelVar))
                self.viewsLabel.place(x = 10, y = 55)
                self.globalRecipesDict["recipes"][int(id)]["views"] = str(self.viewsLabelVar)

                # [Layout] - Recipe statistics - author
                self.recipeAuthorEmailVar = ""
                self.recipeAuthorNameVar = ""
                with open(path + "\\author.txt", "r", encoding = "utf-8") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.recipeAuthorEmailVar = DecryptString(line.split(";")[0], "auth")
                            self.recipeAuthorNameVar = self.MainProgram_GlobalFunctions("GetUserNameFromEmail", self.globalRecipesDict["recipes"][int(id)]["email"])
                self.authorLabel = Label(self.recipeStatistics, text = "Criado por: " + str(self.recipeAuthorNameVar))
                self.authorLabel.place(x = 245, y = 5)

                # [Layout] - Recipe statistics - creation date
                self.creationDateLabel = "01/01/2021"
                self.wasDateFoundChecker = False
                with open(path + "\\date.txt", "r") as f:
                    for line in f.readlines():
                        if line.strip().replace(" ", ""):
                            self.creationDateLabel = DecryptString(line, "auth")
                            self.wasDateFoundChecker = True
                if self.wasDateFoundChecker: self.dateObject = datetime.datetime.strptime(self.creationDateLabel, '%Y-%m-%d %H:%M:%S.%f')
                self.authorLabel = Label(self.recipeStatistics, text = "Criado em: " + str(self.dateObject.strftime("%d/%m/%Y %H:%M")))
                self.authorLabel.place(x = 245, y = 30)

                # [Layout] - User interactions fieldset
                self.userInteractions = LabelFrame(self.recipeDetailsWindow, width = "420", height = "100", text = "Ações")
                self.userInteractions.place(x = 10, y = 490)

                # [Layout] - Verifies if the like/fav icons exist and/or have been tampered with
                CreatePath()
                if MD5Checksum(3) != ["4838e2badab07ade21e9e8a714e46b96", "c4dfc88dac9042d626c501c1f07b6545", "e089f20ce2957c46617ec4691214d730", "1fa2f622aa13752e4ed74d8017fa5364"]:
                    messagebox.showerror("Erro", "Os ícones de like/fav não foram reconhecidos\nO programa irá fechar", parent = self.recipeDetailsWindow)
                    os._exit(0)

                # [Layout] - User interactions - likes
                self.userLikes = Label(self.userInteractions, text = "Like:")
                self.userLikes.place(x = 110, y = 10)
                if VerifyUserLike(): self.likeImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\heartIcon.png").resize((20, 20), Image.ANTIALIAS))
                else: self.likeImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\heartIcon2.png").resize((20, 20), Image.ANTIALIAS))
                self.likeButton = Button(self.userInteractions, image = self.likeImage, compound = CENTER, relief = "flat", width = "20", height = "20", highlightthickness = 0, bd = 0, command = LikeRecipe)
                self.likeButton.currentImg = "heartIcon2.png"
                self.likeButton.place(x = 150, y = 10)

                # [Layout] - Recipe interaction - favorites
                self.userFav = Label(self.userInteractions, text = "Adicionar aos favoritos:")
                self.userFav.place(x = 10, y = 40)
                if VerifyUserFavorite(): self.favImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\favIcon.png").resize((20, 20), Image.ANTIALIAS))
                else: self.favImage = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\favIcon2.png").resize((20, 20), Image.ANTIALIAS))
                self.favButton = Button(self.userInteractions, image = self.favImage, compound = CENTER, relief = "flat", width = "20", height = "20", highlightthickness = 0, bd = 0, command = FavoriteRecipe)
                self.favButton.currentImg = "favIcon2.png"
                self.favButton.place(x = 150, y = 40)

                # [Layout] - Recipe interaction - ratings
                self.ratingLabel = Label(self.userInteractions, text = "Avaliar:")
                self.ratingLabel.place(x = 200 , y = 10)
                self.ratingSpinBox = Spinbox(self.userInteractions, from_ = 1, to = 5, width = 2)
                self.ratingSpinBox.place(x = 250 , y = 11)
                self.ratingButton = ttk.Button(self.userInteractions, text = "Avaliar", command = RateRecipe)
                self.ratingButton.place(x = 285 , y = 8)
                self.usersRatingLabel = Label(self.userInteractions, text = "A sua avaliação: Nenhuma")
                self.usersRatingLabel.place(x = 200, y = 40)
                UpdateUserRating()

                # [Layout] - Recipe interaction - users comments fieldset
                self.commentsLabelFrame = LabelFrame(self.recipeDetailsWindow, width = "390", height = "580", text = "Comentários")
                self.commentsLabelFrame.place(x = 440, y = 10)
                UpdateComments()
            except:
                messagebox.showerror("Erro", "Ocorreu um erro inesperado\nO programa vai fechar", parent = self.master)
                os._exit(0)

    def UpdateDictionary(self, index):
        copia = self.globalRecipesDict.copy()
        self.globalRecipesDict.clear()
        self.globalRecipesDict = { "recipes": [] }
        currentIndex = 0
        self.currentDictId -= 1
        for i in range(len(copia["recipes"])):
            if int(index) != i:
                self.globalRecipesDict["recipes"].append(copia["recipes"][i])
                self.globalRecipesDict["recipes"][currentIndex]["index"] = str(currentIndex)
                currentIndex += 1

    def MainProgram_EditRecipe(self, id, page, filters):
        def SelectRecipeImageEdit():
            self.pathImageRecipeEdit = filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
            if self.pathImageRecipeEdit:
                try:
                    Image.open(self.pathImageRecipeEdit).verify()
                    self.recipeImageCheck = True
                except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem", parent = self.editRecipe)
                if self.recipeImageCheck:
                    try:
                        if Image.open(self.pathImageRecipeEdit).size[0] >= 100:
                            if Image.open(self.pathImageRecipeEdit).size[1] >= 100:
                                if os.stat(self.pathImageRecipeEdit).st_size <= 5000000:
                                    self.recipePictureCanvasEdit.imgpath = self.pathImageRecipeEdit
                                    self.recipePictureCanvasEdit.image = ImageTk.PhotoImage(Image.open(self.recipePictureCanvasEdit.imgpath).resize((100, 100)))
                                    self.recipePictureCanvasEdit.create_image(50, 50, image = self.recipePictureCanvasEdit.image, anchor = CENTER)
                                else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb", parent = self.editRecipe)
                            else: messagebox.showerror("Erro", "A altura da imagem é inferior a 100px", parent = self.editRecipe)
                        else: messagebox.showerror("Erro", "A largura da imagem é inferior a 100px", parent = self.editRecipe)
                    except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema", parent = self.editRecipe)
                    except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.editRecipe)

        def AddNewIngredientEdit():
            def AddIngredient():
                if self.listboxRecipeIngredientsEdit.size() < 30:
                    if str(self.recipeIngredientsTextEdit.get()).replace(" ", ""):
                        if len(str(self.recipeIngredientsTextEdit.get()).replace(" ", "")) > 2:
                            self.listboxRecipeIngredientsEdit.insert(END, str(self.recipeIngredientsTextEdit.get()))
                            self.editNewIngredientWindow.destroy()
                            self.master.update()
                            self.master.grab_set()
                        else: messagebox.showerror("Erro", "O campo de ingrediente tem de ter, pelo menos, 3 caracteres", parent = self.editNewIngredientWindow)
                    else: messagebox.showerror("Erro", "Introduza algum ingrediente", parent = self.editNewIngredientWindow)
                else: messagebox.showerror("Erro", "Atingiu o limite máximo de ingredientes (30)", parent = self.editNewIngredientWindow)

            def AddNewIngredientCustomClose():
                self.editNewIngredientWindow.destroy()
                self.master.update()
                self.master.grab_set()

            # [Layout] - Add ingredient window
            self.editNewIngredientWindow = Toplevel(self.master)
            self.editNewIngredientWindow.geometry("250x100")
            CenterWindow(self.editNewIngredientWindow)
            self.editNewIngredientWindow.title("Adicionar Ingrediente")
            self.editNewIngredientWindow.resizable(False, False)
            self.editNewIngredientWindow.grab_set()
            self.editNewIngredientWindow.protocol("WM_DELETE_WINDOW", AddNewIngredientCustomClose)

            # [Layout] - Add new ingredient textbox
            self.recipeIngredientsLabelEdit = Label(self.editNewIngredientWindow, text = "Nome do ingrediente:")
            self.recipeIngredientsLabelEdit.place(x = 60, y = 10)
            self.recipeIngredientsTextEdit = Entry(self.editNewIngredientWindow, width = 35)
            self.recipeIngredientsTextEdit.place(x = 18, y = 35)
            self.recipeIngredientsTextEdit.focus_force()

            # [Layout] - Add new ingredient button
            self.recipeIngredientsButton = ttk.Button(self.editNewIngredientWindow, text = "Adicionar", command = AddIngredient)
            self.recipeIngredientsButton.place(x = 85, y = 65)

        def RemoveIngredientEdit():
            try:
                self.selectedIngredientEdit = self.listboxRecipeIngredientsEdit.curselection()[0]
                self.listboxRecipeIngredientsEdit.delete(self.selectedIngredientEdit)
            except:
                messagebox.showerror("Erro", "Selecione um ingrediente para remover", parent = self.editRecipe)

        def AddCategory():
            def AddCategoryToList():
                # Verify if category has already been chosen
                self.wasCategoryAlreadyChosen = False
                for i in range(self.listboxRecipeCategoriesEdit.size()):
                    if self.selectNewCategoryDropdownEdit.get() == self.listboxRecipeCategoriesEdit.get(i):
                        self.wasCategoryAlreadyChosen = True
                        break
                if not self.wasCategoryAlreadyChosen:
                    self.listboxRecipeCategoriesEdit.insert(END, self.selectNewCategoryDropdownEdit.get())
                    AddCategoryCustomClose()
                else:
                    messagebox.showerror("Erro", "A categoria selecionada já foi escolhida", parent = self.addCategoryWindowEdit)

            def AddCategoryCustomClose():
                self.addCategoryWindowEdit.destroy()
                self.master.update()
                self.master.grab_set()

            # [Initial configuration]
            self.addCategoryWindowEdit = Toplevel(self.master)
            self.addCategoryWindowEdit.geometry("250x100")
            CenterWindow(self.addCategoryWindowEdit)
            self.addCategoryWindowEdit.title("Adicionar Categoria")
            self.addCategoryWindowEdit.resizable(False, False)
            self.addCategoryWindowEdit.grab_set()
            self.addCategoryWindowEdit.focus_force()
            self.addCategoryWindowEdit.protocol("WM_DELETE_WINDOW", AddCategoryCustomClose)

            # [Layout] - Category select box
            self.selectNewCategoryLabelEdit = Label(self.addCategoryWindowEdit, text = "Categoria:")
            self.selectNewCategoryLabelEdit.place(x = 90, y = 5)
            self.selectNewCategoryDropdownEdit = ttk.Combobox(self.addCategoryWindowEdit, value = self.globalCategoriesList, width = "25")
            self.selectNewCategoryDropdownEdit.place(x = 40, y = 40)
            self.selectNewCategoryDropdownEdit.current(0)

            # [Layout] - Add category button
            self.addNewCategoryButtonEdit = ttk.Button(self.addCategoryWindowEdit, text = "Adicionar", command = AddCategoryToList)
            self.addNewCategoryButtonEdit.place(x = 85, y = 65)

        def RemoveCategory():
            try:
                self.selectedCategory = self.listboxRecipeCategoriesEdit.curselection()[0]
                self.listboxRecipeCategoriesEdit.delete(self.selectedCategory)
            except:
                messagebox.showerror("Erro", "Selecione uma categoria para remover", parent = self.editRecipe)

        def EditRecipeCustomClose():
            self.editRecipe.destroy()
            self.master.update()

        def EditAllRecipe():
            if str(self.recipeNameTextEdit.get()).replace(" ", ""):
                if re.compile(r"^[^\W\d_]+(-[^\W\d_]+)?$", re.U).match(str(self.recipeNameTextEdit.get()).replace(" ", "")):
                    if len(str(self.recipeNameTextEdit.get()).replace(" ", "")) > 10:
                        if len(str(self.recipeNameTextEdit.get()).replace(" ", "")) <= 50:
                            if str(self.recipeDescriptionTextEdit.get("1.0", END)).strip().replace(" ", ""):
                                if len(str(self.recipeDescriptionTextEdit.get("1.0", END)).replace(" ", "")) > 20:
                                    if len(str(self.recipeDescriptionTextEdit.get("1.0", END)).replace(" ", "")) <= 255:
                                        if self.listboxRecipeIngredientsEdit.size() > 0:
                                            if str(self.recipeProcedureTextEdit.get("1.0", END)).strip().replace(" ", ""):
                                                if len(str(self.recipeProcedureTextEdit.get("1.0", END)).replace(" ", "")) > 20:
                                                    if len(str(self.recipeProcedureTextEdit.get("1.0", END)).replace(" ", "")) <= 1250:
                                                        if str(self.recipeHoursSpinboxEdit.get()) == "0" and str(self.recipeMinutesSpinboxEdit.get()) == "0":
                                                            messagebox.showerror("Erro", "O tempo de confeção é inválido", parent = self.editRecipe)
                                                        else:
                                                            if self.listboxRecipeCategoriesEdit.size() > 0:
                                                                self.doesUserWantToContinueRecipePictureEdit = True
                                                                if self.recipePictureCanvasEdit.imgpath.split("\\")[-1] == "default_recipes.jpg":
                                                                    self.continueDefaultRecipeEdit = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de receita, se continuar irá ser selecionada a foto de receita padrão, prosseguir?", icon = "warning", parent = self.master)
                                                                    if self.continueDefaultRecipeEdit == "no":
                                                                        self.doesUserWantToContinueRecipePictureEdit = False
                                                                    else:
                                                                        if MD5Checksum(2) != "8b53223e6b0ba3a1564ef2a5397bb03e":
                                                                            messagebox.showerror("Erro", "A foto de receita padrão não foi reconhecida\nO programa irá fechar", parent = self.editRecipe)
                                                                            os._exit(0)
                                                                if self.doesUserWantToContinueRecipePictureEdit:
                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\name.txt", "w") as f:
                                                                        f.write(EncryptString(str(self.recipeNameTextEdit.get()), "auth"))
                                                                    self.globalRecipesDict["recipes"][int(id)]["titulo"] = str(self.recipeNameTextEdit.get())

                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\description.txt", "w") as f:
                                                                        f.write(EncryptString(str(self.recipeDescriptionTextEdit.get("1.0", END)), "auth"))
                                                                    self.globalRecipesDict["recipes"][int(id)]["descricao"] = str(self.recipeDescriptionTextEdit.get("1.0", END))

                                                                    self.globalRecipesDict["recipes"][int(id)]["ingredientes"].clear()
                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\ingredients.txt", "w") as f:
                                                                        for i in range(self.listboxRecipeIngredientsEdit.size()):
                                                                            self.globalRecipesDict["recipes"][int(id)]["ingredientes"].append(self.listboxRecipeIngredientsEdit.get(i))
                                                                            f.write(EncryptString(self.listboxRecipeIngredientsEdit.get(i), "auth") + "\n")

                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\procedure.txt", "w") as f:
                                                                        f.write(EncryptString(str(self.recipeProcedureTextEdit.get("1.0", END)), "auth"))
                                                                    self.globalRecipesDict["recipes"][int(id)]["procedimento"] = str(self.recipeProcedureTextEdit.get("1.0", END))

                                                                    self.globalRecipesDict["recipes"][int(id)]["categorias"].clear()
                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\categories.txt", "w") as f:
                                                                        for i in range(self.listboxRecipeCategoriesEdit.size()):
                                                                            self.globalRecipesDict["recipes"][int(id)]["categorias"].append(self.listboxRecipeCategoriesEdit.get(i))
                                                                            f.write(EncryptString(self.listboxRecipeCategoriesEdit.get(i), "auth") + "\n")

                                                                    with open(self.globalRecipesDict["recipes"][int(id)]["path"] + "\\time.txt", "w") as f:
                                                                        f.write(str(self.recipeHoursSpinboxEdit.get()) + ";" + str(self.recipeMinutesSpinboxEdit.get()))
                                                                    self.globalRecipesDict["recipes"][int(id)]["tempo_confecao"] = str(self.recipeHoursSpinboxEdit.get()) + ";" + str(self.recipeMinutesSpinboxEdit.get())

                                                                    if self.recipePictureCanvasEdit.imgpath != self.globalRecipesDict["recipes"][int(id)]["imgpath"]:
                                                                        os.remove(self.globalRecipesDict["recipes"][int(id)]["imgpath"])
                                                                        shutil.copy2(self.recipePictureCanvasEdit.imgpath, self.globalRecipesDict["recipes"][int(id)]["path"] + "\\picture" + os.path.splitext(self.recipePictureCanvasEdit.imgpath)[1])
                                                                        self.globalRecipesDict["recipes"][int(id)]["imgpath"] = self.globalRecipesDict["recipes"][int(id)]["path"] + "\\picture" + os.path.splitext(self.recipePictureCanvasEdit.imgpath)[1]

                                                                    messagebox.showinfo("Sucesso", "A receita foi editada com sucesso", parent = self.editRecipe)
                                                                    EditRecipeCustomClose()
                                                                    self.MainProgram_ShowRecipeCards(page, filters)
                                                            else: messagebox.showerror("Erro", "A receita tem de ter, pelo menos, 1 categoria", parent = self.editRecipe)
                                                    else: messagebox.showerror("Erro", "O campo de procedimentos da receita não pode exceder os 1250 caracteres", parent = self.editRecipe)
                                                else: messagebox.showerror("Erro", "O campo de procedimentos da receita tem de ter, pelo menos, 20 caracteres", parent = self.editRecipe)
                                            else: messagebox.showerror("Erro", "O campo de procedimenos da receita é obrigatório", parent = self.editRecipe)
                                        else: messagebox.showerror("Erro", "A receita tem de ter, pelo menos, 1 ingrediente", parent = self.editRecipe)
                                    else: messagebox.showerror("Erro", "O campo de descrição da receita não pode exceder os 255 caracteres", parent = self.editRecipe)
                                else: messagebox.showerror("Erro", "O campo de descrição da receita tem de ter, pelo menos, 20 caracteres", parent = self.editRecipe)
                            else: messagebox.showerror("Erro", "O campo de descrição da receita é obrigatório", parent = self.editRecipe)
                        else: messagebox.showerror("Erro", "O campo de nome da receita não pode exceder os 50 caracteres", parent = self.editRecipe)
                    else: messagebox.showerror("Erro", "O campo de nome da receita tem de ter, pelo menos, 10 caracteres", parent = self.editRecipe)
                else: messagebox.showerror("Erro", "O campo de nome da receita não pode conter caracteres especiais nem números", parent = self.editRecipe)
            else: messagebox.showerror("Erro", "O campo de nome da receita é obrigatório", parent = self.editRecipe)

        self.editRecipe=Toplevel(self.master)
        self.editRecipe.geometry("500x780")
        CenterWindow(self.editRecipe)
        self.editRecipe.title("Editar receita")
        self.editRecipe.resizable(False, False)
        self.editRecipe.grab_set()
        self.editRecipe.focus_force()
        self.editRecipe.protocol("WM_DELETE_WINDOW", EditRecipeCustomClose)

        # [Layout] - Recipe general information fieldset
        self.generalInformationLabelFrame = LabelFrame(self.editRecipe, text = "Informação Geral", width = "490", height = "280", bd = "2")
        self.generalInformationLabelFrame.place(x = 5, y = 5)

        # [Layout] - Recipe name
        self.recipeNameLabelEdit = Label(self.generalInformationLabelFrame, text = "Nome da receita:")
        self.recipeNameLabelEdit.place(x = 130, y = 35, anchor = E)
        self.recipeNameTextEdit = Entry(self.generalInformationLabelFrame, width = "45")
        self.recipeNameTextEdit.place(x = 150, y = 37.5, anchor = W)
        self.recipeNameTextEdit.insert(END, self.globalRecipesDict["recipes"][int(id)]["titulo"])

        # [Layout] - Recipe description
        self.recipeDescriptionLabelEdit = Label(self.generalInformationLabelFrame, text = "Descrição da receita:")
        self.recipeDescriptionLabelEdit.place(x = 130, y = 70, anchor = E)
        self.recipeDescriptionTextEdit = Text(self.generalInformationLabelFrame, height = "4", width = "45", wrap = WORD, font = ('TkDefaultFont'))
        self.recipeDescriptionTextEdit.place(x = 150, y = 97.5, anchor = W)
        self.recipeDescriptionTextEdit.insert(END, self.globalRecipesDict["recipes"][int(id)]["descricao"])

        # [Layout] - Recipe picture
        self.labelSelectRecipeImage = Label(self.generalInformationLabelFrame, text = "Foto do prato:")
        self.labelSelectRecipeImage.place(x = 130, y = 155, anchor = E)
        self.recipePictureCanvasEdit = Canvas(self.generalInformationLabelFrame, width = "100", height = "100")
        self.recipePictureCanvasEdit.place(x = 150, y = 200, anchor = W)

        try:
            self.recipePictureCanvasEdit.imgpath = self.globalRecipesDict["recipes"][int(id)]["imgpath"]
            self.recipePictureCanvasEdit.image = ImageTk.PhotoImage(Image.open(self.recipePictureCanvasEdit.imgpath).resize((100, 100)))
        except:
            CreatePath()
            if str(MD5Checksum(2)) == "8b53223e6b0ba3a1564ef2a5397bb03e":
                self.recipePictureCanvasEdit.imgpath = os.getcwd() + "\\data\\images\\default_recipes.jpg"
                self.recipePictureCanvasEdit.image = ImageTk.PhotoImage(Image.open(self.recipePictureCanvasEdit.imgpath).resize((100, 100)))
            else:
                messagebox.showerror("Erro", "A foto padrão das receitas não foi reconhecida\nO programa irá fechar", parent = self.master)
                os._exit(0)

        self.recipePictureCanvasEdit.create_image(0, 0, image = self.recipePictureCanvasEdit.image, anchor = NW)
        self.selectRecipeImageButtonEdit = ttk.Button(self.generalInformationLabelFrame, text = "Enviar imagem", command = SelectRecipeImageEdit)
        self.selectRecipeImageButtonEdit.place(x = 265, y = 164, anchor = W, width = 117)
        self.selectRecipeImageInfoEdit = Label(self.generalInformationLabelFrame, text = ".jpg .jpeg ou .png", wraplength = 200, justify = LEFT, font=(None, 8))
        self.selectRecipeImageInfoEdit.place(x = 265, y = 195, anchor = W)
        self.selectRecipeImageInfo2 = Label(self.generalInformationLabelFrame, text = "Atenção: Nem a largura nem a altura da imagem devem ser inferiores a 100px", wraplength = 150, justify = LEFT, font=(None, 8))
        self.selectRecipeImageInfo2.place(x = 265, y = 230, anchor = W)

        # [Layout] - Recipe ingredients fieldset
        self.ingredientsLabelFrameEdit = LabelFrame(self.editRecipe, text = "Ingredientes", width = "490", height = "130", bd = "2")
        self.ingredientsLabelFrameEdit.place(x = 5, y = 290)

        # [Layout] - Recipe ingredients
        self.recipeIngredientsLabelEdit = Label(self.ingredientsLabelFrameEdit, text = "Lista de ingredientes:")
        self.recipeIngredientsLabelEdit.place(x = 130, y = 20, anchor = E)

        # [Layout] - Ingredients list
        self.listboxRecipeIngredientsEdit = Listbox(self.ingredientsLabelFrameEdit, height = "5", width = "46")
        self.listboxRecipeIngredientsEdit.place(x = 149, y = 58, anchor = W)
        for i in range(len(self.globalRecipesDict["recipes"][int(id)]["ingredientes"])):
            self.listboxRecipeIngredientsEdit.insert(END, self.globalRecipesDict["recipes"][int(id)]["ingredientes"][i])

        # [Layout] - Add ingredients button
        self.addRecipeIngredientsEdit = ttk.Button(self.ingredientsLabelFrameEdit, text = "Adicionar", width = "17", command = AddNewIngredientEdit)
        self.addRecipeIngredientsEdit.place(x = 15, y = 40)

        # [Layout] - Remove ingredients button
        self.removeRecipeIngredientsEdit = ttk.Button(self.ingredientsLabelFrameEdit, text = "Remover", width = "17", command = RemoveIngredientEdit)
        self.removeRecipeIngredientsEdit.place(x = 15, y = 72)

        # [Layout] - Recipe procedure fieldset
        self.recipeProcedureLabelFrameEdit = LabelFrame(self.editRecipe, text = "Confeção", width = "490", height = "160", bd = "2")
        self.recipeProcedureLabelFrameEdit.place(x = 5, y = 425)

        # [Layout] - Recipe procedure textbox
        self.recipeProcedureLabelEdit = Label(self.recipeProcedureLabelFrameEdit, text = "Procedimentos:")
        self.recipeProcedureLabelEdit.place(x = 130, y = 20, anchor = E)
        self.recipeProcedureTextEdit = Text(self.recipeProcedureLabelFrameEdit, height = "4", width = "45", wrap = WORD, font = ('TkDefaultFont'))
        self.recipeProcedureTextEdit.place(x = 150, y = 47.5, anchor = W)
        self.recipeProcedureTextEdit.insert(END, self.globalRecipesDict["recipes"][int(id)]["procedimento"])

        # [Layout] - Recipe time textbox
        self.recipeTimeLabelEdit = Label(self.recipeProcedureLabelFrameEdit, text = "Tempo de confeção:")
        self.recipeTimeLabelEdit.place(x = 130, y = 110, anchor = E)

        # [Layout] - Recipe time textbox - hours
        self.recipeHoursLabelEdit = Label(self.recipeProcedureLabelFrameEdit, text = "Horas:")
        self.recipeHoursLabelEdit.place(x = 190, y = 110, anchor = E)
        self.recipeHoursSpinboxEdit = Spinbox(self.recipeProcedureLabelFrameEdit, from_ = 0, to = 24, width = 3)
        self.recipeHoursSpinboxEdit.place(x = 200 , y = 102.5)
        self.recipeHoursSpinboxEdit.delete(0,END)
        self.recipeHoursSpinboxEdit.insert(END, int(self.globalRecipesDict["recipes"][int(id)]["tempo_confecao"].split(";")[0]))

        # [Layout] - Recipe time textbox - minutes
        self.recipeMinutesLabelEdit = Label(self.recipeProcedureLabelFrameEdit, text = "Minutos:")
        self.recipeMinutesLabelEdit.place(x = 310, y = 110, anchor = E)
        self.recipeMinutesSpinboxEdit = Spinbox(self.recipeProcedureLabelFrameEdit, from_ = 0, to = 59, width = 3)
        self.recipeMinutesSpinboxEdit.place(x = 320 , y = 102.5)
        self.recipeMinutesSpinboxEdit.delete(0,END)
        self.recipeMinutesSpinboxEdit.insert(END, int(self.globalRecipesDict["recipes"][int(id)]["tempo_confecao"].split(";")[1]))

        # [Layout] - Recipe category fieldset
        self.recipeCategoryLabelFrameEdit = LabelFrame(self.editRecipe, text = "Categorias", width = "490", height = "130", bd = "2")
        self.recipeCategoryLabelFrameEdit.place(x = 5, y = 590)

        # [Layout] - Recipe category textbox
        self.recipeCategoryLabelEdit = Label(self.recipeCategoryLabelFrameEdit, text = "Categorias:")
        self.recipeCategoryLabelEdit.place(x = 130, y = 20, anchor = E)

        # [Layout] - Recipe categories list
        self.listboxRecipeCategoriesEdit = Listbox(self.recipeCategoryLabelFrameEdit, height = "5", width = "46")
        self.listboxRecipeCategoriesEdit.place(x = 149, y = 58, anchor = W)
        for i in range(len(self.globalRecipesDict["recipes"][int(id)]["categorias"])):
            self.listboxRecipeCategoriesEdit.insert(END, self.globalRecipesDict["recipes"][int(id)]["categorias"][i])

        # [Layout] - Add categories button
        self.recipeAddCategoryEdit = ttk.Button(self.recipeCategoryLabelFrameEdit, text = "Adicionar", width = "17", command = AddCategory)
        self.recipeAddCategoryEdit.place(x = 15, y = 40)

        # [Layout] - Remove categories button
        self.recipeRemoveCategoryEdit = ttk.Button(self.recipeCategoryLabelFrameEdit, text = "Remover", width = "17", command = RemoveCategory)
        self.recipeRemoveCategoryEdit.place(x = 15, y = 72)

        # [Layout] - Add recipe button
        self.editRecipeButton = Button(self.editRecipe, text = "Editar", relief = "groove", width = "20", height = "2", command = EditAllRecipe)
        self.editRecipeButton.place(x = 175, y = 730)

    def MainProgram_ShowRecipeCards(self, page, filters):
        def RemoveRecipe(path, index):
            self.messageBoxAnswer = messagebox.askquestion("Eliminar", "Tem a certeza que pretende eliminar a receita?", icon = 'warning')
            if self.messageBoxAnswer=="yes":
                shutil.rmtree(path)
                self.UpdateDictionary(index)
                self.MainProgram_ShowRecipeCards(page, filters)

        CreatePath()
        if str(MD5Checksum(2)) != "8b53223e6b0ba3a1564ef2a5397bb03e":
            messagebox.showerror("Erro", "A foto padrão das receitas não foi reconhecida\nO programa irá fechar", parent = self.master)
            os._exit(0)

        # Delete the frame that contains the recipe cards
        if page == "AllRecipes":
            try:
                self.recipesFrame.destroy()
                self.recipesCanvas.destroy()
                self.recipesCanvasScrollbar.destroy()
                self.recipesSecondFrame.destroy()
            except: pass
            self.recipesFrame = Frame(self.recipesPanel, width = 625, height = 280)
            self.recipesFrame.place(x = 5, y = 45)
            self.recipesCanvas = Canvas(self.recipesFrame, width = 605)
            self.recipesCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.recipesCanvasScrollbar = ttk.Scrollbar(self.recipesFrame, orient = VERTICAL, command = self.recipesCanvas.yview)
            self.recipesCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.recipesCanvas.configure(yscrollcommand = self.recipesCanvasScrollbar.set)
            self.recipesCanvas.bind("<Configure>", partial(self.MainProgram_GlobalFunctions, "ResetScrollRegion", self.recipesCanvas))
            self.recipesSecondFrame = Frame(self.recipesCanvas)
            self.recipesCanvas.create_window((0, 0), window = self.recipesSecondFrame, anchor = NW)
        elif page == "UsersRecipes":
            try:
                self.usersRecipesFrame.destroy()
                self.usersRecipesCanvas.destroy()
                self.usersRecipesCanvasScrollbar.destroy()
                self.usersRecipesSecondFrame.destroy()
            except: pass
            self.usersRecipesFrame = Frame(self.usersRecipesPanel, width = 625, height = 280)
            self.usersRecipesFrame.place(x = 5, y = 45)
            self.usersRecipesCanvas = Canvas(self.usersRecipesFrame, width = 605)
            self.usersRecipesCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.usersRecipesCanvasScrollbar = ttk.Scrollbar(self.usersRecipesFrame, orient = VERTICAL, command = self.usersRecipesCanvas.yview)
            self.usersRecipesCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.usersRecipesCanvas.configure(yscrollcommand = self.usersRecipesCanvasScrollbar.set)
            self.usersRecipesCanvas.bind('<Configure>', lambda e: self.usersRecipesCanvas.configure(scrollregion = self.usersRecipesCanvas.bbox("all")))
            self.usersRecipesSecondFrame = Frame(self.usersRecipesCanvas)
            self.usersRecipesCanvas.create_window((0, 0), window = self.usersRecipesSecondFrame, anchor = NW)
        elif page == "UsersFavorites":
            try:
                self.usersFavoritesFrame.destroy()
                self.usersFavoritesCanvas.destroy()
                self.usersFavoritesCanvasScrollbar.destroy()
                self.usersFavoritesSecondFrame.destroy()
            except: pass
            self.usersFavoritesFrame = Frame(self.usersFavoritesPanel, width = 625, height = 280)
            self.usersFavoritesFrame.place(x = 5, y = 45)
            self.usersFavoritesCanvas = Canvas(self.usersFavoritesFrame, width = 605)
            self.usersFavoritesCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.usersFavoritesCanvasScrollbar = ttk.Scrollbar(self.usersFavoritesFrame, orient = VERTICAL, command = self.usersFavoritesCanvas.yview)
            self.usersFavoritesCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.usersFavoritesCanvas.configure(yscrollcommand = self.usersFavoritesCanvasScrollbar.set)
            self.usersFavoritesCanvas.bind('<Configure>', lambda e: self.usersFavoritesCanvas.configure(scrollregion = self.usersFavoritesCanvas.bbox("all")))
            self.usersFavoritesSecondFrame = Frame(self.usersFavoritesCanvas)
            self.usersFavoritesCanvas.create_window((0, 0), window = self.usersFavoritesSecondFrame, anchor = NW)
        elif page == "UsersNotifications":
            pass
        else:
            messagebox.showerror("Erro", "Ocorreu um erro inesperado\nO programa vai fechar", parent = self.master)
            os._exit(0)

        # Apply the filters coming from the button
        self.resultingDict = { "recipes": [] }

        if page != "UsersFavorites":
            if len(filters) > 0:
                # Order by category
                if not filters[2] == "Qualquer":
                    self.wasCategoryFound = False
                    self.orderedByCategoryDict = { "recipes": [] }
                    for i in range(len(self.globalRecipesDict["recipes"])):
                        for j in range(len(self.globalRecipesDict["recipes"][i]["categorias"])):
                            if self.globalRecipesDict["recipes"][i]["categorias"][j] == filters[2]:
                                self.orderedByCategoryDict["recipes"].append(self.globalRecipesDict["recipes"][i])
                                self.wasCategoryFound = True
                                self.shouldTheNoRecipesCardBeDisplayed = False
                    if not self.wasCategoryFound: self.shouldTheNoRecipesCardBeDisplayed = True
                else:
                    self.shouldTheNoRecipesCardBeDisplayed = False
                    self.orderedByCategoryDict = self.globalRecipesDict.copy()

                # Order by...
                self.orderedByDict = { "recipes": [] }
                if filters[3] == "Mais recentes":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: i['data'], reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais antigos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: i['data']):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais vistos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['views']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menos vistos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['views'])):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais gostados":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['likes']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menos gostados":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['likes'])):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Maior rating":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: float(i['rating']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menor rating":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: float(i['rating'])):
                        self.orderedByDict["recipes"].append(recipe)

                # Search by title
                self.searchByNameDict = { "recipes": [] }
                if filters[0]:
                    for i in range(len(self.orderedByDict["recipes"])):
                        if filters[0].lower() in self.orderedByDict["recipes"][i]["titulo"].lower():
                            self.searchByNameDict["recipes"].append(self.orderedByDict["recipes"][i])
                else: self.searchByNameDict = self.orderedByDict.copy()

                # Search by ingredient
                self.searchByIngredientDict = { "recipes": [] }
                if filters[1]:
                    for i in range(len(self.searchByNameDict["recipes"])):
                        for j in range(len(self.searchByNameDict["recipes"][i]["ingredientes"])):
                            if filters[1].lower() in self.searchByNameDict["recipes"][i]["ingredientes"][j].lower():
                                self.searchByIngredientDict["recipes"].append(self.searchByNameDict["recipes"][i])
                                break
                else: self.searchByIngredientDict = self.searchByNameDict.copy()

                self.resultingDict.clear()
                self.resultingDict = self.searchByIngredientDict.copy()
                if len(self.resultingDict["recipes"]) <= 0:
                    self.shouldTheNoRecipesCardBeDisplayed = True
            else:
                if len(self.globalRecipesDict["recipes"]) > 0:
                    self.shouldTheNoRecipesCardBeDisplayed = False
                    self.orderedByDict = { "recipes": [] }
                    for recipe in sorted(self.globalRecipesDict["recipes"], key = lambda i: i['data'], reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                    self.resultingDict.clear()
                    self.resultingDict = self.orderedByDict.copy()
                else: self.shouldTheNoRecipesCardBeDisplayed = True
        else:
            self.allFavoritedRecipes = { "recipes": [] }
            # Load all favorited recipes
            self.wereFavoritesFoundCustomMade = False
            for i in range(len(os.listdir(os.getcwd() + "\\data\\recipes"))):
                if os.path.isdir(os.getcwd() + "\\data\\recipes\\" + os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                    if "-" in str(os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                        with open(os.getcwd() + "\\data\\recipes\\" + str(os.listdir(os.getcwd() + "\\data\\recipes")[i]) + "\\favoritedby.txt", "r") as f:
                            for line in f:
                                if line.strip():
                                    if line.strip() == EncryptSHA256(self.loggedInUserInformation[1]):
                                        self.wereFavoritesFoundCustomMade = True
                                        self.gottenIdCustomMade = str(os.listdir(os.getcwd() + "\\data\\recipes")[i]).split("-")[-1]
                                        for j in range(len(self.globalRecipesDict["recipes"])):
                                            if int(self.globalRecipesDict["recipes"][j]["id"]) == int(self.gottenIdCustomMade):
                                                self.allFavoritedRecipes["recipes"].append(self.globalRecipesDict["recipes"][j])
                                                break
            if not self.wereFavoritesFoundCustomMade: self.shouldTheNoRecipesCardBeDisplayed = True
            if len(filters) > 0:
                # Order by category
                if not filters[2] == "Qualquer":
                    self.wasCategoryFound = False
                    self.orderedByCategoryDict = { "recipes": [] }
                    for i in range(len(self.allFavoritedRecipes["recipes"])):
                        for j in range(len(self.allFavoritedRecipes["recipes"][i]["categorias"])):
                            if self.allFavoritedRecipes["recipes"][i]["categorias"][j] == filters[2]:
                                self.orderedByCategoryDict["recipes"].append(self.allFavoritedRecipes["recipes"][i])
                                self.wasCategoryFound = True
                                self.shouldTheNoRecipesCardBeDisplayed = False
                    if not self.wasCategoryFound: self.shouldTheNoRecipesCardBeDisplayed = True
                else:
                    self.shouldTheNoRecipesCardBeDisplayed = False
                    self.orderedByCategoryDict = self.allFavoritedRecipes.copy()

                # Order by...
                self.orderedByDict = { "recipes": [] }
                if filters[3] == "Mais recentes":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: i['data'], reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais antigos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: i['data']):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais vistos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['views']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menos vistos":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['views'])):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Mais gostados":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['likes']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menos gostados":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: int(i['likes'])):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Maior rating":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: float(i['rating']), reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                elif filters[3] == "Menor rating":
                    for recipe in sorted(self.orderedByCategoryDict["recipes"], key = lambda i: float(i['rating'])):
                        self.orderedByDict["recipes"].append(recipe)

                # Search by title
                self.searchByNameDict = { "recipes": [] }
                if filters[0]:
                    for i in range(len(self.orderedByDict["recipes"])):
                        if filters[0].lower() in self.orderedByDict["recipes"][i]["titulo"].lower():
                            self.searchByNameDict["recipes"].append(self.orderedByDict["recipes"][i])
                else: self.searchByNameDict = self.orderedByDict.copy()

                # Search by ingredient
                self.searchByIngredientDict = { "recipes": [] }
                if filters[1]:
                    for i in range(len(self.searchByNameDict["recipes"])):
                        for j in range(len(self.searchByNameDict["recipes"][i]["ingredientes"])):
                            if filters[1].lower() in self.searchByNameDict["recipes"][i]["ingredientes"][j].lower():
                                self.searchByIngredientDict["recipes"].append(self.searchByNameDict["recipes"][i])
                                break
                else: self.searchByIngredientDict = self.searchByNameDict.copy()

                self.resultingDict.clear()
                self.resultingDict = self.searchByIngredientDict.copy()
                if len(self.resultingDict["recipes"]) <= 0:
                    self.shouldTheNoRecipesCardBeDisplayed = True
            else:
                if len(self.allFavoritedRecipes["recipes"]) > 0:
                    self.shouldTheNoRecipesCardBeDisplayed = False
                    self.orderedByDict = { "recipes": [] }
                    for recipe in sorted(self.allFavoritedRecipes["recipes"], key = lambda i: i['data'], reverse=True):
                        self.orderedByDict["recipes"].append(recipe)
                    self.resultingDict.clear()
                    self.resultingDict = self.orderedByDict.copy()
                else: self.shouldTheNoRecipesCardBeDisplayed = True

        # Create the recipes cards again
        if not self.shouldTheNoRecipesCardBeDisplayed:
            if page == "AllRecipes":
                for i in range(len(self.resultingDict["recipes"])):
                    self.allRecipesCard = Frame(self.recipesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                    self.allRecipesCard.pack(pady = 3)
                    self.allRecipesPictureCanvas = Canvas(self.allRecipesCard, width = "65", height = "65")
                    self.allRecipesPictureCanvas.place(x = 10, y = 5)
                    self.allRecipesPictureCanvas.image = ImageTk.PhotoImage(Image.open(self.resultingDict["recipes"][i]["imgpath"]).resize((65, 65)))
                    self.allRecipesPictureCanvas.create_image(32.5, 32.5, image = self.allRecipesPictureCanvas.image, anchor = CENTER)
                    self.allRecipesName = Label(self.allRecipesCard, text = "Título: " + self.resultingDict["recipes"][i]["titulo"])
                    self.allRecipesName.place(x = 90, y = 5)
                    self.allRecipesTime = Label(self.allRecipesCard, text = "Tempo de confeção: " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[0] + "h " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[1] + "min")
                    self.allRecipesTime.place(x = 90, y = 30)
                    self.allRecipesLikes = Label(self.allRecipesCard, text = "Likes: " + self.resultingDict["recipes"][i]["likes"])
                    self.allRecipesLikes.place(x = 90, y = 55)
                    self.allRecipesRating = Label(self.allRecipesCard, text = "Rating: " + str(self.resultingDict["recipes"][i]["rating"]))
                    self.allRecipesRating.place(x = 150, y = 55)
                    self.allRecipesDateTimeObject = datetime.datetime.strptime(self.resultingDict["recipes"][i]["data"], '%Y-%m-%d %H:%M:%S.%f')
                    self.allRecipesCreator = Label(self.allRecipesCard, text = "Criado por: " + self.MainProgram_GlobalFunctions("GetUserNameFromEmail", self.resultingDict["recipes"][i]["email"]) + ", " + str(self.allRecipesDateTimeObject.strftime("%d/%m/%Y")))
                    self.allRecipesCreator.place(x = 220, y = 55)
                    if self.loggedInUserInformation[3] == "administrator":
                        self.allRecipesSeeMore = Button(self.allRecipesCard, text = "Ver mais", command = partial(self.MainProgram_ShowRecipeDetails, self.resultingDict["recipes"][i]["index"], self.resultingDict["recipes"][i]["path"], "AllRecipes", filters))
                        self.allRecipesSeeMore.place(x = 450, y = 27)
                        self.allRecipesEdit = Button(self.allRecipesCard, text = "Editar", width=7, command=partial(self.MainProgram_EditRecipe,self.resultingDict["recipes"][i]["index"], page, filters))
                        self.allRecipesEdit.place(x = 520, y = 10)
                        self.allRecipesRemove = Button(self.allRecipesCard, text = "Remover", width=7, command=partial(RemoveRecipe, self.resultingDict["recipes"][i]["path"], self.resultingDict["recipes"][i]["index"]))
                        self.allRecipesRemove.place(x = 520, y = 39)
                    else:
                        self.allRecipesSeeMore = Button(self.allRecipesCard, text = "Ver mais", command = partial(self.MainProgram_ShowRecipeDetails, self.resultingDict["recipes"][i]["index"], self.resultingDict["recipes"][i]["path"], "AllRecipes", filters))
                        self.allRecipesSeeMore.place(x = 500, y = 27)
                    self.MainProgram_GlobalFunctions("ResetScrollRegion", self.recipesCanvas)
            elif page == "UsersRecipes":
                for i in range(len(self.resultingDict["recipes"])):
                    if EncryptSHA256(self.resultingDict["recipes"][i]["email"]) == EncryptSHA256(self.loggedInUserInformation[1]):
                        self.usersRecipesCard = Frame(self.usersRecipesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                        self.usersRecipesCard.pack(pady = 3)
                        self.usersRecipesPictureCanvas = Canvas(self.usersRecipesCard, width = "65", height = "65")
                        self.usersRecipesPictureCanvas.place(x = 10, y = 5)
                        self.usersRecipesPictureCanvas.image = ImageTk.PhotoImage(Image.open(self.resultingDict["recipes"][i]["imgpath"]).resize((65, 65)))
                        self.usersRecipesPictureCanvas.create_image(32.5, 32.5, image = self.usersRecipesPictureCanvas.image, anchor = CENTER)
                        self.usersRecipesName = Label(self.usersRecipesCard, text = "Título: " + self.resultingDict["recipes"][i]["titulo"])
                        self.usersRecipesName.place(x = 90, y = 5)
                        self.usersRecipesTime = Label(self.usersRecipesCard, text = "Tempo de confeção: " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[0] + "h " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[1] + "min")
                        self.usersRecipesTime.place(x = 90, y = 30)
                        self.usersRecipesLikes = Label(self.usersRecipesCard, text = "Likes: " + self.resultingDict["recipes"][i]["likes"])
                        self.usersRecipesLikes.place(x = 90, y = 55)
                        self.usersRecipesRating = Label(self.usersRecipesCard, text = "Rating: " + str(self.resultingDict["recipes"][i]["rating"]))
                        self.usersRecipesRating.place(x = 150, y = 55)
                        self.usersRecipesDateTimeObject = datetime.datetime.strptime(self.resultingDict["recipes"][i]["data"], '%Y-%m-%d %H:%M:%S.%f')
                        self.usersRecipesCreator = Label(self.usersRecipesCard, text = "Criado por: " + self.MainProgram_GlobalFunctions("GetUserNameFromEmail", self.resultingDict["recipes"][i]["email"]) + ", " + str(self.usersRecipesDateTimeObject.strftime("%d/%m/%Y")))
                        self.usersRecipesCreator.place(x = 220, y = 55)
                        self.usersRecipesSeeMore = Button(self.usersRecipesCard, text = "Ver mais", command = partial(self.MainProgram_ShowRecipeDetails, self.resultingDict["recipes"][i]["index"], self.resultingDict["recipes"][i]["path"], "UsersRecipes", filters))
                        self.usersRecipesSeeMore.place(x = 450, y = 27)
                        self.usersRecipesEdit = Button(self.usersRecipesCard, text = "Editar", width=7, command=partial(self.MainProgram_EditRecipe,self.resultingDict["recipes"][i]["index"], page, filters))
                        self.usersRecipesEdit.place(x = 520, y = 10)
                        self.usersRecipesRemove = Button(self.usersRecipesCard, text = "Remover", width=7, command=partial(RemoveRecipe, self.resultingDict["recipes"][i]["path"], self.resultingDict["recipes"][i]["index"]))
                        self.usersRecipesRemove.place(x = 520, y = 39)
                        self.MainProgram_GlobalFunctions("ResetScrollRegion", self.usersRecipesCanvas)
            elif page == "UsersFavorites":
                for i in range(len(self.resultingDict["recipes"])):
                    self.usersFavoritesCard = Frame(self.usersFavoritesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                    self.usersFavoritesCard.pack(pady = 3)
                    self.usersFavoritesPictureCanvas = Canvas(self.usersFavoritesCard, width = "65", height = "65")
                    self.usersFavoritesPictureCanvas.place(x = 10, y = 5)
                    self.usersFavoritesPictureCanvas.image = ImageTk.PhotoImage(Image.open(self.resultingDict["recipes"][i]["imgpath"]).resize((65, 65)))
                    self.usersFavoritesPictureCanvas.create_image(32.5, 32.5, image = self.usersFavoritesPictureCanvas.image, anchor = CENTER)
                    self.usersFavoritesName = Label(self.usersFavoritesCard, text = "Título: " + self.resultingDict["recipes"][i]["titulo"])
                    self.usersFavoritesName.place(x = 90, y = 5)
                    self.usersFavoritesTime = Label(self.usersFavoritesCard, text = "Tempo de confeção: " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[0] + "h " + self.resultingDict["recipes"][i]["tempo_confecao"].split(";")[1] + "min")
                    self.usersFavoritesTime.place(x = 90, y = 30)
                    self.usersFavoritesLikes = Label(self.usersFavoritesCard, text = "Likes: " + self.resultingDict["recipes"][i]["likes"])
                    self.usersFavoritesLikes.place(x = 90, y = 55)
                    self.usersFavoritesRating = Label(self.usersFavoritesCard, text = "Rating: " + str(self.resultingDict["recipes"][i]["rating"]))
                    self.usersFavoritesRating.place(x = 150, y = 55)
                    self.usersFavoritesDateTimeObject = datetime.datetime.strptime(self.resultingDict["recipes"][i]["data"], '%Y-%m-%d %H:%M:%S.%f')
                    self.usersFavoritesCreator = Label(self.usersFavoritesCard, text = "Criado por: " + self.MainProgram_GlobalFunctions("GetUserNameFromEmail", self.resultingDict["recipes"][i]["email"]) + ", " + str(self.usersFavoritesDateTimeObject.strftime("%d/%m/%Y")))
                    self.usersFavoritesCreator.place(x = 220, y = 55)
                    self.usersFavoritesSeeMore = Button(self.usersFavoritesCard, text = "Ver mais", command = partial(self.MainProgram_ShowRecipeDetails, self.resultingDict["recipes"][i]["index"], self.resultingDict["recipes"][i]["path"], "UsersFavorites", filters))
                    self.usersFavoritesSeeMore.place(x = 500, y = 27)
                    self.MainProgram_GlobalFunctions("ResetScrollRegion", self.usersFavoritesCanvas)
        else:
            if page == "AllRecipes":
                self.allRecipesNoRecipesFoundCard = Frame(self.recipesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                self.allRecipesNoRecipesFoundCard.pack(pady = 3)
                self.allRecipesNoRecipesLabel = Label(self.recipesSecondFrame, text = "Não foram encontradas receitas")
                self.allRecipesNoRecipesLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            elif page == "UsersRecipes":
                self.usersRecipesNoRecipesFoundCard = Frame(self.usersRecipesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                self.usersRecipesNoRecipesFoundCard.pack(pady = 3)
                self.usersRecipesNoRecipesLabel = Label(self.usersRecipesSecondFrame, text = "Não foram encontradas receitas")
                self.usersRecipesNoRecipesLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)
            elif page == "UsersFavorites":
                self.usersFavoritesNoRecipesFoundCard = Frame(self.usersFavoritesSecondFrame, width = "590", height = "80", highlightbackground = "black", highlightthickness = 1)
                self.usersFavoritesNoRecipesFoundCard.pack(pady = 3)
                self.usersFavoritesNoRecipesLabel = Label(self.usersFavoritesSecondFrame, text = "Não tem receitas nos favoritos")
                self.usersFavoritesNoRecipesLabel.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    def UpdateLeaveTimeStamp(self):
        with open(os.getcwd() + "\\data\\user\\" + EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".txt", "w") as f:
            f.write(str(datetime.datetime.now()))

class Login:
    def __init__(self, master):
        # [Initial configuration]
        self.master = master
        self.master.geometry("400x250")
        CenterWindow(self.master)
        self.master.title("Iniciar Sessão")
        self.master.resizable(False, False)
        self.master.focus_force()
        self.master.bind('<Return>', self.UserLogin)

        # [Initial configuration - variables]
        self.loginEmailInput = StringVar()
        self.loginPasswordInput = StringVar()

        # [Layout] - Login fieldset
        self.loginPanel = LabelFrame(self.master, text = "Iniciar Sessão", width = "380", height = "230", bd = "2")
        self.loginPanel.place(x = 10, y = 10)

        # [Layout] - Email textbox
        self.labelEmail = Label(self.loginPanel, text = "E-mail:")
        self.labelEmail.place(x = 115, rely = 0.20, anchor = E)
        self.emailText = Entry(self.loginPanel, width = "30", textvariable = self.loginEmailInput)
        self.emailText.place(relx = 0.35, rely = 0.20, anchor = W)
        self.emailText.focus_force()

        # [Layout] - Password textbox
        self.labelPassword = Label(self.loginPanel, text = "Palavra-passe:")
        self.labelPassword.place(x = 115, rely = 0.35, anchor = E)
        self.passwordText = Entry(self.loginPanel, width = "30", show = "*", textvariable = self.loginPasswordInput)
        self.passwordText.place(relx = 0.35, rely = 0.35, anchor = W)

        # [Layout] - Show password checkbox
        self.loginPasswordCheckbox = ttk.Checkbutton(self.loginPanel, text = "Mostrar palavra-passe")
        self.loginPasswordCheckbox.var = IntVar()
        self.loginPasswordCheckbox["variable"] = self.loginPasswordCheckbox.var
        self.loginPasswordCheckbox["command"] = partial(ShowPassword, self.loginPasswordCheckbox, self.passwordText)
        self.loginPasswordCheckbox.place(x = 270, rely = 0.48, anchor = E)

        # [Layout] - Login button
        self.loginButton = ttk.Button(self.loginPanel, text = "Iniciar Sessão", command = self.UserLogin)
        self.loginButton.place(relx = 0.5, rely = 0.70, width = "100", anchor = CENTER)

        # [Layout] - Register label
        self.labelRegister = Label(self.loginPanel, text = "Efetuar Registo", cursor="hand2")
        self.labelRegister.place(x = 285, y = 185)
        self.labelRegister.bind("<Button-1>", partial(self.OpenRegisterWindow))
        self.labelRegister.bind("<Enter>", partial(ChangeTextColor, self.labelRegister, "gray"))
        self.labelRegister.bind("<Leave>", partial(ChangeTextColor, self.labelRegister, "black"))

    def UserLogin(self, event = None):
        try:
            app.loggedInUserInformation.clear()
            app.loggedInUserInformation.append(False)
            self.loginEmail = self.loginEmailInput.get().strip().lower()
            self.loginPassword = self.loginPasswordInput.get().strip()
            if re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(self.loginEmail):
                if len(self.loginEmail.split("@")[0]) <= 64:
                    if len(self.loginEmail.split("@")[1]) <= 255:
                        if len(self.loginPassword) >= 8:
                            CreatePath()
                            self.encryptedLoginEmail, self.encrypedLoginPassword, self.wasAccountFound = EncryptSHA256(self.loginEmail), EncryptSHA256(self.loginPassword), False
                            if os.path.exists(os.getcwd() + "\\data\\user\\users_info.txt"):
                                with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                                    for line in f.readlines():
                                        if line.split(";")[0][0:len(line.split(";")[0]) - 10] == self.encryptedLoginEmail:
                                            self.wasAccountFound = True
                                            if line.split(";")[1] == self.encrypedLoginPassword:
                                                app.loggedInUserInformation[0] = True
                                                app.loggedInUserInformation.append(self.loginEmail)
                                                app.loggedInUserInformation.append(DecryptString(line.split(";")[2], line.split(";")[0][0:len(line.split(";")[0]) - 10]))
                                                self.loggedInSucessInfo = "\nNome: " + app.loggedInUserInformation[2]
                                                self.loggedInSucessInfo += "\nE-mail: " + app.loggedInUserInformation[1]
                                                if line.split(";")[0][-10:] == EncryptSHA256("user")[:10]: self.loggedInSucessInfo += "\nTipo: utilizador"
                                                else: self.loggedInSucessInfo += "\nTipo: admin"
                                                app.loggedInUserInformation.append(self.loggedInSucessInfo.replace(" ", "").split(":")[-1])
                                                # messagebox.showinfo("Sucesso", "Sessão iniciada com sucesso!\n\nBem-vindo!" + self.loggedInSucessInfo)
                                                # Close login window and open main program back up
                                                self.master.destroy()
                                                app.master.update()
                                                app.master.deiconify()
                                                app.MainProgram_FrontPage()
                                            else: messagebox.showerror("Erro", "A palavra-passe introduzida está incorreta", parent = self.master)
                                if not self.wasAccountFound: messagebox.showerror("Erro", "O e-mail introduzido não foi encontrado", parent = self.master)
                            else: messagebox.showerror("Erro", "As informações inseridas não foram encontradas", parent = self.master)
                        else: messagebox.showerror("Erro", "O campo de palavra-passe tem de ter 8 ou mais caracteres", parent = self.master)
                    else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
                else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
            else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
        except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.master)

    def OpenRegisterWindow(self, event):
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = Register(self.newWindow)

class Register:
    def __init__(self, master):
        # [Initial configuration]
        self.master = master
        self.master.geometry("400x375")
        CenterWindow(self.master)
        self.master.title("Efetuar Registo")
        self.master.resizable(False, False)
        self.master.focus_force()
        self.master.bind('<Return>', self.UserRegister)

        # [Initial configuration - variables]
        self.nameInput = StringVar()
        self.emailInput = StringVar()
        self.passwordInput = StringVar()
        self.defaultProfilePicture = "28c17e68aa44166d1c8e716bd535676a"

        # [Layout] - Register fieldset
        self.registerPanel = LabelFrame(self.master, text = "Efetuar Registo", width = "380", height = "355", bd = "2")
        self.registerPanel.place(x = 10, y = 10)

        # [Layout] - Name textbox
        self.labelNameRegister = Label(self.registerPanel, text = "Nome:")
        self.labelNameRegister.place(x = 115, y = 35, anchor = E)
        self.nameTextRegister = Entry(self.registerPanel, textvariable = self.nameInput, width = "30")
        self.nameTextRegister.place(relx = 0.35, y = 37.5, anchor = W)
        self.nameTextRegister.focus_force()

        # [Layout] - Email textbox
        self.labelEmailRegister = Label(self.registerPanel, text = "E-mail:")
        self.labelEmailRegister.place(x = 115, y = 70, anchor = E)
        self.emailTextRegister = Entry(self.registerPanel, textvariable = self.emailInput, width = "30")
        self.emailTextRegister.place(relx = 0.35, y = 72.5, anchor = W)

        # [Layout] - Password textbox
        self.labelPasswordRegister = Label(self.registerPanel, text = "Palavra-passe:")
        self.labelPasswordRegister.place(x = 115, y = 105, anchor = E)
        self.passwordTextRegister = Entry(self.registerPanel, textvariable = self.passwordInput, width = "30", show = "*")
        self.passwordTextRegister.place(relx = 0.35, y = 107.5, anchor = W)

        # [Layout] - Show password checkbox
        self.registerPasswordCheckbox = ttk.Checkbutton(self.registerPanel, text = "Mostrar palavra-passe")
        self.registerPasswordCheckbox.var = IntVar()
        self.registerPasswordCheckbox["variable"] = self.registerPasswordCheckbox.var
        self.registerPasswordCheckbox["command"] = partial(ShowPassword, self.registerPasswordCheckbox, self.passwordTextRegister)
        self.registerPasswordCheckbox.place(x = 269, y = 135, anchor = E)

        # [Layout] - Profile picture
        self.labelRegisterProfilePicture = Label(self.registerPanel, text = "Foto de perfil:")
        self.labelRegisterProfilePicture.place(x = 115, y = 170, anchor = E)
        self.registerProfilePicture = Label(self.master)
        CreatePath()

        # [Layout] - Verifies if the default image exists and/or has been tampered with
        if MD5Checksum(1) == self.defaultProfilePicture:
            self.registerProfilePicture.imgpath = os.getcwd() + "\\data\\images\\default.jpg"
            self.registerProfilePicture.image = ImageTk.PhotoImage(Image.open(self.registerProfilePicture.imgpath).resize((50, 50)))
        else:
            messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar", parent = self.master)
            os._exit(0)
        self.registerProfilePicture["image"] = self.registerProfilePicture.image
        self.registerProfilePicture.place(x = 142, y = 217.5, anchor = W)
        self.registerChangeProfilePicture = ttk.Button(self.registerPanel, text = "Enviar imagem", command = partial(self.SelectPicture, self.registerProfilePicture))
        self.registerChangeProfilePicture.place(x = 200, y = 177, anchor = W, width = 117)
        self.registerChangeProfilePictureInfo = Label(self.registerPanel, text = ".jpg .jpeg ou .png", wraplength = 140, justify = LEFT, font=(None, 8))
        self.registerChangeProfilePictureInfo.place(x = 197, y = 200, anchor = W)
        self.registerChangeProfilePictureInfo2 = Label(self.registerPanel, text = "Atenção: A largura e a altura da imagem devem ser iguais e não inferiores a 50px", wraplength = 175, justify = LEFT, font=(None, 8))
        self.registerChangeProfilePictureInfo2.place(x = 129, y = 240, anchor = W)

        # [Layout] - Register button
        self.registerButton = ttk.Button(self.registerPanel, text = "Efetuar Registo", command = self.UserRegister)
        self.registerButton.place(relx = 0.5, rely = 0.87, width = "100", anchor = CENTER)

        # [Layout] - Back label
        self.labelBack = Label(self.registerPanel, text = "Voltar", cursor="hand2")
        self.labelBack.place(x = 330, y = 310)
        self.labelBack.bind("<Button-1>", partial(self.BackToLogin))
        self.labelBack.bind("<Enter>", partial(ChangeTextColor, self.labelBack, "gray"))
        self.labelBack.bind("<Leave>", partial(ChangeTextColor, self.labelBack, "black"))

    def UserRegister(self, event = None):
        try:
            self.registerName = " ".join(self.nameInput.get().lower().split())
            self.registerEmail = self.emailInput.get().strip().lower()
            self.registerPassword = self.passwordInput.get()
            if self.registerName.replace(" ", ""):
                if self.registerName.count(" ") >= 1:
                    self.isNameAcceptable = True
                    for i in range(len(self.registerName.split(" "))):
                        if len(self.registerName.split(" ")[i]) < 2: self.isNameAcceptable = False
                    if self.isNameAcceptable:
                        if re.compile(r"^[^\W\d_]+(-[^\W\d_]+)?$", re.U).match(self.registerName.replace(" ", "")):
                            if len(self.registerName) <= 55:
                                if re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(self.registerEmail):
                                    if len(self.registerEmail.split("@")[0]) <= 64:
                                        if len(self.registerEmail.split("@")[1]) <= 255:
                                            if len(self.registerPassword) >= 8:
                                                self.registerName = " ".join(self.registerName.split(" ")[i].capitalize() for i in range(len(self.registerName.split(" "))))
                                                CreatePath()
                                                self.registerEncryptedEmail, self.isEmailBeingUsed = EncryptSHA256(self.registerEmail), False
                                                if os.path.exists(os.getcwd() + "\\data\\user\\users_info.txt"):
                                                    with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                                                        for line in f.readlines():
                                                            if self.registerEncryptedEmail == line.split(";")[0][0:len(line.split(";")[0]) - 10]:
                                                                self.isEmailBeingUsed = True
                                                if not self.isEmailBeingUsed:
                                                    self.doesUserWantToContinue = True
                                                    if self.registerProfilePicture.imgpath.split("\\")[-1] == "default.jpg":
                                                        self.continueDefault = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de perfil, se continuar irá ser selecionada a foto de perfil padrão, prosseguir?", icon = "warning", parent = self.master)
                                                        if self.continueDefault == "no": self.doesUserWantToContinue = False
                                                        else:
                                                            if MD5Checksum(1) != self.defaultProfilePicture:
                                                                messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar", parent = self.master)
                                                                os._exit(0)
                                                    if self.doesUserWantToContinue:
                                                        shutil.copy2(self.registerProfilePicture.imgpath, os.getcwd() + "\\data\\images\\" + self.registerEncryptedEmail[:15] + os.path.splitext(self.registerProfilePicture.imgpath)[1])
                                                        with open(os.getcwd() + "\\data\\user\\users_info.txt", "a") as f:
                                                            f.write(self.registerEncryptedEmail + EncryptSHA256("user")[:10] + ";" + EncryptSHA256(self.registerPassword) + ";" + EncryptString(self.registerName, self.registerEncryptedEmail) + "\n")
                                                        messagebox.showinfo("Sucesso", "O registo foi concluído com sucesso", parent = self.master)
                                                else: messagebox.showerror("Erro", "O e-mail introduzido já está registado na plataforma", parent = self.master)
                                            else: messagebox.showerror("Erro", "A palavra-passe escolhida tem de ter 8 ou mais caracteres", parent = self.master)
                                        else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
                                    else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
                                else: messagebox.showerror("Erro", "O e-mail introduzido não é válido", parent = self.master)
                            else: messagebox.showerror("Erro", "O campo de nome não pode exceder os 55 caracteres", parent = self.master)
                        else: messagebox.showerror("Erro", "O campo de nome não pode conter caracteres especiais nem números", parent = self.master)
                    else: messagebox.showerror("Erro", "O nome introduzido é inválido", parent = self.master)
                else: messagebox.showerror("Erro", "Introduza, pelo menos, o primeiro e último nome", parent = self.master)
            else: messagebox.showerror("Erro", "O nome introduzido é inválido", parent = self.master)
        except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.master)

    def SelectPicture(self, origin):
        self.imageCheck, self.path = False, filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
        if self.path:
            try:
                Image.open(self.path).verify()
                self.imageCheck = True
            except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem", parent = self.master)
            if self.imageCheck:
                try:
                    if Image.open(self.path).size[0] == Image.open(self.path).size[1]:
                        if Image.open(self.path).size[0] >= 50:
                            if os.stat(self.path).st_size <= 5000000:
                                origin.imgpath = self.path
                                origin.image = ImageTk.PhotoImage(Image.open(origin.imgpath).resize((50, 50)))
                                origin["image"] = origin.image
                            else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb", parent = self.master)
                        else: messagebox.showerror("Erro", "A imagem é inferior a 50x50px", parent = self.master)
                    else: messagebox.showerror("Erro", "A largura e altura da imagem não são iguais", parent = self.master)
                except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema", parent = self.master)
                except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.master)

    def BackToLogin(self, event):
        self.master.destroy()
        app.newWindow.update()
        app.newWindow.deiconify()

class Recipe:
    def __init__(self, master, page, filters):
        def NewRecipeCustomClose():
            self.master.destroy()
            app.master.update()

        def AddCategory():
            def AddCategoryToList():
                # Verify if category has already been chosen
                self.wasCategoryAlreadyChosen = False
                for i in range(self.listboxRecipeCategories.size()):
                    if self.selectNewCategoryDropdown.get() == self.listboxRecipeCategories.get(i):
                        self.wasCategoryAlreadyChosen = True
                        break
                if not self.wasCategoryAlreadyChosen:
                    self.listboxRecipeCategories.insert(END, self.selectNewCategoryDropdown.get())
                    AddCategoryCustomClose()
                else:
                    messagebox.showerror("Erro", "A categoria selecionada já foi escolhida", parent = self.addCategoryWindow)

            def AddCategoryCustomClose():
                self.addCategoryWindow.destroy()
                self.master.update()
                self.master.grab_set()

            # [Initial configuration]
            self.addCategoryWindow = Toplevel(self.master)
            self.addCategoryWindow.geometry("250x100")
            CenterWindow(self.addCategoryWindow)
            self.addCategoryWindow.title("Adicionar Categoria")
            self.addCategoryWindow.resizable(False, False)
            self.addCategoryWindow.grab_set()
            self.addCategoryWindow.focus_force()
            self.addCategoryWindow.protocol("WM_DELETE_WINDOW", AddCategoryCustomClose)

            # [Layout] - Category select box
            self.selectNewCategoryLabel = Label(self.addCategoryWindow, text = "Categoria:")
            self.selectNewCategoryLabel.place(x = 90, y = 5)
            self.selectNewCategoryDropdown = ttk.Combobox(self.addCategoryWindow, value = app.globalCategoriesList, width = "25")
            self.selectNewCategoryDropdown.place(x = 40, y = 40)
            self.selectNewCategoryDropdown.current(0)

            # [Layout] - Add category button
            self.addNewCategoryButton = ttk.Button(self.addCategoryWindow, text = "Adicionar", command = AddCategoryToList)
            self.addNewCategoryButton.place(x = 85, y = 65)

        def RemoveCategory():
            try:
                self.selectedCategory = self.listboxRecipeCategories.curselection()[0]
                self.listboxRecipeCategories.delete(self.selectedCategory)
            except:
                messagebox.showerror("Erro", "Selecione uma categoria para remover", parent = self.master)

        # [Initial configuration]
        self.master = master
        self.master.geometry("500x780")
        CenterWindow(self.master)
        self.master.title("Nova receita")
        self.master.resizable(False, False)
        self.master.grab_set()
        self.master.focus_force()
        self.master.protocol("WM_DELETE_WINDOW", NewRecipeCustomClose)
        self.page = page
        self.filters = filters

        # [Layout] - Recipe general information fieldset
        self.generalInformationLabelFrame = LabelFrame(self.master, text = "Informação Geral", width = "490", height = "280", bd = "2")
        self.generalInformationLabelFrame.place(x = 5, y = 5)

        # [Layout] - Recipe name
        self.recipeNameLabel = Label(self.generalInformationLabelFrame, text = "Nome da receita:")
        self.recipeNameLabel.place(x = 130, y = 35, anchor = E)
        self.recipeNameText = Entry(self.generalInformationLabelFrame, width = "45")
        self.recipeNameText.place(x = 150, y = 37.5, anchor = W)

        # [Layout] - Recipe description
        self.recipeDescriptionLabel = Label(self.generalInformationLabelFrame, text = "Descrição da receita:")
        self.recipeDescriptionLabel.place(x = 130, y = 70, anchor = E)
        self.recipeDescriptionText = Text(self.generalInformationLabelFrame, height = "4", width = "45", wrap = WORD, font = ('TkDefaultFont'))
        self.recipeDescriptionText.place(x = 150, y = 97.5, anchor = W)

        # [Layout] - Recipe picture
        self.labelSelectRecipeImage = Label(self.generalInformationLabelFrame, text = "Foto do prato:")
        self.labelSelectRecipeImage.place(x = 130, y = 155, anchor = E)
        self.recipePictureCanvas = Canvas(self.generalInformationLabelFrame, width = "100", height = "100")
        self.recipePictureCanvas.place(x = 150, y = 200, anchor = W)

        # [Layout] - Verifies if the default recipe image exists and/or has been tampered with
        CreatePath()
        if str(MD5Checksum(2)) == "8b53223e6b0ba3a1564ef2a5397bb03e":
            self.recipePictureCanvas.imgpath = os.getcwd() + "\\data\\images\\default_recipes.jpg"
            self.recipePictureCanvas.image = ImageTk.PhotoImage(Image.open(self.recipePictureCanvas.imgpath).resize((100, 100)))
        else:
            messagebox.showerror("Erro", "A foto padrão das receitas não foi reconhecida\nO programa irá fechar", parent = self.master)
            os._exit(0)

        self.recipePictureCanvas.create_image(0, 0, image = self.recipePictureCanvas.image, anchor = NW)
        self.selectRecipeImageButton = ttk.Button(self.generalInformationLabelFrame, text = "Enviar imagem", command = self.SelectRecipeImage)
        self.selectRecipeImageButton.place(x = 265, y = 164, anchor = W, width = 117)
        self.selectRecipeImageInfo = Label(self.generalInformationLabelFrame, text = ".jpg .jpeg ou .png", wraplength = 200, justify = LEFT, font=(None, 8))
        self.selectRecipeImageInfo.place(x = 265, y = 195, anchor = W)
        self.selectRecipeImageInfo2 = Label(self.generalInformationLabelFrame, text = "Atenção: Nem a largura nem a altura da imagem devem ser inferiores a 100px", wraplength = 150, justify = LEFT, font=(None, 8))
        self.selectRecipeImageInfo2.place(x = 265, y = 230, anchor = W)

        # [Layout] - Recipe ingredients fieldset
        self.ingredientsLabelFrame = LabelFrame(self.master, text = "Ingredientes", width = "490", height = "130", bd = "2")
        self.ingredientsLabelFrame.place(x = 5, y = 290)

        # [Layout] - Recipe ingredients
        self.recipeIngredientsLabel = Label(self.ingredientsLabelFrame, text = "Lista de ingredientes:")
        self.recipeIngredientsLabel.place(x = 130, y = 20, anchor = E)

        # [Layout] - Ingredients list
        self.listboxRecipeIngredients = Listbox(self.ingredientsLabelFrame, height = "5", width = "46")
        self.listboxRecipeIngredients.place(x = 149, y = 58, anchor = W)

        # [Layout] - Add ingredients button
        self.addRecipeIngredients = ttk.Button(self.ingredientsLabelFrame, text = "Adicionar", width = "17", command = self.AddNewIngredient)
        self.addRecipeIngredients.place(x = 15, y = 40)

        # [Layout] - Remove ingredients button
        self.removeRecipeIngredients = ttk.Button(self.ingredientsLabelFrame, text = "Remover", width = "17", command = self.RemoveIngredient)
        self.removeRecipeIngredients.place(x = 15, y = 72)

        # [Layout] - Recipe procedure fieldset
        self.recipeProcedureLabelFrame = LabelFrame(self.master, text = "Confeção", width = "490", height = "160", bd = "2")
        self.recipeProcedureLabelFrame.place(x = 5, y = 425)

        # [Layout] - Recipe procedure textbox
        self.recipeProcedureLabel = Label(self.recipeProcedureLabelFrame, text = "Procedimentos:")
        self.recipeProcedureLabel.place(x = 130, y = 20, anchor = E)
        self.recipeProcedureText = Text(self.recipeProcedureLabelFrame, height = "4", width = "45", wrap = WORD, font = ('TkDefaultFont'))
        self.recipeProcedureText.place(x = 150, y = 47.5, anchor = W)

        # [Layout] - Recipe time textbox
        self.recipeTimeLabel = Label(self.recipeProcedureLabelFrame, text = "Tempo de confeção:")
        self.recipeTimeLabel.place(x = 130, y = 110, anchor = E)

        # [Layout] - Recipe time textbox - hours
        self.recipeHoursLabel = Label(self.recipeProcedureLabelFrame, text = "Horas:")
        self.recipeHoursLabel.place(x = 190, y = 110, anchor = E)
        self.recipeHoursSpinbox = Spinbox(self.recipeProcedureLabelFrame, from_ = 0, to = 24, width = 3)
        self.recipeHoursSpinbox.place(x = 200 , y = 102.5)

        # [Layout] - Recipe time textbox - hours
        self.recipeMinutesLabel = Label(self.recipeProcedureLabelFrame, text = "Minutos:")
        self.recipeMinutesLabel.place(x = 310, y = 110, anchor = E)
        self.recipeMinutesSpinbox = Spinbox(self.recipeProcedureLabelFrame, from_ = 0, to = 59, width = 3)
        self.recipeMinutesSpinbox.place(x = 320 , y = 102.5)

        # [Layout] - Recipe category fieldset
        self.recipeCategoryLabelFrame = LabelFrame(self.master, text = "Categorias", width = "490", height = "130", bd = "2")
        self.recipeCategoryLabelFrame.place(x = 5, y = 590)

        # [Layout] - Recipe category textbox
        self.recipeCategoryLabel = Label(self.recipeCategoryLabelFrame, text = "Categorias:")
        self.recipeCategoryLabel.place(x = 130, y = 20, anchor = E)

        # [Layout] - Recipe categories list
        self.listboxRecipeCategories = Listbox(self.recipeCategoryLabelFrame, height = "5", width = "46")
        self.listboxRecipeCategories.place(x = 149, y = 58, anchor = W)

        # [Layout] - Add categories button
        self.recipeAddCategory = ttk.Button(self.recipeCategoryLabelFrame, text = "Adicionar", width = "17", command = AddCategory)
        self.recipeAddCategory.place(x = 15, y = 40)

        # [Layout] - Remove categories button
        self.recipeRemoveCategory = ttk.Button(self.recipeCategoryLabelFrame, text = "Remover", width = "17", command = RemoveCategory)
        self.recipeRemoveCategory.place(x = 15, y = 72)

        # [Layout] - Add recipe button
        self.addRecipe = Button(self.master, text = "Adicionar", relief = "groove", width = "20", height = "2", command = self.SaveNewRecipe)
        self.addRecipe.place(x = 175, y = 730)

    def SelectRecipeImage(self):
        self.pathImageRecipe = filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
        if self.pathImageRecipe:
            try:
                Image.open(self.pathImageRecipe).verify()
                self.recipeImageCheck = True
            except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem", parent = self.master)
            if self.recipeImageCheck:
                try:
                    if Image.open(self.pathImageRecipe).size[0] >= 100:
                        if Image.open(self.pathImageRecipe).size[1] >= 100:
                            if os.stat(self.pathImageRecipe).st_size <= 5000000:
                                self.recipePictureCanvas.imgpath = self.pathImageRecipe
                                self.recipePictureCanvas.image = ImageTk.PhotoImage(Image.open(self.recipePictureCanvas.imgpath).resize((100, 100)))
                                self.recipePictureCanvas.create_image(50, 50, image = self.recipePictureCanvas.image, anchor = CENTER)
                            else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb", parent = self.master)
                        else: messagebox.showerror("Erro", "A altura da imagem é inferior a 100px", parent = self.master)
                    else: messagebox.showerror("Erro", "A largura da imagem é inferior a 100px", parent = self.master)
                except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema", parent = self.master)
                except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido", parent = self.master)

    def AddNewIngredient(self):
        def AddIngredient():
            if self.listboxRecipeIngredients.size() < 30:
                if str(self.recipeIngredientsText.get()).replace(" ", ""):
                    if len(str(self.recipeIngredientsText.get()).replace(" ", "")) > 2:
                        self.listboxRecipeIngredients.insert(END, str(self.recipeIngredientsText.get()))
                        self.addNewIngredientWindow.destroy()
                        self.master.update()
                        self.master.grab_set()
                    else: messagebox.showerror("Erro", "O campo de ingrediente tem de ter, pelo menos, 3 caracteres", parent = self.addNewIngredientWindow)
                else: messagebox.showerror("Erro", "Introduza algum ingrediente", parent = self.addNewIngredientWindow)
            else: messagebox.showerror("Erro", "Atingiu o limite máximo de ingredientes (30)", parent = self.addNewIngredientWindow)

        def AddNewIngredientCustomClose():
            self.addNewIngredientWindow.destroy()
            self.master.update()
            self.master.grab_set()

        # [Layout] - Add ingredient window
        self.addNewIngredientWindow = Toplevel(self.master)
        self.addNewIngredientWindow.geometry("250x100")
        CenterWindow(self.addNewIngredientWindow)
        self.addNewIngredientWindow.title("Adicionar Ingrediente")
        self.addNewIngredientWindow.resizable(False, False)
        self.addNewIngredientWindow.grab_set()
        self.addNewIngredientWindow.protocol("WM_DELETE_WINDOW", AddNewIngredientCustomClose)

        # [Layout] - Add new ingredient textbox
        self.recipeIngredientsLabel = Label(self.addNewIngredientWindow, text = "Nome do ingrediente:")
        self.recipeIngredientsLabel.place(x = 60, y = 10)
        self.recipeIngredientsText = Entry(self.addNewIngredientWindow, width = 35)
        self.recipeIngredientsText.place(x = 18, y = 35)
        self.recipeIngredientsText.focus_force()

        # [Layout] - Add new ingredient button
        self.recipeIngredientsButton = ttk.Button(self.addNewIngredientWindow, text = "Adicionar", command = AddIngredient)
        self.recipeIngredientsButton.place(x = 85, y = 65)

    def RemoveIngredient(self):
        try:
            self.selectedIngredient = self.listboxRecipeIngredients.curselection()[0]
            self.listboxRecipeIngredients.delete(self.selectedIngredient)
        except:
            messagebox.showerror("Erro", "Selecione um ingrediente para remover", parent = self.master)

    def SaveNewRecipe(self, event = None, page = "", filters = []):
        if str(self.recipeNameText.get()).replace(" ", ""):
            if re.compile(r"^[^\W\d_]+(-[^\W\d_]+)?$", re.U).match(str(self.recipeNameText.get()).replace(" ", "")):
                if len(str(self.recipeNameText.get()).replace(" ", "")) > 10:
                    if len(str(self.recipeNameText.get()).replace(" ", "")) <= 50:
                        if str(self.recipeDescriptionText.get("1.0", END)).strip().replace(" ", ""):
                            if len(str(self.recipeDescriptionText.get("1.0", END)).replace(" ", "")) > 20:
                                if len(str(self.recipeDescriptionText.get("1.0", END)).replace(" ", "")) <= 255:
                                    if self.listboxRecipeIngredients.size() > 0:
                                        if str(self.recipeProcedureText.get("1.0", END)).strip().replace(" ", ""):
                                            if len(str(self.recipeProcedureText.get("1.0", END)).replace(" ", "")) > 20:
                                                if len(str(self.recipeProcedureText.get("1.0", END)).replace(" ", "")) <= 1250:
                                                    if str(self.recipeHoursSpinbox.get()) == "0" and str(self.recipeMinutesSpinbox.get()) == "0":
                                                        messagebox.showerror("Erro", "O tempo de confeção é inválido", parent = self.master)
                                                    else:
                                                        if self.listboxRecipeCategories.size() > 0:
                                                            self.doesUserWantToContinueRecipePicture = True
                                                            if self.recipePictureCanvas.imgpath.split("\\")[-1] == "default_recipes.jpg":
                                                                self.continueDefaultRecipe = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de receita, se continuar irá ser selecionada a foto de receita padrão, prosseguir?", icon = "warning", parent = self.master)
                                                                if self.continueDefaultRecipe == "no":
                                                                    self.doesUserWantToContinueRecipePicture = False
                                                                else:
                                                                    if MD5Checksum(2) != "8b53223e6b0ba3a1564ef2a5397bb03e":
                                                                        messagebox.showerror("Erro", "A foto de receita padrão não foi reconhecida\nO programa irá fechar", parent = self.master)
                                                                        os._exit(0)
                                                            if self.doesUserWantToContinueRecipePicture:
                                                                CreatePath()
                                                                self.wasAnyIdFound = False
                                                                if len(os.listdir(os.getcwd() + "\\data\\recipes")) > 0:
                                                                    self.savedRecipeID = 0
                                                                    for i in range(len(os.listdir(os.getcwd() + "\\data\\recipes"))):
                                                                        if os.path.isdir(os.getcwd() + "\\data\\recipes\\" + os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                                                                            if "-" in str(os.listdir(os.getcwd() + "\\data\\recipes")[i]):
                                                                                self.currentID = int(os.listdir(os.getcwd() + "\\data\\recipes")[i].split("-")[-1]) + 1
                                                                                if self.currentID >= self.savedRecipeID: self.savedRecipeID = self.currentID
                                                                                self.wasAnyIdFound = True
                                                                        else:
                                                                            if i == (len(os.listdir(os.getcwd() + "\\data\\recipes")) - 1) and not self.wasAnyIdFound:
                                                                                self.savedRecipeID = 1
                                                                else: self.savedRecipeID = 1
                                                                self.newRecipe = {}
                                                                self.newRecipe["id"] = self.savedRecipeID
                                                                self.newRecipe["index"] = str(app.currentDictId)
                                                                app.currentDictId += 1
                                                                self.newRecipe["email"] = app.loggedInUserInformation[1]
                                                                self.newRecipe["titulo"] = str(self.recipeNameText.get())
                                                                self.newRecipe["descricao"] = str(self.recipeDescriptionText.get("1.0", END)).strip()
                                                                self.newRecipe["procedimento"] = str(self.recipeProcedureText.get("1.0", END)).strip()
                                                                self.newRecipe["ingredientes"] = []
                                                                self.newRecipe["categorias"] = []
                                                                self.newRecipe["views"] = "0"
                                                                self.newRecipe["likes"] = "0"
                                                                self.newRecipe["rating"] = 0.0
                                                                self.newRecipe["tempo_confecao"] = str(self.recipeHoursSpinbox.get()) + ";" + str(self.recipeMinutesSpinbox.get())
                                                                self.newRecipe["data"] = str(datetime.datetime.now())
                                                                self.newRecipe["path"] = os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID)
                                                                self.newRecipe["imgpath"] = os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\picture" + os.path.splitext(self.recipePictureCanvas.imgpath)[1]
                                                                os.mkdir(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID))
                                                                os.mkdir(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\comments")
                                                                os.mkdir(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\views")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\views\\nviews.txt", "w") as f:
                                                                    f.write("0")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\views\\whoviewed.txt", "w") as f:
                                                                    pass
                                                                os.mkdir(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\likes")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\likes\\nlikes.txt", "w") as f:
                                                                    f.write("0")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\likes\\wholiked.txt", "w") as f:
                                                                    pass
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\id.txt", "w") as f:
                                                                    f.write(str(self.savedRecipeID))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\author.txt", "w") as f:
                                                                    f.write(EncryptString(app.loggedInUserInformation[1], "auth"))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\date.txt", "w") as f:
                                                                    f.write(EncryptString(str(datetime.datetime.now()), "auth"))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\name.txt", "w") as f:
                                                                    f.write(EncryptString(str(self.recipeNameText.get()), "auth"))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\description.txt", "w") as f:
                                                                    f.write(EncryptString(str(self.recipeDescriptionText.get("1.0", END)), "auth"))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\ingredients.txt", "w") as f:
                                                                    for i in range(self.listboxRecipeIngredients.size()):
                                                                        self.newRecipe["ingredientes"].append(self.listboxRecipeIngredients.get(i))
                                                                        f.write(EncryptString(self.listboxRecipeIngredients.get(i), "auth") + "\n")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\procedure.txt", "w") as f:
                                                                    f.write(EncryptString(str(self.recipeProcedureText.get("1.0", END)), "auth"))
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\categories.txt", "w") as f:
                                                                    for i in range(self.listboxRecipeCategories.size()):
                                                                        self.newRecipe["categorias"].append(self.listboxRecipeCategories.get(i))
                                                                        f.write(EncryptString(self.listboxRecipeCategories.get(i), "auth") + "\n")
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\rating.txt", "w") as f:
                                                                    pass
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\favoritedby.txt", "w") as f:
                                                                    pass
                                                                with open(os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\time.txt", "w") as f:
                                                                    f.write(str(self.recipeHoursSpinbox.get()) + ";" + str(self.recipeMinutesSpinbox.get()))
                                                                app.globalRecipesDict["recipes"].append(self.newRecipe)
                                                                shutil.copy2(self.recipePictureCanvas.imgpath, os.getcwd() + "\\data\\recipes\\recipe-id-" + str(self.savedRecipeID) + "\\picture" + os.path.splitext(self.recipePictureCanvas.imgpath)[1])
                                                                messagebox.showinfo("Sucesso", "A receita foi criada com sucesso", parent = self.master)
                                                                self.master.destroy()
                                                                app.master.update()
                                                                app.MainProgram_ShowRecipeCards(self.page, self.filters)
                                                        else: messagebox.showerror("Erro", "A receita tem de ter, pelo menos, 1 categoria", parent = self.master)
                                                else: messagebox.showerror("Erro", "O campo de procedimentos da receita não pode exceder os 1250 caracteres", parent = self.master)
                                            else: messagebox.showerror("Erro", "O campo de procedimentos da receita tem de ter, pelo menos, 20 caracteres", parent = self.master)
                                        else: messagebox.showerror("Erro", "O campo de procedimenos da receita é obrigatório", parent = self.master)
                                    else: messagebox.showerror("Erro", "A receita tem de ter, pelo menos, 1 ingrediente", parent = self.master)
                                else: messagebox.showerror("Erro", "O campo de descrição da receita não pode exceder os 255 caracteres", parent = self.master)
                            else: messagebox.showerror("Erro", "O campo de descrição da receita tem de ter, pelo menos, 20 caracteres", parent = self.master)
                        else: messagebox.showerror("Erro", "O campo de descrição da receita é obrigatório", parent = self.master)
                    else: messagebox.showerror("Erro", "O campo de nome da receita não pode exceder os 50 caracteres", parent = self.master)
                else: messagebox.showerror("Erro", "O campo de nome da receita tem de ter, pelo menos, 10 caracteres", parent = self.master)
            else: messagebox.showerror("Erro", "O campo de nome da receita não pode conter caracteres especiais nem números", parent = self.master)
        else: messagebox.showerror("Erro", "O campo de nome da receita é obrigatório", parent = self.master)

if __name__ == '__main__':
    root = Tk()
    app = MainProgram(root)
    root.mainloop()
