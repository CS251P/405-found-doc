from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .forms import CreateFileForm
import os


class node():
    def __init__(self,name,stat,path):
        self.name = name
        self.stat = stat
        self.child = []
        self.path= path
    def add_child(self,child_node):
        self.child.append(child_node)


def builder(top):
    curr = list(os.popen('ls'))

    for i in range(len(curr)):
        curr[i]= curr[i].strip()
        dir_check = os.path.isdir(curr[i])
        if(dir_check):
            new_dir=node(curr[i],'dir',top.path+"/"+curr[i])
            os.chdir(curr[i])
            builder(new_dir)
            os.chdir('..')
            top.add_child(new_dir)
        else:
            new_file=node(curr[i],'file',top.path+"/"+curr[i])
            top.add_child(new_file)


@login_required
def home(request):
	top = node('CodeFiles','dir','CodeFiles')
	os.chdir('CodeFiles')
	builder(top)
	os.chdir('..')
	user_index=0	
	for i in range(len(top.child)):
		if(top.child[i].name == str(request.user.id)):
			user_index = i
	contents = [top.child[user_index]]
	
	return render(request, 'blog/home.html', {'contents':contents,'user_id':request.user.id})



def detail(request):
	return render(request)	

@login_required
def create(request,folderpath):
	if request.method == 'POST':
		form = CreateFileForm(request.POST)
		
		if form.is_valid():
			form.save()

			title = form.cleaned_data.get('title')
			os.popen('touch %s/%s',(folderpath,title))
			return redirect('blog-home')
		
	else:
		form = CreateFileForm()
	
	return render(request, 'blog/create.html', {'form': form})



@login_required
def folderview(request,folderpath):
	print(folderpath)
	if request.method == 'POST':
		button = request.POST.get('pressed',False)
		if(button == "Create File"):
			return redirect("/create/"+folderpath+"!")
		elif( button == "Create Folder"):
			return redirect("/create/"+folderpath+"@")
		elif( button == "Delete Folder"):
			return redirect("/create/"+folderpath+"^")
	return render(request,'blog/folderview.html')



@login_required
def create_file_in_folder(request,folderpath):
	option = folderpath[len(folderpath)-1]
	print(option)
	if(option=='^' or option=='*'):
		os.popen('rm -rf '+folderpath[:len(folderpath)-1])
		return redirect('blog-home')
	
		
	if request.method =='POST':
		
		if(option =='!'):
			filename = request.POST.get('filename',False)
			os.popen('touch %s/%s' %(folderpath[:len(folderpath)-1],filename))
			prev_url = '/folderview/'+folderpath[:len(folderpath)-1]
			return redirect('blog-home')

		elif(option =='@'):
			foldername= folderpath[:len(folderpath)-1]+"/"+request.POST.get('filename',False)
			os.popen('mkdir %s' %foldername)
			return redirect('blog-home')	
	return render(request,'blog/create_file_in_folder.html')


def about(request):
	return render(request, 'blog/about.html',{'title': 'About'})
