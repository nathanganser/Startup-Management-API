import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Project, Member, Team
from datetime import datetime
from auth import requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def hello():
        return str(datetime.now())

    @app.route('/projects', methods=['POST'])
    @requires_auth('post:projects')
    def create_project(payload):
        try:
            name = request.json.get('name')
            deadline = request.json.get('deadline')
            team = request.json.get('team')

            # Check if team member exists
            all_team_members = Member.query.all()
            all_members_id = []
            for member in all_team_members:
                all_members_id.append(member.id)
            for member in team:
                if member not in all_members_id:
                    return jsonify({
                        'success': False,
                        'message': "One more more team members don't exist"
                    })

            # Add project to DB
            new_project = Project(name=name, deadline=deadline)
            new_project.insert()
            for member in team:
                teamlink = Team(project_id=new_project.id, member_id=member)
                teamlink.insert()

            return jsonify({
                'success': True,
                'message': "The new project was created successfully",
                'project': new_project.show()

            })

        except:
            return jsonify({
                'success': False,
                'message': 'An unknown error occured'
            })

    @app.route('/projects', methods=['GET'])
    def get_projects():
        try:
            all_projects = Project.query.all()
            projects = [project.show() for project in all_projects]
            return jsonify({
                'success': True,
                'message': 'The projects have been successfully returned',
                'projects': projects
            })
        except:
            return jsonify({
                'success': False,
                'message': 'An unknown error occured'
            })

    @app.route('/projects/<int:id>', methods=['GET'])
    def get_project(id):
        try:
            project = Project.query.filter_by(id=id).one()
            return jsonify({
                'success': True,
                'message': 'The project has been successfully returned',
                'projects': project.show()
            })
        except:
            return jsonify({
                'success': False,
                'message': 'An unknown error occured'
            })

    @app.route('/projects/<int:id>', methods=['PATCH'])
    @requires_auth('patch:projects')
    def edit_project(payload, id):
        try:
            # Check if project exists
            project_exists = False
            all_projects = Project.query.all()
            for project in all_projects:
                if project.id == id:
                    project_exists = True

            if not project_exists:
                return jsonify({
                    'success': False,
                    'message': 'The project does not exist'
                })
            project_to_patch = Project.query.filter_by(id=id).one()

            if request.json.get('name'):
                project_to_patch.name = request.json.get('name')
                project_to_patch.update()

            if request.json.get('deadline'):
                project_to_patch.deadline = request.json.get('deadline')
                project_to_patch.update()

            if request.json.get('team'):
                team = request.json.get('team')
                # Check if team member exists
                all_team_members = Member.query.all()
                all_members_id = []
                for member in all_team_members:
                    all_members_id.append(member.id)

                for member in team:
                    if member not in all_members_id:
                        return jsonify({
                            'success': False,
                            'message': "One more more team members don't exist"
                        })
                # Remove current team
                to_delete_teams = Team.query.filter_by(project_id=id).all()

                for team_delete in to_delete_teams:
                    team_delete.delete()

                # Add new team
                for member in team:
                    teamlink = Team(project_id=id, member_id=member)
                    teamlink.insert()

            return jsonify({
                'success': True,
                'message': "The project has been successfully updated",
                'project': project_to_patch.show()

            })

        except:
            return jsonify({
                'success': False,
                'message': 'An unknown error occured'
            })

    @app.route('/projects/<int:id>', methods=['DELETE'])
    @requires_auth('delete:projects')
    def delete_project(payload, id):
        try:
            # Check if project exists
            project_exists = False
            all_projects = Project.query.all()
            for project in all_projects:
                if project.id == id:
                    project_exists = True

            if not project_exists:
                return jsonify({
                    'success': False,
                    'message': 'The project does not exist'
                })

            # Delete project
            project_to_delete = Project.query.filter_by(id=id).one()
            project_to_delete.delete()

            # Delete team
            to_delete_teams = Team.query.filter_by(project_id=id).all()

            for team_delete in to_delete_teams:
                team_delete.delete()

            return jsonify({
                'success': True,
                'message': "The project & team associated has been successfully deleted"
            })

        except:
            return jsonify({
                'success': False,
                'message': 'An unknown error occured'
            })



    # END OF THE APP #

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
