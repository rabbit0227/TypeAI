# TypeAI
## Setup:

This documentaion is for the setup to start making the project.

### Steps to Set Up the Project

#### 1 - Make sure `python` and `git` are installed on your machine

#### 2 - Clone the repo 
Using the link from the **code** slide-down in the github page.

```bash
git clone https://github.com/rabbit0227/TypeAI.git
```
#### 3 - Move to the project folder
Make sure to be in the `TypeAI` folder.
```bash
cd TypeAI
```
---


#### 3.5 - Additional optional step for testing branches code

- Check the remote branches and break the loop with `Q`
```bash
git branch -a
```
- You can use `checkout` to switch to the remote branch of your choice to test code
```bash
git checkout remotes/origin/md-branch
```

- You can use `checkout` to switch to the a branch that exists on the repo for your development
```bash
git checkout md-branch
```

- You can use `checkout -b` to make and switch to the a new branch that doesn't exist on the repo for your development, afterwards 
```bash
git checkout -b new-branch-name
git push -u origin new-branch-name
```

---
#### 4 - Create a Virtual Environment
Create a virtual environment for the project. And then activate it.
```bash
python -m venv env
```
on Windows
```bash
./env/Scripts/activate
```
on Linux/Mac
```bash
source venv/bin/activate 
```

#### 5 - Install requirments

```bash
pip install django
```
save requirments
```bash
pip freeze > req.txt
```

#### 6 - Start the django project

You can make the project in the same directory
```bash
django-admin startproject myproject .
```

Or you can make the project in a directory named `myproject`, for clean struction we can use this one
```bash
django-admin startproject myproject
```

#### 7 - Run the current Django project and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

```bash
python myproject/manage.py runserver
```
#### 8 - Now you can visit:
- Django admin page [Link](http://127.0.0.1:8000/admin/)

## Check [Step1.md](Step1.md) for to start the project if the django project is already made.

## Check [Step2.md](Step2.md) for details on how to use the framework for development.