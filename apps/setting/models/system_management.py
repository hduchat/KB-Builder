# coding=utf-8


from django.db import models

from common.mixins.app_model_mixin import AppModelMixin


class SettingType(models.IntegerChoices):
    """系统设置类型"""
    EMAIL = 0, '邮箱'

    RSA = 1, "私钥秘钥"


class SystemSetting(AppModelMixin):
    """
     系统设置
    """
    type = models.IntegerField(primary_key=True, verbose_name='设置类型', choices=SettingType.choices,
                               default=SettingType.EMAIL)

    meta = models.JSONField(verbose_name="配置数据", default=dict)

    class Meta:
        db_table = "system_setting"
