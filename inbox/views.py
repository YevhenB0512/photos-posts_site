from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import InboxMessage, Conversation


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
