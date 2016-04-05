import sqlite3 as dbapi
import os.path
from gi.repository import Gtk,Gdk
from filespy import actualizar,Descatalogar


class engadir:
    def __init__(self,otras):

        self.db=dbapi.connect("database.dat")

        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/insertar.glade")

        self.inventario=otras

        #ventanas
        self.mas=self.build.get_object("window")
        self.mas.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        self.opciones=self.build.get_object("options")
        self.opciones.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))
        #botones
        self.binsertar=self.build.get_object("binsertar")
        self.bactualizar=self.build.get_object("bactualizar")
        self.beliminar=self.build.get_object("descatalogar")

        #imagenes
        self.icono=self.build.get_object("iconoA")

        #entradas de escritura
        self.prod=self.build.get_object("eproducto")
        self.marc=self.build.get_object("emarca")
        self.mode=self.build.get_object("emodelo")
        self.prec=self.build.get_object("eprecio")

        #label
        self.mensaje=self.build.get_object("mensaje")
        self.mensaje.set_text("")
        self.menserr=self.build.get_object("error")
        self.menserr.set_text("")

        self.sinais={"changeinsert":self.actinsert,
                     "changeact":self.changeact,
                     "cierre":self.cierre,
                     "close":self.close,
                     "insert":self.insert,
                     "borrarProd":self.borrar,}

        self.build.connect_signals(self.sinais)

        self.opciones.show_all()

    def actinsert(self,a):
        self.opciones.hide()
        self.mas.show()

    def changeact(self,b):
        self.opciones.hide()
        actualizar.actual(self.inventario)

    def cierre(self,*args):
        self.inventario.show()
        self.opciones.hide()

    def close(self,*args):
        self.mas.hide()
        self.inventario.show()

    def insert(self,c):
        try:
            cursel=self.db.cursor()
            cursel.execute("select * from codigo")
            for co in cursel:
                c=co[0]
            cursel.close()
            cp="po"+str(c)

            c2=c+1
            pro=self.prod.get_text()
            marc=self.marc.get_text()
            mode=self.mode.get_text()
            prez=self.prec.get_text()

            curin=self.db.cursor()
            curin.execute("insert into almacen values(?,?,?,?,?)",(cp,pro,marc,mode,int(prez),))
            curin.close()

            curdel=self.db.cursor()
            curdel.execute("delete from codigo where id=?",(c,))
            curdel.close()

            curic=self.db.cursor()
            curic.execute("insert into codigo values(?)",(c2,))
            curic.close()
            self.db.commit()

            self.prod.set_text("")
            self.marc.set_text("")
            self.mode.set_text("")
            self.prec.set_text("")

            self.mensaje.set_text("insercion realizada")
        except:
            self.menserr.set_text("usuario o contraseña erroneos")

    def borrar(self,*args):
        Descatalogar.borrar(self.opciones)
        self.opciones.hide()

