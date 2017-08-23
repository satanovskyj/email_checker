# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify

from checker import checker


def create_app():
    app = Flask(__name__)

    @app.route('/api/check', methods=['POST'])
    def check_email():
        email = request.form.get('email')
        if not email:
            return jsonify({
                'error': 'Wrong params!'
            })

        return jsonify({
            'is_valid': checker.run(email)
        })

    return app
