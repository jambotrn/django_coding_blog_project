
from unicodedata import name
from wsgiref.validate import validator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
# Create your models here.

class Blog(models.Model):
    """A typical class defining a model, derived from the Model class."""
    # Fields
    title = models.CharField(max_length = 220, help_text = 'This is the title of blog')

    # Foreign Key used because blog can only have one author, but authors can have multiple blogs
    author = models.ForeignKey('Author', on_delete =models.SET_NULL, null = True)
    content = RichTextUploadingField(config_name='special', help_text='Write the content of this blog')
    tags = TaggableManager( help_text = 'Enter the blog keyword')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, help_text = 'Select a category')
    thumbnail_image = models.ImageField(upload_to='blog_pictures',null=True, blank=True)
    slug = models.SlugField(max_length = 250, null = False, unique = True)
    BLOG_STATUS = (
        ('l', 'Live'),
        ('d', 'Draft'),
    )

    status = models.CharField( max_length = 10, choices = BLOG_STATUS, blank = True, default = 'd' )
    published_date = models.DateField(null=True, blank=True)
    short_description = models.CharField(max_length=200, help_text='Enter one or two line about blog')

    """String for representing the Model object."""
    def __str__(self):
        return self.title
    
    """Returns the URL to access a detail record for this book."""
    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug':self.slug})
    
    def save(self, *args, **kwargs):
        try:
            this = Blog.objects.get(id=self.id)
            if this.thumbnail_image != self.thumbnail_image:
                this.thumbnail_image.delete(save=False)
        except:
            pass  # when new photo then we do nothing, normal case
        super().save(*args, **kwargs)
    
        if self.thumbnail_image:
            img = Image.open(self.thumbnail_image.path) # Open image
            # resize image
            if img.height > 300 or img.width > 400:
                output_size = (500,300)
                img.thumbnail(output_size) # Resize image
                img.save(self.thumbnail_image.path) # Save it again and override the larger image """

class Category(models.Model):
    name = models.CharField(max_length=30, help_text='Enter the category name')
    slug = models.SlugField(max_length = 250, null = False, unique=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug':self.slug})

class Author(models.Model):
    
    name = models.CharField(max_length=200, help_text='Enter full name')
    profession = models.CharField(max_length=100)
    bio = models.TextField(max_length=300)
    avater = models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures')
    social_link = models.CharField(max_length=200)
    slug = models.SlugField(max_length = 250, null = False, unique = True)
    date_of_birth = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug':self.slug})

class Comment(models.Model):
    title = models.CharField(max_length = 220, null=True ,help_text = 'Enter the subject of your comment')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    comment = models.TextField(max_length=300, help_text='Leave your valuable comment')
    commenter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    comment_date = models.DateTimeField(auto_now_add = True, blank = True)

    def get_absolute_url(self):
        return reverse('comment-detail',args = [str(self.id)])
    
    class Meta:
        ordering = ['comment_date']

    def __str__(self):
        return self.title[:60]

class Profile(models.Model):
    """ Getting extra information about commentators """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=250, help_text='Tell about your self in brief')
    image = models.ImageField(default='profile_pictures/default.jpg', upload_to='profile_pictures')
    
    def __str__(self) -> str:
        return f'{self.user.username} Profile'

    def save(self):
        super().save()
        if self.image.name != 'default.jpg':
            img = Image.open(self.image.path) # Open image
            # resize image
            if img.height > 150 or img.width > 150:
                output_size = (150, 150)
                img.thumbnail(output_size) # Resize image
                img.save(self.image.path) # Save it again and override the larger image
