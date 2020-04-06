import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Project, Member, Team
from app import APP

# How to use this test file:
# 1. Make sure the manager_auth_token and ceo_auth_token are valid
# 2. Update the project_id to match the id of the project that will be created by the tests.

manager_auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qWXpPRGd3TUVFNFEwUTFOVVkzTWpVMFEwSXhNemsyTmpNeU0wTkVSVFE1UWpNNFFqTXlOUSJ9.eyJpc3MiOiJodHRwczovL25hdC1jcm0uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODk5NmU2YmIzYmMzMGJlZmYzOGZjOCIsImF1ZCI6InN0YXJ0dXAiLCJpYXQiOjE1ODYxNTcwMzYsImV4cCI6MTU4NjI0MzQzNiwiYXpwIjoibjFRRUFneFBTSkQ0SlJzM0w4SlQwb2lEMENQTnRQNGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptZW1iZXJzIiwiZGVsZXRlOnByb2plY3RzIiwicGF0Y2g6bWVtYmVycyIsInBhdGNoOnByb2plY3RzIiwicG9zdDptZW1iZXJzIiwicG9zdDpwcm9qZWN0cyJdfQ.bZU4XC-KZmNksPj2W0FYQ2djcst-JvkPLQ4Gs0W-3DclLZf5hKYwK8DmiIL5riWrPTa6Gep02Gxe0nHZoJi543MPtZLV0i3wSi9oibUXUgOYgVTgYDVz-YARz7QVJxHBZDcHGG8oSWWS4ucUVqH_dAtgnaPcoKpo00IoIUEgURAIzeRIzAUBDDxjpzp-bf7S9slaBySFUJALXwC8DEToUxySiLGVS_qHntaOQLTsQpL4hP7CVmtQFfEygypt-XVsxoI7VROjk7XH8gEQJXiY6SdkqucA0dMNPToKpMiq8Ju92N0fUlZ20-hq6o6W2yj-8kE5Un_zvOzr4Efrl68jNA"
ceo_auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5qWXpPRGd3TUVFNFEwUTFOVVkzTWpVMFEwSXhNemsyTmpNeU0wTkVSVFE1UWpNNFFqTXlOUSJ9.eyJpc3MiOiJodHRwczovL25hdC1jcm0uZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlODk5NmU2YmIzYmMzMGJlZmYzOGZjOCIsImF1ZCI6InN0YXJ0dXAiLCJpYXQiOjE1ODYxNTcwMzYsImV4cCI6MTU4NjI0MzQzNiwiYXpwIjoibjFRRUFneFBTSkQ0SlJzM0w4SlQwb2lEMENQTnRQNGUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTptZW1iZXJzIiwiZGVsZXRlOnByb2plY3RzIiwicGF0Y2g6bWVtYmVycyIsInBhdGNoOnByb2plY3RzIiwicG9zdDptZW1iZXJzIiwicG9zdDpwcm9qZWN0cyJdfQ.bZU4XC-KZmNksPj2W0FYQ2djcst-JvkPLQ4Gs0W-3DclLZf5hKYwK8DmiIL5riWrPTa6Gep02Gxe0nHZoJi543MPtZLV0i3wSi9oibUXUgOYgVTgYDVz-YARz7QVJxHBZDcHGG8oSWWS4ucUVqH_dAtgnaPcoKpo00IoIUEgURAIzeRIzAUBDDxjpzp-bf7S9slaBySFUJALXwC8DEToUxySiLGVS_qHntaOQLTsQpL4hP7CVmtQFfEygypt-XVsxoI7VROjk7XH8gEQJXiY6SdkqucA0dMNPToKpMiq8Ju92N0fUlZ20-hq6o6W2yj-8kE5Un_zvOzr4Efrl68jNA"
project_id = 13
class StartupTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client

        self.database_name = "startup_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()




    def tearDown(self):
        pass

    # CEO tests
    def test_create_project(self):
        new_project = {
            "name": "Great project",
            "deadline": "2020-04-04 10:38:25.038611",
            "team": [1]
        }

        hed = {'Authorization': 'Bearer ' + ceo_auth_token}
        res = self.client().post('/projects', json=new_project, headers=hed)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['project'])
        self.assertEqual(data['success'], True)


    # Public tests

    def test_create_project_no_auth(self):
        new_project = {
            "name": "Great project",
            "deadline": "2020-04-04 10:38:25.038611",
            "team": [1]
        }

        hed = {'Authorization': 'Bearer '}
        res = self.client().post('/projects', json=new_project, headers=hed)
        self.assertEqual(res.status_code, 500)



    def test_return_projects(self):
        res = self.client().get('/projects')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_return_unique_project(self):
        res = self.client().get('/projects/' + str(project_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_return_unique_project_error(self):
        res = self.client().get('/projects/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)

    # Manager tests
    def test_create_project_wrong_auth(self):
        new_project = {
            "name": "Great project",
            "deadline": "2020-04-04 10:38:25.038611",
            "team": [1]
        }

        hed = {'Authorization': 'Bearer ' + manager_auth_token}
        res = self.client().post('/projects', json=new_project, headers=hed)
        self.assertEqual(res.status_code, 500)

    def test_patch_project(self):
        name = "Changed project"
        deadline = "2022-07-04 10:38:25.038611"
        patched_project = {
            "name": name,
            "deadline": deadline,
        }
        hed = {'Authorization': 'Bearer ' + manager_auth_token}
        res = self.client().patch('/projects/' + str(project_id), json=patched_project, headers=hed)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['project']['name'], name)
        self.assertEqual(data['project']['deadline'], deadline)
        self.assertEqual(data['success'], True)

    def test_zdelete_project(self):
        hed = {'Authorization': 'Bearer ' + manager_auth_token}
        res = self.client().delete('/projects/' + str(project_id), headers=hed)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_zdelete_zfake_project(self):
        hed = {'Authorization': 'Bearer ' + manager_auth_token}
        res = self.client().delete('/projects/' + str(project_id), headers=hed)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)


if __name__ == "__main__":
    unittest.main()