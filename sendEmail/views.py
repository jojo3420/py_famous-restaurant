import traceback

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.urls import reverse
from shareRes.models import Restaurant
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


# Create your views here.

def _read_email_info(file_path) -> tuple:
    with open(file_path) as stream:
        lines = stream.readlines()
        return lines[0].strip(), lines[1].strip()


def send_old(request):
    try:
        from_email, from_pwd = _read_email_info('.env')
        checked_restaurants = request.POST.getlist('checked_restaurants')
        if checked_restaurants:
            query_dict = QueryDict(request.body)
            text = f'<html><body>' \
                   f'<h2>맛집 공유</h2>' \
                   f'<p>발신자님께서 공유하신 맛집은 다음과 같습니다.</p>' \
                   f'<p>발신자 메시지: {query_dict["content"]}</p>'
            for restaurant_id in checked_restaurants:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                text += f'<p>맛집 링크: <a href="{restaurant.link}">{restaurant.name}</a></p>' \
                        f'<p>맛집 소개: {restaurant.content}</p>' \
                        f'<p>맛집 키워드: {restaurant.keyword}</p>' \
                        f'<div>---------------------</div>'
            text += f'</body></html>'
            # print(text)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(from_email, from_pwd)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = query_dict['title']
            msg['From'] = from_email
            msg['To'] = query_dict['receivers']
            html = MIMEText(text, 'html')
            msg.attach(html)
            assert isinstance(msg['To'], str) is True
            server.sendmail(from_email, query_dict['receivers'].split(','), msg.as_string())
            server.quit()
            return HttpResponseRedirect(reverse('index'))
    except Exception as e:
        print(str(e))
        return HttpResponse('예외발생: ' + str(e))


def send(request):
    try:
        from_email, from_pwd = _read_email_info('.env')
        checked_restaurants = request.POST.getlist('checked_restaurants')
        restaurants = []
        if checked_restaurants:
            query_dict = QueryDict(request.body)
            for restaurant_id in checked_restaurants:
                restaurants.append(Restaurant.objects.get(id=restaurant_id))
            data = {
                'content': query_dict['content'],
                'restaurants': restaurants
            }
            html_str = render_to_string('sendEmail/email_format.html', data)
            # print(html_str, type(html_str))
            receiver_list = query_dict['receivers'].split(',')
            email_message = EmailMessage(subject=query_dict['title'], body=html_str, from_email=from_email,
                                         bcc=receiver_list)
            email_message.content_subtype = 'html'
            email_message.send()
            return render(request, 'sendEmail/success.html')
    except Exception as e:
        print(str(e))
        traceback.print_exc()
        return render(request, 'sendEmail/failed.html')
