"""Parties"""

val seller by party( 
		named = "the Seller"
)
val buyer by party( 
		named = "the Buyer"
)
"""Things"""

val goods by thing ( 
		named = "the Goods"
)
val contract by thing ( 
		named = "the Contract"
)
"""Actions"""

val give by action( 
		named = "give"
)
val deliver by action( 
		named = "deliver"
)
val terminate by action( 
		named = "terminate"
)
val reveal by action( 
		named = "reveal"
)
"""Clauses"""

"""1"""
seller must give(goods)
""" with yet untranslatable conditions """ 
"""pay for the Goods to the Seller  the Seller""" 

"""2"""
seller must deliver(goods)
""" with yet untranslatable conditions """ 
"""deliver the Goods to the Buyer""" 
"""pay for the Goods to the Buyer      from            to            inclusive""" 
"""pay for the Goods to the Buyer under the  following circumstances""" 
"""         """ 

"""3"""
buyer mayNot terminate(contract)
""" with yet untranslatable conditions """ 
"""terminate the Contract under the following    circumstances""" 
"""deliver the Goods to the Buyer""" 

"""4"""
seller mayNot reveal(contract)
""" with yet untranslatable conditions """ 
"""reveal the Contract under the following    circumstances     from            to            inclusive""" 

"""5"""
buyer mayNot reveal(contract)
""" with yet untranslatable conditions """ 
"""reveal the Contract under the following  circumstances     from            to            inclusive""" 

