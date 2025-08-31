## iteration = 10000000000

```
zig build-lib backend.zig -dynamic -lc -target x86_64-windows

```
result in 43.873060 seconds

```
g++ -shared -o backend.dll backend.cpp -std=c++11
```

result in 43.079437 seconds

```
gfortran -shared -o backend.dll backend.f90 -fPIC

```
result in 43.561556 seconds
