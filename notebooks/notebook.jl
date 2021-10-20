### A Pluto.jl notebook ###
# v0.16.3

using Markdown
using InteractiveUtils

# ╔═╡ 4df79bd4-d5db-4bcf-8728-2fb3bbd9a657
begin
	import Pkg
	Pkg.activate("../.")
	using DataFrames
	using CSV
	using Statistics
end

# ╔═╡ 11b67007-f893-47e9-b2b7-28f8e7e0a865
BASE_PATH = "../data/"

# ╔═╡ f4fdf007-5662-4310-9d34-3f47278148a9
function load_csv(path, name, builder;from_txt=true, rebuild=false)
	csv_path = string(path, name, ".csv")
	
	if !isfile(csv_path) || rebuild
		if from_txt
			txt_path = string(path, name, ".txt")
			df = builder(txt_path)
		else
			df = builder()
		end
		
		CSV.write(csv_path, df)
		return dropmissing(df)
	end
		
	res = CSV.read(csv_path, DataFrame;types=String)
	return dropmissing(res)
end

# ╔═╡ d2a6afb9-7887-4617-aca8-00cbfe4e15a9
function load_def(;path=BASE_PATH)
	function build_def(path)
		res = DataFrame()
		for line in eachline(path)
			arr = split(line, '\t')

			lang = arr[1]
			word = arr[2]
			pos = arr[3]
			parser = arr[4]
			def = join(arr[5:end])

			row = DataFrame(
				lang=lang,
				word=word,
				pos=pos,
				def=def,
			)

			append!(res, row)
		end
		return res
	end
	return load_csv(path, "def", build_def)
end

# ╔═╡ 2f89a1c4-2c68-4251-8436-b37ef1fa2ed2
function load_etym(;path=BASE_PATH)
	function build_etym(path)
		res = DataFrame()
		for line in eachline(path)
			arr = split(line, '\t')

			lang = arr[1]
			word = arr[2]
			etym = string("[(", join(arr[5:end], ")("), ")]")

			row = DataFrame(
				lang=lang,
				word=word,
				etym=etym,
			)

			append!(res, row)
		end
		return res
	end
	return load_csv(path, "etym", build_etym)
end

# ╔═╡ 7b8e6d2f-1e65-4647-93ac-649e765455b5
function clean_etym(df)
	fdf = filter(:lang => ==("eng"), df)
	gdf = groupby(fdf, [:word])
	return combine(gdf, :etym => first => :etym)
end

# ╔═╡ d28976f1-c1e3-4f1a-a2c5-4eb81fe9875d
function clean_def(df)
	function clean_def_group(x)
		function max_entries(x, num)
			# limit number of entries in x to num
			if size(x)[1] > num
				return x[1:num]
			end
			return x
		end
		
		# limit to three definitions per word
		x = max_entries(x, 3)
		
		return x
	end
	
	# filter non-english
	fdf = filter(:lang => ==("eng"), df)
	
	# remove proper pronouns
	pdf = filter(:pos => !=("Proper noun"), fdf)
	
	# remove definition contexts
	reg = r"{{.*}}\s"
	rdf = transform(pdf, :def => ByRow(x -> replace(x, reg=>"")) => :def)
	
	# apply clean_def_group function to each word group
	gdf = groupby(rdf, [:word])
	return combine(gdf, :def => (x -> clean_def_group(x)) => :def)
end

# ╔═╡ 99908e74-1516-450f-9977-309b9b2fc938
function load_dataset(name;path=BASE_PATH)
	function build_dataset()
		edf = load_etym()
		ddf = load_def()

		cedf = clean_etym(edf)
		cddf = clean_def(ddf)
		return innerjoin(cedf, cddf, on=:word)
	end
	return load_csv(path, "final", build_dataset; from_txt=false)
end

# ╔═╡ 0737d9fd-3c0e-4aa5-a474-38b7bfac2045
final = load_dataset("final")

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
# ╠═4df79bd4-d5db-4bcf-8728-2fb3bbd9a657
# ╠═11b67007-f893-47e9-b2b7-28f8e7e0a865
# ╠═f4fdf007-5662-4310-9d34-3f47278148a9
# ╠═d2a6afb9-7887-4617-aca8-00cbfe4e15a9
# ╠═2f89a1c4-2c68-4251-8436-b37ef1fa2ed2
# ╠═7b8e6d2f-1e65-4647-93ac-649e765455b5
# ╠═d28976f1-c1e3-4f1a-a2c5-4eb81fe9875d
# ╠═99908e74-1516-450f-9977-309b9b2fc938
# ╠═0737d9fd-3c0e-4aa5-a474-38b7bfac2045
# ╠═b87aef52-3a0c-4f35-9b9f-75f201a8aeaf
# ╠═5bb3bf23-e382-4d8c-b369-8441accb3793
# ╠═8b0c5a9e-b243-45e3-85a0-8841574b14ed
# ╠═a22934f9-d54f-4a5b-a714-530c150d1656
# ╠═75e8debb-dab3-4733-9586-5c081e817f5c
