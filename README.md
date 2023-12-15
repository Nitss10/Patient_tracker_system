# Patient_tracker_system
The Patient Tracker is a web-based application designed to streamline the management of patient information and medical records. The primary goal is to provide doctors with a convenient and efficient way to access and update patient records during checkups.



In Sprint 1, we identified the functional and non-functional requirements of our project Furthermore, we created UI mockups and database schema modeling.
In Sprint 2, we worked on the architecture diagram, and the low level design of the project, finalizing our tech stack
In Sprint 3, we worked on the development phase
In Sprint 4, we worked on testing (manual+automated regression testing) and writing documentation for the project

***************************************************************************************************************************************************************************************************

STEPS TO RUN THE PROJECT

1. Ensure python 3.11.x is installed, if not install it from https://www.python.org/downloads/
2. Download the libraries needed for running the project mentioned in requirements.txt
   pip install -r requirements.txt or pip3 install -r requirements.txt
3. git clone the repo to the local setup
   git clone https://github.com/Nitss10/Patient_tracker_system.git
4. db.sqlite3 is the sqlite database. You can delete the database and create a new database of your own as well.
5. Make sure all migrations are applied
   python manage.py makemigrations
   python manage.py migrate
6. Run the local host server
   python manage.py runserver

**NOTE: MAKE SURE TO USE DIFFERENT BROWSERS TO OPEN DIFFERENT INSTANCES OF DOCTORS AND PATIENTS. IF OBSERVING ANY ERROR SIMPLY LOGOUT USING http://127.0.0.1:8000/logout/
CURRENTLY SINCE THE WEBSITE IS LOCALLY HOSTED, SESSION MANAGEMENT IS A LIMITATION, WE NEED DIFFERENT BROWSERS OR PRIVATE/INCOGNITO WINDOWS (IF USING THE SAME BROWSER) TO LOGIN TO DIFFERENT DOCTORS AND PATIENTS


TO RUN THE AUTOMATED UNIT TESTS
1. python manage.py test

TO CREATE THE DOCUMENTATION
1. Install sphinx using pip install sphinx
2. create a docs directory
   mkdir $root/docs/
4. "sphinx-apidoc -o docs ." For selecting the source and destination
5. cd docs
6. make html

