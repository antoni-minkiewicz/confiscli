

title = "Minimal example"

val alice by party(
    named = "Alice Lidell",
    description = "born 4 May 1852 in Westminster, London",
)

val bob by party
val licensingFee by thing(
    named = "Licensing fee for customer data",
    description = "10€ in cash"
)

val shareCustomerDataWith by action(
    named = "share the dataset relating to customer data with",
    description = "give a copy of the dataset",
)

val pay by action
val eat by action
val cookie by thing
val cake by thing

alice may { eat(cake) } asLongAs {
    within { (1 of January year 2022)..(31 of December year 2022)}
}

alice must { shareCustomerDataWith(bob) } underCircumstances {
    at { 10 of March year 2024}
}




