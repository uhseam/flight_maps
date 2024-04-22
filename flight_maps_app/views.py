from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .services import get_booking_url

def booking_url_view(request):
    search_hash = request.GET.get('searchHash')
    dest = request.GET.get('Dest')
    id = request.GET.get('id')
    orig = request.GET.get('Orig')
    search_id = request.GET.get('searchId')

    if not all([search_hash, dest, id, orig, search_id]):
        return JsonResponse({"error": "All parameters are required"}, status=400)

    try:
        result = get_booking_url(search_hash, dest, id, orig, search_id)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
