from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from users.models import User
from .models import InboxMessage, Conversation
from .forms import InboxNewMessageForm

@login_required
def inbox(request, conversation_id=None):
    my_conversations = Conversation.objects.filter(participants=request.user)
    if conversation_id:
        conversation = get_object_or_404(my_conversations, id=conversation_id)
    else:
        conversation = None
    context = {
        'conversation': conversation,
        'my_conversations': my_conversations
    }
    return render(request, 'inbox/inbox.html', context)


def search_users(request):
    if request.htmx:
        letters = request.GET.get('search_user')
        print(letters)
        if len(letters) > 0:
            users = User.objects.filter(
                Q(username__icontains=letters) | Q(first_name__icontains=letters)
            ).exclude(
                Q(username=request.user.username) | Q(first_name=request.user.username)
            )
        else:
            return HttpResponse('')

        context = {
            'users': users
        }

        return render(request, 'inbox/list_searchuser.html', context)

    else:
        return Http404()


@login_required
def new_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    new_message_form = InboxNewMessageForm()

    if request.method == 'POST':
        form = InboxNewMessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            my_conversations = request.user.conversations.all()
            for c in my_conversations:
                if recipient in c.participants.all():
                    message.conversation = c
                    message.save()
                    c.lastmessage_created = timezone.now()
                    c.save()
                    return redirect('inbox:inbox', c.id)

            new_conversation = Conversation.objects.create()
            new_conversation.participants.add(request.user, recipient)
            new_conversation.save()
            message.conversation = new_conversation
            message.save()
            return redirect('inbox:inbox', new_conversation.id)

    context = {
        'recipient': recipient,
        'new_message_form': new_message_form
    }
    return render(request, 'inbox/form_new_message.html', context)


@login_required
def new_reply(request, conversation_id):
    new_message_form = InboxNewMessageForm()
    my_conversations = request.user.conversations.all()
    conversation = get_object_or_404(my_conversations, id=conversation_id)

    if request.method == 'POST':
        form = InboxNewMessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.conversation = conversation
            message.save()
            conversation.lastmessage_created = timezone.now()
            conversation.save()
            return redirect('inbox:inbox', conversation.id)

    context = {
        'new_message_form': new_message_form,
        'conversation': conversation
    }
    return render(request, 'inbox/form_new_reply.html', context)
