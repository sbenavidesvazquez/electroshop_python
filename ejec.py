from distutils.core import setup

setup(name="ElectroShop",
      version="Alpha",
      description="Tienda de electrodomesticos",
      author="Sergio Benavides",
      author_email="el mio y punto",
      scripts=["filespy/Inicio.py"],
      packages=["filespy", "imagenes","interfaz"],
      py_modules=["filespy/actualizar","filespy/compras","filespy/Descatalogar","filespy/engadir","filespy/inventario"]
      )