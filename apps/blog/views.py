from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from apps.blog.forms import BlogForm
from apps.blog.models import Blog


# Create your views here.

def is_seller(user):
    return user.is_authenticated and user.role == 'seller'

@login_required
@user_passes_test(is_seller)
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')  # change to your blog list page name
    else:
        form = BlogForm()
    return render(request, 'blog/create_blog.html', {'form': form})

def blog_list(request):
    """View for listing all blogs - accessible to all users"""
    blogs = Blog.objects.all().order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,
        'search_query': search_query,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, blog_id):
    """View for individual blog detail - accessible to all users"""
    try:
        blog = Blog.objects.get(id=blog_id)
        context = {
            'blog': blog,
        }
        return render(request, 'blog/blog_detail.html', context)
    except Blog.DoesNotExist:
        return render(request, 'blog/blog_not_found.html', status=404)

# API Views
@csrf_exempt
@require_http_methods(["GET"])
def api_blog_list(request):
    """API endpoint to get all blogs"""
    try:
        blogs = Blog.objects.all().order_by('-created_at')
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            blogs = blogs.filter(
                Q(title__icontains=search_query) | 
                Q(content__icontains=search_query) |
                Q(author__username__icontains=search_query)
            )
        
        # Pagination
        page = request.GET.get('page', 1)
        per_page = request.GET.get('per_page', 10)
        
        paginator = Paginator(blogs, per_page)
        page_obj = paginator.get_page(page)
        
        blog_data = []
        for blog in page_obj:
            blog_data.append({
                'id': blog.id,
                'title': blog.title,
                'content': blog.content[:200] + '...' if len(blog.content) > 200 else blog.content,
                'image_url': blog.image.url if blog.image else None,
                'author': blog.author.username,
                'created_at': blog.created_at.isoformat(),
                'full_content': blog.content,
            })
        
        response_data = {
            'success': True,
            'blogs': blog_data,
            'pagination': {
                'current_page': page_obj.number,
                'total_pages': page_obj.paginator.num_pages,
                'total_blogs': page_obj.paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        }
        
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def api_blog_detail(request, blog_id):
    """API endpoint to get a specific blog"""
    try:
        blog = Blog.objects.get(id=blog_id)
        
        blog_data = {
            'id': blog.id,
            'title': blog.title,
            'content': blog.content,
            'image_url': blog.image.url if blog.image else None,
            'author': blog.author.username,
            'author_id': blog.author.id,
            'created_at': blog.created_at.isoformat(),
        }
        
        return JsonResponse({
            'success': True,
            'blog': blog_data
        })
    
    except Blog.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Blog not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)