from django.conf.urls import url, include, patterns
from .views import JiraLogin, CreateBug, get_fix_versions, jira_project_epics, add_comments, jira_project_users

urlpatterns=patterns('',
    url(r'^jira-login/$', JiraLogin.as_view(), name='jira-login'),
    url(r'^createbug/$', CreateBug.as_view(), name='createbug'),
    url(r'^projects/(?P<project_key>\w+)/fix-versions/?', get_fix_versions, name='get-fix-versions'),
    url(r'^projects/(?P<project_key>[-\w]+)/epics/?', jira_project_epics, name='jira_project_epics'),
    url(r'^projects/(?P<issue_key>[-\w]+)/comments/?', add_comments, name='add_comment'),
    url(r'^projects/(?P<project_key>[-\w]+)/users/?', jira_project_users, name='jira_users'),
)


