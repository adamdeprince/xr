# XR: Regular expressions for people not just machines

xr: Regular expressions for people.  [Full reference manual on website.](https://xr.deprince.io)

Release v1.0

Xr is an graceful, easy, thoughtful, extensible and testable regular expression library for Python built to be read and written by actual people.

Xr makes it easy to build and reuse libraries of well test regular expression subcomponents. Try xr just once and you'll never again copy-and-paste a regular expression.

## Awesome features

Xr supports modern programming practices
* Optimization
* Composability
* Unittesting support

Xr is tested against Python 2.7 & 3.4-3.8 and PyPy

## Getting started

Xr is distributed on pypi so installation is as easy as running pip:

    pip install xr
    
    
## Hello World

All good introductions to a programming language start with "Hello World." Xr is no different. In this tutorial you will learn how to recognize the string "Hello World" in a regular expression built with the xr library.

    >>> from xr import Text
    >>> hello_world = Text('Hello World')
    >>> hello_world.match_exact('Hello World')
    <re.Match object; span=(0, 11), match='Hello World'>
    >>> hello_world.match_exact('Goodbye World')
    (None)

Notice we return a re.Pattern object when we match, and None if we don't. This matches the behaivor of Python's built in re library. Xr composes regular expression source strings for you and feeds these to the re library where all of the heavy lifting of the actual regular expression matching takes place.

Our Hello World program is pretty good, but it doesn't cover all of the important Hello World use cases: Some programmers become a enthuisastic about learning how to use a new library and show this ethusiasticaly with an exclamation point. We of course want to accomodate enthusiasm so we should allow for an optional exclamation point at the end of the regular expression

    >>> hello.world.match_exact('Hello World!')
    (None)
    >>> hello_world = Text('Hello World') + Text('!').optional()
    >>> hello_world.match_exact('Hello World!')
    <re.Match object; span=(0, 12), match='Hello World!'>

So far so good, but what if our programmer is really really enthusiastic? What if we encounter two, three or more exclamation marks? Enthusiasm is good and we want to welcome it all!!!

    >>> hello.world.match_exact('Hello World!!!!!!!!!!')
    (None)
    >>> hello_world = Text('Hello World') + Text('!').many()
    >>> hello_world.match_exact('Hello World!!!!!!!!!!')
    <re.Match object; span=(0, 21), match='Hello World!!!!!!!!!!'>
 
Xr supports operator overloading, letting us make our example a little bit simpiler. Because the underlying regular expression object implements both `__add__` and `__radd__` so were able to simplify expressions like `Text('a') + Text('b')` If one side of a + expression is a `xr.R`E object, our library is smart enough to do what makes sense if the other side is just a string. In this case we can reduce the code volume a little bit by writing:

    >>> hello_world = "Hello World" + Text('!').many()

So far we've accommodated enthusiastic programmers, but only English speaking enthusiastic programmers. The majority of the world's population does not speak English natively. Far more people are thinking "Nǐ hǎo shìjiè" than they do "Hello World" when become excited about learning how to use a new library.

Before we can accomodate a new lanugae, we should refactor our code a little bit. One of the powerful features of the xr library is that you build your regular expressions in plain python. This makes available all of the features and convienences of writing in a programming language, like variable names for subcomponents.

    >>> verbiage = "Hello World"
    >>> punctuation = "!".many()
    >>> hello_world = verbiage + punctuation

Now that this code is refactored we can modify our program to recognize Chinesse. When reading this code keep in mind that for operators to work between xr expressions at least one side of the operator must be a xr.RE subclass. We have to write something like `Text('a') | 'b' | 'c' | 'd'` or `'a' | 'b' | Text('c') | 'd'`. We cannot write this: `'a' | 'b' | 'c' | 'd'` .

    >>> verbiage = Text("Hello World") | "你好世界"

While we are at this, lets add a few more languages. Most of the world's potential enthusiastic programmers don't speak English or Mandarin when they feel very very enthusiastic.

    >>> verbiage = Text("Hello World") | "你好世界" | "Hola Mundo" | "Привет мир";

When creating regular expresions it can be easy to forget that youre actually describing your regular expressions ina n abstract syntax tree in the python language. Remember that xr expressions are composiable - you can build your tree programatically.

    >>> from functools import reduce # For python 3 users 
    >>> verbiage = ["Hello World",
    ... "你好世界",
    ... "Hola Mundo",
    ... "Привет мир",
    ... "مرحبا بالعالم"]
    >>> verbiage = reduce(lambda x,y: x|y, map(Text, verbiage))
    >>> punctuation = "!".many()
    >>> hello_world = verbiage + punctuation
    >>> hello_world.match('你好世界!!!')
    <re.Match object;span=(0, 7), match='你好世界!!!'>
    >>> hello_world.match('Hola Mundo')
    < re.Match object;span=(0, 10), match='Hola Mundo'>
    >>> hello_world.match('Hello World')
    <re.Match object; span=(0, 11), match='Hello World'>

Our Hello World is now far more inclusive, but what about multilingual programmers? Lets modify our Hello World program to accept multiple utterances of Hello World in any language.

In addition to concatenation, regular expressions support or operators - Text("a") | Text("b") matches both the strings "a" and "b".

    >>> hello_worlds = hello_world + (Text(" ").many(1) + hello_world).many()
