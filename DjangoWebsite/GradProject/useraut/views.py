from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from json import loads

from .scripts import CompareAll,Predict
from .models import Data
from .forms import CreateUserForm
# Create your views here.



def useraut(request):

	data = Data.objects.all()
	context = {'data':data}
	return render(request, 'useraut/useraut.html', context)


@login_required(login_url='login')
def userprofile(request):
	data = None

	if request.user.is_authenticated:
		data = Data.objects.filter(author=request.user.id)

	context = {'data':data}
	return render(request, 'useraut/userprofile.html', context)




@login_required(login_url='login')
def train(request):
	result = ''
	score  = ''
	predicted = ''
	if request.method == ('POST') and 'sessiondata' in request.POST:
		
		jsondata = request.POST.get('session')
		traindata = loads(jsondata)
		code = request.POST.get('code')
		result = CompareAll(code)
		data =  Data.objects.create(content = traindata,author= request.user,code = code) 
		data.save()
		



	if request.method == ('POST') and 'codes' in request.POST:
		try:
		#predicted = Oneclass(traindata)
			kernel = request.POST.get('kernel')
			code = request.POST.get('code2')
			result,score,model = CompareAll(code,kernel)
		except:
			context = {'result':result,'score':score}
			return render(request, 'useraut/train.html', context)

	if request.method == ('POST') and 'One-classCode' in request.POST:


		try:
			testdata = Data.objects.all()
			Oneclasscode = loads(request.POST.get('OneCode'))
			code 		 = request.POST.get('code3')
			kernel = 'rbf'
			username = request.POST.get('Username')

			result,score,model = CompareAll(code,kernel)

			predicted = model.predict(Oneclasscode)

			testsmt1,testsmt2,testsmt3,testsmt4,testsmt5 = Predict(username,code,Oneclasscode)
			testsmt5 = 'These are the other f2 scores of the models:'

			if username == predicted:
				predicted = 'model matched'
			else:
				predicted = 'Try Again'

			context = {'result':result,'score':score,'prediction':predicted,'smt1':testsmt1,'smt2':testsmt2,'smt3':testsmt3,'smt4':testsmt4,'smt5':testsmt5}
			return render(request, 'useraut/train.html', context)	
		except:
			predicted = 'opps'
			context = {'result':result,'score':score,'prediction':predicted,'smt1':'','smt2':'','smt3':'','smt4':'','smt5':''}
			return render(request, 'useraut/train.html', context)
	context = {'result':result,'score':score,'prediction':predicted,'smt1':'','smt2':'','smt3':'','smt4':'','smt5':''}	
	return render(request, 'useraut/train.html', context)	
	




def register(request):
	form = CreateUserForm()

	if request.method == ('POST'):
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('login')

	context = {'form':form}
	return render(request, 'useraut/register.html', context)

def loginpage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('userprofile')
		else:
			messages.info(request, 'account name or password is wrong')
	context = {}
	return render(request,'useraut/login.html',context)

def logoutuser(request):
	logout(request)
	return redirect('login')

