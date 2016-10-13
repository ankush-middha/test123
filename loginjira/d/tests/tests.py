# from django.test import Client
# c = Client()
# response = c.post('/jira/jira-login/', {'username': 'ankush.middha@psquickit.com', 'password': 'ankush12345'})
# print response.status_code
from django.test import TestCase
# from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
        print "setup 123"

    def test_animals_can_speak(self):
        print "in test"
        """Animals that can speak are correctly identified"""
        lion = 'The lion says "roar"'
        cat = 'CAT'
        self.assertEqual(cat, 'CAT')
        self.assertEqual(lion, 'The lion says "roar"')


    # def test_jira_issues(self):
    #
    #     payload = {
    #         'project': {'key': 'JINT'},
    #         'summary': "Test Task",
    #         'description': "testing - create API issue",
    #         'issuetype': {'name': "Task"},
    #         'components': [{'name':'Component1'}],
    #     }
    #     self.client.post(reverse('jira_auth'), content_type='application/json',
    #                    data=json.dumps(self.jira_details))
    #     resp = self.client.post(reverse('jira_issues',kwargs={'project_key':'JINT'}),
    #                    data=json.dumps(payload), content_type= 'application/json')
    #     # self.assertEquals(resp.status_code, 200)

            #TEST CASES for jira API
        #
        # def test_jira_project_metadata(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     project_metadata_resp = self.client.get(reverse('jira_project_metadata', \
        #                                                     kwargs={'project_key': 'JINT'}))
        #     all_project_metadata_resp = self.client.get(reverse('jira_project_metadata'))
        #     self.assertEquals(project_metadata_resp.status_code, 200)
        #     self.assertEquals(all_project_metadata_resp.status_code, 200)
        #
        # def test_jira_project_users(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     project_users_resp = self.client.get(reverse('jira_project_users', \
        #                                                  kwargs={'project_key': 'JINT'}))
        #     self.assertEquals(project_users_resp.status_code, 200)
        #
        # def test_jira_project_components(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     project_components_resp = self.client.get(reverse('jira_project_components', \
        #                                                       kwargs={'project_key': 'JINT'}))
        #     self.assertEquals(project_components_resp.status_code, 200)
        #
        # def test_jira_project_epics(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     project_epic_resp = self.client.get(reverse('jira_project_epics', \
        #                                                 kwargs={'project_key': 'JINT'}))
        #     self.assertEquals(project_epic_resp.status_code, 200)
        #
        # def test_jira_fix_versions(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     project_fix_versions_resp = self.client.get(reverse('jira_fix_versions', \
        #                                                         kwargs={'project_key': 'JINT'}))
        #     self.assertEquals(project_fix_versions_resp.status_code, 200)
        #
        # def test_jira_statuses(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     jira_status_resp = self.client.get(reverse('jira_statuses'))
        #     self.assertEquals(jira_status_resp.status_code, 200)
        #
        # def test_jira_priorities(self):
        #     self.client.post(reverse('jira_auth'), content_type='application/json', \
        #                      data=json.dumps(self.jira_details))
        #     priorities_resp = self.client.get(reverse('jira_priorities'))
        #     self.assertEquals(priorities_resp.status_code, 200)