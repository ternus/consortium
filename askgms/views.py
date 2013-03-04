# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now
from askgms.models import Question
from consortium.consortium import send_mail

def player_view(request, template='askgms/askgms.html'):
    if request.method == 'POST':
        email = request.POST.get('email'),
        q = Question(
            asker_email=email[0],
            question=request.POST.get('question'),
            public=request.POST.get('public', False)
        )
        q.save()
        send_mail('[Consortium] New question #%s from %s' % (q.id, q.asker_email),
                  "%s has a question: \n\n%s\n\nGo to http://consortium.so/ask/gm/#q%s to answer." % (q.asker_email, q.question, q.id),
                  'consortium-gms@cternus.net', ["consortium-gms@mit.edu"])
        messages.success(request, "Question asked! You'll receive an answer as soon as possible.")
    questions = Question.objects.filter(public=True).exclude(answer='').order_by('-answered_on')
    return render(request, template, {'questions': questions})

@login_required()
def gm_view(request, template='askgms/askgms.html'):
    if not request.user.is_superuser: raise Http404
    if request.method == 'POST':
        email=request.POST.get('email', '')[0],
        q = get_object_or_404(Question, id=request.POST.get('qid', None))
        updated = q.answer != ''
        q.answer = request.POST.get('answer')
        q.answered_by = request.POST.get('answered_by')
        q.answered_on = now()
        q.public = request.POST.get('public', False)
        q.save()
        verb = "updated" if updated else "answered"
        send_mail('[Consortium] Question #%s from %s %s by %s' % (q.id, q.asker_email, verb, q.answered_by),
                  "%s %s %s's question: \n\n'%s'\n---\n%s" % (q.answered_by, verb, q.asker_email, q.question, q.answer),
                  'consortium-gms@cternus.net', ["consortium-gms@mit.edu", q.asker_email])
        messages.success(request, "Question %s!" % verb)
    questions = Question.objects.all().order_by('-id')
    return render(request, template, {'questions': questions})
