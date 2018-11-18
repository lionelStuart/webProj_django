from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from .forms import CommentForm
from .models import Post


def post_list(request, tag_slug=None):
    # published?
    obj_list = Post.published.all()
    tag = None

    # if tag_slug:
    # tag = get_object_or_404(Tag)

    paginator = Paginator(obj_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # page start from 1
        posts = paginator.page(1)
    except EmptyPage:
        # last page
        posts = paginator.page(paginator.num_pages)
        # render with param:page/posts
    return render(request, 'blog/post/list.html', {
        'page': page,
        'posts': posts
    })


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # post comments
    comments = post.comments.filter(active=True)

    # new comments
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            print("send new comment")
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form, })
