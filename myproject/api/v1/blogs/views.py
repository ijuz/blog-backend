from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User


from blogApp.models import UserProfile,Posts,Comment,Category
from .serializers import PostSerializers,DetailPost,CreatePost,CommentSerializer,UserSerializer

@api_view(["GET"])
@permission_classes([AllowAny])
def blog_list(request):
    queryset = Posts.objects.filter(is_deleted=False, is_draft=False)
    
    # Filter by category ID
    category_id = request.query_params.get('category_id')
    if category_id:
        queryset = queryset.filter(categories__id=category_id)
    
    # Filter by author name
    author_id = request.query_params.get('author_id')
    if author_id:
        queryset = queryset.filter(author__id=author_id)

    context = {"request": request}
    serializer = PostSerializers(instance=queryset, many=True, context=context)
    response_data = {
        "status": 6000,
        "message": "success",
        "data": serializer.data
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrive_blog(request,pk):
    if Posts.objects.filter(pk=pk).exists():
        instance=Posts.objects.get(pk=pk)
        context={
            "request":request
        }
        serializer=DetailPost(instance=instance,context=context)
        response_data={
            "status":6000,
            "message":"success",
            "data":serializer.data
        }
        return Response(response_data)
    else:
        context={
            "status":6001,
            'data':serializer.errors
        }
        return Response(response_data)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create(request):
    serilizer=CreatePost(data=request.data)
    if serilizer.is_valid():
        user_profile, created=UserProfile.objects.get_or_create(user=request.user)
        serilizer.save(author=user_profile)
       
        Response_data={
            "status":6000,
            "message":"success",
        }
        return Response(Response_data)
    else:
        Response_data={
            "status":6001,
            "message":"validation error",
            "errors":serilizer.errors
        }
        return Response(Response_data)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_blog(request, pk):
    # Using get_object_or_404 to simplify object retrieval and 404 handling
    instance = get_object_or_404(Posts, pk=pk)
    
    serializer = DetailPost(instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            "status": 6000,
            "message": 'Successfully updated',
        }
        return Response(response_data)
    else:
        response_data = {
            "status": 6001,
            "message": "Not a valid",
            "errors": serializer.errors  # Corrected to serializer.errors
        }
        return Response(response_data, status=400)  # Indicate a client error
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_post(request):
    if Posts.objects.filter(author__user=request.user).exists():
        Post = Posts.objects.filter(author__user=request.user,is_deleted=False)
        context = {
            "request":request
        }
        serializer=DetailPost(instance=Post,many=True,context=context)
        response_data={
            "status":6000,
            "message":"success",
            "data":serializer.data
        }
    else:
        response_data={
            "status":6001,
            "message":"not a valid post",
            "data":[]
            
        }
    return Response(response_data)

@api_view(['GET'])
def Search_Post(request):
    query = request.query_params.get('query','')
    post = Posts.objects.filter(Q(title__icontains=query))
    context = {
        'request':request
    }
    serializer=PostSerializers(instance=post,many=True,context=context)
    response_data = {
        'data':serializer.data,

    }
    return Response(response_data)

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def likes(request, pk):
    instance = Posts.objects.filter(pk=pk).first()
    if instance is not None:
        context = {
            "request":request
        }
        if instance.likes.filter(username=request.user.username).exists():
            DetailPost(instance=instance,context=context)
            instance.likes.remove(request.user)
            message = "Likes Removed"
        else:
            instance.likes.add(request.user)
            message = "Liked"

        response_data = {
            "status": 6000,
            "message": message
        }
        return Response(response_data)
    else:
        response_data = {
            'status': 6001,
            "message": "Post not found"
        }
        return Response(response_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_posts(request,pk):
    instance = Posts.objects.filter(pk=pk).first()
    context = {
        "request":request
    }
    if instance is not None:
        if instance.save_post.filter(username=request.user.username).exists():
            DetailPost(instance=instance,many=True,context=context)
            instance.save_post.remove(request.user)
            response_data={
                'status':6000,
                'message':"removed"
            }
        else:
            instance.save_post.add(request.user)
            response_data ={
                "status":6000,
                "message":"added"
            }
        return Response(response_data)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def saved_posts(request):
    # Fetching posts that are marked as saved by the logged-in user
    posts = Posts.objects.filter(save_post=request.user)

    # Check if any posts are found
    if posts.exists():
        context = {'request': request}
        serializer = PostSerializers(instance=posts,many=True,context=context)
        return Response({
            'status': 200,  # HTTP 200 OK
            'data': serializer.data
        })
    else:
        return Response({
            'status': 404,  # HTTP 404 Not Found
            'message': 'No saved posts found.'
        })
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    serializer = CommentSerializer(data=request.data, context={'request': request,})
    
    if serializer.is_valid():
        # Save the comment instance through serializer.save() by passing additional arguments
        serializer.save(user=request.user, blog=post)
        
        response_data = {
            "status": 6000,
            "data": serializer.data  # Return the serialized data of the newly created comment
        }
        return Response(response_data, status=201)
    else:
        response_data = {
            "status": 6001,
            "errors": serializer.errors
        }
        return Response(response_data, status=400)
    

@api_view(["GET"])
@permission_classes([AllowAny])
def view_comments(request,pk):
    if Posts.objects.filter(pk=pk).exists():
        post = Posts.objects.get(pk=pk)
        comment = Comment.objects.filter(blog=post)
        context = {
            "request":request
        }
        serializer = CommentSerializer(instance=comment,context=context,many=True)
    
        response_data={
            "status":6000,
            "data":serializer.data,
        }
       
    else:
        response_data={
            "status":6001,
            "message":"Place not found"
        }
    return Response(response_data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if UserProfile.objects.filter(user=request.user).exists():
        Profile = UserProfile.objects.get(user=request.user)
        context={
            "request":request
        }
        serializer = UserSerializer(instance=Profile,context=context)
        response_data={
            "status":6000,
            "data":serializer.data
        }
        return Response(response_data)
    else:
        response_data={
            "status":6001,
            "message":"user not found"
        }
        return Response(response_data)


