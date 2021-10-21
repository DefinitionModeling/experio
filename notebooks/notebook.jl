### A Pluto.jl notebook ###
# v0.16.3

using Markdown
using InteractiveUtils

# ╔═╡ 9ee29e42-20f2-4678-96ad-3ffaaa8fe1af
include("../experio/experio.jl")

# ╔═╡ 0737d9fd-3c0e-4aa5-a474-38b7bfac2045
final = load_dataset()

# ╔═╡ b87aef52-3a0c-4f35-9b9f-75f201a8aeaf
# number of definitions
num_def = size(final)[1]

# ╔═╡ 5bb3bf23-e382-4d8c-b369-8441accb3793
# vocabulary (unique)
vocab = size(unique(final, :word)[!, :word])[1]

# ╔═╡ 8b0c5a9e-b243-45e3-85a0-8841574b14ed
# average definitions per word
num_def/vocab

# ╔═╡ a22934f9-d54f-4a5b-a714-530c150d1656
# average etymology length
begin
	elengths = select(final, :etym => ByRow(x->length(x)) => :etym_length)
	mean(elengths[!, :etym_length])
end

# ╔═╡ 75e8debb-dab3-4733-9586-5c081e817f5c
# average definitions length
begin
	dlengths = select(final, :def => ByRow(x->length(x)) => :def_length)
	mean(dlengths[!, :def_length])
end

# ╔═╡ Cell order:
# ╠═9ee29e42-20f2-4678-96ad-3ffaaa8fe1af
# ╠═0737d9fd-3c0e-4aa5-a474-38b7bfac2045
# ╠═b87aef52-3a0c-4f35-9b9f-75f201a8aeaf
# ╠═5bb3bf23-e382-4d8c-b369-8441accb3793
# ╠═8b0c5a9e-b243-45e3-85a0-8841574b14ed
# ╠═a22934f9-d54f-4a5b-a714-530c150d1656
# ╠═75e8debb-dab3-4733-9586-5c081e817f5c
