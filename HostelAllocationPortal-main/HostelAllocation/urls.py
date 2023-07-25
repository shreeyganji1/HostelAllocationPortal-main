from argparse import Namespace
from django.contrib import admin
from django.urls import path
from MainSite import views
from django.urls import include, re_path
from django.conf import settings


urlpatterns =[
    path('admin/', admin.site.urls),
    path('', views.home, name='register'),
    path('login/', views.user_login, name='login'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('warden_login/', views.warden_login, name='warden_login'),
    path('warden_login/leave', views.leave_admin, name='leave_admin'),
    path('warden_login/student_leaves/<int:std_id>/', views.student_leaves, name='student_leaves'),
    path('warden_login/leave_confirm/<int:lv_id>/', views.leave_confirm, name='leave_confirm'),
    path('warden_login/leave_reject/<int:lv_id>/', views.leave_reject, name='leave_reject'),
    path('present_leaves/', views.present_leaves, name='present_leaves'),
    path('warden_profile/', views.warden_profile, name='warden_profile'),
    path('warden_dues/', views.warden_dues, name='warden_dues'),
    path('document_verification/', views.document_verification, name='document_verification'),
    path('warden_add_due/', views.warden_add_due, name='warden_add_due'),
    path('warden_remove_due/', views.warden_remove_due, name='warden_remove_due'),
    path('login/upload/', views.upload, name='upload'),
    path('login/select/', views.select, name='select'),
    path('repair/', views.repair, name='repair'),
    path('logout/', views.logout_view, name='logout'),
    path('login/leave', views.user_leave, name='leave_status'),
    path('upload/', views.upload, name='upload'),
]
