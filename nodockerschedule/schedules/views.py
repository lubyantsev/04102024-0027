from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ScheduleForm, PasswordForm, EventForm
from .models import Schedule, Event


def create_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, 'Расписание успешно создано!')
            return redirect('home')
    else:
        form = ScheduleForm()
    return render(request, 'schedules/create_schedule.html', {'form': form})


def schedule_detail_view(request, schedule_id):
    try:
        schedule = Schedule.objects.get(id=schedule_id)
    except Schedule.DoesNotExist:
        messages.error(request, 'Расписание не найдено.')
        return redirect('home')

    events = Event.objects.filter(schedule=schedule)
    buttons = Event.objects.filter(schedule=schedule)

    event_form = EventForm()

    if request.method == 'POST':
        if 'edit_event' in request.POST:
            event_id = request.POST['edit_event']
            try:
                event = Event.objects.get(id=event_id)
                event_form = EventForm(request.POST, instance=event)
                if event_form.is_valid():
                    event_form.save()
                    messages.success(request, 'Событие обновлено!')
            except Event.DoesNotExist:
                messages.error(request, 'Событие не найдено.')
        elif 'new_event' in request.POST:
            event_form = EventForm(request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.schedule = schedule
                event.save()
                messages.success(request, 'Событие добавлено!')
        elif 'new_button' in request.POST:
                messages.success(request, 'Кнопка добавлена!')

    return render(request, 'schedules/schedule_detail.html', {
        'schedule': schedule,
        'events': events,
        'event_form': event_form,
        'buttons': buttons,
    })


def home_view(request):
    if request.method == 'POST':
        password_form = PasswordForm(request.POST)
        if password_form.is_valid():
            try:
                schedule = Schedule.objects.get(password=password_form.cleaned_data['password'])
                return redirect('schedule_detail', schedule_id=schedule.id)
            except Schedule.DoesNotExist:
                messages.error(request, 'Расписание с таким паролем не найдено.')
    else:
        password_form = PasswordForm()

    # Логика для создания нового расписания
    if request.method == 'POST' and 'create_schedule' in request.POST:
        new_schedule = Schedule.objects.create(password=request.POST['new_password'])
        messages.success(request, 'Новое расписание создано!')
        return redirect('schedule_detail', schedule_id=new_schedule.id)

    return render(request, 'schedules/home.html', {
        'password_form': password_form,
        'new_schedule_form': True,  # Флаг для отображения формы нового расписания
    })

def main_page(request):
    if request.method == 'POST':
        if 'create_schedule' in request.POST:
            password = request.POST.get('password')
            new_schedule = Schedule.objects.create(password=password)
            return redirect('main_page')  # Перенаправление на главную страницу
        elif 'open_schedule' in request.POST:
            password = request.POST.get('schedule_password')
            try:
                schedule = Schedule.objects.get(password=password)
                request.session['schedule_id'] = schedule.id
                return redirect('edit_schedule')  # Перенаправление на страницу редактирования
            except Schedule.DoesNotExist:
                error_message = "Неверный пароль расписания"
                return render(request, 'main_page.html', {'error_message': error_message})

    return render(request, 'main_page.html')

def edit_schedule(request):
    schedule_id = request.session.get('schedule_id')
    schedule = Schedule.objects.get(id=schedule_id)
    events = schedule.events.all()

    if request.method == 'POST':
        if 'save_event' in request.POST:
            when = request.POST.get('when')
            where = request.POST.get('where')
            who = request.POST.get('who')
            Event.objects.create(schedule=schedule, when=when, where=where, who=who)
            return redirect('edit_schedule')  # Перезагрузка страницы редактирования
        elif 'save_changes' in request.POST:
            # Логика для сохранения изменений
            pass

    return render(request, 'edit_schedule.html', {'schedule': schedule, 'events': events})