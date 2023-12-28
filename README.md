# Cyber Security Base 2023 - Project I
The task for this project was to build a web application with at least five different security flaws from the [OWASP top ten list](https://owasp.org/www-project-top-ten/), including CSRF. For my project, I specifically used the 2021 version of this list.

### Run the project (on Windows):

The app is made using Python and Django. Therefore, to run the app, you should first follow the [installation guide]() used in this course to install all the required libraries and dependencies.

After doing that, open a command prompt and clone this repository by entering the following command:
```
git clone https://github.com/Dravde01/CSB-Project-1.git
```
Next, navigate to the directory where you cloned the repository. For example, if you saved it to your desktop, navigate to the upper project folder using:
```
cd C:\Users\[Your Username]\Desktop\csb_project_1
```
When you are here, run the following two commands one after another to make the necessary migrations:
```
python manage.py makemigrations
python manage.py migrate
```
Lastly, start the server by entering:
```
python manage.py runserver
```
Now, the website should be up and running on your localhost server found at http://127.0.0.1:8000/.

### Available users:

The web application has the following authenticated users to play around with:
| Username | Password | Staff/Superuser |
|:--------:|:--------:|:--------:|
| user | user | No |
| admin | admin | No |
| superuser | superuser | Yes |

Next up, I will locate each and every flaw in the code, describe them and provide fixes for them.

## Flaw 1: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
**Source links:**
- CSRF token: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/templates/polls/index.html#L27
- Exempt decorator: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L30
- SameSite cookies: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L128

**Description:**  
CSRF stands for *Cross-Site Request Forgery* and is a fundamental flaw that, fortunately, is not so common nowadays due to more secure web frameworks. It allows users to send unauthorized web requests to a website through another site where the user is authenticated. A common example is if someone opens a web browser and logs into a CSRF-vulnerable website with their credentials. If the user opens another tab with a site containing a malicious hidden request (e.g. through a form submission), and triggers the request, then this malicious request can be performed on the website where the user is already logged in. This way, personal data from the site where the user is logged in can be accessed and stolen by the attacker performing the request.

In my project, CSRF attacks are possible due to built-in CSRF protection (such as tokens) being disabled.

**Fix:**  
The fixes here are simple. First, go to the linked line in the index.html file and remove the comment around {% csrf_token %} to enable the protection. Next, in the views.py file, remove the decorator @csrf_exempt before the definition of "addquestion" to enable CSRF protection on that function. Lastly, delete the final row in settings.py reading "SESSION_COOKIE_SAMESITE = None" to set it back to default, enabling additional CSRF protection.

## Flaw 2: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
**Source links:**  
GET requests:
- https://github.com/Dravde01/CSB-Project-1/blob/master/polls/templates/polls/index.html#L26
- https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L32-L35

Login decorators:
1. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L17
2. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L22
3. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L32
4. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L47

**Description:**  
Broken Access Control encapsules everything regarding improper setup of user access control mechanisms. This often means that users have access to do things they should not be allowed to (e.g. viewing sensitive data or performing administrative actions), which inherently causes security concerns. However, other things like weak passwords and an overall weak authentication policy are also included under Broken Access Control. In web applications, data is sometimes stored in path variables which can be modified to give certain users access to that data.

In my application, users can vote in polls and view the results without being logged in to the website. Without logging in, they can also create new questions by opening a link like http://localhost:8000/addquestion?q=you&c1=have%20been&c2=hacked while the server is running. This will create a poll with the question as "you" and the choices "have been" and "hacked".

**Fix:**  
This problem can be fixed by switching the linked GET requests to POST requests instead, which will hide variable parameters in the URL. There are four lines that have to be changed in views.py and one line in index.html. Additionally, you should uncomment the decorator @login_required on the four definitions in views.py to make it so that a user has to log in to be able to access them.  
**Keep in mind!** POST requests require CSRF tokens to be activated. So for this to work properly, you also have to uncomment the CSRF token mentioned in Flaw 1.

## Flaw 3: []()
**Source links:**
- ...

**Description:**  
...

**Fix:**  
...

## Flaw 4: []()
**Source links:**
- ...

**Description:**  
...

**Fix:**  
...

## Flaw 5: []()
**Source links:**
- ...

**Description:**  
...

**Fix:**  
...
