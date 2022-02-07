from tkinter import *
from tkinter import messagebox as MessageBox
import pygame
from pygame import mixer
import socket
import sys
import threading
import os
pygame.init()

class Luna:#Clase del socket TCP
    pygame.init()#Inicia el audio
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Socket TCP para mandar datos
    def interfazTCP(self,usuario,ip,puerto):#Metodo que inicializa variables
        self.usuario=usuario
        self.ip=ip
        self.puerto=puerto
        print (self.usuario,self.ip,self.puerto)
        self.s.connect((ip,puerto))
    
    def botonenviar0(self):#Metodo para enviar mensajes TCP
        sonido=pygame.mixer.Sound("bienve.wav")
        sonido.play()
        try:
            self.nombreDestinatario = self.escribe0.get().split()[0]#Obtiene nombre del destinatario
            self.comandoValido = True
        except Exception:
            print ('Ingresa un comando valido')
            self.comandoValido = False
        if self.comandoValido:
            try:
                self.mensaje = self.escribe0.get().split()[1:]
                self.mensajeCompleto = ' '.join(self.mensaje)#Mensaje a enviar al destinatario
                self.msg = 'mensaje ' + self.nombreDestinatario +' '+ self.usuario + ': ' + self.mensajeCompleto
                self.byt = self.msg.encode('utf-8')
                self.s.send(self.byt)
                self.s.settimeout(10)
            except socket.timeout:
                print ('Ya se tardo, cerrando chat')
        else:
            print ('Comando erroneo')
            MessageBox.showerror("Error", "Debe ingresar un mensaje")       
        self.pantalla0.insert(END, "yo: "+self.escribe0.get())
        self.escribe0.delete(0, END)

    def descargar0(self):#Metodo para obtener lista de usuarios conectados por TCP
        sonido=pygame.mixer.Sound("normal.wav")
        sonido.play()
        self.comando0 = 'lista'
        self.pantalla_usu0.delete(0,'end')
        try:
            self.msg = self.comando0 + ' ' + self.usuario
            self.byt = self.msg.encode('utf-8')
            self.s.send(self.byt)
            self.s.settimeout(10)
            self.listaUsuarios = self.s.recv(4096)
            self.l = self.listaUsuarios.decode().strip()
            self.s.settimeout(None)
            if self.l:
                print ('Usuarios en chat: ' + str(self.l).strip('[]'))
                self.pantalla_usu0.insert(END, self.l)
            else:
                print ('Solo estas tu: ' + self.usuario)
        except socket.timeout:
            print ('Ya se tardo, cerrando chat')
        
    def imprimir0(self,mostrarMensaje):#Metodo para imprimir mensajes entrantes TCP
            self.sms=mostrarMensaje
            self.pantalla0.insert(END, self.sms)

    def hilo0(self):#Metodo que crea hilo para recibir mensajesTCP
        hilo_tcp= threading.Thread(target=self.oso)
        hilo_tcp.start()

    def oso(self):#Metodo que crea la interfaz grafica
        self.mesa0=Tk()
        self.mesa0.geometry("+400+180")#Ubicacion ventana
        self.mesa0.title("Autores: Eduardo y Oscar")#Titulo  
        self.mesa0.resizable(0,0)
        self.mesa0.geometry("500x350")#Tamaño ventana

        self.mantel0=Frame()#Crea un frame
        self.mantel0.pack(fill="both",expand="True")
        self.mantel0.config(bg="#b7d9e7")#Color del frame 
        self.mantel0.config(width="500",height="350")#Tamaño del frame
        self.mantel0.pack()

        self.imagen2=PhotoImage(file="vo1.png")#Imagen boton ENVIAR
        self.imagen3=PhotoImage(file="vo3.png")#Imagen boton USUARIOS

        self.botonenvio0=Button(self.mantel0,image=self.imagen2, height=40,width=40,bg='#dedede',command=self.botonenviar0)#Boton enviar TCP
        self.botonenvio0.place(x=415, y=290)

        self.boton_usu0=Button(self.mantel0,image=self.imagen3, height=40,width=40,bg='#dedede',command=self.descargar0)#Boton usuarios TCP
        self.boton_usu0.place(x=415, y=230)

        self.escribe0 = Entry(self.mantel0)
        self.escribe0.config(fg="black",bg= "white")
        self.escribe0.place(x=30,y=290, height=45, width=380)

        self.tipo0=Label(self.mantel0,text="Tipo: TCP",fg="black",bg= "#b7d9e7",font=("Georgia"))#Etiqueta chat TCP TIPO TCP
        self.tipo0.place(x=250,y=20)

        self.envia0=Label(self.mantel0,text="Nombre: "+self.usuario,fg="black",bg= "#b7d9e7",font=("Georgia"))#Etiqueta chat TCP Nombre
        self.envia0.place(x=30,y=20)

        self.pantalla0=Listbox(self.mantel0)#Listbox para mostrar la conversacion del usuario
        self.pantalla0.insert(0,"Bienvenido")
        self.pantalla0.config(fg="black",bg= "white")
        self.pantalla0.place(x=30,y=50, height=170, width=425)

        self.scroll0=Scrollbar(self.mantel0,command=self.pantalla0.yview)#Scrollbar para poder recorrer el listbox de la conversacion
        self.scroll0.place(x=450,y=50,height=170)

        self.pantalla0.config(yscrollcommand=self.scroll0.set)

        self.pantalla_usu0=Listbox(self.mantel0)#Listbox que muestra la lista de usuarios
        self.pantalla_usu0.config(fg="black",bg= "white")
        self.pantalla_usu0.place(x=30,y=230, height=45, width=380)

        self.mesa0.mainloop()#Inicia la ventana del chat

def mundoTCP(w,x,y):#Metodo principal del socket TCP que crea el socket y recibe los parametros
    usuario = w
    puerto = int(y)
    ip = x
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#Creacion del socket cliente TCP
        s.connect((ip, puerto))
        print('Conectado al servidor')
        so = s.getsockname()
        ipC = so[0]
        dirC = str(so[1])
        mensaje = 'registrar '+ usuario +' '+ ipC +' '+ dirC
        s.send(mensaje.encode('utf-8'))#Mensaje que valida registro del cliente
        msgServidor = s.recv(1024)
        m = msgServidor.decode()
        print (m)
        lobo=Luna()
        lobo.interfazTCP(usuario, ip, puerto)
        lobo.hilo0()
        while True:#Ciclo que recibe mensajes TCP
            msgRemitente = s.recv(4096)
            if not msgRemitente:
                break
            dirRemitente = s.getsockname()
            msgR = msgRemitente.decode().strip()
            print ('Lo que se recibe: '+msgR)
            comprobar = msgR.split()[0]
            if comprobar == usuario:
                mensaje = ' '.join(msgR.split()[1:])
                lobo.imprimir0(mensaje)

class Estrella:#Clase del socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
        pygame.init()
        
        def interfazUDP(self,usuario,ip,puerto):#Metodo que inicializa las variables
            self.usuario=usuario
            self.ip=ip
            self.puerto=puerto
            print (self.usuario,self.ip,self.puerto)
            
        def botonenviar(self):#Metodo para enviar mensajes UDP
            pygame.init()
            self.nombreDestinatario = self.escribe.get().split()[0]
            try:
                self.msg = 'mensaje ' + self.nombreDestinatario
                self.byt = self.msg.encode('utf-8')
                self.s.sendto(self.byt, (self.ip, self.puerto))
                self.s.settimeout(10)
                self.infoDestinatario, self.dirServidor = self.s.recvfrom(4096)
                self.iD = self.infoDestinatario.decode().strip()
                print ('informacion del destinatario: '+self.iD)
                self.s.settimeout(None)
                if "no encontrado" in self.iD:
                    print (self.iD)
                    MessageBox.showerror("Error", "Usuario no encontrado")
                else:
                    self.ipD = self.iD.split()[0]
                    self.puertoD = int(self.iD.split()[1])
                    self.mensaje = self.escribe.get().split()[1:]
                    self.mensajeCompleto = ' '.join(self.mensaje)
                    self.msg2 = self.usuario+': ' + self.mensajeCompleto
                    self.byt2 = self.msg2.encode('utf-8')
                    self.s.sendto(self.byt2, (self.ipD,self.puertoD))
                    sonido=pygame.mixer.Sound("enviar.wav")
                    sonido.play()
                    self.pantalla.insert(END, "yo: "+self.escribe.get())
                    self.escribe.delete(0, END)
            except socket.timeout:
                print ('Ya se tardo, cerrando chat')

        def descargar(self):#Metodo para obtener la lista de usuarios conectados por UDP
            self.comando = 'lista'
            self.pantalla_usu.delete(0,'end')
            try:
                self.msg = self.comando + ' ' + self.usuario
                self.byt = self.msg.encode('utf-8')
                self.s.sendto(self.byt, (self.ip, self.puerto))
                self.s.settimeout(10)
                self.listaUsuarios, self.dirServidor = self.s.recvfrom(4096)
                self.l = self.listaUsuarios.decode().strip()
                print ("Lista recibida: "+self.l)
                self.s.settimeout(None)
                if self.l:
                    print ('Usuarios en chat: ' + str(self.l).strip('[]'))
                    sonido=pygame.mixer.Sound("download.wav")
                    sonido.play()
                    self.pantalla_usu.insert(END, self.l)
                else:
                    print ('Solo estas tu: ' + self.usuario)
                    MessageBox.showwarning("Alerta", "Solo estas conectado tu")
            except socket.timeout:
                print ('Ya se tardo, cerrando chat')
                os._exit(1)
            
        
        def imprimir(self,mostrarMensaje):#Metodo que imprime mensajes UDP
            self.sms=mostrarMensaje
            self.pantalla.insert(END, self.sms)
        
        def hilo(self):#Metodo que crea hilo para recibir mensajes UDP
            hilo_udp= threading.Thread(target=self.perro)
            hilo_udp.start()
        
        def perro(self):#Metodo que crea la interfaz grafica UDP
            self.mesa=Tk()#Creacion venta UDP
            self.mesa.geometry("+400+180")
            self.mesa.title("Autores: Oscar y Eduardo")
            self.mesa.resizable(0,0)
            self.mesa.geometry("500x350")

            self.mantel=Frame()
            self.mantel.pack(fill="both",expand="True")
            self.mantel.config(width="500",height="350")
            self.mantel.pack()

            self.imagen2=PhotoImage(file="enviar2.png")#Imagen de boton enviar
            self.imagen3=PhotoImage(file="user.png")#Imagen de boton usuarios

            self.wall=Label(self.mantel)
            self.wall.place(x=-2,y=0)

            self.botonenvio=Button(self.mantel,image=self.imagen2, height=40,width=40,bg='#dedede',command=self.botonenviar)#Boton enviar UDP
            self.botonenvio.place(x=415, y=290)

            self.boton_usu=Button(self.mantel,image=self.imagen3, height=40,width=40,bg='#dedede',command=self.descargar)#Boton usuarios UDP
            self.boton_usu.place(x=415, y=230)

            self.escribe = Entry(self.mantel)#Entrada de mensajes UDP texto
            self.escribe.config(fg="black",bg= "white")
            self.escribe.place(x=30,y=290, height=45, width=380)

            self.nombre=Label(self.mantel,text="Nombre :",fg="black",bg= "#dedede",font=("Georgia"))#Etiqueta chat UDP Nombre
            self.nombre.place(x=30,y=20)

            self.name=Label(self.mantel,text=self.usuario,fg="black",bg= "#dedede",font=("Georgia"))#Etiqueta chat UDP
            self.name.place(x=110,y=20)

            self.tipo=Label(self.mantel,text="Tipo: UDP",fg="black",bg= "#dedede",font=("Georgia"))#Etiqueta chat UDP TIPO UDP
            self.tipo.place(x=250,y=20)#lo coloca

            self.pantalla=Listbox(self.mantel)#Listbox para mostrar la conversacion del usuario
            self.pantalla.insert(0,"Bienvenido")
            self.pantalla.config(fg="black",bg= "white")
            self.pantalla.place(x=30,y=50, height=170, width=425)

            self.scroll=Scrollbar(self.mantel,command=self.pantalla.yview)#Scrollbar para recorrer conversacion del usuario
            self.scroll.place(x=450,y=50,height=170)
            self.pantalla.config(yscrollcommand=self.scroll.set)

            self.pantalla_usu=Listbox(self.mantel)#Listbox que muestra la lista de usuarios conectados en UDP
            self.pantalla_usu.config(fg="black",bg= "white")
            self.pantalla_usu.place(x=30,y=230, height=45, width=380)
            self.mesa.mainloop()#Inicia ventana UDP

def mundoUDP(w,x,y):#Metodo principal del socket UDP
    usuario = w
    ip = x
    puerto = int(y)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:#Creacion de socket UDP para conectar a servidor
        mensaje = 'registrar '+ usuario
        s.sendto(mensaje.encode('utf-8'),(ip,puerto))
        msgServidor, dirServidor = s.recvfrom(1024)
        m = msgServidor.decode()
        print (m)
        gato=Estrella()
        gato.interfazUDP(usuario, ip, puerto)
        gato.hilo()
        while True:#Ciclo que recibe mensajes TCP
            msgRemitente, dirRemitente = s.recvfrom(4096)
            msgR = msgRemitente.decode().strip()
            mensaje = ' '.join(msgR.split()[0:])
            gato.imprimir(mensaje)

def main():#Metodo principal del programa
    inicio = Tk()#Creacion ventana de inicio
    inicio.geometry("+500+200")
    inicio.resizable(0,0)
    varOpcion=IntVar()
    def datos():
        print(varOpcion.get())
        if varOpcion.get()==1:
            print ("UDP")
            return 1
        elif varOpcion.get()==2:
            print ("TCP")
            return 2
        else:
            return 0

    def botoninicio():#Metodo del boton que incia la ventana de chat y pasa los datos obtenidos en la ventana principal
        v=datos()
        w=cuadro.get()
        x=cuadro0.get()
        y=cuadro1.get()
        print (v,w,x,y)
        if v==1:#Inicia interfaz UDP y cierra la ventana principal
            inicio.destroy()
            mundoUDP(w,x,y)
        if v==2:#Inicia interfaz TCP y cierra la ventana principal
            inicio.destroy()
            mundoTCP(w,x,y)
        if v==0:
            sonido=pygame.mixer.Sound("error.wav")
            sonido.play()
            MessageBox.showerror("Error", "Debe elegir un Protocolo")
    
    inicio.title("Sistemas operativos")#Titulo ventana principal

    wall=Label(inicio)
    wall.place(x=-100,y=-10)

    etiqueta=Label(inicio,text="Protocolo:",fg="black",font=("Georgia")).pack()#Etiqueta Protocolo

    Radiobutton(inicio, text="UDP", variable=varOpcion, value=1, command=datos, fg="black").pack()
    Radiobutton(inicio, text="TCP", variable=varOpcion, value=2, command=datos, fg="black").pack() 

    etiqueta=Label(inicio,text="Nombre:",fg="black",font=("Georgia")).pack()#Etiqueta Nombre

    cuadro = Entry(inicio)#Entrada de nombre
    cuadro.config(fg="black",bg= "white")
    cuadro.pack()

    etiqueta0=Label(inicio,text="IP:",fg="black",font=("Georgia")).pack()#Etiqueta IP 
    etiqueta1=Label(inicio,text="(Ejemplo de IP '127.0.0.1')",fg="black",font=("Georgia")).pack()

    cuadro0 = Entry(inicio)#Entrada de IP
    cuadro0.config(fg="black",bg= "white")
    cuadro0.pack()

    etiqueta2=Label(inicio,text="Puerto:",fg="black",font=("Georgia")).pack()#Etiqueta Puerto

    cuadro1 = Entry(inicio)#Entrada de puerto
    cuadro1.config(fg="black",bg= "white")
    cuadro1.pack()

    imagen=PhotoImage(file="save1.png")#Imagen boton GUARDAR

    boton=Button(inicio,image=imagen, height=30,width=45,bg='#283747',command=botoninicio)#Boton de guardar datos
    boton.pack()

    inicio.mainloop()#Inicia la ventana principal

main()
