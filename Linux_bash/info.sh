
. - The Current Directory
.. - The Parent Directory
../ - The parent Directory with slash (Used to navigate from the parent)
../../ - The parent of the parent Directory
~/ - The current users home directory
.hiddenfile - A file that starts with a dot is a hidden file. ( They are normally configuration files )

============================================

Wildcards:
? - Use to represent any ONE character
* - Use to represent any SET of characters
[xbc] - Use to represent any ONE of the characters listed within the bracket
[a-z] - Use to represent any character between the range

============================================

Redirection - Redirect the output or input of a command into files, devices, and the input
of other commands

> - To redirect the standard output of a command into a file.
( Will replace the contents of a file
& any redirection that uses only 1 ">" will do this )
>> - To append into the end of a file.
< - To export the contents of a file into the the command.
<< - To append the contents of a file into the command
2> - To redirect standard error of a command into a file.
2>> - To append standard error of a command into the end of a file.
&> - To redirect standard error & standard output when redirecting text
&>> - To append standard error & standard output when redirecting text

{aa,bb,cc,dd} => aa bb cc dd
{0..12} => 0 1 2 3 4 5 6 7 8 9 10 11 12
{3..-2} => 3 2 1 0 -1 -2
{a..g} => a b c d e f g
{g..a} => g f e d c b a

mkdir {dir1,dir2,dir3} - makes three folders dir1 dir2 and dir3

