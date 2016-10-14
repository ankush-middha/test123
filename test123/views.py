# Test 
from django.shortcuts import render
from django.views.generic import View, TemplateView
from django.http import HttpResponse, HttpResponseRedirect
# import jira.client
# from jira.client import JIRA
from jira.exceptions import JIRAError
import json

def login_to_jira(options, username, password):


    import pdb; pdb.set_trace()
    

    try:   
        JIRA(options, basic_auth=(username, password))


    except Exception as e:

        print e 
    return JIRA(options, basic_auth=(username, password))


class JiraLogin(View):
    '''
    Class to login on Jira & get appropriate values.
    Take username password and hit post request.
    user jira module to connect with JiraAPi.
    '''

    def get(self, request):
        issue_type = all_users = {}
        if 'all_users' in request.session:
            all_users = request.session['all_users']
        if 'issue_type' in request.session:
            issue_type = request.session['issue_type']
        return render(request, "load_data.html", {'issues': issue_type, 'assignee': all_users })

    def post(self, request):
        # options = {'server': 'https://logglyu.jira.com/'}
        # options = {'server': 'https://jira-jira.atlassian.net'}
        options = {'server': 'https://gongio.atlassian.net'}
        username = 'eilon.reshef+loggly@gong.io' # request.POST['username']
        password = 'loggly123' #request.POST['password']

        try:
            jira_obj = login_to_jira(options, username, password)
            # jira_obj.project('key=sefs')
        except JIRAError as e:

            print str(e)
            return HttpResponse(e)

        # project_data, issue_type = self.get_issue_types(jira_obj)
        all_users = self.get_all_assignee(jira_obj)

        #set issue and users in session for get method
        # request.session['issue_type'] = issue_type
        # request.session['all_users'] = all_users
        return render(request,"load_data.html",{'projects': project_data, 'issues': issue_type, 'assignee': all_users })

    def get_issue_types(self,jira):
        issue_type ={}
        project_data = {}
        all_projects = jira.projects()  # show all projects of Logged in user

        for proj in all_projects:
            project_data[int(proj.id)] = str(proj.name)

        for proj in all_projects:
            issue_type[str(proj.name)] = [str(name.name) for name in jira.project(id=proj.id).issueTypes]
        return project_data, issue_type

    def get_all_assignee(self, jira_obj):
        all_users = {}
        assignee_obj= jira_obj.search_assignable_users_for_projects('', 'JINT', maxResults=False)
        # assignee_obj = jira_obj.search_users(user='%')
        for assignee in assignee_obj:
            all_users[assignee.key] = assignee.name
        return all_users

import requests
class CreateBug(View):
    '''
    class to create bug/task on Jira
    '''
    def post(self, request):

        # Login to jira
        # options = {'server': 'https://loggly.jira.com'}
        options = {'server': 'https://datami2.atlassian.net'}
        username = 'ankush.middha@psquickit.com' #'amiddha@loggly.com' #
        password = 'ankush12345'#''ankush54321'
        try:
            jira_obj = login_to_jira(options, username, password)
        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))

        # Get data from submit Form
        import pdb;
        pdb.set_trace()
        proj_id = request.POST['project_name'].split(',')[0]
        desc = request.POST['description']
        summary = request.POST['summery']
        issue_type = request.POST['issue_type']
        assignee = request.POST['assignee']

        # epic_dict = project_wise_epics(jira_obj)
        # create new bug/issue
        try:
            issue_dict = {
                'project': {'key': 'JINT'},
                'summary': "test 123",
                'description': "the description",
                'issuetype': {'namef': "Task" },
                # 'components': [{'name':'Component1'}],
                # 'custom123':'let me see',
            }
            new_issue = jira_obj.create_issue(fields=issue_dict)

        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
        # assign newly created issue to some user
        try:
            jira_obj.assign_issue(new_issue,assignee)
        except JIRAError as e:
            print e
            return HttpResponse('error in assigning new issue')

        try:
            jira_obj.add_issue_to_epic('epic_id',['issue_id'])
        except:
            "error"

        return HttpResponse('All done, cheersss!!!')

    def get(self, request):
        print 'in Get'
        api = 'https://loggly.jira.com/rest/api/2/issue/picker?currentIssueKey=jint-12&projectId=12300'
        username = 'amiddha@loggly.com'
        password = 'ankush54321'
        result = requests.get(api, auth=(username,password))
        print result.text
        return HttpResponse(result.text)



def project_wise_epics(jira_obj):
    '''
    take jira object and return dictionary in below given format
    {'project1':[(epic1_id,epic1_name), (epic2_id,epic2_name)], 'project2':[(epic_id, epic_name)] }
    '''

    project_wise_epic = {}
    projects_without_epic=[]
    all_projects = jira_obj.projects()  # get all projects

    for proj in all_projects:  # Exclude projects where issueType is not Epic
        projects_without_epic += [proj for proj_data in jira_obj.project(id=proj.id).issueTypes
                                 if proj_data.name == 'Epic']

    for proj in projects_without_epic:
        project_wise_epic[str(proj.name)] = [epic.id for epic in jira_obj.search_issues('project=%s'%proj.id)
                                           if epic.raw['fields']['issuetype']['name'] == 'Epic']
    return project_wise_epic

from  django.http import HttpResponseBadRequest
def get_fix_versions(request, project_key=None):
    '''
    method to fetch project wise Fix version list
    '''
    options = {'server': 'https://jira-jira.atlassian.net'}
    username = 'ankush.middha@psquickit.com'  # 'amiddha@loggly.com' #
    password = 'ankush12345'  # ''ankush54321'
    if request.method == 'POST':
        try:
            jira_obj = login_to_jira(options, username, password)
            versions = jira_obj.project(project_key).versions
            version_list = [{'id':version.id, 'name':version.name} for version in versions]
            print version_list
            return HttpResponse(version_list, status=200)

        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
        except Exception as e:
            return HttpResponse(status=500, reason=str(e))
    return HttpResponseBadRequest()
    # return HttpResponse(status=400)


def add_comments(request, issue_key=None):

    options = {'server': 'https://loggly.jira.com'}
    username = 'amiddha@loggly.com'
    password = 'ankush54321'

    try:
        jira_obj = login_to_jira(options, username, password)
    except JIRAError as e:
        return HttpResponse(status=e.status_code, reason=str(e))
    import pdb;
    pdb.set_trace()
    issue_obj = jira_obj.issue(issue_key)
    jira_obj.add_comment('issue_key', 'comment_text')

    #get previosly added comments
    if request.method == 'GET':
        comments = issue_obj.fields.comment.comments
        print comments
    elif request.method == 'POST':
        jira_obj.add_comment('issue_key','comment_text')


    # GET AND UPDATE DESCRIPTION
    issue_obj = jira_obj.issue(issue_key)
    old_desc = issue_obj.fields.description
    issue_obj.update(description=old_desc +' UPDATED-DESCRIPTION')

    #link an issue
    issue = jira.issue('JINT-12')
    issue2 = jira.issue('JINT-16')
    jira.add_remote_link(issue, issue2)


def jira_project_users(request, project_key=None):
    if request.method == 'GET':
        try:
            print "@1231231231231"
            options = {'server': 'https://loggly.jira.com'}
            username = 'amiddha@loggly.com'
            password = 'ankush54321'


            import pdb; pdb.set_trace()
            jira  = login_to_jira(options, username, password)
            user_list = jira.search_assignable_users_for_projects('', project_key, maxResults=False)

            users = [user.raw for user in user_list]
            return HttpResponse(json.dumps(users), status=200)
        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
    return HttpResponseBadRequest()


def jira_project_epics(request, project_key=None):
    '''
    method to fetch project wise Fix version list
    '''
    options = {'server': 'https://loggly.jira.com'}
    username = 'amiddha@loggly.com'
    password = 'ankush54321'

    # options = {'server': 'https://jira-jira.atlassian.net'}
    # username = 'ankush.middha@psquickit.com'
    # password = 'ankush12345'

    if request.method == 'POST':
        try:
            jira_obj = login_to_jira(options, username, password)
        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
        #     epic_list = [{'id':epic.id, 'name':epic.raw['fields']['summary'], 'key':epic.key}
        #                    for epic in jira_obj.search_issues('project=%s' % project_key)
        #                      if epic.raw['fields']['issuetype']['name'] == 'Epic']
        #     print epic_list
        #     # print project_wise_epic
        #     import pdb;
        #     pdb.set_trace()
        # except JIRAError as e:
        #     return HttpResponse(status=e.status_code, reason=str(e))
        # except Exception as e:
        #     return HttpResponse(status=500, reason=str(e))
        import pdb; pdb.set_trace()
        payload = {
            'project': {'key': 'JINT'},
            'summary': "test 123",
            'description': "the description",
            'issuetype': {'name': "Task" },  # Get data from request
            # 'epic_id':1201
            }
        epic_id = None
        if 'epic_id' in payload:
            epic_id = payload.pop('epic_id')

        try:  # create new bug/issue with all the data
            new_issue = jira_obj.create_issue(fields=payload)
            if epic_id:  # Link issue to epic
                jira_obj.add_issues_to_epic(epic_id, [new_issue.id])
        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
        except Exception as e:
            return HttpResponse(status=500, reason=str(e))
    return HttpResponse(status=400)


# jira.models.py
# def create_or_update(self, **kwargs):
#     customer = kwargs.get('customer')
#     jira_auth_setting = JiraIntegrationSettings.objects.filter(customer_id=customer)
#     kwargs['modified_at'] = timezone.now()
#     if jira_auth_setting:
#         # update jira integration object with new settings
#         jira_auth_setting.update(**kwargs)
#     else:
#         # create new jira integration object
#         self.create(**kwargs)
#
class A(View):
    def let(self):
        print 123


# Inherit jira class to my local class & test
from jira import JIRA
class TestInheritJira(JIRA):
    '''
    class to inherit JIRA base class.
    '''

    def __init__(self, options=None, basic_auth=None, oauth=None, async=None):
        JIRA.__init__(
            self, options=options, basic_auth=basic_auth, oauth=oauth, async=async)

    def test_func(self):
        return "working!"

    def search_jira_issues(request, url, user_name, password, search_key=None):
        '''
        method to search & fetch jira issues based on searchKey entered by user.
        Uses issuePicker rest API of JIRA to get response.
        '''
        try:
            JIRA_API_ISSUE_SEARCH_URL = "/rest/api/2/issue/picker?showSubTasks=true&showSubTaskParent=true&query="
            url_path = "{}{}{}".format(url, JIRA_API_ISSUE_SEARCH_URL, search_key)
            resp = requests.get(url_path, auth=(user_name, password))
            return HttpResponse(resp.text, status=200)
        except JIRAError as e:
            return HttpResponse(status=e.status_code, reason=str(e))
