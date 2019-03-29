Compounded
==========
compounds methods with base classes'  
tested with python 3.6


## Motivation

Designed to support compounding so actual handling for each parameter is delivered to different layer of the handlers.  

This is also useful when certain frameworks attempt to parse parameter names for configurations. Simple inheritance would require the user to repeat the parameters and explicitly call super() for initialization. By marking such methods as `@compounded`, actual method signature/initialization is compounded.   


## Examples

See [tests](https://github.com/chen-charles/compounded/tree/master/tests) for actual usages. 
