# Guía de instalación

### Requisitos
- Python
- Git

### Instalación
**Abrir consola de Git y clonar el repositorio:**
```
git clone https://github.com/gerov12/consistencia-listados-geo.git nombre_carpeta
```

**Ingresar a la carpeta en la que se creó:**
```
cd nombre_carpeta
```

(Opcional) Crear un entorno virtual de Python para evitar instalar las dependencias de forma global en su equipo
```
python -m ./venv
```  

**Instalar dependencias:**

Si se creó el entorno virtual se deberá activar antes de instalar las dependencias
```
source venv/Scripts/activate
```
Verá que la consola indica (venv) en el prompt

Instalar las dependencias desde el archivo *requirements.txt*
```
pip install -r requirements.txt
```

### Uso
```
python consistencia_listados.py
```

*Recuerde que cada vez que abra una nueva consola para usar este script deberá activar el entorno virtual (venv) si es que lo creó*