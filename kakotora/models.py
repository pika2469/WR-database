from django.db import models

# Create your models here.
class ModelName(models.Model):
    product_name = models.CharField("製品名", max_length=100)
    model_name = models.CharField("モデル名", max_length=100)
    design_site = models.CharField("設計拠点", max_length=100, blank=True, null=True)
    MPAN_date = models.DateField("MPAN年月", blank=True, null=True)

    class Meta:
        verbose_name = "モデル情報"
        verbose_name_plural = "モデル情報"
        ordering = ["product_name", "model_name"]
    
    def __str__(self):
        return f"{self.product_name} - {self.model_name}"

class Kakotora(models.Model):
    product_name = models.ForeignKey(
        'ModelName',
        on_delete=models.CASCADE,
        related_name='kakotora_products',
        verbose_name='製品名'
    )
    model_names = models.ManyToManyField(
        'ModelName',
        related_name='kakotora_models',
        verbose_name='モデル名'
    )

    title = models.CharField("タイトル", max_length=200)
    category = models.CharField("カテゴリ", max_length=50)
    status = models.CharField("ステータス", max_length=50)

    content = models.JSONField("内容", blank=True, null=True)
    mechanism = models.JSONField("メカニズム", blank=True, null=True)
    cause_occurrence = models.JSONField("発生原因", blank=True, null=True)
    cause_outflow = models.JSONField("流出原因", blank=True, null=True)
    temporary_action = models.JSONField("暫定対策", blank=True, null=True)
    permanent_action = models.JSONField("恒久対策", blank=True, null=True)
    horizontal_deployment = models.JSONField("水平展開", blank=True, null=True)

    # 参考資料
    reference_link = models.URLField("参考リンク", blank=True, null=True)
    reference_path = models.CharField("参考パス", max_length=255, blank=True, null=True)
    reference_file = models.FileField("参考ファイル", upload_to='reference_files/', blank=True, null=True)

    created_at = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    class Meta:
        verbose_name = "過去トラ"
        verbose_name_plural = "過去トラ"
        ordering = ["-updated_at"]
    
    def __str__(self):
        return f"{self.product_name} - {self.title}"