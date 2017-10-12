# Jenkins2TestrailSync
Sync test results from Jenkins to TestRail

testrail_2.py & testrail_3.py are the original TestRail API with minor tweak in APIError.
testrail_flow.py contains higher level generic method for TestRail API
jenkins_flow.py contains higher level generic method for Jenkins API

testFetchURL.py is the sketch to exercise using the APIs, it currently pull the latest Android HP Smart BAT result from Jenkins and push it to TestRail.
