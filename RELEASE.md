# Cambios en esta versión

- Añadida dependencia explícita `setuptools == 76.0.0` para corregir el error `ModuleNotFoundError: No module named 'pkg_resources'` al arrancar Gunicorn.
