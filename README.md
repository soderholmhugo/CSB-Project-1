# Cyber Security Base 2023 - Project I
## Introduction
The task for this project was to build a web application with at least five different security flaws from the [OWASP top ten list](https://owasp.org/www-project-top-ten/), including CSRF. For my project, I specifically used the 2021 version of this list.  
The project is strongly backend-based, since the flaws are meant to be fundamental and the user can manipulate the frontend as much as they want to. 

### Run the project (on Windows):

The app is made using Python and Django templates (default SQLite database). Therefore, to run the app, you should first follow the [installation guide](https://cybersecuritybase.mooc.fi/installation-guide) used in this course to install all the required libraries and dependencies.

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
| admin | admin | No |
| superuser | superuser | Yes |

Next up, I will locate each and every flaw in the code, describe them and provide fixes for them.

## Flaw 1: [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
**Source links:**
- CSRF token: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/templates/polls/index.html#L27
- Exempt decorator: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L47
- SameSite cookies: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L133

**Description:**  
CSRF stands for Cross-Site Request Forgery and is a fundamental flaw that, fortunately, is not so common nowadays due to more secure web frameworks. It allows users to send unauthorized web requests to a website, through another site where the user is authenticated. A common example is if someone opens a web browser and logs into a CSRF-vulnerable website with their credentials. If the user opens another tab with a site containing a malicious hidden request (e.g. through a form submission), and triggers the request, then this malicious request can be performed on the website where the user is already logged in. This way, personal data from the site where the user is authenticated can be accessed and stolen by the attacker performing the request.

In my project, CSRF attacks are possible due to built-in CSRF protection (such as tokens) being disabled.

**Fix:**  
The fixes here are simple. First, go to the linked line in the *index.html* file and remove the comment around {% csrf_token %} to enable the protection. Next, in the *views.py* file, remove the decorator @csrf_exempt before the definition of "addquestion" to enable CSRF protection on that function. Lastly, delete the final row in *settings.py* reading "SESSION_COOKIE_SAMESITE = None" to set it back to default, enabling additional CSRF protection.

## Flaw 2: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
**Source links:**  
GET requests:
- https://github.com/Dravde01/CSB-Project-1/blob/master/polls/templates/polls/index.html#L26
- https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L49-L52

Login decorators:
1. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L31
2. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L36
3. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L46
4. https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L61

**Description:**  
Broken Access Control encapsules everything regarding improper setup of user access control mechanisms. This often means that users have access to do things they should not be allowed to (e.g. viewing sensitive data or performing administrative actions), which inherently causes security concerns. However, other things like weak passwords and an overall weak authentication policy are also sometimes included under Broken Access Control. In web applications, data is sometimes stored in path variables which can be modified to give certain users access to that data.

In my application, users can vote in polls and view the results without being logged in to the website. Without logging in, they can also create new questions by opening a link like http://localhost:8000/addquestion?q=you&c1=have%20been&c2=hacked while the server is running. This will create a poll with the question as "you" and the choices "have been" and "hacked".

**Fix:**  
This problem can be fixed by switching the linked GET requests to POST requests instead, which will in turn hide variable parameters in URLs. There are four lines that have to be changed in *views.py* and one line in *index.html*. Additionally, you should uncomment the decorator @login_required on the four definitions in *views.py* to make it so that a user has to log in to be able to access them.  
**Keep in mind!** POST requests require CSRF protection to be activated. So for this to work properly, you also have to do the fixes mentioned in Flaw 1.

## Flaw 3: [Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
**Source links:**
- DEBUG enabled: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L26
- Undefined hosts: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L28
- Visible secret key: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L23

**Description:**  
Security Misconfiguration is another broad term describing all kinds of incorrect implementation of security measures. These may have been explicitly misdefined by the programmer or could have been left as default values, ultimately leading to anyone having easy access to valuable information about the misconfigured application. In Django-based web applications, there exists a *settings.py* file which can be configured according to the needed user and administrator use cases. However, the default settings in this file are not very safe. There are even comments about it in the file itself.

In my application, the *settings.py* file has only been slightly changed. DEBUG is still set to its default value True, allowing attackers to see useful information about the website build by e.g. trying to view a nonexistent page URL like http://127.0.0.1:8000/hack. ALLOWED_HOSTS is undefined meaning anyone is allowed to run the server. The secret key is also visible in the code by default. This should be hidden in order to preserve its security benefits.  
All potential security issues can be seen by running `python manage.py check --deploy` in a CMD window.

**Fix:**  
Pretty much all fixes for these include explicitly defining them correctly in the *settings.py* file. Set DEBUG to False and set ALLOWED_HOSTS to your localhost (default being '127.0.0.1'). Doing this will make sure that an empty "Not Found" page is always shown when someone tries to view a nonexistent page. Finally, hide the secret key in a local *.env* file by following the steps [here](https://dev.to/themfon/how-to-protect-your-django-projects-secret-key-2ac6).  
**Keep in mind!** These are just fixes for the problems that I have mentioned in this part. There are still many possible security misconfigurations to fix here. However, I will not be bringing them up since this paragraph would become too long.

## Flaw 4: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
**Source links:**
- Password validators: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L88-L105
- Secure session cookies: https://github.com/Dravde01/CSB-Project-1/blob/master/csb_project_1/settings.py#L107

**Description:**  
In my opinion, the name of this flaw is slightly misleading. Basically, it refers to security issues surfacing as a result of inadequate authentication and verification of user identity in, specifically, business applications. A common and good protection tool here is issuing each logged-in user a session ID to keep track of them and ensure that attackers don't try to impersonate them. These are by default implemented in Django applications and, essentially, temporarily replace the users actual login credentials in favor of a more secure identification method. A hacker can easily obtain and use anyone's credentials through brute force, if the authentication methods used are weak enough. Therefore, topics like weak password policies are also included in this flaw.

In my project, password validators have been commented out. This is why the two authenticated users "admin" and "superuser" are able to have very predictable passwords. Additionally, secure session cookies are by default set to False. This means that session IDs are unencrypted and can be sent across any connection (not only HTTPS), allowing e.g. packet sniffers to be used to hijack a user's session.

**Fix:**  
To fix these problems, simply uncomment the linked lines in *settings.py* to enable strict password control and secure session cookies. After doing so, all session cookies will be encrypted and new user passwords:
1. will require a minimum length of 10 characters,
2. can't be too similar to the user's username,
3. can't be a commonly used password (e.g. 'password'), and
4. can't consist of only numbers.

To increase the security further, navigate to http://127.0.0.1:8000/admin/ when the server is running and change the password of, atleast, the very important superuser according to the new rules you have set up.

## Flaw 5: [Injection](https://owasp.org/Top10/A03_2021-Injection/)
**Source links:**
- Injection vulnerable code: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L85-L89
- Fixed function: https://github.com/Dravde01/CSB-Project-1/blob/master/polls/views.py#L82-L84

**Description:**  
Injection is a technique where attackers inject malicious data through an unsanitized data input field in an application. The data is interpreted as part of a command or query which is then executed by the application, possibly giving the attacker unauthorized access to the data. The most well-known injection method is called SQL injection. SQL injection is where an attacker inserts a malicious SQL query into an input field, with the goal of manipulating the backend database and giving the attacker access to some form of the data stored on there. To protect against this, programmer's should properly sanitize input fields or, if possible, use another injection-safe method in the code.

In my application, SQL injection is possible due to the input field for giving feedback being improperly sanitized. For example, if you log in as the user admin and write `',1); DELETE FROM polls_feedback; INSERT INTO polls_feedback (text, user_id) VALUES ('you have been hacked',1) --` into the input field for giving feedback, then all the content of the table will be deleted and there will only be one input saying "you have been hacked". An even worse case is if you enter `',1); DROP TABLE polls_feedback; --`. This text input will completely break the application and make it impossible for the superuser to log in to the website, without reverting the database changes.

**Fix:**  
To fix this very serious flaw, reverse the commenting of the linked lines in *views.py* at the definition of "givefeedback". What I mean by that is, comment out the lines 85-89 and uncomment the lines 82-84. This will change the function so that it uses Django's standard way of creating objects with models instead of using a SQL query INSERT INTO. This way, the input field will be completely safe from any injection attempts.

## Conclusion
To summarize, I have created a backend web application using Python and Django templates. This application has five different security flaws from the 2021 version of the [OWASP top ten list](https://owasp.org/www-project-top-ten/), including CSRF. The five flaws in my application include:
1. [CSRF](https://cybersecuritybase.mooc.fi/module-2.3/1-security)
2. [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)
3. [Security Misconfiguration](https://owasp.org/Top10/A05_2021-Security_Misconfiguration/)
4. [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)
5. [Injection](https://owasp.org/Top10/A03_2021-Injection/)

In this *README.md* file, I have described each and every one of these flaws, explained how they are present and affect my application and provided specific solutions to fix all of them in my application.

This was the first course project as part of the [Cyber Security Base 2023](https://cybersecuritybase.mooc.fi/) MOOC course provided by [Helsingin yliopisto](https://www.helsinki.fi/en).

Overall, it was a very fun and interesting challenge that I learned a lot from.  
Thanks for this opportunity and enjoy my project!
