module propensity_scoring
using CSV
using DataFrames

df = DataFrame(CSV.File("../marketing_data.csv"))
display(first(df,5))

end # module
