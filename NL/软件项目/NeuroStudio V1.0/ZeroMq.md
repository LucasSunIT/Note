https://github.com/zeromq/libzmq/releases

# 克隆源码
git clone https://github.com/zeromq/libzmq.git

cd libzmq
git checkout v4.3.5

# 编译（使用 Qt 自带的 CMake 或系统 CMake）
mkdir build && cd build
cmake .. -G "Visual Studio 17 2022" -A x64 -DCMAKE_INSTALL_PREFIX=E:\code\qtmqtt-dev\install
cmake --build . --config Debug
cmake --install .

# 继续在 build 目录下操作
# 构建 Release 版本
cmake --build . --config Release

# 安装 Release 版本（会安装到同一个 prefix 目录下，自动区分 Debug/Release 子目录）

cmake --install . --config Release
mqtt