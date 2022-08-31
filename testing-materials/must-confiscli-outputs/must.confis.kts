"""Parties"""

val bob by party( 
		named = "bob"
)
"""Things"""

val alice by thing ( 
		named = "  alice"
)
"""Actions"""

val pay by action( 
		named = "pay"
)
"""Clauses"""

"""1"""
bob must pay(alice)
""" with yet untranslatable conditions """ 
"""pay alice       from            to            inclusive""" 

