from django import forms
from .models import ModelName, Kakotora

class KakotoraFilterForm(forms.Form):
    # フィールド定義
    product = forms.ChoiceField(label="製品名", required=False)
    category = forms.ChoiceField(label="カテゴリ", required=False)
    status = forms.ChoiceField(label="ステータス", required=False)

    # 親クラス(Django Form)の初期化処理を実行して、生成したFormにfieldsを設定する
    # この処理を行わないとself.fieldsのように呼び出してもエラーが出てします
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 生成したfieldsに設定を追加
        # 製品名：Modelnameからdistinct
        product_names = (
            ModelName.objects
            .values_list("product_name", flat=True)
            .distinct()
            .order_by("product_name")
        )
        self.fields["product"].choices = [("", "すべて")] + [(p, p) for p in product_names]

        # カテゴリはKakotoraからdistinct
        categories = (
            Kakotora.objects
            .exclude(category__isnull=True)
            .exclude(category__exact="")
            .values_list("category", flat=True)
            .distinct()
            .order_by("category")
        )
        self.fields["category"].choices = [("", "すべて")] + [(c, c) for c in categories]

        # ステータスもKakotoraからdistinct
        statuses = (
            Kakotora.objects
            .exclude(status__isnull=True)
            .exclude(status__exact="")
            .values_list("status", flat=True)
            .distinct()
            .order_by("status")
        )
        self.fields["status"].choices = [("", "すべて")] + [(s, s) for s in statuses]

        # フィールドにTailwind CSSを適用
        for f in self.fields.values():
            f.widget.attrs.update({
                "class": "border-gray-300"
            })

