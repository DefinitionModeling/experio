
function open_file(path)
    f = open(path, "r")
    s = read(f, String)
    close(f)
    return s
end
