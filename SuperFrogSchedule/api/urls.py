from django.urls import path, include
from django.conf.urls import url
from .router import router
# from.views import AppearanceByStatusList

from .views import (
    list_by_status,
    appearances,
    detail,
    create,
    events_customer_monthly,
    getSuperfrog,
    getAdmin,
    signUp,
    list_by_status_list,
    login_view,
    logout_view,
    acceptAppearance,
    rejectAppearance,
    payroll_detail,
    payroll_appearance,
    email, 
    list_by_status_superfrog,
    generatePayroll,
    list_SuperfrogAppearance_by_Status,
    Appearance_to_Change, 
    update_appearance,
    superfrog_appearance_detail,
    )

urlpatterns = [
    url(r'^appearances/$', appearances),
    url(r'^appearances/status/(?P<status>\w+)/$', list_by_status),
    url(r'^appearances/(?P<id>\d+)/$', detail),
    url(r'^events/customer-monthly/(?P<year>\d+)/(?P<month>\d+)/$', events_customer_monthly),   
    url(r'^employee/(?P<id>\d+)/$', getSuperfrog),
    url(r'^get-admin/(?P<id>\d+)/$', getAdmin),
    url(r'^employeeAppearance/(?P<id>\d+)/(?P<sId>\d+)/$', signUp),
    url(r'^listAppearances/status/(?P<status>\w+)/(?P<sID>\d+)/$', list_by_status_list),
    url(r'^auth/login/$', login_view.as_view(), name='Login'),
    url(r'^auth/logout/$', logout_view.as_view(), name='Logout'),
    url(r'^adminAccept/(?P<id>\d+)/$',acceptAppearance),
    url(r'^adminReject/(?P<id>\d+)/$', rejectAppearance),
    url(r'^appearance/(?P<id>\d+)/$', payroll_detail),
    url(r'^SuperFrogappearance/status/(?P<status>\w+)/$', payroll_appearance),
    url(r'^email/', email),
    url(r'^landingAppearance/status/(?P<status>\w+)/(?P<sId>\d+)/$', list_by_status_superfrog),
    url(r'^payrollAppearances/(?P<SFAid>\d+)/(?P<adminID>\d+)/$', generatePayroll),
    url(r'^superfrogappearances/status/(?P<status>\w+)/$',list_SuperfrogAppearance_by_Status),
    url(r'^SuperFrogappearance/(?P<AID>\d+)/$', Appearance_to_Change),
    url(r'^updateAppearance/$', update_appearance),
    url(r'^superfrogappearancedetails/(?P<id>\d+)/$', superfrog_appearance_detail)
]
