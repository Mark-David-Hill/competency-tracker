# competency-tracker

Overview

This is a Competency Tracking Tool for employees of Business Inc. LLC (fictional company), made for my Dev Pipeline Capstone project. This application let's the user read and write data from a database of Business Inc. LLC's employees and managers. Standard users can view/edit their own profile as well as view their own competency and assessment data. In addition to this, Managers can also view/edit informartion for Users, Competencies, Assessments, and Assessment Results.

Getting Started

  -To get started you will need to run 'app.py' in the src folder. You should be okay to work with the app from there, but if need be you can start a pipenv shell and run it from there by putting the following commands into the terminal (You may need to use 'python' rather than 'python3' depending on your operating system.):
  python3 -m pipenv shell
  cd src
  python3 app.py

  -Once in the App you will have the option to login or Quit the App. You will need to input a username and password to login. The username is a User's email. For testing purposes, many of the Users in the database were given a username that is just first_name@gmail.com, and were given a password that is first_name_pass. Some examples of database Users you can log in as:

    Standard Users:
    -username: daxter@gmail.com password: daxter_pass
    -username: rune@gmail.com password: rune_pass
    -username: alphonse@gmail.com password: alphonse_pass
    -username: hazel@gmail.com password: hazel_pass
    -username: fiver@gmail.com password: fiver_pass
    Managers:
    -username: mark@gmail.com password: mark_pass
    -username: krystal@gmail.com password: krystal_pass
    -username: frodo@gmail.com password: frodo_pass
    -username: atrus@gmail.com password: atrus_pass

  -Note that if a User is inactive they cannot login. Their data can still be viewed/edited by a manager.
    Inactive Users:
    -username: inactiboy@gmail.com password: inactiboy_pass
    -username: inactigirl@gmail.com password: inactigiril_pass

Using the App
  
  Once you have logged into the app you have different options depending on if you have logged in as a Standard User or as a Manager.
  -Standard User Menu Options:
    -View/Edit Profile: Users can view their own information and edit things such as name, phone, email, and password.
    -View User Competency Summary: Users can view a Summary of all their competency scores.
    -View Assessment Results: Views all Assessment Results for the current user
    -Logout: Logs out of the current User's Account

  -Manager Options:
    -Personal Profile Menu: Has the same options as are available to a Standard User (though Managers can also edit their User Type/Active Status)
    -Users Menu
      -View/Edit Users: Here Managers can view data for all Users, select a user, then can edit that User's information, View a Competency Summary for the User, View all Assessment Results for the User, or record a new Assessment Result for the User.
      -Search for Users: Managers can search for User's based on First or Last Name. They can then select users and will have the option to edit that User's information, View a Competency Summary for the User, View all Assessment Results for the User, or record a new Assessment Result for the User.
      -Add new User: Managers can fill out a form to add a new User to the database.
    -Competencies Menu
      -View/Edit Competencies: Here Managers can view data for all Competencies, select a competency, then can change the name of the Competency or view a Competency Results Summary for the chosen Competency.
      -Add new Competency: Managers can fill out a form to add a new Competency to the database.
    -Assessments Menu
      -View/Edit Assessments: Here Managers can view data for all Assessments, select an Assessment, then can edit the Assessment's name or Competency.
      -Add new Assessment: Managers can fill out a form to add a new Competency to the database.
    -Assessments Results Menu
      -View/Edit Assessment Results: Here Managers can view data for all Assessment Results, select a Result, then can edit the Result's information.
      -Add new Assessment Result: Managers can fill out a form to add a new Assessment Result for a User.
      -Delete Assessment Result: Managers can select an Assessment Result to delete/remove from the database.
    -Import/Export Menu
      -Import CSV Files: Managers can specify the filename for a CSV file in the imports folder in order to import those Assessment Results from the file and add the results to the database.
      -Export CSV File
        -Export User Competency Summary: The Manager can choose a User to create a User Competency Summary Report and export it as a CSV File.
        -Export Competency Results Summary: The Manager can choose a Competency to create a Competency Results Summary Report and export it as a CSV File.
    -Logout: Logs out of the current User's Account

Testing
  Though the average User should not need to worry about testing, there are a set of Unit Tests that run with Pytest available in tests/test_app.py. In order to run the tests, you will need to install Pytest then run the command:
    PYTHONPATH=src python3 -m pytest
  Writing these tests was a learning process and I would have done some things differently were I to start over, but they were still a valuable asset during development and are here in case you want to play around with them.