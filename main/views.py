from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# Importe requests y json
import requests
import json
import re
from datetime import datetime
from collections import defaultdict

# Importe el decorador login_required
from django.contrib.auth.decorators import login_required

# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

# Restricción de acceso con @login_required
@login_required



# Restricción de acceso con @login_required y permisos con @permission_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)

def index(request):
    # return HttpResponse("Hello, World!")
    # return render(request, 'main/base.html')

    # Arme el endpoint del REST API
    current_url = request.build_absolute_uri()
    url = current_url + '/api/v1/landing'

    # Petición al REST API
    response_http = requests.get(url)
    response_dict = json.loads(response_http.content)

    print("Endpoint ", url)
    print("Response ", response_dict)

    # Respuestas totales
    total_responses = len(response_dict.keys())

    # Convertir las fechas a objetos datetime y recopilar para análisis
    saved_dates = []
    day_counts = defaultdict(int)

    for key, value in response_dict.items():
        # Manejar posibles claves faltantes como 'suscripcion'
        saved_str = value.get('saved')
        if saved_str:
            try:
                # Reemplazar 'a. m.' y 'p. m.' con 'AM' y 'PM' usando expresiones regulares
                saved_str = re.sub(r'a\.\s*m\.', 'AM', saved_str, flags=re.IGNORECASE)
                saved_str = re.sub(r'p\.\s*m\.', 'PM', saved_str, flags=re.IGNORECASE)

                # Eliminar posibles caracteres no imprimibles o espacios no estándar
                saved_str = saved_str.strip()

                # Ajustar el formato de la fecha según tus datos
                saved_date = datetime.strptime(saved_str, '%m/%d/%Y, %I:%M:%S %p')
                saved_dates.append(saved_date)
                day = saved_date.date()
                day_counts[day] += 1

                print(f"Fecha procesada: {saved_date}")  # Para depuración
            except ValueError as e:
                print(f"Error al parsear la fecha: {e}")

    # Calcular primera y última respuesta
    if saved_dates:
        first_response = min(saved_dates).strftime('%d/%m/%Y, %H:%M:%S')
        last_response = max(saved_dates).strftime('%d/%m/%Y, %H:%M:%S')
    else:
        first_response = 'N/A'
        last_response = 'N/A'

    # Calcular el día con más respuestas
    if day_counts:
        high_rate_day = max(day_counts, key=day_counts.get).strftime('%d/%m/%Y')
        high_rate_responses = day_counts[max(day_counts, key=day_counts.get)]
    else:
        high_rate_day = 'N/A'
        high_rate_responses = 0

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
    }

    # Valores de la respuesta
    responses = response_dict.values()

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_response': first_response,
        'last_response': last_response,
        'high_rate_day': high_rate_day,
        'high_rate_responses': high_rate_responses,
    }

    # Renderización en la plantilla
    return render(request, 'main/index.html', data)