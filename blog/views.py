from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.core.paginator import Paginator
from django.utils import timezone
from .form import BlogPost
# Create your views here.
def home(request):
    blogs = Blog.objects 
    #모든 블로그 글들을 대상으로
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 3) #글 세개를 한페이지로 자르기
    page = request.GET.get('page') #request한 페이지를 알아내기
    posts = paginator.get_page(page) #해당 페이지가 posts에 담김
    return render(request, 'home.html', {'blogt':blogs, 'posts':posts})

def detail(request,blog_id):
    details = get_object_or_404(Blog,pk=blog_id)
    return render(request, 'detail.html', {'details':details})

def new(request): #n ew 띄워주는 함수
    return render(request,"new.html")

def create(request): #입력받은 내용을 데이터베이스에 넣어줌
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save() #쿼리셋 메소드 - 위에 내용을 데이터베이스에 저장해라
    #객체.delete도 있음
    return redirect('/blog/'+str(blog.id)) #blog.id 어디서 오는건지,,

def blogpost(request):
    #입력된 내용을 처리 -> POST
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    #빈 페이지를 띄워주는 기능 ->  GET방식
    else:
        form = BlogPost()
        return render(request,'new.html', {'form':form})