from django.shortcuts import render
from django.views import generic  # FormViewを利用するため
from django.contrib.auth.mixins import LoginRequiredMixin   # ログオンユーザのみアクセス可とするために利用する
from django.conf import settings  # settings.pyの定義内容を利用するため
from .forms import UploadForm   # forms.pyで定義したUploadFormをインポート
# ファイルオブジェクト操作のためdefault_storageを利用する
from django.core.files.storage import default_storage
import shutil
import os

# Create your views here.


def top(requests):
    return render(requests, 'pdfmr/top.html')


class UploadView(LoginRequiredMixin, generic.FormView):
    form_class = UploadForm
    template_name = 'pdfmr/upload_form.html'

    def form_valid(self, form):
        user_name = self.request.user.username  # ログオンユーザ名の取得
        user_dir = os.path.join(settings.MEDIA_ROOT,
                                "excel", user_name)  # ユーザディレクトリパスの生成
        if not os.path.isdir(user_dir):  # ユーザディレクトリの作成
            os.makedirs(user_dir)
        temp_dir = form.save()  # upload一時フォルダの取得
        # pdf -> PDF⇒excel変換処理の実行（あとで実装）
        shutil.rmtree(temp_dir)  # upload一時フォルダの削除
        _, file_list = default_storage.listdir(
            os.path.join(settings.MEDIA_ROOT, "excel", user_name))
        message = "正常終了しました。"
        context = {
            'file_list': file_list,
            'user_name': user_name,
            'message': message,
        }
        return render(self.request, 'pdfmr/complete.html', context)

    def form_invalid(self, form):
        return render(self.request, 'pdfmr/upload_form.html', {'form': form})
