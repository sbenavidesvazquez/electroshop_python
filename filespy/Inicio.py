import sqlite3 as dbapi
import os.path
from gi.repository import Gtk,Gdk
from filespy import inventario,compras

class principal:
    """ Clase inicial de la aplicacion """
    def __init__(self):
        """
        inicial de la clase principal
        """
        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/inicio.glade")
        #si no existe la base de datos la crea de nuevo
        if os.path.exists("database.dat"):
            self.bd=dbapi.connect("database.dat")
            self.cursor=self.bd.cursor()
            self.bd.commit()
        else:
            self.bd=dbapi.connect("database.dat")
            self.cursor=self.bd.cursor()
            self.bd.commit()
            self.cursor.execute("create table almacen( cod varchar(6) primary key not null,"
                                "producto varchar(20) not null,"
                                "marca varchar(20) not null,"
                                "modelo varchar(20),"
                                "precio int)")
            self.bd.commit()
            self.cursor.execute("create table codigo(id int primary key not null)")
            self.bd.commit()
            self.cursor.execute("insert into codigo values(1)")
            self.bd.commit()

        self.inicio=self.build.get_object("window")
        self.inicio.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        self.inicio.show_all()
        #funciones
        self.sinais={"cierre":self.cierre,
                     "inventario":self.salto,
                     "compra":self.compra,}

        self.build.connect_signals(self.sinais)
    #cierra la aplicacion
    def cierre(self, *args):
        """
        Cierra la aplicacion
        """
        Gtk.main_quit(*args)
    #salta al inventario
    def salto(self,a):
        """Cierra la interfaz de inicio y abre la interfaz de inventario"""
        inventario.almacen(self.inicio)
        self.inicio.hide()
    #salta a la interfaz de compra
    def compra(self,b):
        """Cierra la interfaz de inicio y abre la de compra"""
        compras.comprar(self.inicio)
        self.inicio.hide()

ventana=principal()
Gtk.main()