import json
import os
from datetime import datetime

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput


# ==================================================
# COLORES
# ==================================================

NARANJA = (0.96, 0.49, 0.0, 1)
GRIS_OSCURO = (0.20, 0.20, 0.20, 1)
GRIS_CLARO = (0.95, 0.95, 0.95, 1)
BLANCO = (1, 1, 1, 1)
ROJO = (0.85, 0.1, 0.1, 1)


# ==================================================
# FUNCIONES PARA ARCHIVOS
# ==================================================

def cargar_datos(archivo, valor_inicial):

    if os.path.exists(archivo):

        try:

            with open(
                archivo,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except:

            return valor_inicial

    return valor_inicial


def guardar_datos(archivo, datos):

    with open(
        archivo,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            datos,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==================================================
# APLICACIÓN
# ==================================================

class ControlVentasApp(App):


    # ==============================================
    # INICIAR
    # ==============================================

    def build(self):

        self.title = "Control de Ventas"

        # ------------------------------------------
        # CARPETA INTERNA DE LA APP
        # ------------------------------------------

        carpeta = self.user_data_dir

        self.archivo_productos = os.path.join(
            carpeta,
            "productos.json"
        )

        self.archivo_ventas = os.path.join(
            carpeta,
            "ventas.json"
        )

        self.archivo_config = os.path.join(
            carpeta,
            "configuracion.json"
        )

        # ------------------------------------------
        # CARGAR DATOS
        # ------------------------------------------

        self.productos = cargar_datos(
            self.archivo_productos,
            []
        )

        self.ventas = cargar_datos(
            self.archivo_ventas,
            []
        )

        self.configuracion = cargar_datos(
            self.archivo_config,
            {
                "negocio": "MI NEGOCIO",
                "stock_minimo": 5,
                "moneda": "$"
            }
        )

        # ------------------------------------------
        # DISEÑO PRINCIPAL
        # ------------------------------------------

        self.layout_principal = BoxLayout(
            orientation="vertical"
        )

        self.crear_header()

        self.contenido = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        self.layout_principal.add_widget(
            self.contenido
        )

        self.crear_menu()

        self.mostrar_inicio()

        return self.layout_principal


    # ==================================================
    # HEADER
    # ==================================================

    def crear_header(self):

        header = BoxLayout(
            size_hint_y=None,
            height=dp(65),
            padding=dp(10)
        )

        header.canvas.before

        self.titulo = Label(
            text=self.configuracion["negocio"],
            font_size="24sp",
            bold=True,
            color=BLANCO
        )

        header.add_widget(
            self.titulo
        )

        self.layout_principal.add_widget(
            header
        )

        header.bind(
            pos=self.dibujar_header,
            size=self.dibujar_header
        )


    def dibujar_header(self, widget, value):

        pass


    # ==================================================
    # MENÚ
    # ==================================================

    def crear_menu(self):

        menu = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(3)
        )

        botones = [

            ("Inicio", self.mostrar_inicio),
            ("Productos", self.mostrar_productos),
            ("Ventas", self.mostrar_ventas),
            ("Historial", self.mostrar_historial),
            ("Config", self.mostrar_configuracion)

        ]

        for texto, funcion in botones:

            boton = Button(
                text=texto,
                font_size="13sp"
            )

            boton.bind(
                on_release=funcion
            )

            menu.add_widget(
                boton
            )

        self.layout_principal.add_widget(
            menu
        )


    # ==================================================
    # LIMPIAR CONTENIDO
    # ==================================================

    def limpiar_contenido(self):

        self.contenido.clear_widgets()


    # ==================================================
    # CREAR SCROLL
    # ==================================================

    def crear_scroll(self):

        scroll = ScrollView()

        caja = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=dp(10),
            padding=dp(5)
        )

        caja.bind(
            minimum_height=caja.setter("height")
        )

        scroll.add_widget(caja)

        self.contenido.add_widget(scroll)

        return caja


    # ==================================================
    # MENSAJES
    # ==================================================

    def mensaje(self, titulo, texto):

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )

        contenido.add_widget(
            Label(
                text=texto,
                halign="center"
            )
        )

        popup = Popup(
            title=titulo,
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        boton = Button(
            text="Aceptar",
            size_hint_y=None,
            height=dp(45)
        )

        boton.bind(
            on_release=popup.dismiss
        )

        contenido.add_widget(boton)

        popup.open()


    # ==================================================
    # INICIO
    # ==================================================

    def mostrar_inicio(self, *args):

        self.limpiar_contenido()

        caja = self.crear_scroll()

        caja.add_widget(
            Label(
                text="INICIO",
                font_size="28sp",
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        cantidad_productos = len(
            self.productos
        )

        caja.add_widget(
            Label(
                text=f"Productos registrados: {cantidad_productos}",
                font_size="18sp",
                size_hint_y=None,
                height=dp(45)
            )
        )

        caja.add_widget(
            Label(
                text="PRODUCTOS CON POCO STOCK",
                font_size="20sp",
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        productos_stock_bajo = []

        for producto in self.productos:

            if (
                producto["cantidad"]
                <=
                self.configuracion["stock_minimo"]
            ):

                productos_stock_bajo.append(
                    producto
                )

        if productos_stock_bajo:

            for producto in productos_stock_bajo:

                caja.add_widget(
                    Label(
                        text=(
                            f"⚠ {producto['nombre']} - "
                            f"Quedan {producto['cantidad']}"
                        ),
                        color=ROJO,
                        font_size="17sp",
                        size_hint_y=None,
                        height=dp(40)
                    )
                )

        else:

            caja.add_widget(
                Label(
                    text="No hay productos con poco stock.",
                    font_size="17sp",
                    size_hint_y=None,
                    height=dp(40)
                )
            )


    # ==================================================
    # PRODUCTOS
    # ==================================================

    def mostrar_productos(self, *args):

        self.limpiar_contenido()

        caja = self.crear_scroll()

        caja.add_widget(
            Label(
                text="PRODUCTOS",
                font_size="28sp",
                bold=True,
                size_hint_y=None,
                height=dp(60)
            )
        )

        boton_agregar = Button(
            text="+ AGREGAR PRODUCTO",
            size_hint_y=None,
            height=dp(50)
        )

        boton_agregar.bind(
            on_release=self.ventana_producto
        )

        caja.add_widget(
            boton_agregar
        )

        if not self.productos:

            caja.add_widget(
                Label(
                    text="No hay productos registrados.",
                    font_size="18sp",
                    size_hint_y=None,
                    height=dp(100)
                )
            )

            return

        for producto in self.productos:

            self.crear_tarjeta_producto(
                caja,
                producto
            )


    # ==================================================
    # TARJETA PRODUCTO
    # ==================================================

    def crear_tarjeta_producto(
        self,
        caja,
        producto
    ):

        tarjeta = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(210),
            padding=dp(10),
            spacing=dp(5)
        )

        tarjeta.add_widget(
            Label(
                text=producto["nombre"],
                font_size="20sp",
                bold=True
            )
        )

        tarjeta.add_widget(
            Label(
                text=(
                    f"Cantidad: "
                    f"{producto['cantidad']}"
                ),
                font_size="16sp"
            )
        )

        tarjeta.add_widget(
            Label(
                text=(
                    f"Precio: "
                    f"{self.configuracion['moneda']}"
                    f"{producto['precio']}"
                ),
                font_size="16sp"
            )
        )

        if (
            producto["cantidad"]
            <=
            self.configuracion["stock_minimo"]
        ):

            tarjeta.add_widget(
                Label(
                    text="⚠ POCO STOCK",
                    color=ROJO,
                    bold=True
                )
            )

        botones = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(5)
        )

        boton_stock = Button(
            text="+ Stock"
        )

        boton_editar = Button(
            text="Editar"
        )

        boton_eliminar = Button(
            text="Eliminar"
        )

        boton_stock.bind(
            on_release=lambda x:
            self.agregar_stock(producto)
        )

        boton_editar.bind(
            on_release=lambda x:
            self.ventana_producto(
                x,
                producto
            )
        )

        boton_eliminar.bind(
            on_release=lambda x:
            self.confirmar_eliminar(
                producto
            )
        )

        botones.add_widget(
            boton_stock
        )

        botones.add_widget(
            boton_editar
        )

        botones.add_widget(
            boton_eliminar
        )

        tarjeta.add_widget(
            botones
        )

        caja.add_widget(
            tarjeta
        )


    # ==================================================
    # AGREGAR / EDITAR PRODUCTO
    # ==================================================

    def ventana_producto(
        self,
        instancia=None,
        producto=None
    ):

        editar = producto is not None

        formulario = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(10)
        )
