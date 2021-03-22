from flask import request, jsonify, render_template

from app import app, db
from app.models import Credential


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", title="CLI Password manager")


@app.route('/api/add_creds', methods=['POST'])
def add_creds():
    service = request.json['service']
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    key = app.config['ENC_KEY']

    if len(Credential.query.filter_by(service=service, email=email).all()) == 0:
        creds = Credential(service=service, username=username,
                           email=email, password=password, key=key)
        db.session.add(creds)
        db.session.commit()

        return jsonify({
            'status': 'success'
        })

    else:
        return jsonify({
            'status': 'fail',
            'message': 'A credential with this service name and email exists'
        })


@app.route('/api/get_creds_all', methods=['GET'])
def get_creds_all():

    try:
        creds = Credential.query.all()
        if creds:
            all_creds = []
            for cred in creds:
                all_creds.append({'status': 'success',
                                  'id': cred.id,
                                  'service': cred.service,
                                  'username': cred.username,
                                  'email': cred.email,
                                  'password': cred.decrypt(app.config['ENC_KEY'])
                                  })
            return jsonify(all_creds)

        return jsonify({
            'status': 'fail',
            'message': 'There are no credentials yet'
        })
    except:
        return jsonify({
            'status': 'fail',
            'message': 'Database error contact admin to fix issue'
        })


@app.route('/api/get_creds/<id>', methods=['GET'])
def get_creds_by_id(id):
    creds = Credential.query.filter_by(id=id).all()
    if creds:
        return jsonify({'status': 'success',
                        'id': creds.id,
                        'service': creds.service,
                        'username': creds.username,
                        'email': creds.email,
                        'password': creds.decrypt(app.config['ENC_KEY'])
                        })

    return jsonify({
        'status': 'fail',
        'message': 'There are no credentials with this id'
    })


@app.route('/api/get_creds', methods=['GET'])
def get_creds_by_service():
    service = request.args.get('service')
    creds = Credential.query.filter_by(service=service).all()

    if creds:
        all_creds = []
        for cred in creds:
            all_creds.append({'status': 'success',
                              'id': cred.id,
                              'service': cred.service,
                              'username': cred.username,
                              'email': cred.email,
                              'password': cred.decrypt(app.config['ENC_KEY'])
                              })

        return jsonify(all_creds)

    return jsonify({
        'status': 'fail',
        'message': 'There are no credentials with this service name'
    })


@app.route('/api/del_creds/<id>', methods=['DELETE'])
def delete_creds_by_id(id):

    cred = Credential.query.filter_by(id=id).first()
    if cred:
        db.session.delete(cred)
        db.session.commit()
        return jsonify({
            'status': 'success'
        })

    return jsonify({
        'status': 'fail',
        'message': 'There are no credentials with this id'
    })


@app.route('/api/update_creds/<id>', methods=['PUT'])
def update_creds_by_id(id):
    creds = Credential.query.filter_by(id=id)
    if creds:
        # fetch request json data
        creds.service = request.json['service']
        creds.username = request.json['username']
        creds.email = request.json['email']

        creds.password_enc = creds.encrypt(
            request.json['password'], app.config['ENC_KEY'])

        db.session.commit()
        return jsonify({
            'status': 'success'
        })

    return jsonify({
        'status': 'fail',
        'message': 'There are no credentials with this id'
    })
