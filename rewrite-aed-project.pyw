import sys
import os
import re # Usado para verificar certos campos (e-mail, nome, etc.) com expressões regulares (regex)
import cryptocode # Usado para encriptar informações gerais (primeiros e últimos nomes)
import hashlib # Usado para encriptar informações confidenciais (e-mails e passwords) com a função SHA256
import shutil # Usado para copiar ficheiros de um directório para outro
import traceback # Usado para facilitar o debugging
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from functools import partial # Usado para acionar eventos com argumentos customizados
from PySide2 import QtWidgets, QtGui # Usado para centrar a janela no ecrã
from PIL import ImageTk, Image # Usado para converter imagens em formato PGM/PPM
# pip install cryptocode
# pip install PySide2
# pip install Pillow

# Paste for traceback:
# print("Error:\n" + str(err) + "\n")
# print("Traceback:")
# traceback.print_exc()

def CreatePath():
    if not os.path.exists(os.getcwd() + "\\data"): os.mkdir(os.getcwd() + "\\data")
    if not os.path.exists(os.getcwd() + "\\data\\user"): os.mkdir(os.getcwd() + "\\data\\user")
    if not os.path.exists(os.getcwd() + "\\data\\images"): os.mkdir(os.getcwd() + "\\data\\images")

def MD5Checksum():
    if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
        md5hash = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\default.jpg").tobytes())
        return str(md5hash.hexdigest())
    else:
        messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar")
        os._exit(0)

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

def UseMouseWheel(target, event):
    target.yview_scroll(int(-1 * (event.delta / 100)), "units")

class MainProgram:
    def __init__(self, master):
        # [Initial configuration]
        self.master = master
        self.loggedInUserInformation = [False]
        self.master.geometry("850x500")
        CenterWindow(self.master)
        self.master.title("Projeto AED")
        self.master.resizable(False, False)
        self.MainProgram_Authentication()

    def ClearWindowWidgets(self, target):
        widgetsList = target.winfo_children()
        for widget in widgetsList:
            if widget.winfo_children():
                widgetsList.extend(widget.winfo_children())
        for widget in widgetsList: widget.destroy()

    def ExitProgram(self):
        self.exitPrompt = messagebox.askquestion ("Sair", "Tem a certeza que prentende sair do programa?", icon = "warning")
        if self.exitPrompt == "yes":
            os._exit(0)

    def MainProgram_Authentication(self):
        if self.loggedInUserInformation[0]:
            self.logoutPrompt = messagebox.askquestion ("Terminar sessão", "Tem a certeza que prentende terminar sessão?", icon = "warning")
            if self.logoutPrompt == "yes":
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
            if a == 2: self.MainProgram_AllRecipesPage()
            if a == 1: self.MainProgram_UsersRecipesPage()

        # [Configuration] - Control variables
        self.hasUserGoneToPage0 = False
        self.hasUserGoneToPage1 = False
        self.hasUserGoneToPage2 = False
        self.hasUserGoneToPage3 = False
        self.hasUserGoneToPage4 = False

        # [Layout] - Admin menu
        if self.loggedInUserInformation[3] == "admin":
            self.master.geometry("850x518")
            self.adminBar = Menu(self.master)
            self.adminMenu = Menu(self.adminBar, tearoff = 0)
            self.adminMenu.add_command(label = "Admin", command = "noaction")
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
                if MD5Checksum() == "28c17e68aa44166d1c8e716bd535676a":
                    self.profilePicture = Label(self.master)
                    self.profilePicture.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\default.jpg").resize((70, 70)))
                    self.profilePicture["image"] = self.profilePicture.image
                    self.profilePicture.place(x = 60, y = 20)
                else:
                    messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar")
                    os._exit(0)
            else:
                messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar")
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
        self.tabEditProfile = Frame(self.tabControl, width = 649, height = 500, bg = "blue")
        self.tabUsersRecipes = Frame(self.tabControl, width = 649, height = 500)
        self.tabAllRecipes = Frame(self.tabControl, width = 649, height = 500)
        self.tabUsersFavourite = Frame(self.tabControl, width = 649, height = 500, bg = "black")
        self.tabUsersNotifications = Frame(self.tabControl, width = 649, height = 500, bg = "yellow")
        self.tabControl.add(self.tabEditProfile)
        self.tabControl.add(self.tabUsersRecipes)
        self.tabControl.add(self.tabAllRecipes)
        self.tabControl.add(self.tabUsersFavourite)
        self.tabControl.add(self.tabUsersNotifications)
        self.tabControl.select(4)
        self.tabControl.place(x = 200, y = -23)

    def MainProgram_UsersRecipesPage(self):
        if not self.hasUserGoneToPage1:
            self.hasUserGoneToPage1 = True

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
            self.usersRecipesSearchByCategoryList = ["Qualquer", "Vegetariano", "Bolos", "Tradicional"]
            self.usersRecipesSearchByCategoryDropdown = ttk.Combobox(self.usersRecipesFilterPanel, value = self.usersRecipesSearchByCategoryList, width = "25")
            self.usersRecipesSearchByCategoryDropdown.place(x = 228, y = 30)
            self.usersRecipesSearchByCategoryDropdown.current(0)
            self.usersRecipesSearchByCategoryDropdownClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesSearchByCategoryDropdown))
            self.usersRecipesSearchByCategoryDropdownClearButton.place(x = 405, y = 28)

            # [Layout] - Order by filter
            self.usersRecipesOrderByLabel = Label(self.usersRecipesFilterPanel, text = "Ordernar por:")
            self.usersRecipesOrderByLabel.place(x = 225, y = 55)
            self.usersRecipesOrderByList = ["Aleatório", "Mais vistos", "Menos vistos", "Mais gostados", "Menos gostados"]
            self.usersRecipesOrderByDropdown = ttk.Combobox(self.usersRecipesFilterPanel, value = self.usersRecipesOrderByList, width = "25")
            self.usersRecipesOrderByDropdown.place(x = 228, y = 80)
            self.usersRecipesOrderByDropdown.current(0)
            self.usersRecipesOrderByDropdownClearButton = ttk.Button(self.usersRecipesFilterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.usersRecipesOrderByDropdown))
            self.usersRecipesOrderByDropdownClearButton.place(x = 405, y = 78)

            # [Layout] - Clear filters button
            self.usersRecipesClearAllFiltersButton = ttk.Button(self.usersRecipesFilterPanel, text = "Limpar todos os filtros", width = "25", command = partial(self.MainProgram_GlobalFunctions, "ClearAllFilters", False))
            self.usersRecipesClearAllFiltersButton.place(x = 468, y = 28)

            # [Layout] - Apply filters button
            self.usersRecipesApplyAllFiltersButton = ttk.Button(self.usersRecipesFilterPanel, text = "Aplicar filtros", width = "25")
            self.usersRecipesApplyAllFiltersButton.place(x = 468, y = 78)

            # [Layout] - Recipes fieldset
            self.usersRecipesPanel = LabelFrame(self.tabUsersRecipes, text = "Minhas Receitas", width = "640", height = "345", bd = "2")
            self.usersRecipesPanel.place(x = 5, y = 150)

            # [Layout] - Create recipe button
            self.usersCreateRecipeButton = Button(self.usersRecipesPanel, text = "Criar receita", relief = "groove", width = "50", height = "1", command = self.MainProgram_AddRecipe)
            self.usersCreateRecipeButton.place(x = 140, y = 10)

            # [Layout] - Recipes frame
            self.usersRecipesFrame = Frame(self.usersRecipesPanel, width = 625, height = 280)
            self.usersRecipesFrame.place(x = 5, y = 45)
            self.usersRecipesCanvas = Canvas(self.usersRecipesFrame, width = 605)
            self.usersRecipesCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.usersRecipesCanvasScrollbar = ttk.Scrollbar(self.usersRecipesFrame, orient = VERTICAL, command = self.usersRecipesCanvas.yview)
            self.usersRecipesCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.usersRecipesCanvas.configure(yscrollcommand = self.usersRecipesCanvasScrollbar.set)
            self.usersRecipesCanvas.bind('<Configure>', lambda e: self.usersRecipesCanvas.configure(scrollregion = self.usersRecipesCanvas.bbox("all")))
            self.usersRecipesCanvas.bind("<MouseWheel>", partial(UseMouseWheel, self.usersRecipesCanvas))
            self.usersRecipesSecondFrame = Frame(self.usersRecipesCanvas)
            self.usersRecipesCanvas.create_window((0, 0), window = self.usersRecipesSecondFrame, anchor = "nw")

            for i in range(100):
                Label(self.usersRecipesSecondFrame, text = "teste").pack()

    def MainProgram_AllRecipesPage(self):
        if not self.hasUserGoneToPage2:
            self.hasUserGoneToPage2 = True

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
            self.searchByCategoryList = ["Qualquer", "Vegetariano", "Bolos", "Tradicional"]
            self.searchByCategoryDropdown = ttk.Combobox(self.filterPanel, value = self.searchByCategoryList, width = "25")
            self.searchByCategoryDropdown.place(x = 228, y = 30)
            self.searchByCategoryDropdown.current(0)
            self.searchByCategoryDropdownClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.searchByCategoryDropdown))
            self.searchByCategoryDropdownClearButton.place(x = 405, y = 28)

            # [Layout] - Order by filter
            self.orderByLabel = Label(self.filterPanel, text = "Ordernar por:")
            self.orderByLabel.place(x = 225, y = 55)
            self.orderByList = ["Aleatório", "Mais vistos", "Menos vistos", "Mais gostados", "Menos gostados"]
            self.orderByDropdown = ttk.Combobox(self.filterPanel, value = self.orderByList, width = "25")
            self.orderByDropdown.place(x = 228, y = 80)
            self.orderByDropdown.current(0)
            self.orderByDropdownClearButton = ttk.Button(self.filterPanel, text = "X", width = "2", command = partial(self.MainProgram_GlobalFunctions, "ClearFilters", self.orderByDropdown))
            self.orderByDropdownClearButton.place(x = 405, y = 78)

            # [Layout] - Clear filters button
            self.clearAllFiltersButton = ttk.Button(self.filterPanel, text = "Limpar todos os filtros", width = "25", command = partial(self.MainProgram_GlobalFunctions, "ClearAllFilters", True))
            self.clearAllFiltersButton.place(x = 468, y = 28)

            # [Layout] - Apply filters button
            self.applyAllFiltersButton = ttk.Button(self.filterPanel, text = "Aplicar filtros", width = "25")
            self.applyAllFiltersButton.place(x = 468, y = 78)

            # [Layout] - Recipes fieldset
            self.recipesPanel = LabelFrame(self.tabAllRecipes, text = "Receitas", width = "640", height = "345", bd = "2")
            self.recipesPanel.place(x = 5, y = 150)

            # [Layout] - Create recipe button
            self.createRecipeButton = Button(self.recipesPanel, text = "Criar receita", relief = "groove", width = "50", height = "1", command = self.MainProgram_AddRecipe)
            self.createRecipeButton.place(x = 140, y = 10)

            # [Layout] - Recipes frame
            self.recipesFrame = Frame(self.recipesPanel, width = 625, height = 280)
            self.recipesFrame.place(x = 5, y = 45)
            self.recipesCanvas = Canvas(self.recipesFrame, width = 605)
            self.recipesCanvas.pack(side = LEFT, fill = BOTH, expand = 1)
            self.recipesCanvasScrollbar = ttk.Scrollbar(self.recipesFrame, orient = VERTICAL, command = self.recipesCanvas.yview)
            self.recipesCanvasScrollbar.pack(side = RIGHT, fill = Y)
            self.recipesCanvas.configure(yscrollcommand = self.recipesCanvasScrollbar.set)
            self.recipesCanvas.bind('<Configure>', lambda e: self.recipesCanvas.configure(scrollregion = self.recipesCanvas.bbox("all")))
            self.recipesCanvas.bind("<MouseWheel>", partial(UseMouseWheel, self.recipesCanvas))
            self.recipesSecondFrame = Frame(self.recipesCanvas)
            self.recipesCanvas.create_window((0, 0), window = self.recipesSecondFrame, anchor = "nw")
            
            def ShowNumber(x):
                print(x)

            for i in range(100):
                self.allRecipeCard = Frame(self.recipesSecondFrame, width="590", height="80", highlightbackground="black", highlightthickness=1)
                self.allRecipeCard.pack(pady=3)
                self.allRecipePictureCanvas=Canvas(self.allRecipeCard, width = "65", height = "65")
                self.allRecipePictureCanvas.place(x=10,y=5)
                self.allRecipePictureCanvas.imgpath = os.getcwd() + "\\data\\images\\default_recipes.jpg"
                self.allRecipePictureCanvas.image = ImageTk.PhotoImage(Image.open(self.allRecipePictureCanvas.imgpath).resize((65,65)))
                self.allRecipePictureCanvas.create_image(0, 0, image = self.allRecipePictureCanvas.image, anchor = NW)
                self.allRecipiName=Label(self.allRecipeCard, text="ola")
                self.allRecipiName.place(x=90,y=5)
                self.allRecipiLikes=Label(self.allRecipeCard, text="Likes: ")
                self.allRecipiLikes.place(x=90,y=55)
                self.allRecipiSeeMore=Button(self.allRecipeCard, text="Ver mais", command=partial(ShowNumber,i))
                self.allRecipiSeeMore.place(x=500,y=27)

    def MainProgram_GlobalFunctions(self, func, *arg):
        def ClearFilters(a):
            if str(type(a)) == "<class 'tkinter.Entry'>": a.delete(0, END)
            else: a.current(0)

        def ClearAllFilters(a):
            if a:
                self.orderByDropdown.current(0)
                self.searchByCategoryDropdown.current(0)
                self.searchByIngredientText.delete(0, END)
                self.searchByTitleText.delete(0, END)
            else:
                self.usersRecipesOrderByDropdown.current(0)
                self.usersRecipesSearchByCategoryDropdown.current(0)
                self.usersRecipesSearchByIngredientText.delete(0, END)
                self.usersRecipesSearchByTitleText.delete(0, END)

        if func == "ClearFilters":
            ClearFilters(list(arg)[0])
        elif func == "ClearAllFilters":
            ClearAllFilters(list(arg)[0])

    def MainProgram_AddRecipe(self):
        self.newRecipeWindow = Toplevel(self.master)
        self.app = Recipe(self.newRecipeWindow)

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

        # ONLY FOR DEBUGGING - DELETE THIS
        # ONLY FOR DEBUGGING - DELETE THIS
        # ONLY FOR DEBUGGING - DELETE THIS
        # ONLY FOR DEBUGGING - DELETE THIS
        self.emailText.delete(0, END)
        self.emailText.insert(0, "diogo@borges.pt")
        self.passwordText.delete(0, END)
        self.passwordText.insert(0, "diogo123")

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
                                                messagebox.showinfo("Sucesso", "Sessão iniciada com sucesso!\n\nBem-vindo!" + self.loggedInSucessInfo)
                                                # Close login window and open main program back up
                                                self.master.destroy()
                                                app.master.update()
                                                app.master.deiconify()
                                                app.MainProgram_FrontPage()
                                            else: messagebox.showerror("Erro", "A palavra-passe introduzida está incorreta")
                                if not self.wasAccountFound: messagebox.showerror("Erro", "O e-mail introduzido não foi encontrado")
                            else: messagebox.showerror("Erro", "As informações inseridas não foram encontradas")
                        else: messagebox.showerror("Erro", "O campo de palavra-passe tem de ter 8 ou mais caracteres")
                    else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
                else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
            else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
        except Exception as err:
            print("Error:\n" + str(err) + "\n")
            print("Traceback:")
            traceback.print_exc()
            #messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

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
        if MD5Checksum() == self.defaultProfilePicture:
            self.registerProfilePicture.imgpath = os.getcwd() + "\\data\\images\\default.jpg"
            self.registerProfilePicture.image = ImageTk.PhotoImage(Image.open(self.registerProfilePicture.imgpath).resize((50, 50)))
        else:
            messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar")
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
                                                        self.continueDefault = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de perfil, se continuar irá ser selecionada a foto de perfil padrão, prosseguir?", icon = "warning")
                                                        if self.continueDefault == "no": self.doesUserWantToContinue = False
                                                        else:
                                                            if MD5Checksum() != self.defaultProfilePicture:
                                                                messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar")
                                                                os._exit(0)
                                                    if self.doesUserWantToContinue:
                                                        shutil.copy2(self.registerProfilePicture.imgpath, os.getcwd() + "\\data\\images\\" + self.registerEncryptedEmail[:15] + os.path.splitext(self.registerProfilePicture.imgpath)[1])
                                                        with open(os.getcwd() + "\\data\\user\\users_info.txt", "a") as f:
                                                            f.write(self.registerEncryptedEmail + EncryptSHA256("user")[:10] + ";" + EncryptSHA256(self.registerPassword) + ";" + EncryptString(self.registerName, self.registerEncryptedEmail) + "\n")
                                                        messagebox.showinfo("Sucesso", "O registo foi concluído com sucesso")
                                                else: messagebox.showerror("Erro", "O e-mail introduzido já está registado na plataforma")
                                            else: messagebox.showerror("Erro", "A palavra-passe escolhida tem de ter 8 ou mais caracteres")
                                        else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
                                    else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
                                else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
                            else: messagebox.showerror("Erro", "O campo de nome não pode exceder os 55 caracteres")
                        else: messagebox.showerror("Erro", "O campo de nome não pode conter caracteres especiais nem números")
                    else: messagebox.showerror("Erro", "O nome introduzido é inválido")
                else: messagebox.showerror("Erro", "Introduza, pelo menos, o primeiro e último nome")
            else: messagebox.showerror("Erro", "O nome introduzido é inválido")
        except Exception as err:
            print("Error:\n" + str(err) + "\n")
            print("Traceback:")
            traceback.print_exc()
            #messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

    def SelectPicture(self, origin):
        self.imageCheck, self.path = False, filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
        if self.path:
            try:
                Image.open(self.path).verify()
                self.imageCheck = True
            except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem")
            if self.imageCheck:
                try:
                    if Image.open(self.path).size[0] == Image.open(self.path).size[1]:
                        if Image.open(self.path).size[0] >= 50:
                            if os.stat(self.path).st_size <= 5000000:
                                origin.imgpath = self.path
                                origin.image = ImageTk.PhotoImage(Image.open(origin.imgpath).resize((50, 50)))
                                origin["image"] = origin.image
                            else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb")
                        else: messagebox.showerror("Erro", "A imagem é inferior a 50x50px")
                    else: messagebox.showerror("Erro", "A largura e altura da imagem não são iguais")
                except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema")
                except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

    def BackToLogin(self, event):
        self.master.destroy()
        app.newWindow.update()
        app.newWindow.deiconify()

class Recipe:
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x700")
        CenterWindow(self.master)
        self.master.title("Nova receita")
        self.master.focus_force()
        # self.master.bind('<Return>', self.UserRegister)

        # [Layout] - Select recipe image button
        self.selectRecipeImageButton = Button(self.master, text = "Adicionar imagem", command = self.SelectRecipeImage)
        self.selectRecipeImageButton.place(x = 20, y = 20)

        # [Layout] - Recipe general information fieldset
        self.nameAndDescriptionFrame = LabelFrame(self.master, text = "Informação Geral", bg = "blue")
        self.nameAndDescriptionFrame.place(x = 260, y = 60)

        # [Layout] - Recipe name
        self.recipeNameLabel = Label(self.master, text = "Nome da receita:")
        self.recipeNameLabel.place(x = 20, y = 70)
        self.recipeNameText = Entry(self.master)
        self.recipeNameText.place(x = 160, y = 70)

        # [Layout] - Recipe description
        self.recipeDescriptionLabel = Label(self.master, text = "Descrição da receita: ")
        self.recipeDescriptionLabel.place(x = 20, y = 120)
        self.recipeDescriptionText = Text(self.master, height = "4", width = "40")
        self.recipeDescriptionText.place(x = 160, y = 120)

        # [Layout] - Recipe ingredients
        self.recipeIngredientsLabel = Label(self.master, text = "Ingredientes da receita: ")
        self.recipeIngredientsLabel.place(x = 20, y = 210)
        self.recipeIngredientsText = Entry(self.master)
        self.recipeIngredientsText.place(x = 160, y = 210)

        # [Layout] - Add ingredients button
        self.addRecipeIngredients = Button(self.master, text = "Adicionar", command = self.AddNewIngredient)
        self.addRecipeIngredients.place(x = 290, y = 205)
        self.listboxRecipeIngredients = Listbox(self.master, height = "6", width = "26")
        self.listboxRecipeIngredients.place(x = 160, y = 250)

        # [Layout] - Remove ingredients button
        self.removeRecipeIngredients = Button(self.master, text = "Remover", command = self.RemoveIngredient)
        self.removeRecipeIngredients.place(x = 160, y = 355)

        # [Layout] - Recipe procedure
        self.recipeProcedureLabel = Label(self.master, text = "Procedimentos:")
        self.recipeProcedureLabel.place(x=20,y=390)
        self.recipeProcedureText = Text(self.master, height = "4", width = "40")
        self.recipeProcedureText.place(x=160,y=390)

        # [Layout] - Add recipe button
        self.addRecipe = Button(self.master, text = "Adicionar", width = "20")
        self.addRecipe.place(x=160,y=500)

    def SelectRecipeImage(self):
        self.pathImageRecipe = filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])

    def AddNewIngredient(self):
        if not self.recipeIngredientsText.get():
            messagebox.showerror("Erro", "Introduza algum ingrediente")
        else:
            self.listboxRecipeIngredients.insert(END, self.recipeIngredientsText.get())
            self.recipeIngredientsText.delete(0, END)

    def RemoveIngredient(self):
        try:
            self.selectedIngredient = self.listboxRecipeIngredients.curselection()
            self.listboxRecipeIngredients.delete(self.selectedIngredient)
        except:
            messagebox.showerror("Erro", "Selecione um ingrediente para remover")

if __name__ == '__main__':
    root = Tk()
    app = MainProgram(root)
    root.mainloop()
