"""Parties"""

val alice by party( 
		named = "Alice Liddell"
)
"""Things"""

val bobby by thing ( 
		named = "Bobby"
)
"""Actions"""

val pay by action( 
		named = "pay"
)
val notify by action( 
		named = "notify"
)
val notify by action( 
		named = "Notify"
)
"""Clauses"""

"""1"""
alice must pay(bobby)

"""2"""
alice must pay(bobby)
""" with yet untranslatable conditions """ 
"""pay Bobby     with Internal purpose   """ 

"""3"""
alice may notify(bobby)

"""4"""
alice may notify(bobby)
""" with yet untranslatable conditions """ 
"""notify Bobby under the following circumstances    """ 
"""Alice did pay Bobby""" 
"""pay Bobby    with Commercial purpose   """ 

"""5"""
alice mayNot notify(bobby)

"""6"""
alice mayNot notify(bobby)
""" with yet untranslatable conditions """ 
"""notify Bobby except under the following  circumstances""" 

