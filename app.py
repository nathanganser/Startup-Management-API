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
            'name': name,
            'deadline': deadline,
            'team': team

        })

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
