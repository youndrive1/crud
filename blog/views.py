from django.shortcuts import render, redirect, get_object_or_404 #import redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm # forms.py에서 PostForm 가져오기 


def detail(request, pk): # request와 pk도 인자로 받음
    post = get_object_or_404(Post, pk=pk) # 해당 객체가 있으면 가져오고 없으면 404에러, pk로 pk 사용
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        comment_form.instance.blog_id = pk
        if comment_form.is_valid():
            comment = comment_form.save()
    comment_form = CommentForm()
    comments = post.comments.all()
    return render(request, 'detail.html', {'blog': post, 'comments':
    comments, 'comment_form': comment_form})

def main(request):
    posts = Post.objects # Post.objects를 posts 변수에 담기
    return render(request, 'posts.html', {'posts':posts}) # 인자 3개: request, template, context

def create(request):
    if request.method == 'POST': # POST vs. GET 분기
        form = PostForm(request.POST) # form 변수에 PostForm 할당
        if form.is_valid(): # form 유효성 검증
            form.save() #저장하고
            return redirect('main') # main페이지로 가기
    else:
        form = PostForm() # 빈 form 열기
    return render(request, 'create.html', {'form':form})

def update(request, pk):
    post = get_object_or_404(Post, pk=pk) #있으면 가져오고 없으면 404에러
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post) # post 객체 가져와서 form 생성
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = PostForm(instance=post) # post 객체 가져와서 form 생성
    return render(request, 'update.html', {'form':form})

def delete(request,pk):
    post = Post.objects.get(pk=pk)
    post.delete() # delete함수 실행
    return redirect('main')

def comment_update(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Post, pk=comment.blog.id)

    if request.method =='POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('/detail/'+str(blog.id))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment_update.html', {'form':form})
    
def comment_delete(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    blog = get_object_or_404(Post, pk=comment.blog.id)

    if request.method == 'POST':
        comment.delete()
        return redirect('/detail/'+str(blog.id))
    else:
        return render(request, 'comment_delete.html', {'object': comment})
