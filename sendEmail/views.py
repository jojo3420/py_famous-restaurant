import traceback

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from shareRes.models import Restaurant


# Create your views here.


def read_file(file_path):
    with open(file_path) as stream:
        lines = stream.readlines()
        if len(lines) == 2:
            return lines[0].strip(), lines[1].strip()


def send(request):
    restaurants = []
    query_dict = QueryDict(request.body)
    try:
        receivers = query_dict['receivers'].split(',')
        from_email, _pwd = read_file('.env')
        for restaurant_id in query_dict['checked_restaurants']:
            restaurants.append(Restaurant.objects.get(id=restaurant_id))
        data = {
            'restaurants': restaurants,
            'content': query_dict['content'],
        }
        html_str = render_to_string('sendEmail/email_format.html', data)
        email_message = EmailMessage(subject=query_dict['title'], body=html_str, from_email=from_email, bcc=receivers)
        email_message.content_subtype = 'html'  # content_subtype 설정하지 않으면 메일 확인시 html 인식X 문자열로 인식함!
        email_message.send()
        return render(request, 'sendEmail/success.html')
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return render(request, 'sendEmail/failed.html')