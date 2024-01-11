from django.db.models import Model, TextField, CharField, CASCADE, DateTimeField, IntegerField, ForeignKey, \
    ManyToManyField, ImageField

from ckeditor.fields import RichTextField


class Category(Model):
    name = CharField(max_length=255)


class Tag(Model):
    name = CharField(max_length=255)


class Blog(Model):
    name = CharField(max_length=255)
    author = ForeignKey('auth.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    image = ImageField(upload_to='products/images/', default='products/default.jpg')
    tags = ManyToManyField('apps.Tag')
    text = RichTextField(blank=True, null=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Comment(Model):
    text = RichTextField()
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('auth.User', CASCADE, 'comments')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)
