##imports
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .forms import SnippetForm
from django.views.decorators.csrf import csrf_exempt
import os, subprocess

## Documentation for class node
# Class node represents a node in the tree structure of code_directory.
# Variable stat distinguishes between file and folder.
class node():
    def __init__(self,name,stat):
        self.name = name
        self.stat = stat
        self.child = []
        self.path= name

    ## adding files as children to the parent folder
    def add_child(self,child_node):
        self.child.append(child_node)
        child_node.path = self.path+"/"+child_node.path

top = node('c_directory','dir')

## This function builds the whole directory structure in a bredth-first search manner where we iterate through the tree of directory with each file
#representing a leaf in the graph.
def builder(top):
    curr = list(os.popen('ls'))

    for i in range(len(curr)):
        curr[i]= curr[i].strip()
        dir_check = os.path.isdir(curr[i])
        if(dir_check):
            new_dir=node(curr[i],'dir')
            os.chdir(curr[i])
            builder(new_dir)
            os.chdir('..')
            top.add_child(new_dir)
        else:
            new_file=node(curr[i],'file')
            top.add_child(new_file)

##This function registers the details of a new user in the database via a POST request.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

## This Function lets the user update its personal information including username and profile picture.
@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)

##This function is called when the user clicks on the editor option. This function is for the compilation and running of temporary files in C++ only.
#The save functionality does not work here and the code is deleted after the user exits the site.
@login_required
@csrf_exempt
def simple(request):
    output = ""
    input_data = ""
    initial_val = ""
    if request.method == 'POST':
        form = SnippetForm(request.POST)

        if form.is_valid():
            newcode = request.POST['text']
            button = request.POST.get('pressed', False)
            input_data = request.POST['input']
            initial_val = newcode

            if(button == "Compile and run"):
                os.chdir("./CodeFiles")

                os.popen("touch test.cpp")
                f = open("test.cpp", 'w')
                f.write(newcode)
                f.close()

                p1 = subprocess.run(['g++', 'test.cpp'], capture_output=True, text=True)

                if p1.returncode == 0:
                    p2 = subprocess.run(['./a.out'], capture_output=True, text=True, input=input_data)

                    if p2.returncode == 0:
                        output = p2.stdout
                    else:
                        output = "Some error in code :("
                else:
                    output = "Compilation Error :("

                os.chdir("..")

        return render(request, "snippets.html", {
        "form": form,
        "initial_val": initial_val,
        "lang": "c_cpp",
        "output": output,
        "inp_Data": input_data,
        })

    else:
        form = SnippetForm()
    return render(request, "snippets.html", {
        "form": form,
        "initial_val": "",
        "lang": "c_cpp",
        "output": "",
        "inp_Data": "",
    })

##This function is called when the user clicks on file in the tree structure of the directory. It then redirects to the editor with the respective
#code file opened. Here, the user has both options of saving and running the code. This function supports the execution of programs in Java,C++ and Python.
@login_required
@csrf_exempt
def codeviewer(request, filepath):

    file_path = "./CodeFiles/"+filepath

    initial_dir = os.getcwd()
    i = len(file_path)-1
    while i >= 0:
        if(file_path[i] == '/'):
            break
        i = i-1

    parent_dir = file_path[:i]
    file_name = file_path[i+1:]
 
    f = open(file_path, 'r')
    initial_val = f.read()

    print(initial_val)
    f.close()
    i = len(file_path)-1
    while i >= 0:
        if(file_path[i] == '.'):
            break
        i = i - 1
    lang = file_path[i+1:]
    if(lang == "cpp"):
        lang = "c_cpp"
    elif lang == "py":
        lang = "python"
    elif lang == "java":
        lang = "java"
    else:
        lang = "text"

    print(lang)

    output = "Run the code First"
    input_data = "enter you input here"

    if request.method == 'POST':
        form = SnippetForm(request.POST)
    
        if form.is_valid():
            newcode = request.POST['text']
            button = request.POST.get('pressed', False)
            input_data = request.POST['input']

            if(button == "Save"):
                f = open(file_path, 'w')
                f.write(newcode)
                f.close()
                f = open(file_path, 'r')
                initial_val = f.read()
                f.close()

            else:
                os.chdir(parent_dir)

                if lang == "c_cpp":
                    p1 = subprocess.run(['g++', file_name], capture_output=True, text=True)

                    if p1.returncode == 0:
                        p2 = subprocess.run(['./a.out'], capture_output=True, text=True, input=input_data)

                        if p2.returncode == 0:
                            output = p2.stdout
                        else:
                            output = "Some error in code :("
                    else:
                        output = "Compilation Error :("
                    
                    p3 = subprocess.run(['rm', 'a.out'])
                    if p3.returncode == 0:
                        print("file delete successfull")
                    else:
                        print(p3.stderr)

                elif lang == "python":
                    p1 = subprocess.run(['python3', file_name], capture_output=True, text=True, input=input_data)

                    if p1.returncode == 0:
                        output = p1.stdout
                    else:
                        output = "there is some error in the code"
                elif lang == "java":
                    p1 = subprocess.run(['javac', file_name], capture_output=True, text=True)

                    if p1.returncode == 0:
                        p2 = subprocess.run(['java', file_name[:-5]], capture_output=True, text=True, input=input_data)
                        if p2.returncode == 0:
                            output = p2.stdout
                        else:
                            output = "Some error in code :("
                    else:
                        output = "Compilation Error :("

                    p3 = subprocess.run(['rm', file_name[:-5]+".class"])

                os.chdir(initial_dir)

        f = open(file_path, 'r')
        initial_val = f.read()
        f.close()

        return render(request, "snippets.html", {
        "form": form,
        "initial_val": initial_val,
        "lang": lang,
        "output": output,
        "inp_Data": input_data,
        })

    else:
        form = SnippetForm()
    return render(request, "snippets.html", {
        "form": form,
        "initial_val": initial_val,
        "lang": lang,
        "output": output,
        "inp_Data": input_data,
    })
