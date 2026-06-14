from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Show


# READ - All Shows
def shows_list(request):
    """Display all shows"""
    shows = Show.objects.all()
    context = {'shows': shows}
    return render(request, 'shows/index.html', context)


# CREATE - Show Form
def shows_new(request):
    """Display create form"""
    context = {'errors': {}}
    return render(request, 'shows/new.html', context)


# CREATE - Process Form
def shows_create(request):
    """Process form submission"""
    if request.method == 'POST':
        # Prepare data
        data = {
            'title': request.POST.get('title', ''),
            'network': request.POST.get('network', ''),
            'release_date': request.POST.get('release_date', ''),
            'description': request.POST.get('description', ''),
        }

        # Create show with validation
        result = Show.objects.create_show(data)

        if result['success']:
            show = result['show']
            messages.success(request, f'{show.title} created successfully!')
            return redirect('shows:show_detail', pk=show.pk)
        else:
            # Re-render form with errors
            context = {
                'errors': result['errors'],
                'old_data': data
            }
            return render(request, 'shows/new.html', context)

    return redirect('shows:shows_list')


# READ - Show Details
def shows_detail(request, pk):
    """Display single show"""
    show = get_object_or_404(Show, pk=pk)
    context = {'show': show}
    return render(request, 'shows/show.html', context)


# UPDATE - Show Edit Form
def shows_edit(request, pk):
    """Display edit form"""
    show = get_object_or_404(Show, pk=pk)
    context = {
        'show': show,
        'errors': {},
        'old_data': {
            'title': show.title,
            'network': show.network,
            'release_date': show.release_date.strftime('%Y-%m-%d'),
            'description': show.description or '',
        }
    }
    return render(request, 'shows/edit.html', context)


# UPDATE - Process Form
def shows_update(request, pk):
    """Process edit form submission"""
    show = get_object_or_404(Show, pk=pk)

    if request.method == 'POST':
        # Prepare data
        data = {
            'title': request.POST.get('title', ''),
            'network': request.POST.get('network', ''),
            'release_date': request.POST.get('release_date', ''),
            'description': request.POST.get('description', ''),
        }

        # Update show with validation
        result = Show.objects.update_show(pk, data)

        if result['success']:
            updated_show = result['show']
            messages.success(request, f'{updated_show.title} updated successfully!')
            return redirect('shows:show_detail', pk=updated_show.pk)
        else:
            # Re-render form with errors
            context = {
                'show': show,
                'errors': result['errors'],
                'old_data': data
            }
            return render(request, 'shows/edit.html', context)

    return redirect('shows:show_detail', pk=show.pk)


# DELETE
def shows_delete(request, pk):
    """Delete show"""
    show = get_object_or_404(Show, pk=pk)
    title = show.title
    show.delete()
    messages.success(request, f'{title} deleted successfully!')
    return redirect('shows:shows_list')