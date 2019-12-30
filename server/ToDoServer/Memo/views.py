from django.shortcuts import render
from Memo.models import Group
from Memo.models import Memo
from django.http import HttpResponseServerError

# Create your views here.


def get_all_memo(request):
    data = []
    user = request.Get.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
    try:
        for item in Memo.objects.filter(owner=user).order_by('-created_at'):
            data.append({
                'id': item.id,
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
    user = request.Get.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
    try:
        for item in Group.objects.filter(owner=user).order_by('-created_at'):
            data.append({
                'id': item.id,
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
    user = request.Get.get('user', None)
    # user에 대한 자세한 값은 후에 인증기능 추가 후 알맞게 수정
    # 임시로 모양만 구현
    # group 이름을 받든 id를 받든 역시 추후 수정 필요

    if not group:
        return HttpResponse(status=400)

    try:
        for item in Memo.objects.filter(Q(user=user) & Q(group=group_id)).order_by('-created_at'):
            data.append({
                'id': item.id,
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


def add_memo(request):
    user = request.POST['user']
    memo = request.POST['memo']
    # memo 안에 JSON 오브젝트 형태로 담을 예정
    # String으로 값이 넘어올 수 있음, 확인 후 변환작업 필요

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        memo_obj = Memo(owner=user, group=memo.group, content=memo.content,
                        isDo=memo.isDo, isStar=memo.isStar, targetDate=memo.targetDate)
        memo_obj.save()
    except:
        print("[Add request: Memo] ERROR")
        return HttpResponseServerError()
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
    return HttpResponse(status=200)


def add_group(request):
    user = request.POST['user']
    group_name = request.POST['group_name']

    ########################
    # user 검증 코드 들어가야함 #
    # 아니면 데코레이터로 처리   #
    ########################

    try:
        group_obj = Group(owner=user, group_name=group_name)
        group_obj.save()
    except:
        print("[Add request: Group] ERROR")
        return HttpResponseServerError()
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
    return HttpResponse(status=200)
