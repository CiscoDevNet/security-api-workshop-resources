##################################################################
#                                                                #
#                                                                #
#       Python Basics                                            #
#       The code below walks through the building blocks         #
#       of the Python programing language                        #
#       Author: Brennnan Bouchard, brebouch@cisco.com            #
#                                                                #
###################################################################


#
#                               Execution flow
#
#
#
#        Program will execute from the top down unless dictated otherwise by control
#        statements, function calls, or class instantiation.
#
#
#
#                               Variable Scope
#
#
#        Variables lifetime depends on the scope in which it is created.
#        For example, variables declared outside any control statements
#        are considered to be Global and will exist for the entire lifetime
#        of the app. Variables defined as arguments in function calls will
#        only exist during the call, in order to access data from function
#        variables, they must be returned. Similarly, variables created in
#        loops will only exist for that iteration, in order to modify a
#        variable within a loop it must already exist.


#
#                           Simple data types
#


# Char - Single alphanumeric character
example_char = 'a'
print(type(example_char))
print(example_char)


# Strings - Worlds, spaces, numbers, and punctuation as a single object (Python handles these as Char Arrays)
# Written in double " or single ' quotes for single line,  triple quotes ''' or """ for multiline
example_string = 'Example String'
print(type(example_string))
print(example_string)


# Bool - (Boolean) True or False
example_bool = True
print(type(example_bool))
print(example_bool)


# Int - (Integer) Whole number
example_int = 50
print(type(example_int))
print(example_int)


# Float - Number with decimal place, additional lengths exist depending on memory need
example_float = 1.5
print(type(example_float))
print(example_float)


#
#                           Complex data types
#


# List - Ordered iterable data, similar to array in C languages
# Written with [ ] and can contain just about any data type
example_list = ['text', 450, ['inner list', 'another string']]
print(type(example_list))
print(example_list)


# Tuple - Immutable list
# Written with ( ) and can contain just about any data type
example_tuple = ('string', 456)
print(type(example_tuple))
print(example_tuple)


# Dictionary - Key:value pair
# Written with { } and keys must be unique and of basic type, string, int, char
# Values accessed by calling the 'key' value in square brackets following the variable
example_dictionary = {'key': 'value'}
print(type(example_dictionary))
print(example_dictionary['key'])


#
#                           Control Statements
#
#
#           Control the flow of an application to dictate the way
#           it should act and under what conditions.
#
#           Examples:
#           If/Then/Else
#           For Loop
#           While Loop
#           Switch


# If statement performs a comparision and takes an action depending on if the result is True or False
# Statement ends in colon and indention following determines the scope
if 5 > 2:
    print('Its true 5 is greater than 2')

if not 2 > 5:
    print('Also true, 2 is not greater than 5')


# For Loops iterate through a list or range to execute a finite number of times
# upon completion of the iterations the execution flow continues
# A local variable containing the value of the iteration can be used during each execution

fruit_list = ['apple', 'bananas', 'orange', 'pear']

for fruit in fruit_list:
    print('This time around the fruit variable is: ' + fruit)


# While Loops run a comparison opertation each iteration and stop only if the condition is no longer True or
# the loop is ended via a break statement, an endless loop can be created by comparing directly against True

# Example while loop with comparison
a = 5
b = 2
while a > b:
    print('b currently equals: ' + str(b))
    b += 1


# Example while loop with break statement
outside_variable = 1
while True:
    print('will keep looping until variable equals 5 in check below, current value: ' + str(outside_variable))
    if outside_variable == 5:
        print('time to go')
        break
    outside_variable += 1


#
#                               Functions
#
#       Sections of code which perform a certain action, built for reusability so that
#       rather than writing the same code over again and again you can simple call a
#       function. Functions can take zero or more arguments and can return values but
#       they do not have to. Very simple "Hello" example included below
#


def say_hi(name):
    hello = 'Hello ' + name
    print(hello)
    return hello


say_hi('Bob')


#       As you can see here, we created a function called say_hi that takes a single
#       argument we call name. As with all programming you are free to name your functions
#       and variables whatever you want so long as they begin with an alphabetical
#       character and are not a system keyword. We then do a little string concatenation to
#       create a new string variable we call hello, which is then printed, and returned from
#       the call to be used later in the application.


#
#                               Classes
#
#       Classes allow for Python to act as an object-oriented programming language.
#       By creating a class, you define the blueprint of everything that makes up the class.
#       This will include things like variables and functions to be called on class objects
#       as methods. Classes will be initialized when an object is created and can require
#       certain properties to be defined at this point, or defaulted. Similarly, the initialization
#       flow can. Be defined in a class or if left to the default it will simply run from the top
#       down instantiating variables and running any code not contained in a function call.
#
#       Another component of a class that is critical to understand is the idea of self. Objects of
#       classes may be created many times with vastly different values that will remain persistent
#       to the life of the class object. Within the declaration you must work with variables by
#       calling the self.VARIABLE_NAME in order to maintain persistence within the scope.


# Example class
class Example:
    def __init__(self):
        self.variable = 'class string variable'

    def class_method(self):
        print(self.variable)


# Create instantiation of class
e = Example()
# Change class variables
e.variable = 'new variable'
# Call objects class methods
e.class_method()
