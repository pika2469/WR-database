from django.shortcuts import render
from django.views.generic import ListView
from .models import Kakotora
from .forms import KakotoraFilterForm
from django.http import QueryDict

# Create your views here.
class KakotoraListView(ListView):
    model = Kakotora
    template_name = 'kakotora/kakotora_list.html'
    context_object_name = 'kakotoras'

    # ソート対象フィールドのマッピング
    ORDER_FIELD_MAP = {
        "title": "title",
        "product": "product_name__product_name",
        "category": "category",
        "status": "status",
    }

    # ListViewのget()関数内の処理をオーバーライド
    def get_queryset(self):
        qs = (
            Kakotora.objects
            .select_related("product_name")
            .prefetch_related("model_names")
            .all()
        )

        # -----フィルター-----
        form = KakotoraFilterForm(self.request.GET or None)
        if form.is_valid():
            product = form.cleaned_data.get("product")
            category = form.cleaned_data.get("category")
            status = form.cleaned_data.get("status")

            # フォームにフィルター条件が適用されている場合は処理
            if product:
                qs = qs.filter(product_name__product_name=product)
            if category:
                qs = qs.filter(category=category)
            if status:
                qs = qs.filter(status=status)
        
        # -----ソート-----
        # orderクエリを読み取り（例："-title")
        order = self.request.GET.get("order")
        if order:
            # orderクエリが-で始まっていたらTrue、そうでなければFalse⇒昇順/降順の判定に使う
            desc = order.startswith("-")
            # orderクエリから-を取り除いたものをkeyとする
            key = order[1:] if desc else order
            if key in self.ORDER_FIELD_MAP:
                field = self.ORDER_FIELD_MAP[key]
                qs = qs.order_by(f"-{field}" if desc else field)
        else:
            # orderクエリが存在しない場合は、デフォルトの並び順
            pass
        
        return qs

    # 並び替えの状況を取得
    # テンプレート用：各列の「次のorder値」「現在アクティブか」「向き」を返す。
    def _build_ordering_context(self, current_order: str | None):
        def next_order_for(field_key: str):
            if current_order == field_key:
                # 昇順⇒降順
                return f"-{field_key}"  
            if current_order == f"-{field_key}":
                # 降順⇒昇順
                return field_key
            return field_key
        
        # 列の選択有無と、その向きを返す
        def status_for(field_key: str):
            if current_order == field_key:
                return {"active": True, "dir": "asc"}
            if current_order == f"-{field_key}":
                return {"active": True, "dir": "desc"}
            return {"active":False, "dir": None}

        # 対象列分のソート条件をまとめて辞書型データとして出力
        # 例： "title":{"next": "title" or "-title", "active": True/False, "dir": "asc/desc/None"}
        fields = ["title", "product", "category", "status"]
        ordering = {}
        for f in fields:
            ordering[f] = {
                "next": next_order_for(f),
                **status_for(f),
            }
        return ordering



    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # フィルタフォーム作成
        ctx["filter_form"] = KakotoraFilterForm(self.request.GET or None)

        # 現在フィルタフォームに適用されているフィルタを辞書にまとめる（クエリパラメーターから取得）
        ctx["active_filters"] = {
            k: v for k, v in self.request.GET.items()
            if k in {"product", "category", "status"} and v
        }

        # フィルタだけ残してソート情報(order)を取り除いたクエリ文字列を作る
        # テンプレート側でフィルターを残したまま並び替えを実行するため
        q: QueryDict = self.request.GET.copy()
        q.pop("order", None)
        ctx["base_qs"] = q.urlencode()

        # ソート状態
        current_order = self.request.GET.get("order")
        ctx["ordering"] = self._build_ordering_context(current_order)

        return ctx
    