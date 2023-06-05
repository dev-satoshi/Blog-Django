from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from .forms import CommentCreateForm
from .models import Post, Category, Comment


class IndexView(generic.ListView):
  model = Post
  paginate_by = 1

  def get_queryset(self): #新しい記事から表示する
    queryset = Post.objects.order_by('-create_at')
    keyword = self.request.GET.get('keyword') #formで指定したkeywordを取得する 検索フォームの入力内容を取得できる
    if keyword :
      queryset=queryset.filter( #フィールド名__icontains=keywordでキーワードが含むかどうかで検索することができる　完全一致の場合はフィールド名=keywordで良い
        Q(title__icontains=keyword)|Q(text__icontains=keyword)) #Qでor検索ができる　これで本文にマッチしたkeywordも取得することができる
    return queryset
  


class CategoryView(generic.ListView):
  model = Post #CategoryViewといってもそのカテゴリで絞り込んだ記事の一覧なのでListViewでモデルはPostになる
  paginate_by = 10

  def get_queryset(self):
    category = get_object_or_404(Category, pk=self.kwargs['pk']) #カテゴリオブジェクトを取得している pkでカテゴリオブジェクトがなければ404ページに遷移させる
    queryset = Post.objects.order_by('-create_at').filter(category=category) #降順かつcategoryでヒットしたものだけ取得する
    # category_pk = self.kwargs['pk']
    # queryset = Post.objects.order_by('-created_at').filter(category__pk=category_pk)
    return queryset



class DetailView(generic.DetailView):
  model = Post


# コメント投稿ページに移動する際に記事のプライマリーキーをURLに含めてコメント投稿のviewに渡すことでどの記事に紐づいたコメント
# なのかがすぐにわかり、そのプライマリーキーで記事を取得してその記事をコメントに紐づける
class CommentView(generic.CreateView):
  model = Comment
  # fields = ('name', 'text')
  form_class = CommentCreateForm

  def form_valid(self, form):
    post_pk = self.kwargs['post_pk']
    comment = form.save(commit=False)
    comment.post = get_object_or_404(Post, pk=post_pk)
    comment.save()
    return redirect('blog:detail', pk=post_pk)