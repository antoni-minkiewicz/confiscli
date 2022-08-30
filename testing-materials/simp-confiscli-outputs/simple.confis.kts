"""Parties"""

val alice by party( 
		named = "Alice Liddell"
)
val bob by party( 
		named = "Bob"
)
"""Things"""

val data by thing ( 
		named = " the Data"
)
"""Actions"""

val pay by action( 
		named = "pay"
)
val send by action( 
		named = "send"
)
"""Clauses"""

"""1"""
alice must pay(bob)

"""2"""
alice must pay(bob)
""" with yet untranslatable conditions """ 
"""pay Bob       from            to           """ 
"""          """ 

"""3"""
alice mayNot pay(bob)

"""4"""
alice mayNot pay(bob)
""" with yet untranslatable conditions """ 
"""pay Bob under the following circumstances""" 
"""Alice did pay Bob""" 

"""5"""
bob must send(data)

"""6"""
bob must send(data)
""" with yet untranslatable conditions """ 
"""Alice did pay Bob""" 
"""pay Bob      from            to            inclusive""" 

