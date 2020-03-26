from django.shortcuts import render
from django.views import View
from renting.models import Sala, Rezerwacja
from datetime import date, datetime


class AddSalaView(View):

    def get(self, request):
        return render(request, 'renting/add_sala.html', {'title': 'Add Room Page'})

    def post(self, request):
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = request.POST.get('has_projector')
        if name and capacity:
            projector = True if has_projector == 'on' else False
            Sala.objects.create(name=name,
                                capacity=capacity,
                                has_projector=projector
                                )
            ctx = {
                'success': 'Dodano salę'
            }
        return render(request, 'renting/add_sala.html', ctx)


class ModifySalaView(View):

    def get(self, request, sid):
        sala = Sala.objects.get(id=sid)
        ctx = {
            'sala': sala,
            'title': 'Edit Room Page'
        }
        return render(request, 'renting/modify_sala.html', ctx)

    def post(self, request, sid):
        sala_to_mod = Sala.objects.get(id=sid)
        name = request.POST.get('name')
        capacity = request.POST.get('capacity')
        has_projector = request.POST.get('has_projector')
        if name and capacity:
            projector = True if has_projector == 'on' else False
            sala_to_mod.name = name
            sala_to_mod.capacity = capacity
            sala_to_mod.has_projector = projector
            sala_to_mod.save()
            ctx = {
                'success': 'Pomyślnie zmodyfikowano salę'
            }
            return render(request, 'renting/modify_sala.html', ctx)


class DeleteSalaView(View):

    def get(self, request, sid):
        sala = Sala.objects.get(id=sid)
        ctx = {
            'sala': sala,
            'title': 'Delete Page',
        }
        return render(request, 'renting/delete_confirmation_page.html', ctx)

    def post(self, request, sid):
        sala = Sala.objects.get(id=sid)
        confirmation = request.POST.get('delete-room')
        if confirmation is not None:
            sala.delete()
            ctx = {
                'confirmation': confirmation,
                'msg': f'Sala {sala.name} została usunięta',
                'title': 'Delete Page',
            }
            return render(request, 'renting/delete_sala.html', ctx)


class MainView(View):

    def get(self, request):
        salas = Sala.objects.all().order_by('id')
        ctx = {
            'salas': salas,
            'title': 'Home Page'
        }
        return render(request, 'renting/home.html', ctx)


class SearchView(View):

    def get(self, request):
        name = request.GET.get('name')
        capacity_from = request.GET.get('capacity_from')
        capacity_to = request.GET.get('capacity_to')
        has_projector = request.GET.get('has_projector')
        salas = Sala.objects.all().order_by('id')
        if name:
            salas = salas.filter(name__icontains=name)
        if capacity_from:
            salas = salas.filter(capacity__gte=capacity_from)
        if capacity_to:
            salas = salas.filter(capacity__lte=capacity_to)
        if has_projector:
            salas = salas.filter(has_projector=True)
        ctx = {
            'salas': salas,
            'title': 'Search Page'
        }
        return render(request, 'renting/search.html', ctx)


class DetailSalaView(View):

    def get(self, request, sid):
        sala = Sala.objects.get(id=sid)
        date_today = date.today()
        reservations = Rezerwacja.objects.filter(date__gte=date_today).filter(sala_id=sid)
        ctx = {
            'sala': sala,
            'reservations': reservations,
        }
        return render(request, 'renting/detail_sala.html', ctx)


class ReservationView(View):

    def get(self, request, sid):
        sala = Sala.objects.get(id=sid)
        return render(request, 'renting/reservation.html', {'sala': sala, 'title': 'Reservation Page'})

    def post(self, request, sid):
        sala = Sala.objects.get(id=sid)
        comment = request.POST.get('comment')
        reservation_date = request.POST.get('date')
        date_today = date.today()
        date_to_check = datetime.strptime(reservation_date, "%Y-%m-%d").date()
        if date_to_check is not None:
            rezerwacja = Rezerwacja.objects.filter(sala_id=sid).filter(date=date_to_check)
            if rezerwacja:
                ctx = {
                    'error': 'Rezerwacja nieudana. Sprawdź inny termin lub wpisz poprawną datę.',
                    'title': 'Error'
                }
                return render(request, 'renting/reservation.html', ctx)
            if date_today > date_to_check:
                ctx = {
                    'error': 'Rezerwacja nieudana. Sprawdź inny termin lub wpisz poprawną datę.',
                    'title': 'Error'
                }
                return render(request, 'renting/reservation.html', ctx)
            Rezerwacja.objects.create(date=reservation_date, comment=comment, sala=sala)
            ctx = {
                'success': 'Rezerwacja przebiegła pomyślnie',
                'title': 'Reservation Page'
            }
            return render(request, 'renting/reservation.html', ctx)


class AboutView(View):

    def get(self, request):
        return render(request, 'renting/about.html', {'title': 'About Page'})