"""Parties"""

val licensee by party( 
		named = "the Licensee"
)
"""Things"""

val data by thing ( 
		named = "the Data"
)
val member by thing ( 
		named = "Another member"
)
val licence by thing ( 
		named = " this Licence"
)
val services by thing ( 
		named = "services"
)
"""Actions"""

val transfer by action( 
		named = "transfer"
)
val sell by action( 
		named = "sell"
)
val provide by action( 
		named = "provide"
)
val adapt by action( 
		named = "adapt"
)
val become by action( 
		named = "become"
)
val access by action( 
		named = "access"
)
"""Clauses"""

"""1"""
licensee mayNot transfer(licence)
""" with yet untranslatable conditions """ 
"""transfer this Licence except under the    following circumstances""" 

"""2"""
licensee may transfer(licence)
""" with yet untranslatable conditions """ 
"""transfer this Licence under the following  circumstances""" 

"""3"""
licensee mayNot sell(data)

"""4"""
licensee mayNot sell(data)

"""5"""
licensee mayNot provide(services)
""" with yet untranslatable conditions """ 
"""provide services with the Data   a  rd party may access the Data under the following  circumstances     with the consent from the Licensee    only after a  rd party did agree to this Licence    only after a  rd party did agree to a confidentiality  agreement  the Licensee may not copy or adapt the Data except under the  following circumstances     with the consent from the Library    with Internal purpose""" 

"""6"""
licensee may adapt( )
""" with yet untranslatable conditions """ 
"""adapt the Data under the following  circumstances""" 

"""7"""
licensee may become(member)

"""8"""
group may access(data)
""" with yet untranslatable conditions """ 
"""access the Data  under the following circumstances     only after the Licensee did become a member of a Joint  Venture Group    only after a member of a Joint Venture Group did become  a member of a Joint Venture Group    with the consent""" 
"""agree to  this Licence""" 

