#Bentha Technologies Mega Project Website

#Description
Bentha Technologies is full stack webapp of a company specializing in computer science and information technology solutions and services. Bentha Technologies company offers a wide range of services including software development, programming, computer training, and more. Our goal is to provide innovative and effective solutions to help businesses and individuals succeed in the digital world. The code presented in this software project is a complete and functional server side and client code developed using 5 computer programming languages ie, Python (Django), SQL (SQlite), Javascript, HTML, css, and Django templating language.

#Target market

This app will focus on entrepreneurs with the businesses revolving around technology like technology Schools, software develop firms, Cyber cafes or similar fields. This includes Software Engineering, Programming, Technology Training Institutes, Cyber Cafe etc.

#What the Betha Technologie Website will do

important

1.	Track keeping on restocking
2.	Track keeping of Profits
3.	Track any losses incurred
4.	Employee attendance
5.	Employee salary
6.	Any expenses incurred not related to buying and selling
7.	Give statement or keep record of progress
8.	Have a point-of-sale system (not mandatory)
9.  Allow customers to purchase services like request for software develpment task, Computer Training, etc.
10. Managing Students and Alumni

#Breakdown of the app
1.  Home Page or index page - This is the first page that appears when the website loads. This page display all services offered by Bentha Technologies including programming, software development, Computer Packages, Cyber Services, Electronics Repair etc.
2.	Login page- this is a page accessible to all. The app will be divided into 3 categories. The employee/Student and the employer/Administration and the Admin interfaces.

#Employee access
1.	Update the inventory of items being restocked that day
2.	Money is paid via cash or mpesa. So the employee can update the money they make in their shift in those 2 categories
3. Students can attend Tutorials
4.	Before clocking out update on restock items needed
#Employer access
1.	See who clocked in and who didn’t
2.	Access the sale history of all employees
3.	Access the list to be restocked
4.  Access Students learning activities
5.	Access to profit of day month and year based on selection
5.	See transactions made by date

#Architecture
Webstack: LAMP(Linux Apache, MySQL, Python) for backend(to be discussed) 
Framework: Django (MVT - Model, View, Template Architecture)
Frontend: react, css, HTML, ES6 Javascript, Bootstrap


#Development Steps:

1. Requirements Gathering: Detailed discussions with the users will help refine and finalize the app's features and functionalities.

2. Design and Wire framing: we will create a visual representation of how the app will look and flow, including user interfaces and navigation.

3. Backend Development: We will choose python programming language and a web framework Django, to build the backend. This will enhance Implementation of user authentication, database design, Scalability and API endpoints for data manipulation.

4. Frontend Development: we will use HTML, CSS, JavaScript or ES6, Bootstrap to create the user interface. We might also consider using a frontend framework like React, Angular, or Vue.js for a more interactive user experience.

5. Database Setup: We will choose MySQL database system on deployment server and SQLite on the development server to store user data, inventory information, sales records, system data and more.

6. Employee/Students and Employer/Administration Access: we will Implement separate dashboards for employees and employers with functionalities as described in the breakdown you send.

7. Data tracking and Reporting: We will develop mechanisms to track sales, expenses, and restocking needs. Generate reports for profits, attendance, and transactions.

8. Testing: we will thoroughly test the app to identify and fix any bugs or usability issues. We will perform unit testing as well as integration testing. We will implement both built in or customized middleware to test security

9. Deployment: We will Host the app on a Heroku/Python anywhere web server. This will give us added advantage like server console, Database console, deployment from GitHub branch, code editors which will enhance smooth collaboration since our programmers can edit the code on the server with one account.

10. User Training: We will provide a user guide or tutorial to help users understand how to use the app effectively.

11. Feedback and Iteration: We will gather user feedback and iterate on the app to improve its usability and performance.

#Technologies:

(a). Backend: Python programming language and Django web framework. This will provide us a strong foundation for building the features we've outlined. Django is commonly used for complex web applications like our Bentha Technologies app, it's also flexible enough to create smaller projects.
(b). Frontend: HTML, CSS, JavaScript, and frontend frameworks.
(c). Database: MySQL, SQLite relational database system.
(d). Authentication: Implementing secure user authentication mechanisms.
(e). Hosting: Heroku or Pythonanywhere web server.

NB: We may need more assistant from experienced software engineers to bring this ideas to life, but we may use ChatGPT as our helper


#cloning the program

1. git clone https://github.com/Benson480/webstack.git
2. create a new repository on the command line using below commands

echo "# Bentha Technologies" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Benson480/webstack.git
git push -u origin main


…or push an existing repository from the command line
git remote add origin https://github.com/Benson480/webstack.git
git branch -M main
git push -u origin main

…or import code from another repository
You can initialize this repository with code from a Subversion SVN, Mercurial, or Team Foundation server TFS project.


#Installation: 

To freeze the currently installed Python packages into a requirements.txt file using pip, you can use the following command:

pip freeze > requirements.txt

This command will generate a requirements.txt file in the current directory containing a list of all the installed packages and their versions. Each line in the file will represent one package in the format package-name==version.

After running this command, you can use the requirements.txt file to recreate the same environment by installing the packages listed in it using pip. For example, to install the packages from requirements.txt into a virtual environment, you can use:

pip install -r requirements.txt

Make sure you run these commands in the appropriate directory or virtual environment where you want to create or update the requirements.txt file.


#Presentation link

https://docs.google.com/presentation/d/1N1wG1yhFRmbHfc5WSBCVBJNk7f_cMpBx2nkFX14Y4ik/edit#slide=id.g27ac641283c_0_17

#Architecture Link

https://app.diagrams.net/#G1LzeLET_FNLyQ7tWyZTLRmjoDehbatj2k

#Useful Resources
Daraja API link

https://youtu.be/ycVQGmaR-Lo


#Deployment on heroku

git push heroku main
heroku run python manage.py migrate

heroku restart

heroku open



Creative Commons Attribution 4.0 International (CC BY 4.0)

You are free to:

- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:

- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.


#Authors: 

<Name: Benson Mwangi Kingori>

<Emails: bensonmwangi101@gmail.com
       : benthatechnologies@gmail.com
>
<Role: Lead Programmer and Software Engineer>

