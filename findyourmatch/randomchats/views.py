from django.shortcuts import render

def random_chat_view(request):
    return render(request, "randomchats/randomchat.html")
