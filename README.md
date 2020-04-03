# Startup-Management-API
Udacity's Capstone project

## Description
Modelling a startup team. With employees that work on projects. I am creating an API to streamline the process

## Milestones 
 - [x] Connect to Github
 - [ ] Get a basic app running locally (with DB, / get request)
 - [ ] Make it running on AWS 

## Models

### Projects
With names & due dates

### Team members
With names, role
```
--> Many to many relationships. Projects have multiple team members and team members work on multiple projects. 
```
# Endpoints
## /projects

### GET projects
Returns all the projects

### POST projects
Create a new project. Requires name & due date.
And requires members who will work on the project.

### DELETE projects/<int:id>/
Deletes a specific project

### PATCH projects/<int:id>/
Edit a specific project, change name & due date

### GET projects/<int:id>/
Return information about a specific project including: 
- name
- due date
- members working on that project

## /members

### GET members
Returns all the members

### POST members
Create a new team member. Requires name, role.

### DELETE members/<int:id>/
Deletes a specific member

### PATCH members/<int:id>/
Edit a specific member, change name & role

### GET members/<int:id>/
Returns information about a specific member including: 
- name
- role
- projects


## Roles

### Public
Can view projects and team

### Manager
Can POST new projects and assign team members. 
Can PATCH projects & members

### CEO
Can do everything above + 
POST & DELETE members