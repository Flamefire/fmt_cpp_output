from fmt_cpp_output import *

def testFiltering():
    assert cleanStd("std::__cxx11::basic_string<char>") == "string"
    assert cleanStd("boost::variant<int, foo, boost::detail::variant::void_, boost::detail::variant::void_>") == "boost::variant<int, foo>"
    assert cleanStd("std::__cxx11::basic_string<char>", stripSTD = False) == "std::string"

testCases = []
testCases.append(("tuple<int>", "tuple<int>"))
testCases.append(("tuple<const int>", "tuple<const int>"))
testCases.append(("tuple<int const>", "tuple<int const>"))
testCases.append(("tuple<int, int>", "tuple<int, int>"))
testCases.append(("tuple<const int, int>", "tuple<const int, int>"))
testCases.append(("tuple<int const, int>", "tuple<int const, int>"))
testCases.append(("tuple<int, int, int>", """
tuple<
  int,
  int,
  int
>"""))
testCases.append(("tuple<int, vector<int>>", """
tuple<
  int,
  vector<int>
>"""))
testCases.append(("tuple<tuple<int, vector<int>, int>, float>", """
tuple<
  tuple<
    int,
    vector<int>,
    int
  >,
  float
>"""))
testCases = [(x[0], x[1].lstrip("\n")) for x in testCases]

def testFormat():
    for case in testCases:
        print(case[0])
        assert formatTypeString(case[0]) == case[1]

def testFormatTypes():
    for case in testCases:
        assert formatTypes(case[0]) == "\n" + case[1]
    for case in testCases:
        assert formatTypes("foo const " + case[0]) == "foo \nconst " + case[1]
    bigCase = ["", ""]
    for case in testCases:
        bigCase[0] += case[0] + " "
        bigCase[1] += "\n" + case[1] + " "
    assert formatTypes(bigCase[0]) == bigCase[1]

