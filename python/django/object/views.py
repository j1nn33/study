from django.shortcuts import render, HttpResponseRedirect,  get_object_or_404
from .models import Vch, Author
from .forms import VchForm

# ----------------------index.html ----------------------------

def index(request):
    return render(request,'object/index.html', )

# ----------------------contact.html ----------------------------

def contact(request):
    return render(request, 'object/contact.html')

# ---------------------list.html--------------------------------
def list(request):
    object_list=Vch.objects.all()
    return render(request, 'object/list.html', {'object_list': object_list})

# ----------------------report.html-------------------------------
def report(request):
    num_object = Vch.objects.all().count()
    num_users = Author.objects.all().count()

    return render(
        request,
        'object/report.html',
        context={'num_object': num_object,
                 'num_users': num_users}
    )

# ----------------------create.html ----------------------------

def create(request):
    object_list = Vch.objects.all()

    if request.method == 'POST':
        form = VchForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            form.save()
            #return render(request, 'object/izdelye.html', {'izdelye': post})
            return render(request,'object/list.html',{'object_list': object_list})

    form = VchForm()
    return render(request, 'object/create.html', {'form': form})


# ----------------------izdelye.html ----------------------------

def izdelye(request, pk):
    izdelye = get_object_or_404(Vch, pk=pk)
    return render(request, 'object/izdelye.html', {'izdelye': izdelye})

# ----------------------edit.html ----------------------------

def edit(request, pk):
    object_list = Vch.objects.all()
    post = get_object_or_404(Vch, pk=pk)
    # ветка когда нажимается кнопка сохранить
    if request.method == 'POST':
        form = VchForm(request.POST, instance=post)
        # Check if the form is valid:
        if form.is_valid():
            post = form.save(commit=False)

            form.save()
            # выводит страничку после заполнения
            return render(request, 'object/izdelye.html',  {'izdelye': post})
            #return render(request,'object/list.html',{'object_list': object_list})

    else:
        form = VchForm(instance=post)
    # выводит форму на редактирование
    return render(request, 'object/edit.html', {'form': form})




