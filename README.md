# brace
Add curly braces and semicolons to indented code.

```c
  #include <stdio.h>
  int main( int argc, char* argv[] )
     if( !argc )
        printf( "say sth pls" )
        return 1
     else
        prinf( "i agree" )
        return 0
```
### becomes
```c
  #include <stdio.h>
  int main( int argc, char* argv[] ) {
     if( !argc ) {
        printf( "say sth pls" );
        return 1; }
     else {
        prinf( "i agree" );
        return 0; }
```
