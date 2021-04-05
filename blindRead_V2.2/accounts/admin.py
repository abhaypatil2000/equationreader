from django.contrib import admin
from accounts import models as acct_mdls
# Register your models here.

admin.site.register(acct_mdls.User)