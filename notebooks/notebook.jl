### A Pluto.jl notebook ###
# v0.16.1

using Markdown
using InteractiveUtils

# ╔═╡ 4df79bd4-d5db-4bcf-8728-2fb3bbd9a657
begin
	import Pkg
	Pkg.activate("../.")
	using DataFrames
end

# ╔═╡ 11b67007-f893-47e9-b2b7-28f8e7e0a865
function extract_etym(path)
	res = DataFrame()
	for line in eachline(path)
		arr = split(line, '\t')
		
		lang = arr[1]
		word = arr[2]
		etym = string("[(", join(arr[5:end], ")("), ")]")
		
		if lang != "eng"
			continue
		end
		
		row = DataFrame(
			word=word,
			etym=etym,
		)
		
		append!(res, row)
	end
	return res
end

# ╔═╡ b665ea7e-0530-4bf6-afe8-b84fc3cce3a4
function extract_def(path)
	res = DataFrame()
	for line in eachline(path)
		arr = split(line, '\t')
		
		lang = arr[1]
		word = arr[2]
		pos = arr[3]
		parser = arr[4]
		def = join(arr[5:end])
		
		if lang != "eng"
			continue
		end
		
		row = DataFrame(
			word=word,
			pos=pos,
			def=def,
		)
		
		append!(res, row)
	end
	return res
end

# ╔═╡ e14bb891-7912-474c-9fd3-7aafea58ecf3
begin
	etym_raw = "../data/etym.text"
	etym_df = extract_etym(etym_raw)
end

# ╔═╡ e9ddaa82-11e1-4bc2-98cd-ec01c881f343
begin
	def_raw = "../data/def.text"
	def_df = extract_def(def_raw)
end

# ╔═╡ 7b8e6d2f-1e65-4647-93ac-649e765455b5
function clean_etym(df)
	gdf = groupby(df, :word)
	return combine(gdf, :etym => join => :etym)
end

# ╔═╡ d4311972-a821-40be-982a-fb915d24ffce
etym_clean = clean_etym(etym_df)

# ╔═╡ d28976f1-c1e3-4f1a-a2c5-4eb81fe9875d
function clean_def(df)
	gdf = groupby(df, [:word, :pos])
	return combine(gdf, :def => join => :def)
end

# ╔═╡ dfbe48df-e71e-45f2-9f56-7f0e37a0fdc7
def_clean = clean_def(def_df)

# ╔═╡ 4a3f6b0f-2cb7-4fe1-a5f8-5b48c01101a8
innerjoin(etym_clean, def_clean, on=:word)

# ╔═╡ a4489e55-b75d-47f7-b404-17d86ece04f5
md"""
TODO:
1. drop proper nouns
2. remove curly braces from definition type
3. remove other types of definitions? recursive definitions?
4. concat definitions from every part of speech?
"""

# ╔═╡ Cell order:
# ╠═4df79bd4-d5db-4bcf-8728-2fb3bbd9a657
# ╠═11b67007-f893-47e9-b2b7-28f8e7e0a865
# ╠═b665ea7e-0530-4bf6-afe8-b84fc3cce3a4
# ╠═e14bb891-7912-474c-9fd3-7aafea58ecf3
# ╠═e9ddaa82-11e1-4bc2-98cd-ec01c881f343
# ╠═7b8e6d2f-1e65-4647-93ac-649e765455b5
# ╠═d4311972-a821-40be-982a-fb915d24ffce
# ╠═d28976f1-c1e3-4f1a-a2c5-4eb81fe9875d
# ╠═dfbe48df-e71e-45f2-9f56-7f0e37a0fdc7
# ╠═4a3f6b0f-2cb7-4fe1-a5f8-5b48c01101a8
# ╠═a4489e55-b75d-47f7-b404-17d86ece04f5
