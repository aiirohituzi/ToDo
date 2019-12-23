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
