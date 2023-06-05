from django import forms
from .models import Comment


class CommentCreateForm(forms.ModelForm): #コメントモデルをもとに入力欄を生成してくれる

  # 入力欄のカスタマイズをしてる
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
  
  class Meta:
    model = Comment
    fields = ['name', 'text'] #本文と入力欄だけ表示される