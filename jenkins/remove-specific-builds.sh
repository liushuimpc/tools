
###### NOTE: Another way is Jenkins - > Manage Jenkins -> Jenkins CLI ######


#Remove the range build history of a job in Jenkins
## Jenkins - > Manage Jenkins -> Script Console

def jobName = "my_test_job"

def buildRange = "20-40"

import jenkins.model.*;
import hudson.model.Fingerprint.RangeSet;
def j = jenkins.model.Jenkins.instance.getItem(jobName);

def r = RangeSet.fromString(buildRange, true);

j.getBuilds(r).each { it.delete() }
