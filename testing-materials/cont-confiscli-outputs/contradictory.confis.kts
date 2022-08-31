"""Parties"""

val alice by party( 
		named = "  alice"
)
"""Things"""

val cookie by thing ( 
		named = "cookie"
)
"""Actions"""

val eat by action( 
		named = "eat"
)
"""Clauses"""

"""1"""
alice may eat(cookie)
""" with yet untranslatable conditions """ 
"""eat cookie except under the following  circumstances     with Commercial purpose""" 

"""2"""
alice mayNot eat(cookie)

