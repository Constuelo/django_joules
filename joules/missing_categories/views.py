from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import SubmitButtonWidget
from .EmptyTrackingMegaMenu import run_script
from multiprocessing import Process, Pool

live = [['https://www.joules.com'], ['https://www.joulesusa.com'], ['https://www.tomjoule.de']]
staging = [['https://uk-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://us-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/'], ['https://de-staging.prod.joules.joules-prod01.aws.eclipsegroup.co.uk/']]
uk, us, de = [], [], []
lst = {}

def main(request):
    if request.method == 'POST':
        if 'live' in request.POST.get('env'):
            return JsonResponse(run_environment(live))

        if 'staging' in request.POST.get('env'):
            return JsonResponse(run_environment(staging))

    else:
        form = SubmitButtonWidget()

    return render(request, 'missing_categories/content.html', {'form': form})

def run_environment(env):
    with Pool(processes=3) as pool:
        p1 = pool.apply_async(run_script, (env[0], ))
        p2 = pool.apply_async(run_script, (env[1], ))
        p3 = pool.apply_async(run_script, (env[2], ))

        lst['uk'] = p1.get()
        lst['us'] = p2.get()
        lst['de'] = p3.get()

        return lst