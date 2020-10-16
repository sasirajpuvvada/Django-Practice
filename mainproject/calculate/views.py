from django.shortcuts import render, HttpResponse
from  calculate import views
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
@csrf_exempt
def index(request):
    ans = 0
    try:
        if request.method == 'POST':
            number1 = int(request.POST.get('number1'))
            number2 = int(request.POST.get('number2'))
            operation = request.POST.get('operation')

        if operation == 'sum':
            ans = number1 + number2
        elif operation == 'sub':
            ans = number1 - number2
        elif operation == 'product':
            ans = number1 * number2
        elif operation == 'divison':
            ans = number1 / number2
        else:
            return HttpResponse('Invalid Operation')
    
    except ValueError:
        return HttpResponse('value error!!!!')
    
    except ArithmeticError:
        return HttpResponse('Arithmatic error!!!!')
    except Exception as e:
        return HttpResponse(e)

    data = {
        "num1": number1,
        "num2": number2,
        "operation": operation,
        "answer": ans,
    }

    return JsonResponse(data)