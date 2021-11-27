
function imported()
    println("Hello from Julia!")
end

using Arrow
using CSV
using DataFrames
using Statistics

BASE_PATH = "./data/"

"""
    Loads a CSV file into a DataFrame.

    :param path: The path to the CSV file.
    :param name: The name of the DataFrame.
    :param builder: The builder to use.
    :param from_txt: Whether to read the file as a text file.
    :param rebuild: Whether to rebuild the DataFrame.
    :return: The DataFrame.
"""
function load_csv(path, name, builder; from_txt=true, rebuild=false)
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

function load_arrow(path, name, builder; from_txt=true, rebuild=false)
    arrow_path = string(path, name, ".arrow")

    if !isfile(arrow_path)
        df = load_csv(path, name, builder; from_txt=from_txt, rebuild=rebuild)
        Arrow.write(arrow_path, df)
        return df
    end

    df = DataFrame(Arrow.Table(arrow_path))
    return df
end

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
	return load_arrow(path, "def", build_def)
end

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
	return load_arrow(path, "etym", build_etym)
end

function clean_etym(df)
	fdf = filter(:lang => ==("eng"), df)
	gdf = groupby(fdf, [:word])
	return combine(gdf, :etym => first => :etym)
end


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

function load_dataset(;path=BASE_PATH)
	function build_dataset()
        println("Loading Etymology Dataset...")
		edf = load_etym()
        println("Loading Definition Dataset...")
		ddf = load_def()

        println("Cleaning Etymology Dataset...")
		cedf = clean_etym(edf)
        println("Cleaning Definition Dataset...")
		cddf = clean_def(ddf)

        println("Combining Datasets...")
		return innerjoin(cedf, cddf, on=:word)
	end
	return load_arrow(path, "final", build_dataset; from_txt=false)
end

# EXPORTS
export(load_dataset)
