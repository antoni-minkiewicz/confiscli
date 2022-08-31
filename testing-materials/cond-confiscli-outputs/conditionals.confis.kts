"""Parties"""

val ana by party( 
		named = "ana"
)
val bob by party( 
		named = "bob"
)
"""Things"""

val cookie by thing ( 
		named = " the cookie"
)
val cake by thing ( 
		named = "cake"
)
"""Actions"""

val eat by action( 
		named = "eat"
)
"""Clauses"""

"""1"""
bob may eat(cookie)

"""2"""
ana may eat(cake)
""" with yet untranslatable conditions """ 
"""eat cake under the following circumstances""" 

