from django.test import TestCase
from blog.models import Author
from django.utils.text import slugify
from django.urls import reverse
from django.core.files import File
from mock import MagicMock

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(self):
        # Set up non-modified objects used by all test methods
        Author.objects.create(
        name='bill gates', 
        date_of_birth= '2082-01-06', 
        slug = slugify('bill gates' + "-" + '2082-01-06'),
        )

    def test_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)
    
    def test_slug_value(self):
        author = Author.objects.get(id=1)
        # This will fail if the urlconf is not defined.
        expected = slugify(author.name + "-" + str(author.date_of_birth))
        self.assertEqual(author.slug, expected)

    def test_get_absolut_url(self):
         """ Test that get_absolute_url returns the expected URL"""
         author = Author.objects.get(id=1)
         expected = reverse("author-detail", kwargs={"slug": author.slug})
         actual = author.get_absolute_url()
         self.assertEqual(expected, actual)
    
    def test_author_avater(self):
        author = Author.objects.get(id=1)
        ava_path = author.avater.path
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.jpj'
        author.avater = file_mock
        self.assertEqual(author.avater.name, file_mock.name)