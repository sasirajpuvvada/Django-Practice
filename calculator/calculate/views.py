from django.shortcuts import render, HttpResponse
from  calculate import views
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    ans = 0
    try:
        if request.method == 'POST':
            number1 = int(request.POST.get('number1'))
            number2 = int(request.POST.get('number2'))
            opeation = request.POST.get('operation')

        if opeation == 'sum':
            ans = number1 + number2
        elif opeation == 'sub':
            ans = number1 - number2
        elif opeation == 'product':
            ans = number1 * number2
        elif opeation == 'divison':
            ans = number1 / number2
        else:
            return HttpResponse('Invalid Operation')
    
    except ValueError:
        return HttpResponse('value error!!!!')
    
    except ArithmeticError:
        return HttpResponse('Arithmatic error!!!!')
    except Exception as e:
        return HttpResponse(e)

    return HttpResponse(ans)