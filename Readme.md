# C++ Error Formatter

[![Build Status](https://travis-ci.org/Flamefire/fmt_cpp_output.svg?branch=master)](https://travis-ci.org/Flamefire/fmt_cpp_output)

The goal of this python script is to provide readable C++ error messages.

Problem: Any error involving templates easily produces an unreadable mess and a "block of text". Even finding the actual causing code position is very hard.

Solution:

- Apply a filter to the types to make them more readable:
  - Remove `__cxx::11` namespace *- implementation detail*
  - Replace `basic_string<char>` by `string` *- who uses anything else as `string`?*
  - Remove `void_` from `boost::variant` (non-variadic) templates *- implementation detail*
  - Remove `std` namespace *-mostly it is clear, what a std:: type is*
- Reformat all templates adding newlines and indentation
- Colorize error messages and filenames

Example use:

`make |& colorizeTemplates.py`

This turns this:

	/usr/include/boost/variant/detail/apply_visitor_binary.hpp:168:1: note:   template argument deduction/substitution failed:
	/usr/include/boost/variant/detail/apply_visitor_binary.hpp: In substitution of ‘template<class Visitor, class Visitable1, class Visitable2> typename Visitor::result_type boost::apply_visitor(const Visitor&, Visitable1&, Visitable2&) [with Visitor = main()::<lambda(std::__cxx11::string)>; Visitable1 = boost::variant<boost::detail::variant::recursive_flag<int>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::vector<boost::recursive_variant_, std::allocator<boost::recursive_variant_> >, std::__cxx11::list<boost::recursive_variant_, std::allocator<boost::recursive_variant_> > >; Visitable2 = boost::variant<boost::detail::variant::recursive_flag<int>, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >, std::vector<boost::recursive_variant_, std::allocator<boost::recursive_variant_> >, std::__cxx11::list<boost::recursive_variant_, std::allocator<boost::recursive_variant_> > >]’:
	test.cpp:16:64:   required from here
	/usr/include/boost/variant/detail/apply_visitor_binary.hpp:168:1: error: no type named ‘result_type’ in ‘struct main()::<lambda(std::__cxx11::string)>’
	In file included from /usr/include/boost/variant/apply_visitor.hpp:18:0,
		             from /usr/include/boost/variant/detail/hash_variant.hpp:23,
		             from /usr/include/boost/variant/variant.hpp:34,
		             from /usr/include/boost/variant.hpp:17,
		             from test.cpp:5:


into this:

	/usr/include/boost/variant/detail/apply_visitor_binary.hpp:168:1: note:   template argument deduction/substitution failed:
	/usr/include/boost/variant/detail/apply_visitor_binary.hpp: In substitution of ‘
	template<
	  class Visitor,
	  class Visitable1,
	  class Visitable2
	> typename Visitor::result_type boost::apply_visitor(const Visitor&, Visitable1&, Visitable2&) [with Visitor = main()
	::<lambda(string)>; Visitable1 = 
	boost::variant<
	  boost::detail::variant::recursive_flag<int>,
	  string,
	  vector<
		boost::recursive_variant_,
		allocator<boost::recursive_variant_>
	  >,
	  list<boost::recursive_variant_>
	>; Visitable2 = 
	boost::variant<
	  boost::detail::variant::recursive_flag<int>,
	  string,
	  vector<
		boost::recursive_variant_,
		allocator<boost::recursive_variant_>
	  >,
	  list<boost::recursive_variant_>
	>]’:
	test.cpp:16:64:   required from here
	/usr/include/boost/variant/detail/apply_visitor_binary.hpp:168:1: error: no type named ‘result_type’ in ‘struct main()
	::<lambda(string)>’
	In file included from /usr/include/boost/variant/apply_visitor.hpp:18:0,
		             from /usr/include/boost/variant/detail/hash_variant.hpp:23,
		             from /usr/include/boost/variant/variant.hpp:34,
		             from /usr/include/boost/variant.hpp:17,
		             from test.cpp:5:


