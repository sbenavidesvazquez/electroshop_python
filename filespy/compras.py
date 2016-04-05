import sqlite3 as dbapi
import os.path
from gi.repository import Gtk,Gdk
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image, SimpleDocTemplate, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

class comprar:
    def __init__(self,inicio):

        #build
        self.build=Gtk.Builder()
        self.build.add_from_file("../interfaz/compra.glade")

        self.t=[]

        #ventana inicio
        self.inic=inicio
        #signals
        sig={"cierre":self.close,
             "subir":self.subir_al_carro,
             "comprado":self.comprado,}
        self.build.connect_signals(sig)

        #ventana
        self.ventana=self.build.get_object("window")
        self.ventana.modify_bg(Gtk.StateType.NORMAL,Gdk.color_parse('#CEEAFA'))

        #tabla
        self.tabla=self.build.get_object("tabla")

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

        #botones
        self.bañadir=self.build.get_object("bañadir")
        self.bcompra=self.build.get_object("bcomprar")

        #label
        self.text=" "
        self.total=0
        self.interesado=self.build.get_object("contenido")
        self.interesado.set_text(" ")

        #combobox
        self.caja=self.build.get_object("combobox")
        self.caja.pack_start(rend,True)
        self.caja.add_attribute(rend,"text",0)
        self.listado=Gtk.ListStore(str)

        dat=dbapi.connect("database.dat")
        self.listado=Gtk.ListStore(str)
        cursor=dat.cursor()
        cursor.execute("select cod from almacen")
        for fila in cursor:
            self.listado.append(fila)
        cursor.close()
        self.caja.set_model(self.listado)

        self.actualizar()

        self.ventana.show_all()
    #cerrar venatana
    def close(self,*args):
        self.inic.show()
        self.ventana.hide()
    #inserta en el combo box
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

    def subir_al_carro(self,a):
        db=dbapi.connect("database.dat")
        num=self.caja.get_active()

        if(num==-1):
            print("seleccion fallida")
        else:
            indice=self.listado.get_iter(num)
            co=self.listado[indice][0]

            cur=db.cursor()
            cur.execute("select * from almacen where cod=?",(co,))
            for f in cur:
                self.text=self.text+f[1]+"\t"+f[2]+"\t"+f[3]+"\t"+str(f[4])+"\n"
                self.total=self.total+f[4]
                self.t.append(f)

            self.interesado.set_text(self.text)

    def comprado(self,j):
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

        tab=Table(self.t)

        guion.append(tab)
        guion.append(Spacer(0,20))

        totalpago="pago total= "+str(self.total)+" euros"
        parrafo3=Paragraph(totalpago,estilo)
        guion.append(parrafo3)
        guion.append(Spacer(0,20))

        #imagen
        imagen="../imagenes/glade.jpg"
        imagen_logo=Image(os.path.realpath(imagen),width=100,height=50)
        guion.append(imagen_logo)

        doc=SimpleDocTemplate("Factura.pdf", pagesize=A4, showBoundary=1)
        doc.build(guion)
        print("ticket creado")