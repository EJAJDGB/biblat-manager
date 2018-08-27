# -*- coding: utf-8 -*-
import flask
from flask import current_app, url_for
from flask_breadcrumbs import current_breadcrumbs

from biblat_manager.webapp.controllers import create_user
from biblat_manager.tests.base import BaseTestCase


class UserTestCase(BaseTestCase):

    def test_login_registered_user(self):
        """Test de login de usuario registrado"""
        admin_user = {
            'email': 'admin@biblat.unam.mx',
            'password': 'foobarbaz',
        }
        create_user(admin_user['email'], admin_user['password'], True)
        login_url = url_for('main.login')

        with current_app.app_context():
            with self.client as c:
                # login de usuario
                response = c.post(
                    login_url,
                    data=admin_user,
                    follow_redirects=True)
                self.assertStatus(response, 200)
                self.assertEqual('text/html; charset=utf-8',
                                 response.content_type)
                self.assert_template_used("main/index.html")

    def test_login_unregistered_user(self):
        """Test de login de usuario no registrado"""
        admin_user = {
            'email': 'admin@biblat.unam.mx',
            'password': 'foobarbaz',
        }
        login_url = url_for('main.login')

        with current_app.app_context():
            with self.client as c:
                # login de usuario
                response = c.post(
                    login_url,
                    data=admin_user,
                    follow_redirects=True)
                expected_errors_msg = 'Usuario no registrado'
                self.assertStatus(response, 200)
                self.assertEqual('text/html; charset=utf-8',
                                 response.content_type)
                self.assertIn(expected_errors_msg,
                              response.data.decode('utf-8'))
                self.assert_template_used("auth/login.html")

    def test_login_wrong_password(self):
        """Test de login de usuario con contraseña incorrecta"""
        admin_user = {
            'email': 'admin@biblat.unam.mx',
            'password': 'foobarbaz',
        }
        create_user(admin_user['email'], admin_user['password'], True)
        login_url = url_for('main.login')
        admin_user['password'] = 'quxquuxcorge'

        with current_app.app_context():
            with self.client as c:
                # login de usuario
                response = c.post(
                    login_url,
                    data=admin_user,
                    follow_redirects=True)
                expected_errors_msg = 'Contraseña incorrecta'
                self.assertStatus(response, 200)
                self.assertEqual('text/html; charset=utf-8',
                                 response.content_type)
                self.assertIn(expected_errors_msg,
                              response.data.decode('utf-8'))
                self.assert_template_used("auth/login.html")

    def test_login_unverified_email(self):
        """Test de login de usuario con correo no verificado"""
        admin_user = {
            'email': 'admin@biblat.unam.mx',
            'password': 'foobarbaz',
        }
        create_user(admin_user['email'], admin_user['password'], False)
        login_url = url_for('main.login')

        with current_app.app_context():
            with self.client as c:
                # login de usuario
                response = c.post(
                    login_url,
                    data=admin_user,
                    follow_redirects=True)
                expected_errors_msg = 'Correo electrónico no verificado'
                self.assertStatus(response, 200)
                self.assertEqual('text/html; charset=utf-8',
                                 response.content_type)
                self.assertIn(expected_errors_msg,
                              response.data.decode('utf-8'))
                self.assert_template_used("auth/login.html")

    def test_login_redirect(self):
        """"Test de redirección de usuario con sesión activa"""
        """Test de login de usuario registrado"""
        admin_user = {
            'email': 'admin@biblat.unam.mx',
            'password': 'foobarbaz',
        }
        create_user(admin_user['email'], admin_user['password'], True)
        login_url = url_for('main.login')

        with current_app.app_context():
            with self.client as c:
                # login de usuario
                response = c.post(
                    login_url,
                    data=admin_user,
                    follow_redirects=True)
                self.assertStatus(response, 200)
                # llamada a login nuevamente
                response_login = c.get(login_url, follow_redirects=True)
                self.assertStatus(response_login, 200)
                self.assertEqual('text/html; charset=utf-8',
                                 response.content_type)
                self.assert_template_used("main/index.html")



