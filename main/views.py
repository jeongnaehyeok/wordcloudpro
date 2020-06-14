from django.shortcuts import render
from .API import wordcloud_maker

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

def main(request):
    return render(request, 'main.html')

def result(request):
    if request.method == "POST":
        requests = {'word_color':request.POST['word_color'],
                    'word_font':'./main/static/fonts/'+request.POST['word_font']+'.ttf',
                    'word_background':request.POST['word_background'],
                    'word_width':int(request.POST['word_width']),
                    'word_height':int(request.POST['word_height']),
                    'word_nuber':int(request.POST['word_nuber']),
                    'word_string': request.POST['word_string'],
                    }
        img = wordcloud_maker(requests)
        return render(request, 'result.html', {'img':img})
    else:
        return render(request, "main.html")

def describle(request):
    return render(request, 'describle.html')