from django.shortcuts import render
from Memo.models import Group
from Memo.models import Memo
from django.http import HttpResponseServerError, HttpResponse
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings


from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from Memo.serializers import (
    # NoteSerializer,
    # CreateUserSerializer,
    UserSerializer,
    LoginUserSerializer,
)
from knox.models import AuthToken


# https://velog.io/@killi8n/Dnote-5-1.-Django-%EA%B6%8C%ED%95%9C-%EC%84%A4%EC%A0%95-%EB%B0%8F-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85-%EA%B5%AC%ED%98%84-tmjmep5tcm
# https://behonestar.tistory.com/117


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        print(serializer)
        print(user)
        print('-------------------------')
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


@csrf_exempt
def sign_in(request):
    username = request.POST['username']
    password = request.POST['password']
    # print(username, password)
    user = authenticate(request, username=username, password=password)
    # print(user)
    if user is not None:
        # 인증 성공
        login(request, user)
        print(f'[Login request: "{user}" login success]')
        return HttpResponse("login")
    else:
        # 인증 실패
        print(f'[Login request: login failed..]')
        return HttpResponse("failed")


@login_required
@csrf_exempt
def sign_out(request):
    print(f'[Logout request: {request.user}]')
    logout(request)
    return HttpResponse("logout")


@login_required
def get_all_memo(request):
    user = request.user
    data = []
    print(user)
    
    try:
        for item in Memo.objects.filter(owner=user).order_by('-created_at'):
            data.append({
                'id': item.id,
                'index': item.index,
                'owner': item.owner,
                'group': item.group,
                'content': item.content,
                'created_at': str(item.created_at),
                'updated_at': str(item.updated_at),
                'isDo': item.isDo,
                'isStar': item.isStar,
                'targetDate': item.targetDate,
            })
    except:
        print("[Get request: All Memo] ERROR")
        return HttpResponseServerError()

    print("[Get request: All Memo]")
    data = json.dumps(data, indent=4)
    print(data)

    return HttpResponse(data, content_type="application/json")


@login_required
def get_all_group(request):
    user = request.user
    data = []
    
    try:
        for item in Group.objects.filter(owner=user).order_by('-created_at'):
            data.append({
                'id': item.id,
                'index': item.index,
                'owner': item.owner,
                'group_name': item.group,
            })
    except:
        print("[Get request: All Group] ERROR")
        return HttpResponseServerError()

    print("[Get request: All Group]")
    data = json.dumps(data, indent=4)
    print(data)

    return HttpResponse(data, content_type="application/json")


@login_required
def get_memo_by_group_id(request, group_id):
    user = request.user
    # memo = get_object_or_404(Memo, group=group_id) 이 방식 괜찮은지 후에 검토
    data = []

    if not group:
        return HttpResponse(status=400)

    try:
        for item in Memo.objects.filter(Q(user=user) & Q(group=group_id)).order_by('-created_at'):
            data.append({
                'id': item.id,
                'index': item.index,
                'owner': item.owner,
                'group': item.group,
                'content': item.content,
                'created_at': str(item.created_at),
                'updated_at': str(item.updated_at),
                'isDo': item.isDo,
                'isStar': item.isStar,
                'targetDate': item.targetDate,
            })
    except:
        print("[Get request: Memo by Group ID] ERROR")
        return HttpResponseServerError()

    print("[Get request: Memo by Group ID]")
    data = json.dumps(data, indent=4)
    print(data)

    return HttpResponse(data, content_type="application/json")


@login_required
@csrf_exempt
def add_memo(request):
    user = request.user
    memo = json.loads(request.POST['memo'])
    print(json.dumps(memo, indent=4), type(memo))

    # group = memo.get('group') if memo.get('group') is not None else ''
    group = None
    content = memo.get('content') if memo.get('content') is not None else ''
    isDo = memo.get('isDo') if memo.get('isDo') is not None else False
    isStar = memo.get('isStar') if memo.get('isStar') is not None else False
    targetDate = memo.get('targetDate') if memo.get('targetDate') is not None else None

    print(group, content, isDo, isStar, targetDate)

    last_memo_index_obj = Memo.objects.aggregate(
        index=Max('index')).get('index')
    last_memo_index = last_memo_index_obj + 1 if last_memo_index_obj is not None else 0
    print(last_memo_index)
    try:
        memo_obj = Memo(index=last_memo_index, owner=user, group=group, content=content,
                        isDo=isDo, isStar=isStar, targetDate=targetDate)
        # memo_obj.save()
    except:
        print("[Add request: Memo] ERROR")
        return HttpResponseServerError()
    return HttpResponse(status=200)


@login_required
def update_memo_index(request):
    user = request.user
    memo = json.loads(request.POST['memo'])
    print(json.dumps(memo, indent=4), type(memo))

    if memo.get('index') is None:
        return HttpResponseServerError()

    memo_id = memo.get('id')
    index = memo.get('index')

    try:
        memo_obj = Memo.objects.get(id=memo_id)
    except Photo.DoesNotExist:
        print(
            "[Update request: Index of Memo] Failed!!! No Memo matches the given query.")
        return HttpResponseServerError()

    # filter(Q(<condition_1>)|Q(<condition_2>))

    if memo_obj.index < index:
        # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--
        between_memo_set = Memo.objects.filter(
            Q(id > memo_obj.index) & Q(id <= index))
        for between_memo in between_memo_set:
            between_memo.index = between_memo.index - 1
            between_memo.save()
    elif memo_obj.index > index:
        # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
        between_memo_set = Memo.objects.filter(
            Q(id < memo_obj.index) & Q(id >= index))
        for between_memo in between_memo_set:
            between_memo.index = between_memo.index + 1
            between_memo.save()

    memo_obj.index = index
    memo_obj.save()

    return HttpResponse(status=200)


@login_required
def update_memo(request):
    user = request.user
    memo = json.loads(request.POST['memo'])
    print(json.dumps(memo, indent=4), type(memo))

    memo_id = memo.get('id')
    group = memo.get('group') if memo.get('group') is not None else ''
    content = memo.get('content') if memo.get('content') is not None else ''
    isDo = memo.get('isDo') if memo.get('isDo') is not None else False
    isStar = memo.get('isStar') if memo.get('isStar') is not None else False
    targetDate = memo.get('targetDate') if memo.get('targetDate') is not None else None

    print(group, content, isDo, isStar, targetDate)

    try:
        memo_obj = Memo.objects.get(id=memo_id)
    except Photo.DoesNotExist:
        print("[Update request: Memo] Failed!!! No Memo matches the given query.")
        return HttpResponseServerError()

    # filter(Q(<condition_1>)|Q(<condition_2>))

    # if memo.index is not None:
    #     if memo_obj.index < memo.index:
    #         # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--
    #         between_memo_set = Memo.objects.filter(
    #             Q(id > memo_obj.index) & Q(id <= memo.index))
    #         for between_memo in between_memo_set:
    #             between_memo.index = between_memo.index - 1
    #         between_memo.save()
    #     elif memo_obj.index > memo.index:
    #         # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
    #         between_memo_set = Memo.objects.filter(
    #             Q(id < memo_obj.index) & Q(id >= memo.index))
    #         for between_memo in between_memo_set:
    #             between_memo.index = between_memo.index + 1
    #         between_memo.save()
    #     memo_obj.index = memo.index

    memo_obj.group = group
    memo_obj.content = content
    memo_obj.isDo = isDo
    memo_obj.isStar = isStar
    memo_obj.targetDate = targetDate

    memo_obj.save()
    return HttpResponse(status=200)


@login_required
def delete_memo(request):
    user = request.user
    memo_id = request.POST['memo_id']

    try:
        memo_obj = Memo.objects.get(id=memo_id)
    except Photo.DoesNotExist:
        print("[Delete request: Memo] Failed!!! No Memo matches the given query.")
        return HttpResponseServerError()


    # 삭제 시 삭제할 항목의 뒷번호들의 index--
    between_memo_set = Group.objects.filter(Q(index > memo_obj.index))
    for between_memo in between_memo_set:
        between_memo.index = between_memo.index - 1
        between_memo.save()
        
    memo_obj.delete()

    return HttpResponse(status=200)


@login_required
def add_group(request):
    user = request.user
    group_name = request.POST['group_name']

    last_group_index = Group.objects.aggregate(
        index=Max('index'))['index'] + 1 or 0

    try:
        group_obj = Group(index=last_group_index,
                          owner=user, group_name=group_name)
        group_obj.save()
    except:
        print("[Add request: Group] ERROR")
        return HttpResponseServerError()
    return HttpResponse(status=200)


@login_required
def update_group_index(request):
    user = request.user
    group_index = request.POST['group_index']

    try:
        group_obj = Group.objects.get(id=group.id)
    except Photo.DoesNotExist:
        print(
            "[Update request: Index of Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    # filter(Q(<condition_1>)|Q(<condition_2>))

    if group_obj.index < group_index:
        # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--
        between_group_set = Group.objects.filter(
            Q(id > group_obj.index) & Q(id <= group_index))
        for between_group in between_group_set:
            between_group.index = between_group.index - 1
            between_group.save()
    elif group_obj.index > group_index:
        # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
        between_group_set = Group.objects.filter(
            Q(id < group_obj.index) & Q(id >= group_index))
        for between_group in between_group_set:
            between_group.index = between_group.index + 1
            between_group.save()

    group_obj.index = group_index
    group_obj.save()

    return HttpResponse(status=200)


@login_required
def update_group(request):
    user = request.user
    group = json.loads(request.POST['group'])
    print(json.dumps(group, indent=4), type(group))

    group_id = group.get('id')
    group_name = group.get('name')

    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        print("[Update request: Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    group_obj.group_name = group_name

    group_obj.save()
    return HttpResponse(status=200)


@login_required
def delete_group(request):
    user = request.user
    group_id = request.POST['group_id']

    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        print("[Delete request: Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    # 삭제 시 삭제할 항목의 뒷번호들의 index--  
    between_group_set = Group.objects.filter(Q(index > group_obj.index))
    for between_group in between_group_set:
        between_group.index = between_group.index - 1
        between_group.save()

    group_obj.delete()

    return HttpResponse(status=200)
