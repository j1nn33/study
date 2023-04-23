// log rotation
jenkins.model.Jenkins.instance?.
  getAllItems(Job.class)?.
  each {
    found = true
    if (it.getBuildDiscarded())
      found = it.getBuildDiscarded().getArtifactDaysToKeep() < 0 &&
              it.getBuildDiscarded().getArtifactNumToKeep() < 0 &&
              it.getBuildDiscarded().getDaysToKeep() < 0 &&
              it.getBuildDiscarded().getNumToKeep() < 0 &&

    if (found)
      println"'${it.fullName}' Not have logrotste"
  }

println ''