from api.views import LandingAPI
from rest_framework.request import Request
from django.shortcuts import render
from datetime import datetime
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('main.index_viewer', raise_exception=True)
def index(request):
    # Crear un objeto Request de DRF basado en el request original
    drf_request = Request(request)

    # Llamar directamente al método GET de LandingAPI
    response = LandingAPI().get(drf_request)

    # Extraer los datos JSON directamente
    response_dict = response.data if response and hasattr(response, 'data') else {}

    # Respuestas totales
    total_responses = len(response_dict.keys()) if response_dict else 0

    responses = list(response_dict.values()) if response_dict else []

    # Ordenar las respuestas por la fecha del atributo "saved"
    def parse_date(response):
        try:
            if isinstance(response, dict) and "saved" in response:
                raw_date = response["saved"]

                # Reemplazar espacio no separable y ajustar formato de "a. m." / "p. m."
                cleaned_date = raw_date.replace('\xa0', ' ').replace('a. m.', 'AM').replace('p. m.', 'PM')

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
        'last_responses': last_response_date,
        'high_rate_responses': high_rate_day_response
    }

    return render(request, 'main/index.html', data)
