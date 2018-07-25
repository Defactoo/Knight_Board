from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from .form import NewTopicForm
# Create your views here.

def home(request):
	# boards = Board.objects.all()
	# boards_names = list()

	# for board in boards:
	# 	boards_names.append(board.name)

	# response_html = '<br>'.join(boards_names)

	# return HttpResponse(response_html)
	boards = Board.objects.all()
	return render(request, 'home.html', {'boards': boards})

def board_topics(request,pk):
	board = get_object_or_404(Board, pk=pk)
	return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_date.get('message'),
                topic=topic,
                create_by=user
            )
            return redirect('board_topics', pk=board.pk)
    else:
        form = NewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})