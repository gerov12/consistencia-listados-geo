# Guía de instalación

### Requisitos
- Python
- Git

### Instalación
**Abrir consola de Git y clonar el repositorio:** (Esto creará una carpeta llamada "nombre_carpeta", modificar al nombre que desee)  
```
git clone https://github.com/gerov12/consistencia-listados-geo.git nombre_carpeta
```

**Ingresar a la carpeta en la que se creó:** (Tambien se puede ingresar manualmente desde el explorador de Windows y abrir una nueva consola de Git allí)
```
cd nombre_carpeta
```

(Recomendado) Crear un entorno virtual de Python para evitar instalar las dependencias de forma global en su equipo
```
python -m venv ./venv
```  

**Instalar dependencias:**

Si se creó el entorno virtual se deberá activar antes de instalar las dependencias
```
source venv/Scripts/activate
```
Verá que la consola indica (venv) en el prompt, indicando que el entorno está activo

Instalar las dependencias especificadas en el archivo *requirements.txt*
```
pip install -r requirements.txt
```

### Uso
Asegurarse de estár dentro de la carpeta en la que clonó el directorio.  
Abrir la consola de Git y ejecutar:
```
python consistencia_listados.py
```

*Recuerde que cada vez que abra una nueva consola para usar este script deberá activar el entorno virtual (venv) si es que lo creó*
