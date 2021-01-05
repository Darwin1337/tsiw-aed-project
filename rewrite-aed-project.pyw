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
        # [Initial configuration]
        self.master = master
        self.loggedInUserInformation = []
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

    def MainProgram_Authentication(self):
        self.ClearWindowWidgets(self.master)
        self.master.withdraw()
        self.newWindow = Toplevel(self.master)
        self.app = Login(self.newWindow)
    
    def ExitProgram(self):
        os._exit(0)

    def MainProgram_FrontPage(self):
        # [Layout] - Sidebar > Profile Picture
        self.possiblePaths = [EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".jpeg", EncryptSHA256(self.loggedInUserInformation[1])[:15] + ".png"]
        self.wasPhotoFound = False
        for path in self.possiblePaths:
            if os.path.exists(os.getcwd() + "\\data\\images\\" + path):
                self.profilePicture = Label(self.master)
                self.profilePicture.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\" + path).resize((70, 70)))
                self.profilePicture["image"] = self.profilePicture.image
                self.profilePicture.place(x = 60, y = 40)
                self.wasPhotoFound = True
                break
        if not self.wasPhotoFound:
            if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
                # verify if its really the default image
                # verify if its really the default image
                # verify if its really the default image
                # verify if its really the default image
                self.profilePicture = Label(self.master)
                self.profilePicture.image = ImageTk.PhotoImage(Image.open(os.getcwd() + "\\data\\images\\default.jpg").resize((70, 70)))
                self.profilePicture["image"] = self.profilePicture.image
                self.profilePicture.place(x = 60, y = 40)
            else:
                messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar")
                os._exit(0)

        # FIX THIS BS
        # FIX THIS BS
        # FIX THIS BS
        # FIX THIS BS
        # FIX THIS BS
        # FIX THIS BS
        # [Layout] - Sidebar > Menu admin
        menuBar = Menu(self.master)
        menuAdmin = Menu(menuBar, tearoff=0)
        menuAdmin.add_command(label = "Admin", command="noaction")
        menuBar.add_cascade(label="Admin", menu=menuAdmin)
        self.master.configure(menu=menuBar)
        # [Layout] - Sidebar > User's first and last name
        self.usersName = Label(self.master, text = self.loggedInUserInformation[2])
        self.usersName.place(x = 50, y = 110)

        # [Layout] - Sidebar > User's type
        if self.loggedInUserInformation[3] == "admin": self.loggedInUserInformation[3] = "administrator"
        self.usersType = Label(self.master, text = self.loggedInUserInformation[3])
        self.usersType.place(x = 65, y = 130)

        # [Layout] - Sidebar > Edit profile button
        self.editProfile = Button(self.master, text = "Editar perfil", height = 2, width = 25)
        self.editProfile.place(x = 0, y = 170)

        # [Layout] - Sidebar > Edit profile button
        self.usersRecipes = Button(self.master, text = "As minhas receitas", height = 2, width = 25)
        self.usersRecipes.place(x = 0, y = 215)

        # [Layout] - Sidebar > Edit profile button
        self.allRecipes = Button(self.master, text = "Receitas", height = 2, width = 25)
        self.allRecipes.place(x = 0, y = 260)

        # [Layout] - Sidebar > Favourites button
        self.usersFavourite = Button(self.master, text = "Favoritos", height = 2, width = 25)
        self.usersFavourite.place(x = 0, y = 305)

        # [Layout] - Sidebar > Notifications button
        self.usersNotifications = Button(self.master, text = "Notificações", height = 2, width = 25)
        self.usersNotifications.place(x = 0, y = 350)

        # [Layout] - Sidebar > Log Out button
        self.usersNotifications = Button(self.master, text = "Terminar sessão", height = 2, width = 25, command = self.MainProgram_Authentication)
        self.usersNotifications.place(x = 0, y = 395)

        # [Layout] - Sidebar > Exit button
        self.exitMainProgram = Button(self.master, text = "Sair", height = 2, width = 25, command=self.ExitProgram)
        self.exitMainProgram.place(x = 0, y = 440)

class Login:
    def __init__(self, master):
        # [Initial configuration]
        self.master = master
        self.master.geometry("400x250")
        CenterWindow(self.master)
        self.master.title("Iniciar Sessão")
        self.master.resizable(False, False)
        self.master.focus_force()

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

        # [Layout] - Password textbox
        self.labelPassword = Label(self.loginPanel, text = "Palavra-passe:")
        self.labelPassword.place(x = 115, rely = 0.40, anchor = E)
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

    def UserLogin(self):
        try:
            app.loggedInUserInformation.clear()
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
                                                app.loggedInUserInformation.append(True)
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
        except Exception as err: messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

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

    def UserRegister(self):
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
                                                            if self.registerEncryptedEmail == line.split(";")[0][0:len(line.split(";")[0]) - 10]: self.isEmailBeingUsed = True
                                                if not self.isEmailBeingUsed:
                                                    self.doesUserWantToContinue = True
                                                    if self.registerProfilePicture.imgpath.split("\\")[-1] == "default.jpg":
                                                        self.continueDefault = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de perfil, se continuar irá ser selecionada a foto de perfil padrão, prosseguir?", icon = 'warning')
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
        except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

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

if __name__ == '__main__':
    root = Tk()
    app = MainProgram(root)
    root.mainloop()