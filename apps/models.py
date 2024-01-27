import time

from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CharField, CASCADE, DateTimeField, ForeignKey, \
    ManyToManyField, ImageField, FloatField, PositiveIntegerField, EmailField
from django_resized import ResizedImageField

from apps.task import task_send_email


class User(AbstractUser):
    image = ResizedImageField(size=[90, 90], crop=['middle', 'center'], upload_to='users/images',
                              default='users/default.jpg')


class Category(Model):
    name = CharField(max_length=255)

    def count_bloga(self) -> int:
        return self.blog_set.count()

    def __str__(self):
        return self.name


class Tag(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(Model):
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', CASCADE)
    image = ImageField(upload_to='blog/images/', default='blog/default.jpg')
    tags = ManyToManyField('apps.Tag')
    text = RichTextField(blank=True, null=True, config_name='extends')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is not None:
            super().save(force_insert, force_update, using, update_fields)
            emails: list = Emails.objects.values_list('email', flat=True)
            start = time.time()
            task_send_email.delay('Yangi blog', self.name, list(emails))
            end = time.time()
            print(end - start, '--yuborildi')
        print('yuborilmadi')
    def count_comment(self):
        return self.comment_set.count()

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = FloatField()
    description = RichTextField(blank=True, null=True, config_name='extends')
    quantity = PositiveIntegerField(default=0)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class ProductImage(Model):
    image = ImageField(upload_to='producys/images/')
    product = ForeignKey('apps.Product', CASCADE)


class Comment(Model):
    text = CharField(max_length=255)
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE, 'comments')
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)


class Wishlist(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='wishlists/images/')
    product = ForeignKey('apps.Product', CASCADE)
    price = FloatField()
    stockstatus = PositiveIntegerField(default=0)


class Emails(Model):
    email = CharField(max_length=255)
