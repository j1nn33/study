// Какие pipeline не имеют build description
jenkins.model.Jenkins.instance?.
  getAllItems()?.
  findAll { !it.getDescription() }?.
  each {
    println "'${it.fullName}' does not explain what it does ..."
  }

println ''