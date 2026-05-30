# main.py
# Punto de entrada de la aplicación.
# Instancia el servicio (lógica) y la UI por separado.
 
from core.libreria_service import LibreriaService
from ui.app import App
 
 
def main():
    # 1. Inicializar la capa de lógica de negocio
    service = LibreriaService()
 
    # 2. Inicializar y ejecutar la interfaz gráfica
    app = App(service)
    app.mainloop()
 
 
if __name__ == "__main__":
    main()
