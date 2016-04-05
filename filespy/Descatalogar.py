import sqlite3 as dbapi
import os.path
from gi.repository import Gtk,Gdk
from filespy import actualizar

class borrar:
    def __init__(self,opcion):

        self.db=dbapi.connect("database.dat")

        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/descatalogar.glade")

        #ventanas
        self.opciones=opcion

        self.venEl=self.build.get_object("eliminado")
        self.venEl.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        self.adver=self.build.get_object("window1")
        self.adver.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        self.erro=self.build.get_object("error")
        self.erro.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        #comboBox
        rend=Gtk.CellRendererText()

        self.caja=self.build.get_object("product")
        self.caja.pack_start(rend,True)
        self.caja.add_attribute(rend,"text",0)
        self.listado=Gtk.ListStore(str)

        dat=dbapi.connect("database.dat")
        curs=dat.cursor()
        curs.execute("select cod from almacen")
        for col in curs:
            self.listado.append(col)
        curs.close()

        self.caja.set_model(self.listado)

        #botones
        self.borrar=self.build.get_object("borrar")
        self.atras=self.build.get_object("atras")
        self.aceptar=self.build.get_object("aceptar")
        self.cancelar=self.build.get_object("cancelar")

        #eleccion
        self.elegir=" "

        self.sinais={
            "recoger_item":self.recoger,
            "volver":self.volver,
            "cierre":self.volver,
            "aceptar":self.continuar,
            "cancel":self.cancel,
            "destroy":self.cancel,
        }

        self.build.connect_signals(self.sinais)

        self.venEl.show_all()

    def recoger(self,*args):

        num=self.caja.get_active()

        if(num==-1):
            self.erro.show()
        else:
            indice=self.listado.get_iter(num)
            self.elegir=self.listado[indice][0]
            self.adver.show()

    def volver(self,*args):
        self.venEl.hide()
        self.opciones.show()

    def continuar(self,*args):
        db=dbapi.connect("database.dat")
        cursor=db.cursor()
        cursor.execute("delete from almacen where cod=?",(self.elegir,))
        db.commit()

    def cancel(self,*args):
        self.adver.hide()
