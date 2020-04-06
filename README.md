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
 - [x] Add API backbone
 - [x] Build API with jsonify
 - [ ] Build tests
 - [ ] Add error handling and flash

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
Returns all the projects.
#### Example of a request.
A simple GET request works. 
```
curl http://0.0.0.0:8080/projects
```
#### Response template
A JSON will be returned. The projects will be listed as JSONs inside an array. 
Notice the `success` and `message` parameter that will give you additional information.
```
{
  "message": "The projects have been successfully returned", 
  "projects": [
    {
      "id": 3, 
      "name": "Nice project", 
      "team": [
        1, 
        2
      ]
    }, 
    {
      "id": 4, 
      "name": "Another project", 
      "team": [
        1
      ]
    }
  ], 
  "success": true
}
```

### POST projects
Create a new project. Requires name, due date 
& a list of the members who will work on the project.
This requires the `post:project` permission.

For the date, the `datetime` format is required.
#### Example of a JSON request
```
{
    "name": "Great project",
    "deadline": "2020-04-04 10:38:25.038611",
    "team": [1,2]
}
``` 
#### Response template
It will return a `success` and `message` parameter to indicate how it went. 
Additionally, the created project will be returned from the DB.
```
{
  "deadline": "2020-04-04 10:38:25.038611",
  "message": "The new project was created successfully",
  "project": {
    "id": 3,
    "name": "Great project",
    "team": [2]
  }
}
```
### DELETE projects/<int:id>/
Deletes a specific project
#### Example of a DELETE request
```
```

### PATCH projects/<int:id>/
Edit a specific project, change name & due date. One or 
multiple parameters can be changed. This requires the 
`patch:project` permission. 

If a parameter is absent, it will not be modified.
Regarding the team, patching the team parameter will remove 
the current team and replace it by the team parameter from 
the patch request.

#### Example of a PATCH request
In this case, only the name and the team are modified.

`curl -X PATCH http://0.0.0.0:8080/projects/3`
```
{
    "name": "Great project",
    "team": [2]
}
```
#### Example of a response JSON
{
  "message": "The project has been successfully updated",
  "project": {
    "id": 3,
    "name": "Great project",
    "team": [
      2
    ]
  },
  "success": true
}
### GET projects/<int:id>/
Returns information about a specific project including: 
- name
- due date
- Ids of members working on that project

#### Example of a GET request
```
curl http://0.0.0.0:8080/projects/3
```

#### Example of a JSON response
The response includes a `success` and `message` parameter for further information.
```
{
  "message": "The project has been successfully returned",
  "projects": {
    "id": 3,
    "name": "Great project",
    "team": [
      2
    ]
  },
  "success": true
}
```
## /members

### GET members
Returns all the members
`Coming soon`

### POST members
Create a new team member. Requires name, role.
`Coming soon`

### DELETE members/<int:id>/
Deletes a specific member
`Coming soon`

### PATCH members/<int:id>/
Edit a specific member, change name & role
`Coming soon`

### GET members/<int:id>/
Returns information about a specific member including: 
- name
- role
- projects
`Coming soon`


## Roles & Permissions

Login Link

`https://nat-crm.eu.auth0.com/authorize?audience=startup&response_type=token&client_id=n1QEAgxPSJD4JRs3L8JT0oiD0CPNtP4e&redirect_uri=http://0.0.0.0:8080/`

### Public
Anyone can view projects and members. 
Readonly access is publicly available and does 
not require authentification.

### Manager
Managers can manage projects and members. 
They can delete projects but can't create new ones. 
They also can't delete members.
- `patch:projects`
- `delete:projects`
- `patch:members`
#### Token
``

### CEO
The CEO has all the manager's permissions, 
and in addition, he can create projects and members.
He can also delete members.
- `post:projects`
- `patch:projects`
- `delete:projects`
- `patch:members`
- `post:members`
- `delete:members`
#### Token
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qWXpPRGd3TUVFNFEwUTFOVVkzTWpVMFEwSXhNemsyTmpNeU0wTkVSVFE1UWpNNFFqTXlOUSJ9.eyJpc3MiOiJodHRwczovL25hdC1jcm0uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODk5NmU2YmIzYmMzMGJlZmYzOGZjOCIsImF1ZCI6InN0YXJ0dXAiLCJpYXQiOjE1ODYxNTcwMzYsImV4cCI6MTU4NjI0MzQzNiwiYXpwIjoibjFRRUFneFBTSkQ0SlJzM0w4SlQwb2lEMENQTnRQNGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptZW1iZXJzIiwiZGVsZXRlOnByb2plY3RzIiwicGF0Y2g6bWVtYmVycyIsInBhdGNoOnByb2plY3RzIiwicG9zdDptZW1iZXJzIiwicG9zdDpwcm9qZWN0cyJdfQ.bZU4XC-KZmNksPj2W0FYQ2djcst-JvkPLQ4Gs0W-3DclLZf5hKYwK8DmiIL5riWrPTa6Gep02Gxe0nHZoJi543MPtZLV0i3wSi9oibUXUgOYgVTgYDVz-YARz7QVJxHBZDcHGG8oSWWS4ucUVqH_dAtgnaPcoKpo00IoIUEgURAIzeRIzAUBDDxjpzp-bf7S9slaBySFUJALXwC8DEToUxySiLGVS_qHntaOQLTsQpL4hP7CVmtQFfEygypt-XVsxoI7VROjk7XH8gEQJXiY6SdkqucA0dMNPToKpMiq8Ju92N0fUlZ20-hq6o6W2yj-8kE5Un_zvOzr4Efrl68jNA`
