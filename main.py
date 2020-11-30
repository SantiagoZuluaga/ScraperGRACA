from src.common.Driver import Driver
from src.tutores.tutores import Tutores
from src.estudiantes.estudiantes import Estudiantes
from src.actividades.actividades import Actividades

def main():
    
    driver = Driver().LoginApplication
    estudiantes = Estudiantes(driver)
    estudiantes.getAllEstudiantes()

if __name__ == "__main__":
    main()