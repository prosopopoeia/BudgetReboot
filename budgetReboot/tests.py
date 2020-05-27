from django.test import TestCase
from budgetReboot.models import Category, User


# Create your tests here.



    
# def test_return_find_returning_user(self):
    # response = self.client.post('/listcats', data=)    
    # self.s
    
class NewUserTest(TestCase):

    def test_handle_new_user(self):
        self.client.post('/usertype/', data={'users_name': 'Kip'})
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(User.objects.count(), 1)
        
        
    def test_index_exists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'budgetReboot/index.html')
        
        
class ExistingUserTest(TestCase):
    
    def createUser(self, p_users_name):
        existing_user = User(users_name=p_users_name)
        existing_user.save()
        return existing_user
        
    def createCategory(self, p_user, p_cat_name):
        users_cat = Category(owning_user=p_user, category_name=p_cat_name)
        users_cat.save()
        return users_cat
        
        
        
    def test_user_exists(self):    
        test_user = self.createUser('Foot-Foot')
        self.createCategory(test_user, 'shoes')
        response = self.client.post('/usertype/', data={'users_name' : 'Foot-Foot'})
        self.assertContains(response, "shoes")
        
        
    def test_get_next_cat(self):
        test_user = self.createUser('Foot-Foot')        
        self.createCategory(test_user, 'shoes')
        user_cats = self.createCategory(test_user, 'bags')
        second_cat = Category.objects.filter(owning_user=test_user)[1]
        self.assertEqual(second_cat.category_name, 'bags')
        
    def test_see_cat_detail(self):
        test_user = self.createUser('Foot-Foot')        
        #self.createCategory(test_user, 'shoes')
        user_cats = self.createCategory(test_user, 'bags')
        response = self.client.post('/catdetail/bags', data={'users_name': 'Foot-Foot'})
        self.assertContains(response, "bags")
 
        
