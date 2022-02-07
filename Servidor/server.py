import select
import socket
import sys
import queue
import pickle
import threading

def hilo():#Metodo que ejecuta en paralelo el reciimiento de mensajes UDP
    while True:
        msgUsuario, dirUsuario = s.recvfrom(1024)#Socket que recibe datos al servidor
        msgU = msgUsuario.decode()
        print ('Informacio recibida UDP: '+msgU)
        if msgU.find('registrar') != -1:#Condicional que registra al nuevo usuario
            usuario = msgU.split()[1]
            if usuario in usuariosUDP:
                msg = 'El usuario ya existe'
                byt = msg.encode('utf-8')
                s.sendto(byt,dirUsuario)
            else:
                usuariosUDP.append(usuario)
                infoUsuariosUDP.append(dirUsuario)
                msg = 'registrado'
                byt = msg.encode('utf-8')
                s.sendto(byt,dirUsuario)
        elif msgU.find('lista') != -1:#Condicional que retorna la lista de usuarios
            usuarioEliminar = msgU.split()[1]
            lista = list(usuariosUDP)
            lista.remove(usuarioEliminar)
            byt = (','.join(lista)).encode('utf-8')
            s.sendto(byt,dirUsuario)
        elif msgU.find('mensaje') != -1:#Condicional que retorna el nombre y direccion del destino
            destinatario = msgU.split()[1]
            if destinatario in usuariosUDP:
                index = usuariosUDP.index(destinatario)
                pick = infoUsuariosUDP[index][0]+' '+str(infoUsuariosUDP[index][1])
                byt = pick.encode('utf-8')
                s.sendto(byt, dirUsuario)
            else:
                msg = 'Usuario no encontrado'
                byt = msg.encode('utf-8')
                s.sendto(byt,dirUsuario)
        
puerto = 1500#Puerto del servidor

server_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Creacion socket TCP
server_tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_tcp.setblocking(0)
server_tcp.bind(('', puerto))
server_tcp.listen(10)

server_udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#Creacion socket UDP
server_udp.bind(('',puerto))

inputs = [server_udp,server_tcp]
outputs = []
colaMensajes = {}
usuariosUDP = []
infoUsuariosUDP = []
usuariosTCP = []
infoUsuariosTCP = []
listaEnviar = []
print ('Servidor conectado')
while inputs:#while que acepta entradas del cliente TCP y UDP
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is server_tcp:#if que verifica si la entrada es TCP
            usuario, dirUsuario = s.accept()#Guarda al nuevo socket
            usuario.setblocking(0)
            inputs.append(usuario)
            colaMensajes[usuario] = queue.Queue()
            listaEnviar.append(usuario)

        elif s is server_udp:#if que verifica si la entrada es UDP
            h = threading.Thread(target=hilo)
            h.start()

        else:#Condicional que recibe solicitudes TCP
            mensaje = s.recv(1024)
            if mensaje:
                m = mensaje.decode().strip()
                print("Informacion recibida TCP: ",mensaje)
                if m.find('registrar') != -1:#Condicional que registra al nuevo usuario
                    usuario = m.split()[1]
                    ipC = m.split()[2]
                    dirC = int(m.split()[3])
                    if usuario in usuariosTCP:
                        msg = 'El usuario ya existe'
                        byt = msg.encode('utf-8')
                        colaMensajes[s].put(byt)
                        if s not in outputs:
                            outputs.append(s)
                    else:
                        usuariosTCP.append(usuario)
                        infoUsuariosTCP.append((ipC,dirC))
                        msg = 'registrado'
                        byt = msg.encode('utf-8')
                        colaMensajes[s].put(byt)
                        if s not in outputs:
                            outputs.append(s)

                elif m.find('lista') != -1:#Condicinal que retorna la lista de usuarios
                    usuarioEliminar = m.split()[1]
                    lista = list(usuariosTCP)
                    byt = (','.join(lista)).encode('utf-8')
                    colaMensajes[s].put(byt)
                    if s not in outputs:
                        outputs.append(s)
                elif m.find('mensaje') != -1:
                    destinatario = m.split()[1]
                    if destinatario in usuariosTCP:
                        index = usuariosTCP.index(destinatario)
                        mensaje = m.split()[1:]
                        mensajeCompleto = ' '.join(mensaje)
                        byt = mensajeCompleto.encode('utf-8')
                        for s in listaEnviar:
                            colaMensajes[s].put(byt)
                            if s not in outputs:
                                outputs.append(s)
                    else:
                        msg = 'Usuario no encontrado'
                        byt = msg.encode('utf-8')
                        colaMensajes[s].put(byt)
                        if s not in outputs:
                            outputs.append(s)

    for s in writable:#Condicinal que regresa los mensajes TCP
        if not colaMensajes[s].empty():
            msg = colaMensajes[s].get()
            s.send(msg)         
        else:
            outputs.remove(s)

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del colaMensajes[s]
