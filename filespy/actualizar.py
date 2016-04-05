import sqlite3 as dbapi
import os.path
from gi.repository import Gtk,Gdk
from filespy import *

class actual:
    def __init__(self,inventario):
        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/actualizar.glade")

        #cuadro de inventario
        self.almacen=inventario

        #ventana
        self.ventana=self.build.get_object("window")
        self.ventana.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        #combobox
        self.combo=self.build.get_object("combocodigo")
        rend=Gtk.CellRendererText()
        self.combo.pack_start(rend,True)
        self.combo.add_attribute(rend,"text",0)

        dat=dbapi.connect("database.dat")
        self.lista=Gtk.ListStore(str)
        cursor=dat.cursor()
        cursor.execute("select cod from almacen")
        for fila in cursor:
            self.lista.append(fila)
        cursor.close()
        self.combo.set_model(self.lista)

        #entrys
        self.eprod=self.build.get_object("enpro")
        self.emarc=self.build.get_object("enmarc")
        self.emod=self.build.get_object("enmod")
        self.epre=self.build.get_object("enpre")

        #boton
        self.bot=self.build.get_object("bactualizar")
        self.bot2=self.build.get_object("bbuscar")

        #label
        self.notificar=self.build.get_object("notificacion")
        self.notificar.set_text(" ")

        #conexiones
        self.signal={"cierre":self.cierre,
                     "search":self.buscar,
                     "actualizacion":self.actualizar_base,}

        self.build.connect_signals(self.signal)

        self.ventana.show_all()


    #cierra la ventana
    def cierre(self,*args):
        self.ventana.hide()
        self.almacen.show()
    #busca por producto
    def buscar(self,a):
        dat=dbapi.connect("database.dat")
        num=self.combo.get_active()
        if(num==-1):
            self.eprod.set_text("")
            self.emarc.set_text("")
            self.emod.set_text("")
            self.epre.set_text("")
        else:
            indice=self.lista.get_iter(num)
            row=self.lista[indice][0]
            listas=Gtk.ListStore(str,str,str,str,int)
            curs=dat.cursor()

            curs.execute('select * from almacen where cod=?',(row,))
            for po in curs:
                listas.append(po)
            self.eprod.set_text(po[1])
            self.emarc.set_text(po[2])
            self.emod.set_text(po[3])
            self.epre.set_text(str(po[4]))

    #actualiza el producto escogido
    def actualizar_base(self,c):
        dat=dbapi.connect("database.dat")

        num=self.combo.get_active()
        if(num==-1):
            self.notificar.set_text("has de escoger un producto para actualizar")

        else:
            indice=self.lista.get_iter(num)
            co=self.lista[indice][0]

            pro=self.eprod.get_text()
            mar=self.emarc.get_text()
            mod=self.emod.get_text()
            pre=self.epre.get_text()

            cur=dat.cursor()
            cur.execute("update almacen set producto=?, marca=?, modelo=?, precio=? where cod=?",(pro,mar,mod,pre,co))
            dat.commit()

            self.eprod.set_text("")
            self.emarc.set_text("")
            self.emod.set_text("")
            self.epre.set_text("")

            self.notificar.set_text("actualizacion completada con exito")
