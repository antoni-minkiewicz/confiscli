"""Parties"""

val alice by party( 
		named = "  alice"
)
"""Things"""

val bob by thing ( 
		named = "bob"
)
"""Actions"""

val hug by action( 
		named = "hug"
)
"""Clauses"""

"""1"""
alice may  (bob)

"""2"""
alice may  (bob)
""" with yet untranslatable conditions """ 
"""hug bob under the following circumstances     with Research purpose""" 

"""3"""
alice mayNot hug(bob)

"""4"""
alice mayNot hug(bob)
""" with yet untranslatable conditions """ 
"""hug bob under the following circumstances     with Commercial purpose""" 

