"""Parties"""

val seller by party( 
		named = "the Seller"
)
val buyer by party( 
		named = "the Buyer"
)
"""Things"""

val contract by thing ( 
		named = " the Contract"
)
"""Actions"""

val reveal by action( 
		named = "reveal"
)
"""Clauses"""

"""1"""
seller mayNot reveal(contract)
""" with yet untranslatable conditions """ 
"""reveal the Contract under the following  circumstances     from            to            inclusive""" 

"""2"""
buyer mayNot reveal(contract)
""" with yet untranslatable conditions """ 
"""reveal the Contract under the following  circumstances     from            to            inclusive""" 

