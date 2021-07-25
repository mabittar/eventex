from unittest.mock import Mock

from django.test import TestCase
from eventex.subscriptions.admin import (
    SubscriptionModelAdmin,
    Subscriptions,
    admin
    )


class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        Subscriptions.objects.create(
            name='Marcel Bittar',
            cpf='12345678901',
            email='ma_bittar@yopmail.com',
            phone='21-988887896')
        self.model_admin = SubscriptionModelAdmin(Subscriptions, admin.site)

    
    def test_have_action(self):
        """Action mark as paid shuould be installed"""
        
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        '''It should mark as paid  all selected subscriptions'''
        self.call_action()
        
        self.assertEqual(1, Subscriptions.objects.filter(paid=True).count())
        

    def test_message(self):
        '''it should display message after action'''
        
        mock = self.call_action()

        mock.assert_called_once_with(
            request=None, message='1 inscrição foi marcada como paga.')

    def call_action(self):
        queryset = Subscriptions.objects.all()
        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock
        self.model_admin.mark_as_paid(None, queryset)

        
        SubscriptionModelAdmin.message_user = old_message_user

        return mock
