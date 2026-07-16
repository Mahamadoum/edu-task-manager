from django.http import HttpResponse

def hello(request):
    return HttpResponse('<h1>👋 Bonjour !</h1><p>Le projet Django avec Docker fonctionne !</p>')
