import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("HD{Bu-pythonning-haqiqiy-g'alvasi!}")


def index_table(request):
    return render(request, 'table.html')


HONEYPOT_DIR = settings.HONEYPOT_DIR


def honeypot_view(request, path=''):
    """
    Honeypot papkalarini va fayllarni ko'rsatish.
    """
    # Foydalanuvchi kiritgan marshrutni to'g'rilash
    translated_path = os.path.normpath(os.path.join(HONEYPOT_DIR, path))

    # HONEYPOT_DIR'dan tashqariga chiqishni oldini olish
    if not translated_path.startswith(HONEYPOT_DIR):
        raise Http404("Noto'g'ri marshrut")

    # Agar fayl bo'lsa, o'qing va qaytaring
    if os.path.isfile(translated_path):
        try:
            with open(translated_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return HttpResponse(content, content_type="text/plain")
        except Exception as e:
            raise Http404(f"Faylni o'qishda xato: {e}")

    # Agar papka bo'lsa, ichidagi fayllar va papkalarni ro'yxatlang
    if os.path.isdir(translated_path):
        try:
            files = os.listdir(translated_path)
            response = f"<html><body><h2>HAADY security /skanerlash/{path}</h2><ul>"
            for file in files:
                file_path = os.path.join(path, file)
                response += f'<li><a href="/skanerlash/{file_path}">{file}</a></li>'
            response += "</ul></body></html>"
            return HttpResponse(response, content_type="text/html")
        except Exception as e:
            raise Http404(f"Papkani ko'rsatishda xato: {e}")

    # Agar hech narsa topilmasa, 404 qaytaring
    raise Http404("Fayl yoki papka topilmadi.")


@csrf_exempt
def basic_post(request):
    if request.method == "POST":
        data = request.POST
        if data.get("haady") == 'security':
            return HttpResponse('HD{Tezroq!-bu-flagni-darhol-kiriting!}')
        else:
            response = """<html><head><title>HAADY security</title>
                <style>
                    body {
                        background-color: black;
                        color: white;
                        font-family: Arial, sans-serif;
                        text-align: center;
                    }</style></head><body><h2>Noto'g'ri qiymat junatdingiz web sahifaga etibor bering</h2>"""
            return HttpResponse(response, status=400)
    response = """<html><head><title>HAADY security</title>
    <style>
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }</style></head><body><h2>Salom, men faqat POST ma\'lumotlarini qabul qiladigan veb-sahifaman. <br>"haady" parametriga har qanday POST ma\'lumotlarini yuboring.</h2>"""

    return HttpResponse(response)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if username == 'thobbes' and password == 'leviathan':
            return HttpResponse("HD{Bu-kinoyalar-endi-juda-nazariga-tushadigan-bo'lib-bormoqda}")
        else:
            return HttpResponse("Invalid username and/or password.", status=400)

    return render(request, 'login.html')


@csrf_exempt
def login_2(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        if username == 'rdescartes' and password == 'discourse#!@&%':
            return HttpResponse("HD{Men-bu-kinoyalarni-mukammal-deb-aks-etaman}")
        else:
            return HttpResponse("Invalid username and/or password.", status=400)

    return render(request, 'login.html')


@csrf_exempt
def login_3(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('email')
        password = data.get('color')
        if username == 'damian@example.com' and password == 'orange':
            return HttpResponse(f"Login successful. {username}")
        else:
            return HttpResponse("Invalid email and/or color.", status=400)


FLAG2 = "HD{Siz-bu-flagning-to'liq-matnini-topa-olasizmi-XYZ?}"
file_content = {}

for i in range(1, 50):
    file_content[f"{i}.html"] = FLAG2[i - 1]
file_content["50.html"] = FLAG2[49:]


def flag_view(request, page_name):
    # URL orqali kiritilgan nomni tekshiramiz
    if page_name in file_content:
        content = f"<html><body><h1>{file_content[page_name]}</h1></body></html>"
        return HttpResponse(content)
    else:
        return HttpResponse("<h1>404 Not Found</h1>", status=404)


FLAG3 = "HD{Xush-xabar...bu-juda-ta'sirli-javob}"


def index_flag(request):
    param = request.GET.get('index')
    if param and param.isdigit() and int(param) < len(FLAG3):
        content = f"<html><body><h1>{FLAG3[int(param)]}</h1></body></html>"
        return HttpResponse(content)
    else:
        return HttpResponse("<h1>404 Not Found</h1>", status=404)


FLAG_PARTS = [
    "HD{",  # 1-bo'lak
    "O'n-",  # 2-bo'lak
    "10-",  # 3-bo'lak
    "To'qqiz-",  # 4-bo'lak
    "9-",  # 5-bo'lak
    "Sakkiz-",  # 6-bo'lak
    "8-",  # 7-bo'lak
    "777-",  # 8-bo'lak
    "O'nBesh-",  # 9-bo'lak
    "15-To'rt-4-Uch-3-Ikki-Bir-1}"  # 10-bo'lak
]


def headers_view(request, page_number):
    # Sahifa raqamini tekshiramiz
    if page_number.isdigit() and 1 <= int(page_number) <= len(FLAG_PARTS):
        # Sahifa raqamini indeksga moslashtiramiz
        index = int(page_number) - 1  # List indekslari 0 dan boshlanadi
        response = HttpResponse(f"<h1>Sahifa {page_number}</h1>")
        response["Flag"] = FLAG_PARTS[index]  # "Flag" headerni qo'shamiz
        return response
    else:
        return HttpResponse("<h1>404 Not Found</h1>", status=404)


def about(request):
    employees = [
        {"first_name": "Alice", "email": "alice@example.com", "color": "blue"},
        {"first_name": "Bob", "email": "bob@example.com", "color": "green"},
        {"first_name": "Charlie", "email": "charlie@example.com", "color": "red"},
        {"first_name": "Zoe", "email": "zoe@example.com", "color": "purple"},
        {"first_name": "Damian", "email": "damian@example.com", "color": "orange"},
        {"first_name": "Eva", "email": "eva@example.com", "color": "pink"},
        {"first_name": "Frank", "email": "frank@example.com", "color": "yellow"},
        {"first_name": "Grace", "email": "grace@example.com", "color": "brown"},
        {"first_name": "Hannah", "email": "hannah@example.com", "color": "black"},
        {"first_name": "Ivan", "email": "ivan@example.com", "color": "grey"},
        {"first_name": "Jack", "email": "jack@example.com", "color": "white"},
        {"first_name": "Kathy", "email": "kathy@example.com", "color": "cyan"},
        {"first_name": "Liam", "email": "liam@example.com", "color": "magenta"},
        {"first_name": "Mia", "email": "mia@example.com", "color": "lime"},
        {"first_name": "Noah", "email": "noah@example.com", "color": "indigo"},
        {"first_name": "Olivia", "email": "olivia@example.com", "color": "violet"},
        {"first_name": "Paul", "email": "paul@example.com", "color": "fuchsia"},
        {"first_name": "Quinn", "email": "quinn@example.com", "color": "beige"},
        {"first_name": "Rachel", "email": "rachel@example.com", "color": "silver"},
        {"first_name": "Sam", "email": "sam@example.com", "color": "gold"},
        {"first_name": "Tina", "email": "tina@example.com", "color": "teal"},
        {"first_name": "Ursula", "email": "ursula@example.com", "color": "plum"},
        {"first_name": "Vera", "email": "vera@example.com", "color": "coral"},
        {"first_name": "Walter", "email": "walter@example.com", "color": "limegreen"},
        {"first_name": "Xander", "email": "xander@example.com", "color": "chocolate"},
        {"first_name": "Yara", "email": "yara@example.com", "color": "darkblue"},
        {"first_name": "Zane", "email": "zane@example.com", "color": "crimson"},
        {"first_name": "Amelia", "email": "amelia@example.com", "color": "seagreen"},
        {"first_name": "Benjamin", "email": "benjamin@example.com", "color": "goldenrod"},
        {"first_name": "Catherine", "email": "catherine@example.com", "color": "orchid"}
    ]

    return render(request, 'about.html', {'employees': employees})


def object_views(request):
    # Faylning to'liq yo'lini oling
    file_path = os.path.join(os.path.dirname(__file__), 'object')
    print(file_path)

    # Fayl mavjudligini tekshiring
    if not os.path.exists(file_path):
        return HttpResponseNotFound("Fayl topilmadi")

    # Faylni foydalanuvchiga yuboring
    return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='object')
