from django.shortcuts import render
from Memo.models import Group
from Memo.models import Memo
from django.http import HttpResponseServerError, HttpResponse
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def get_all_memo(request):
    data = []
    user = request.GET.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
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


def get_all_group(request):
    data = []
    user = request.GET.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
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


def get_memo_by_group_id(request, group_id):
    # memo = get_object_or_404(Memo, group=group_id) 이 방식 괜찮은지 후에 검토
    data = []
    user = request.GET.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
    # group 이름을 받든 id를 받든 역시 추후 수정 필요

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


@csrf_exempt
def add_memo(request):
    req = request.POST['memo']
    print(req)
    print(type(req))
    # print(json.dumps(req, indent=4))
    print('------------------------------------------------------------')
    user = request.POST['user']
    memo = request.POST['memo']
    # memo 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    last_memo_index = Memo.objects.aggregate(
        index=Max('index'))['index'] + 1 or 0

    try:
        memo_obj = Memo(index=last_memo_index, owner=user, group=memo.group, content=memo.content,
                        isDo=memo.isDo, isStar=memo.isStar, targetDate=memo.targetDate)
        memo_obj.save()
    except:
        print("[Add request: Memo] ERROR")
        return HttpResponseServerError()
    return HttpResponse(status=200)


def update_memo_index(request):
    user = request.POST['user']
    memo = request.POST['memo']
    # memo 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        memo_obj = Memo.objects.get(id=memo.id)
    except Photo.DoesNotExist:
        print(
            "[Update request: Index of Memo] Failed!!! No Memo matches the given query.")
        return HttpResponseServerError()

    # filter(Q(<condition_1>)|Q(<condition_2>))

    if memo_obj.index < memo.index:
        # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--
        between_memo_set = Memo.objects.filter(
            Q(id > memo_obj.index) & Q(id <= memo.index))
        for between_memo in between_memo_set:
            between_memo.index = between_memo.index - 1
        between_memo.save()
    elif memo_obj.index > memo.index:
        # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
        between_memo_set = Memo.objects.filter(
            Q(id < memo_obj.index) & Q(id >= memo.index))
        for between_memo in between_memo_set:
            between_memo.index = between_memo.index + 1
        between_memo.save()

    memo_obj.index = memo.index
    memo_obj.save()

    return HttpResponse(status=200)


def update_memo(request):
    user = request.POST['user']
    memo = request.POST['memo']
    # memo 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        memo_obj = Memo.objects.get(id=memo.id)
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

    memo_obj.group = memo.group
    memo_obj.content = memo.content
    memo_obj.isDo = memo.isDo == 'True'
    memo_obj.isStar = memo.isStar == 'True'
    memo_obj.targetDate = memo.targetDate

    memo_obj.save()
    return HttpResponse(status=200)


def delete_memo(request):
    user = request.POST['user']
    memo_id = request.POST['memo_id']

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        memo_obj = Memo.objects.get(id=memo_id)
    except Photo.DoesNotExist:
        print("[Update request: Memo] Failed!!! No Memo matches the given query.")
        return HttpResponseServerError()

    memo_obj.delete()

    # 삭제 시 삭제할 항목의 뒷번호들의 index--

    return HttpResponse(status=200)


def add_group(request):
    user = request.POST['user']
    group_name = request.POST['group_name']

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

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


def update_group_index(request):
    user = request.POST['user']
    group = request.POST['group']
    # group 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        group_obj = Group.objects.get(id=group.id)
    except Photo.DoesNotExist:
        print(
            "[Update request: Index of Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    # filter(Q(<condition_1>)|Q(<condition_2>))

    if group_obj.index < group.index:
        # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--
        between_group_set = Group.objects.filter(
            Q(id > group_obj.index) & Q(id <= group.index))
        for between_group in between_group_set:
            between_group.index = between_group.index - 1
        between_group.save()
    elif group_obj.index > group.index:
        # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
        between_group_set = Group.objects.filter(
            Q(id < group_obj.index) & Q(id >= group.index))
        for between_group in between_group_set:
            between_group.index = between_group.index + 1
        between_group.save()

    group_obj.index = group.index
    group_obj.save()

    return HttpResponse(status=200)


def update_group(request):
    user = request.POST['user']
    group = request.POST['group']
    # group 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    # 수정작업 시 index 처리 경우의 수
    # 뒷번호에서 앞번호로 이동한 경우 : 앞번호를 포함한 두 번호 사이에 있는 모든 항목들의 index++
    # 앞번호에서 뒷번호로 이동한 경우 : 뒷번호를 포함한 두 번호 사이에 있는 모든 항목들의 index--

    try:
        group_obj = Group.objects.get(id=group.id)
    except Group.DoesNotExist:
        print("[Update request: Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    group_obj.group_name = group.group_name

    group_obj.save()
    return HttpResponse(status=200)


def delete_group(request):
    user = request.POST['user']
    group_id = request.POST['group_id']

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        group_obj = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        print("[Update request: Group] Failed!!! No Group matches the given query.")
        return HttpResponseServerError()

    group_obj.delete()

    # 삭제 시 삭제할 항목의 뒷번호들의 index--

    return HttpResponse(status=200)
