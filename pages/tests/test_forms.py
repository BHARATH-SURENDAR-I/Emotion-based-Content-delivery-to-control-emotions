from django.test import SimpleTestCase
from pages.forms import LoginForm,Registrationform

class TestForms(SimpleTestCase):
    def test_Login_form_valid_data(self):
        form=LoginForm(data={
            'email':'basu@gmail.com',
            'password':'bharath1712'
            })
        print("checking valid form input data")
        self.assertTrue(form.is_valid())
    def test_Login_form_no_data(self):
        form=LoginForm(data={})
        print("checking no data form input data")
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors),2)
    def test_Login_form_invalid_data(self):
        form=LoginForm(data={
            'email':'12344kjbasjkdbfkjahbajlsbfkjadsbfjlasbdjsbfjkbdjkasbdjkabfjkhbasdjbasjkhfbadhbkajhbfuwrbfkahbfvkjasbabhfoiasudbhuoiabsbjkasdbjkadbfiawudbfiasubvasdiajnfidbfiadbasjkdvbjkabfaisuhfioaufhaihbfjhbfuiqwrho8uqerhahfbvjhbvlajhbilawufhoiuwrfhaijbhvajklsbvakljbfiaufhaeiourfhiwbf',
            'password':123
            })
        print("checking invalid form input data")
        self.assertFalse(form.is_valid())