基于插值法的图像处理
===
+ 使用了双线性插值方法，和三次卷积公式
+ 动态库的编译方法是 
`gcc -fpic -c -l/usr/include/python2.7 -l /usr/lib/python2.7/config getVal.c`
`gcc -shared -o getVal.so getVal.o`
+ 在mac上面可能会有点不同

mac上面的动态库编译方法是`gcc -dynamiclib -I /System/Library/Frameworks/Python.framework/Versions/2.7/Headers/ -lpython2.7 -o getVal.dylib getVal.c;mv getVal.dylib getVal.so`
\\上面的路径是通过python中的sys.path找到的（
