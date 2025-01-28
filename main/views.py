# Importe requests y json
import requests
import json

from django.shortcuts import render
from datetime import datetime

# Create your views here.
from django.http import HttpResponse

# Importe el decorador login_required
from django.contrib.auth.decorators import login_required, permission_required

# Restricción de acceso con @login_required
@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
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

    responses = list(response_dict.values())  # Convertir los valores a lista

    # Ordenar las respuestas por la fecha del atributo "saved"
    def parse_date(response):
        try:
            if isinstance(response, dict) and "saved" in response:
                raw_date = response["saved"]

                # Reemplazar espacio no separable y ajustar formato de "a. m." / "p. m."
                cleaned_date = raw_date.replace('\xa0', ' ').replace('a. m.', 'AM').replace('p. m.', 'PM')

                print("Fecha limpia:", cleaned_date)  # Para depuración
                return datetime.strptime(cleaned_date, "%d/%m/%Y, %I:%M:%S %p")
        except (ValueError, TypeError) as e:
            print("Error al parsear fecha:", e)
        return None

    # Filtrar respuestas con fechas válidas
    responses_with_dates = [
        response for response in responses if parse_date(response) is not None
    ]

    # Ordenar respuestas con fechas válidas
    sorted_responses = sorted(
        responses_with_dates,
        key=parse_date,
        reverse=False,
    )

    # Obtener la primera y última respuesta
    first_response = sorted_responses[0] if sorted_responses else None
    last_response = sorted_responses[-1] if sorted_responses else None

    # Extraer y formatear fechas
    first_response_date = parse_date(first_response).strftime("%d/%m/%Y") if first_response else None
    last_response_date = parse_date(last_response).strftime("%d/%m/%Y") if last_response else None

    # Calcular el día con más respuestas
    date_counts = {}
    for response in responses_with_dates:
        date_obj = parse_date(response)
        if date_obj:
            date_str = date_obj.strftime("%d/%m/%Y")  # Solo la fecha
            date_counts[date_str] = date_counts.get(date_str, 0) + 1

    # Encontrar el día con más respuestas
    high_rate_day = max(date_counts, key=date_counts.get) if date_counts else None
    high_rate_count = date_counts[high_rate_day] if high_rate_day else 0

    high_rate_day_response = high_rate_day if high_rate_day else "Sin datos"

    # Objeto con los datos a renderizar
    data = {
        'title': 'Landing - Dashboard',
        'total_responses': total_responses,
        'responses': responses,
        'first_responses': first_response_date,
        'last_responses':  last_response_date,
        'high_rate_responses': high_rate_day_response
    }

    return render(request, 'main/index.html', data)