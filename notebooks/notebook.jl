### A Pluto.jl notebook ###
# v0.16.1

using Markdown
using InteractiveUtils

# ╔═╡ 11b67007-f893-47e9-b2b7-28f8e7e0a865
function extract_data(path)
	for line in eachline(path)
		arr = split(line, '\t')
		return arr
	end
end

# ╔═╡ e14bb891-7912-474c-9fd3-7aafea58ecf3
extract_data("../data/def.text")

# ╔═╡ Cell order:
# ╠═11b67007-f893-47e9-b2b7-28f8e7e0a865
# ╠═e14bb891-7912-474c-9fd3-7aafea58ecf3
