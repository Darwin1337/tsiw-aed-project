import sys
import os
import re # Usado para verificar certos campos (e-mail, nome, etc.) com expressões regulares (regex)
import cryptocode # Usado para encriptar informações gerais (primeiros e últimos nomes)
import hashlib # Usado para encriptar informações confidenciais (e-mails e passwords) com a função SHA256
import shutil # Usado para copiar ficheiros de um directório para outro
from tkinter import *
from tkinter import messagebox, ttk, filedialog
from functools import partial # Usado para acionar eventos com argumentos customizados
from PySide2 import QtWidgets, QtGui # Usado para centrar a janela no ecrã
from PIL import ImageTk, Image # Usado para converter imagens em formato PGM/PPM
# pip install PySide2
# pip install cryptocode

# TODO:
# Adicionar tipo de utilizador (admin e user).

def CreatePath():
    if not os.path.exists(os.getcwd() + "\\data"): os.mkdir(os.getcwd() + "\\data")
    if not os.path.exists(os.getcwd() + "\\data\\user"): os.mkdir(os.getcwd() + "\\data\\user")
    if not os.path.exists(os.getcwd() + "\\data\\images"): os.mkdir(os.getcwd() + "\\data\\images")

def EncryptSHA256(data):
    EncryptedData = \
        hashlib.sha256(data.encode()).hexdigest()
    return EncryptedData

def EncryptString(data, key):
    return cryptocode.encrypt(data, key)

def DecryptString(data, key):
    return cryptocode.decrypt(data, key)

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

def ChangeTextColor(target, color, event):
    target.config(fg = color)

def ShowPassword(origin, target):
    if int(origin.var.get()) == 0: target["show"] = "*"
    else: target["show"] = ""

def MD5Checksum():
    if os.path.exists(os.getcwd() + "\\data\\images\\default.jpg"):
        md5hash = hashlib.md5(Image.open(os.getcwd() + "\\data\\images\\default.jpg").tobytes())
        return str(md5hash.hexdigest())
    else:
        messagebox.showerror("Erro", "O ficheiro 'data\images\default.jpg' está em falta\nO programa irá fechar")
        os._exit(0)

def RegisterUser(event):
    def BackToLogin(event):
        RegisterWindow.destroy()
        MainWindow.deiconify()

    def RegisterNewUser():
        try:
            RegisterName = " ".join(NameInput.get().lower().split())
            RegisterEmail = EmailInput.get().strip().lower()
            RegisterPassword = PasswordInput.get()
            if RegisterName.replace(" ", ""):
                if RegisterName.count(" ") >= 1:
                    isNameAcceptable = True
                    for i in range(len(RegisterName.split(" "))):
                        if len(RegisterName.split(" ")[i]) < 2: isNameAcceptable = False
                    if isNameAcceptable:
                        if re.compile(r"^[^\W\d_]+(-[^\W\d_]+)?$", re.U).match(RegisterName.replace(" ", "")):
                            if len(RegisterName) <= 55:
                                if re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(RegisterEmail):
                                    if len(RegisterEmail.split("@")[0]) <= 64:
                                        if len(RegisterEmail.split("@")[1]) <= 255:
                                            if len(RegisterPassword) >= 8:
                                                RegisterName = " ".join(RegisterName.split(" ")[i].capitalize() for i in range(len(RegisterName.split(" "))))
                                                CreatePath()
                                                RegisterEncryptedEmail, isEmailBeingUsed = EncryptSHA256(RegisterEmail), False
                                                if os.path.exists(os.getcwd() + "\\data\\user\\users_info.txt"):
                                                    with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                                                        for line in f.readlines():
                                                            if RegisterEncryptedEmail == line.split(";")[0]: isEmailBeingUsed = True
                                                if not isEmailBeingUsed:
                                                    doesUserWantToContinue = True
                                                    if RegisterProfilePicture.imgpath.split("\\")[-1] == "default.jpg":
                                                        ContinueDefault = messagebox.askquestion ("Efetuar registo", "Não selecionou nenhuma foto de perfil, se continuar irá ser selecionada a foto de perfil padrão, prosseguir?", icon = 'warning')
                                                        if ContinueDefault == "no": doesUserWantToContinue = False
                                                        else:
                                                            if MD5Checksum() != DefaultProfilePicture:
                                                                messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar")
                                                                os._exit(0)
                                                    if doesUserWantToContinue:
                                                        shutil.copy2(RegisterProfilePicture.imgpath, os.getcwd() + "\\data\\images\\" + RegisterEncryptedEmail[:15] + os.path.splitext(RegisterProfilePicture.imgpath)[1])
                                                        with open(os.getcwd() + "\\data\\user\\users_info.txt", "a") as f:
                                                            f.write(RegisterEncryptedEmail + ";" + EncryptSHA256(RegisterPassword) + ";" + EncryptString(RegisterName, RegisterEncryptedEmail) + "\n")
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

    def SelectPicture(origin):
        imageCheck, path = False, filedialog.askopenfilename(filetypes=[("Imagem", ".jpg .jpeg .png")])
        if path:
            try:
                Image.open(path).verify()
                imageCheck = True
            except: messagebox.showerror("Erro", "Ocorreu um erro ao tentar ler a imagem")
            if imageCheck:
                try:
                    if Image.open(path).size[0] == Image.open(path).size[1]:
                        if Image.open(path).size[0] >= 50:
                            if os.stat(path).st_size <= 5000000:
                                origin.imgpath = path
                                origin.image = ImageTk.PhotoImage(Image.open(origin.imgpath).resize((50, 50)))
                                origin["image"] = origin.image
                            else: messagebox.showerror("Erro", "O tamanho da imagem é superior a 5mb")
                        else: messagebox.showerror("Erro", "A imagem é inferior a 50x50px")
                    else: messagebox.showerror("Erro", "A largura e altura da imagem não são iguais")
                except IOError: messagebox.showerror("Erro", "Ocorreu um erro a copiar a imagem para o sistema")
                except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

    # Register variables
    NameInput = StringVar()
    EmailInput = StringVar()
    PasswordInput = StringVar()
    DefaultProfilePicture = "28c17e68aa44166d1c8e716bd535676a"

    # Register window
    MainWindow.withdraw()
    RegisterWindow = Toplevel(MainWindow)
    RegisterWindow.geometry("400x375")
    CenterWindow(RegisterWindow)
    RegisterWindow.title("Efetuar Registo")
    RegisterWindow.resizable(False, False)
    RegisterWindow.focus_force()

    # Register fieldset
    RegisterPanel = LabelFrame(RegisterWindow, text = "Efetuar Registo", width = "380", height = "355", bd = "2")
    RegisterPanel.place(x = 10, y = 10)

    # Name textbox
    LabelNameRegister = Label(RegisterPanel, text = "Nome:")
    LabelNameRegister.place(x = 115, y = 35, anchor = E)
    NameTextRegister = Entry(RegisterPanel, textvariable = NameInput, width = "30")
    NameTextRegister.place(relx = 0.35, y = 37.5, anchor = W)

    # Email textbox
    LabelEmailRegister = Label(RegisterPanel, text = "E-mail:")
    LabelEmailRegister.place(x = 115, y = 70, anchor = E)
    EmailTextRegister = Entry(RegisterPanel, textvariable = EmailInput, width = "30")
    EmailTextRegister.place(relx = 0.35, y = 72.5, anchor = W)

    # Password textbox
    LabelPasswordRegister = Label(RegisterPanel, text = "Palavra-passe:")
    LabelPasswordRegister.place(x = 115, y = 105, anchor = E)
    PasswordTextRegister = Entry(RegisterPanel, textvariable = PasswordInput, width = "30", show = "*")
    PasswordTextRegister.place(relx = 0.35, y = 107.5, anchor = W)

    # Show password checkbox
    RegisterPasswordCheckbox = ttk.Checkbutton(RegisterPanel, text = "Mostrar palavra-passe")
    RegisterPasswordCheckbox.var = IntVar()
    RegisterPasswordCheckbox["variable"] = RegisterPasswordCheckbox.var
    RegisterPasswordCheckbox["command"] = partial(ShowPassword, RegisterPasswordCheckbox, PasswordTextRegister)
    RegisterPasswordCheckbox.place(x = 269, y = 135, anchor = E)

    # Profile picture
    LabelRegisterProfilePicture = Label(RegisterPanel, text = "Foto de perfil:")
    LabelRegisterProfilePicture.place(x = 115, y = 170, anchor = E)
    RegisterProfilePicture = Label(RegisterWindow)
    CreatePath()
    if MD5Checksum() == DefaultProfilePicture:
        RegisterProfilePicture.imgpath = os.getcwd() + "\\data\\images\\default.jpg"
        RegisterProfilePicture.image = ImageTk.PhotoImage(Image.open(RegisterProfilePicture.imgpath).resize((50, 50)))
    else:
        messagebox.showerror("Erro", "A foto de perfil padrão não foi reconhecida\nO programa irá fechar")
        os._exit(0)
    RegisterProfilePicture["image"] = RegisterProfilePicture.image
    RegisterProfilePicture.place(x = 142, y = 217.5, anchor = W)
    RegisterChangeProfilePicture = ttk.Button(RegisterPanel, text = "Enviar imagem", command = partial(SelectPicture, RegisterProfilePicture))
    RegisterChangeProfilePicture.place(x = 200, y = 177, anchor = W, width = 117)
    RegisterChangeProfilePictureInfo = Label(RegisterPanel, text = ".jpg .jpeg ou .png", wraplength = 140, justify = LEFT, font=(None, 8))
    RegisterChangeProfilePictureInfo.place(x = 197, y = 200, anchor = W)
    RegisterChangeProfilePictureInfo2 = Label(RegisterPanel, text = "Atenção: A largura e a altura da imagem devem ser iguais e não inferiores a 50px", wraplength = 175, justify = LEFT, font=(None, 8))
    RegisterChangeProfilePictureInfo2.place(x = 129, y = 240, anchor = W)

    # Register button
    RegisterButton = ttk.Button(RegisterPanel, text = "Efetuar Registo", command = RegisterNewUser)
    RegisterButton.place(relx = 0.5, rely = 0.87, width = "100", anchor = CENTER)

    # Back label
    LabelBack = Label(RegisterPanel, text = "Voltar", cursor="hand2")
    LabelBack.place(x = 330, y = 310)
    LabelBack.bind("<Button-1>", partial(BackToLogin))
    LabelBack.bind("<Enter>", partial(ChangeTextColor, LabelBack, "gray"))
    LabelBack.bind("<Leave>", partial(ChangeTextColor, LabelBack, "black"))

def UserLogin():
    try:
        LoggedInUserInformation.clear()
        LoginEmail = LoginEmailInput.get().strip().lower()
        LoginPassword = LoginPasswordInput.get().strip()
        if re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)").match(LoginEmail):
            if len(LoginEmail.split("@")[0]) <= 64:
                if len(LoginEmail.split("@")[1]) <= 255:
                    if len(LoginPassword) >= 8:
                        CreatePath()
                        EncryptedLoginEmail, EncrypedLoginPassword, wasAccountFound = EncryptSHA256(LoginEmail), EncryptSHA256(LoginPassword), False
                        if os.path.exists(os.getcwd() + "\\data\\user\\users_info.txt"):
                            with open(os.getcwd() + "\\data\\user\\users_info.txt", "r") as f:
                                for line in f.readlines():
                                    if line.split(";")[0] == EncryptedLoginEmail:
                                        wasAccountFound = True
                                        if line.split(";")[1] == EncrypedLoginPassword:
                                            LoggedInUserInformation.append(True)
                                            LoggedInUserInformation.append(LoginEmail)
                                            LoggedInUserInformation.append(DecryptString(line.split(";")[2], line.split(";")[0]))
                                            messagebox.showinfo("Sucesso", "Sessão iniciada com sucesso!\nBem-vindo " + LoggedInUserInformation[2])
                                        else: messagebox.showerror("Erro", "A palavra-passe introduzida está incorreta")
                            if not wasAccountFound: messagebox.showerror("Erro", "O e-mail introduzido não foi encontrado")
                        else: messagebox.showerror("Erro", "As informações inseridas não foram encontradas")
                    else: messagebox.showerror("Erro", "O campo de palavra-passe tem de ter 8 ou mais caracteres")
                else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
            else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
        else: messagebox.showerror("Erro", "O e-mail introduzido não é válido")
    except: messagebox.showerror("Erro", "Ocorreu um erro desconhecido")

# Login window
MainWindow = Tk()
MainWindow.geometry("400x250")
CenterWindow(MainWindow)
MainWindow.title("Iniciar Sessão")
MainWindow.resizable(False, False)

# Login variables
LoginEmailInput = StringVar()
LoginPasswordInput = StringVar()
LoggedInUserInformation = []

# Login fieldset
LoginPanel = LabelFrame(MainWindow, text = "Iniciar Sessão", width = "380", height = "230", bd = "2")
LoginPanel.place(x = 10, y = 10)

# Email textbox
LabelEmail = Label(LoginPanel, text = "E-mail:")
LabelEmail.place(x = 115, rely = 0.20, anchor = E)
EmailText = Entry(LoginPanel, width = "30", textvariable = LoginEmailInput)
EmailText.place(relx = 0.35, rely = 0.20, anchor = W)

# Password textbox
LabelPassword = Label(LoginPanel, text = "Palavra-passe:")
LabelPassword.place(x = 115, rely = 0.40, anchor = E)
PasswordText = Entry(LoginPanel, width = "30", show = "*", textvariable = LoginPasswordInput)
PasswordText.place(relx = 0.35, rely = 0.35, anchor = W)

# Show password checkbox
LoginPasswordCheckbox = ttk.Checkbutton(LoginPanel, text = "Mostrar palavra-passe")
LoginPasswordCheckbox.var = IntVar()
LoginPasswordCheckbox["variable"] = LoginPasswordCheckbox.var
LoginPasswordCheckbox["command"] = partial(ShowPassword, LoginPasswordCheckbox, PasswordText)
LoginPasswordCheckbox.place(x = 270, rely = 0.48, anchor = E)

# Login button
LoginButton = ttk.Button(LoginPanel, text = "Iniciar Sessão", command = UserLogin)
LoginButton.place(relx = 0.5, rely = 0.70, width = "100", anchor = CENTER)

# Register label
LabelRegister = Label(LoginPanel, text = "Efetuar Registo", cursor="hand2")
LabelRegister.place(x = 285, y = 185)
LabelRegister.bind("<Button-1>", partial(RegisterUser))
LabelRegister.bind("<Enter>", partial(ChangeTextColor, LabelRegister, "gray"))
LabelRegister.bind("<Leave>", partial(ChangeTextColor, LabelRegister, "black"))

MainWindow.mainloop()
