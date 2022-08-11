from django.contrib import admin
from .models import Blog, Author,Profile, Category, Comment
from django.utils.html import format_html

# Register your models here.

#admin.site.register(Blog)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    # Dishplay each blog record with these field
    list_display = ('title', 'author', 'status', 'published_date','category', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    # Filter of blog list
    list_filter = ('author', 'status', 'published_date', 'category')

    #The fields attribute lists just those fields that are to be displayed on the form, in order
    fields = ['title', 'content', 'short_description', 'slug', ('author','category'), ('tags', 'thumbnail_image'), ('published_date', 'status')]

#admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):

    # Dishplay each author record with these field
    list_display = ('name', 'profession', 'social_link')
    prepopulated_fields = {'slug':('name','date_of_birth',)}
    fields = ['name','profession', 'bio', 'date_of_birth', ('slug', 'social_link'), 'avater']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #list_display = ('image', 'fullname')
    list_display = ('headshot_image',)

    def headshot_image(self, obj):
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=150,
            height=150,
            )
    )
#admin.site.register(Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug',)
    prepopulated_fields = {'slug':('name',)}

#admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    
    # Display each comment record with these field
    list_display = ('blog', 'commenter', 'comment_date')