import sqlite3 as dbapi
from gi.repository import Gtk,Gdk
from reportlab.lib.styles import getSampleStyleSheet
import os.path
from filespy import engadir
from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4


class almacen():
    def __init__(self,inicio):

        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/inventario.glade")

        self.sinais={
            "cierre":self.cerrar,
            "otros":self.otros,
            "entrar":self.entrar,
            "busqueda":self.busqueda,
            "imprimir":self.impresion,
        }

        self.build.connect_signals(self.sinais)

        self.inicial=inicio

        #boton
        self.boton=self.build.get_object("button")
        self.botros=self.build.get_object("botros")

        rend=Gtk.CellRendererText()

        #comboBox
        self.caja=self.build.get_object("combobox")
        self.caja.pack_start(rend,True)
        self.caja.add_attribute(rend,"text",0)
        self.listado=Gtk.ListStore(str)

        dat=dbapi.connect("database.dat")
        curs=dat.cursor()
        curs.execute("select distinct producto from almacen")
        self.listado.append(('*',))
        for col in curs:
            self.listado.append(col)
        curs.close()

        self.caja.set_model(self.listado)

        #ventana
        self.ventana=self.build.get_object("window")
        self.ventana.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        #otra ventana
        self.emergente=self.build.get_object("emergente")
        self.emergente.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        #entrada de texto
        self.usuario=self.build.get_object("eusuario")
        self.clave=self.build.get_object("eclave")
        self.clave.set_visibility(False)

        #label
        self.label=self.build.get_object("lerror")

        #tabla
        self.tabla=self.build.get_object("inventario")
        self.modelo=Gtk.ListStore(str,str,str,str,int)
        self.tabla.set_model(self.modelo)

        rend=Gtk.CellRendererText()
        columna1=Gtk.TreeViewColumn("Cod",rend,text=0)
        columna2=Gtk.TreeViewColumn("Producto",rend,text=1)
        columna3=Gtk.TreeViewColumn("Marca",rend,text=2)
        columna4=Gtk.TreeViewColumn("Modelo",rend,text=3)
        columna5=Gtk.TreeViewColumn("precio",rend,text=4)

        self.tabla.append_column(columna1)
        self.tabla.append_column(columna2)
        self.tabla.append_column(columna3)
        self.tabla.append_column(columna4)
        self.tabla.append_column(columna5)

        self.actualizar()

        self.ventana.show_all()

    def cerrar(self, *args):
        #Gtk.main_quit(*args)
        self.inicial.show()
        self.ventana.hide()

    def otros(self,v):
        self.emergente.show_all()

    def entrar(self,a):
        u=self.usuario.get_text()
        c=self.clave.get_text()

        k="usuario= tienda \n contraseña=123"

        if(u=="tienda" and c=="123"):
            engadir.engadir(self.ventana)
            self.ventana.hide()
            self.emergente.hide()
        else:
            self.label.set_text(k)

    def busqueda(self,j):

        num=self.caja.get_active()
        if(num==-1):
            print("no hay nada")
        else:
            dat=dbapi.connect("database.dat")
            indice=self.listado.get_iter(num)
            row=self.listado[indice][0]
            lista=Gtk.ListStore(str,str,str,str,int)
            if(row=='*'):
                cursa=dat.cursor()
                cursa.execute('select * from almacen')
                for cel in cursa:
                    lista.append(cel)
                self.tabla.set_model(lista)
            else:
                curs=dat.cursor()
                curs.execute('select * from almacen where producto=?',(row,))
                for po in curs:
                    lista.append(po)
                self.tabla.set_model(lista)


    def actualizar(self):
        db=dbapi.connect("database.dat")
        cursor=db.cursor()
        cursor.execute("select * from almacen")
        for fila in cursor:
            self.modelo.append(fila)
        self.tabla.show()
        db.commit()
        cursor.close()
        db.close()

    def impresion(self,f):

        dat=dbapi.connect("database.dat")
        #cabecera
        follaEstilo=getSampleStyleSheet()

        guion=[]

        cabecera=follaEstilo['Heading4']
        cabecera.pageBreakBefore=0
        cabecera.KepWithNext=0  #Empezar pagina en blanco o no
        cabecera.backColor=colors.deepskyblue

        parrafo=Paragraph("Tienda de electrodomesticos", cabecera)

        guion.append(parrafo)
        guion.append(Spacer(0,20))
        #cuerpo
        estilo=follaEstilo['BodyText']

        cadena="informacion del almacen \n"
        cursor=dat.cursor()
        cursor.execute("select * from almacen")
        tabla=[]

        for fila in cursor:
            tabla.append(fila)


        taboa=Table(tabla)

        parrafo2=Paragraph(cadena,estilo)

        guion.append(parrafo2)
        guion.append(taboa)
        guion.append(Spacer(0,20))
        #imagen
        imagen="../imagenes/glade.jpg"
        imagen_logo=Image(os.path.realpath(imagen),width=100,height=50)
        guion.append(imagen_logo)

        doc=SimpleDocTemplate("Almacen.pdf", pagesize=A4, showBoundary=1)

        doc.build(guion)
        print("pdf creado")

