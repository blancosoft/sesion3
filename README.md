# Taller 3: Lógica difusa comercial

Aplicación de escritorio en Python para resolver el taller de lógica difusa de la sesión 3 de Sistemas Expertos e Inteligencia Artificial.

## Requisitos

- Windows 10 u 11
- Python 3.9 o superior
- Tkinter, incluido normalmente en la instalación oficial de Python

## Ejecución

Desde esta carpeta, abrir PowerShell y ejecutar:

```powershell
py app.py
```

La aplicación inicia con los tres conductores solicitados en el taller: `3, 6, 12` años de experiencia. También permite editar la lista y volver a evaluar.

## Modelo difuso

Se implementa `membresia_triangular` sin librerías externas usando tres conjuntos:

- **Novato:** `(0, 0, 5)`
- **Intermedio:** `(2, 5, 8)`
- **Experto:** `(5, 10, 20)`

Para cada conductor se muestran los tres grados de pertenencia. La categoría final se obtiene con `max()` sobre esos grados, tal como solicita el taller.