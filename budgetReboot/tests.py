from django.test import TestCase
from budgetReboot.models import Category, User


# Create your tests here.



    
# def test_return_find_returning_user(self):
    # response = self.client.post('/listcats', data=)    
    # self.s
    
class NewUserTest(TestCase):

    def test_handle_new_user(self):
        self.client.post('/listcats/', data={'users_name': 'Kip'})
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)
        
        
    def test_index_exists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'budgetReboot/index.html')
        
        
class ExistingUserTest(TestCase):
    
    def test_user_exists(self):
    
        existing_user = User(users_name='Foot-Foot')
        existing_user.save()
        users_cat = Category(owning_user=existing_user, category_name='shoes')
        users_cat.save()
        response = self.client.post('/listcats/', data={'users_name' : 'Foot-Foot'})
        self.assertContains(response, "shoes")
        
        
