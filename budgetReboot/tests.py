from django.test import TestCase

# Create your tests here.

def test_index_exists(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'budgetReboot/index.html')
    
    
# def test_return_new_user_template(self):
    # response = self.client.get('/')
    # self.s
