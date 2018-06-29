from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):

    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao Must return status code 200"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contain input tags"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """HTML must contain CSRF"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription Form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):

    def setUp(self):
        data = dict(
            name='Matheus de Sousa Barros',
            cpf='02824886340',
            email='bmatheus91@gmail.com',
            phone='98982858442'
        )

        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST must redirect to /inscricao/"""
        self.assertEqual(302, self.response.status_code)

    def test_send_subscribe_email(self):
        """Before redirect valid POST, send email to subscriber"""
        self.assertEqual(1, len(mail.outbox))

    def test_subscription_email_subject(self):
        """Email subject must be Confirmação de Inscrição"""
        email = mail.outbox[0]
        expect = 'Confirmação de Inscrição'

        self.assertEqual(expect, email.subject)

    def test_subscription_email_from(self):
        """Email from must be contato@eventex.com.br"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, email.from_email)

    def test_subscription_email_to(self):
        """Email to must be contato@eventex.com.br and subscribers email"""
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'bmatheus91@gmail.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        """Email body must contain subscribers information"""
        email = mail.outbox[0]

        self.assertIn('Matheus de Sousa Barros', email.body)
        self.assertIn('02824886340', email.body)
        self.assertIn('bmatheus91@gmail.com', email.body)
        self.assertIn('98982858442', email.body)


class SubscribeInvalidPost(TestCase):

    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """Context must have subscription Form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_erros(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)


class SubscribeSuccessMessage(TestCase):

    def test_message(self):
        """Valid subscription must return success message Inscrição realizada com sucesso!"""
        data = dict(
            name='Matheus de Sousa Barros',
            cpf='02824886340',
            email='bmatheus91@gmail.com',
            phone='98982858442'
        )

        response = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(response, 'Inscrição realizada com sucesso!')
