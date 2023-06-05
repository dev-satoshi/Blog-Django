from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
  name = models.CharField('カテゴリ名', max_length=255)

  def __str__(self):
    return self.name

class Post(models.Model):
  title = models.CharField('title', max_length=255)
  text = models.TextField('本文')
  create_at = models.DateTimeField('作成日', default=timezone.now)
  category = models.ForeignKey(Category, verbose_name='カテゴリ名', on_delete=models.PROTECT)

  def __str__(self):
    return self.title



class Comment(models.Model):
  name = models.CharField('お名前', max_length=30, default='名無し')
  text = models.TextField('本文')
  post = models.ForeignKey(Post, verbose_name='紐づく記事', on_delete=models.PROTECT) #コメントを全て削除しないと投稿を消せない仕様
  create_at = models.DateTimeField('作成日', default=timezone.now)
  def __str__(self):
    return self.text[:10]

