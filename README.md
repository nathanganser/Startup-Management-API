# Startup-Management-API
Udacity's Capstone project

## Description
Modelling a startup team. With employees that work on projects. 
I am creating an API to streamline the process of creating 
projects and assigning team members to projects.

## Milestones 
 - [x] Connect to Github
 - [x] Get a basic app running locally (with DB, / get request)
 - [x] Add migrations
 - [x] Add Auth
 - [ ] Make it running on AWS
 - [ ] Add API backbone
 - [ ] Build API with jsonify
 - [ ] Build Postman tests
 - [ ] Add error handling and flash
 - [ ] Integrate with Fyyur frontend

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


## Roles & Permissions

Login Link
`https://nat-crm.eu.auth0.com/authorize?audience=startup&response_type=token&client_id=n1QEAgxPSJD4JRs3L8JT0oiD0CPNtP4e&redirect_uri=http://0.0.0.0:8080/`

### Public
Can view projects and team

### Manager
Can POST new projects and assign team members. 
Can PATCH projects & members
- post:projects
- patch:projects
- delete:projects
- patch:members



### CEO
#### Token
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qWXpPRGd3TUVFNFEwUTFOVVkzTWpVMFEwSXhNemsyTmpNeU0wTkVSVFE1UWpNNFFqTXlOUSJ9.eyJpc3MiOiJodHRwczovL25hdC1jcm0uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODk5NmU2YmIzYmMzMGJlZmYzOGZjOCIsImF1ZCI6InN0YXJ0dXAiLCJpYXQiOjE1ODYwNzU2NTksImV4cCI6MTU4NjA4Mjg1OSwiYXpwIjoibjFRRUFneFBTSkQ0SlJzM0w4SlQwb2lEMENQTnRQNGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptZW1iZXJzIiwiZGVsZXRlOnByb2plY3RzIiwicGF0Y2g6bWVtYmVycyIsInBhdGNoOnByb2plY3RzIiwicG9zdDptZW1iZXJzIiwicG9zdDpwcm9qZWN0cyJdfQ.J_jhjJDXCJNEfHBIASDKBhUVGV_w4cnZQO1VnufQ4Lq4-6s6UDWjiePcdqz8xI13AK48uQYewsNaZ0yrJAwkqhAP25pg4sq_e_ZF8nFDAbAYidSHDxVQma4-w7Am9e9xwa44FSkN53_oTT3fN0AzvEV86kpNSzdM6oE2hPaYUnSNrTdvBaGdhzrQhNPEsVsgiac9xIiIedYQdFfne3YgFA3YsuCSBQm8od03r7y5d3fgYhXdl-6ZrfGcWnDCEmZQrYw3OAjxeR4YwGCKEWYDE6BZcrme2aP-UMuGLOdW_qKxCtfvFX94x5NfIOAzmOGCvF98C9K5JTV6lAObzoOLHQ`


Can do everything above
- post:projects
- patch:projects
- delete:projects
- patch:members

And also POST & DELETE members

- post:members
- delete:members

[https://nat-crm.eu.auth0.com/authorize?audience=startup&response_type=token&client_id=n1QEAgxPSJD4JRs3L8JT0oiD0CPNtP4e&redirect_uri=http://0.0.0.0:8080/]: https://nat-crm.eu.auth0.com/authorize?audience=startup&response_type=token&client_id=n1QEAgxPSJD4JRs3L8JT0oiD0CPNtP4e&redirect_uri=http