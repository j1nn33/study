// проверяет наличие пробелов в заданиях (название задания это его путь )
jenkins.model.Jenkins.instance?.
  getAllItems()?.
  findAll { it.name.contains(' ') }?.
  each {
    println "'${it.fullName}' remove space from name"
  }

println ''