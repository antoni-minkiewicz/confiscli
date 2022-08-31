"""Parties"""

val bob by party( 
		named = "bob"
)
"""Things"""

val cake by thing ( 
		named = "cake"
)
"""Actions"""

val eat by action( 
		named = "eat"
)
"""Clauses"""

"""1"""
bob may eat(cake)
""" with yet untranslatable conditions """ 
"""eat cake except under the following circumstances     from            to            inclusive""" 

