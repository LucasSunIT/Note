

> 涵盖：C++ 语言基础、现代 C++、STL、Qt、并发、设计模式、模板、二进制协议、IPC、Python C API、IIR 滤波、DLL 导出、工程实践  
> 共 130 题

---

## 一、C++ 语言基础

### 1. `struct` 与 `class` 的默认访问权限有何区别？

**答：** 唯一语法差异是默认访问权限：`struct` 成员默认 `public`，`class` 成员默认 `private`。继承时 `struct` 默认 `public` 继承，`class` 默认 `private` 继承。其余能力相同。

### 2. `enum` 与 `enum class` 的区别是什么？

**答：** 传统 `enum` 会隐式转换为整数，枚举值泄漏到外层作用域。`enum class` 是强类型枚举，不能隐式转整数，作用域限定在枚举名内，更安全、可读性更好。

### 3. 四种 cast 的适用场景？

**答：**
- `static_cast`：编译期可检查的常规转换（数值转换、上行/下行转换）
- `reinterpret_cast`：底层比特 reinterpret（指针类型转换），危险，仅用于底层/协议场景
- `const_cast`：仅去除/添加 `const`/`volatile`
- `dynamic_cast`：多态类型的安全下行转换，失败返回 `nullptr`（指针）或抛异常（引用）

### 4. `reinterpret_cast` 何时合法？有何风险？

**答：** 常用于二进制协议解析、硬件寄存器访问、与 C 接口交互。风险：违反 strict aliasing、未对齐访问、可移植性差、类型安全丧失，可能导致未定义行为。

### 5. `constexpr` 与 `const` 的区别？

**答：** `const` 表示运行时不可变；`constexpr` 表示可在编译期求值。C++14 起 `constexpr` 函数可含更多语句；C++17 起 `if constexpr` 支持编译期分支。

### 6. 虚函数表如何工作？构造函数能否 virtual？

**答：** 含虚函数的类有 vptr 指向 vtable，运行时通过 vtable 动态派发。构造函数不能声明为 `virtual`（对象尚未完整构造）；析构函数常需 `virtual` 以正确析构派生类。

### 7. 纯虚函数、抽象类、接口类？

**答：** 纯虚函数 `= 0` 无默认实现（C++11 起可有实现）。含纯虚函数的类为抽象类，不能实例化。接口类通常只有纯虚函数、无成员数据。

### 8. `override` 和 `final` 的作用？

**答：** `override` 显式标记重写基类虚函数，签名不匹配时编译报错。`final` 阻止进一步 override 或继承。

### 9. 析构函数为何通常要 virtual？

**答：** 通过基类指针删除派生类对象时，若非 virtual 析构，只调用基类析构，派生类资源泄漏。多态基类应声明 virtual 析构。

### 10. RAII 是什么？

**答：** Resource Acquisition Is Initialization：在对象构造时获取资源，析构时自动释放。利用栈对象生命周期管理内存、锁、文件句柄等，异常安全且避免泄漏。

### 11. 拷贝/移动构造与赋值何时调用？

**答：** 拷贝：用左值初始化或赋值。移动：用右值（临时对象、`std::move` 结果）初始化或赋值。编译器可能省略拷贝/移动（RVO/NRVO）。

### 12. Rule of Three / Five / Zero？

**答：** Three：若自定义析构、拷贝构造、拷贝赋值之一，通常需三者都自定义。Five：加上移动构造、移动赋值。Zero：依赖编译器生成或使用智能指针，无需自定义。

### 13. `= default` 和 `= delete` 的使用场景？

**答：** `= default` 显式使用编译器生成的特殊成员。`= delete` 禁止某函数（如禁止拷贝的单例、禁止隐式转换的构造函数）。

### 14. 左值、右值、引用、`std::move`？

**答：** 左值有身份、可取地址；右值临时的、将亡的。左值引用绑定左值；右值引用绑定右值。`std::move` 将左值转为右值引用以启用移动，本身不移动数据。

### 15. 完美转发与 `std::forward`？

**答：** 模板函数将参数原样（左值/右值）转发给另一函数。`std::forward<T>(arg)` 配合万能引用 `T&&` 保持值类别，避免多余拷贝。

### 16. `namespace` 与匿名命名空间？

**答：** `namespace` 组织代码、避免命名冲突。匿名命名空间限制符号为当前翻译单元内部链接，等价于 `static` 全局符号。

### 17. `typedef` 与 `using`？

**答：** 均可声明别名。`using` 语法更清晰，支持模板别名 `using Map = std::map<K,V>`，`typedef` 写模板别名较繁琐。

### 18. 函数重载匹配规则？

**答：** 精确匹配 > 提升 > 标准转换 > 用户定义转换 > `...`。运算符重载不能改变优先级和操作数个数（除 `()` `[]` `->` `=` 等）。

### 19. 头文件 guard 与 `#pragma once`？

**答：** `#ifndef/#define/#endif` 可移植。`#pragma once` 简洁，多数编译器支持，非标准但实践中可靠。

### 20. `extern "C"` 的作用？

**答：** 告诉 C++ 编译器以 C 链接方式导出符号（无 name mangling），便于 C 代码或 `dlsym`/`GetProcAddress` 调用。C++ 调用 C 库时必须使用。

---

## 二、现代 C++（C++11/14/17）

### 21. `auto` 类型推导规则与陷阱？

**答：** 按初始化表达式推导。陷阱：`auto` 丢失顶层 const、`auto&&` 与引用折叠、`{1,2}` 推导为 `initializer_list`。不要过度使用导致可读性下降。

### 22. range-based for 底层实现？

**答：** 编译器展开为对 `begin()`/`end()` 的迭代，等价于 `for(auto it = begin(c); it != end(c); ++it)`。

### 23. `{}` 与 `()` 初始化区别？

**答：** 花括号初始化禁止窄化转换。Most vexing parse：`T obj(Args());` 可能被解析为函数声明而非变量定义。

### 24. `shared_ptr` 与 `unique_ptr`？

**答：** `unique_ptr` 独占所有权，轻量，不可拷贝。`shared_ptr` 共享所有权，引用计数，有控制块开销。优先 `unique_ptr`，需共享时用 `shared_ptr`。

### 25. `make_shared` 的优势？

**答：** 一次分配同时放置控制块和对象，减少内存分配、提高缓存局部性、异常安全（避免 new 后尚未构造 shared_ptr 时泄漏）。

### 26. `shared_ptr` 引用计数与循环引用？

**答：** 每份 `shared_ptr` 共享控制块中的强引用计数。循环引用导致计数永不为零，用 `weak_ptr` 打破循环。

### 27. `weak_ptr` 的作用？

**答：** 观察 `shared_ptr` 管理对象但不增加强引用。`lock()` 获取 `shared_ptr`，对象已销毁则返回空。

### 28. Lambda 捕获方式区别？

**答：** `[=]` 值捕获（默认 const），`[&]` 引用捕获，`[this]` 捕获当前对象指针。混合捕获可指定 `x` 值捕获、`&y` 引用捕获。mutable 允许修改值捕获副本。

### 29. Lambda 与函数指针、`std::function`？

**答：** 无捕获 lambda 可转函数指针。有捕获或状态需用 `std::function` 或模板。`std::function` 有类型擦除和堆分配开销。

### 30. `std::function` 性能？

**答：** 通常涉及堆分配和间接调用。高频回调优先函数指针、模板、`function_ref`（C++23）或 lambda 直接传参。

### 31. 可变参数模板与 `Args&&...`？

**答：** `typename... Args` 声明参数包，`Args&&... args` 为万能引用包，可用 `func(std::forward<Args>(args)...)` 展开转发。

### 32. `quiet_NaN()` 与 NaN 比较？

**答：** NaN 表示非数。`x == NaN` 恒 false，需用 `std::isnan(x)`。NaN 参与运算结果仍为 NaN。

### 33. `noexcept` 的语义？

**答：** 承诺函数不抛异常。移动构造标记 `noexcept` 时容器扩容会用移动而非拷贝。违反 noexcept 会调用 `std::terminate`。

### 34. SFINAE？

**答：** Substitution Failure Is Not An Error：模板替换失败时该重载从候选集移除而非报错。用于 `enable_if` 约束模板参与 overload resolution。

### 35. `optional` 与 `variant`？

**答：** `optional<T>` 表示可能有值。`variant<Ts...>` 类型安全的联合体，存多种类型之一。替代 magic number、void* 或继承层次。

---

## 三、STL 标准库

### 36. `vector` 增长策略与 `reserve`/`resize`？

**答：** 容量不足时通常按倍数（如 2 倍）扩容并搬移元素。`reserve(n)` 只预留容量不改变 size；`resize(n)` 改变元素个数，新增默认构造。

### 37. `std::sort` 复杂度与稳定性？

**答：** 平均 O(n log n)。标准 `sort` 不稳定。需稳定排序用 `stable_sort`（O(n log² n) 或 O(n log n) 视实现）。

### 38. `std::greater` 排序结果？

**答：** 降序排列：较大元素排在前面。

### 39. `map` vs `unordered_map`？

**答：** `map` 红黑树，有序，O(log n)。`unordered_map` 哈希表，均摊 O(1)，无序，需合适哈希函数和负载因子。

### 40. `function` vs `bind`？

**答：** `bind` 绑定参数生成 callable，语法复杂。C++11 后更推荐 lambda 替代 `bind`。`function` 是类型擦除的通用 callable 包装。

### 41. 迭代器失效？

**答：** `vector/string` 插入/删除可能使全部迭代器失效；`deque` 首尾操作可能失效；`list/map/set` 仅失效被删元素迭代器。`unordered_map` rehash 会失效。

### 42. `out_of_range` 何时抛出？

**答：** 如 `vector::at(i)`、`map::at(key)` 越界或 key 不存在时抛出。`operator[]` 对 map 会插入默认值，不抛异常。

### 43. `atomic` 保证什么？

**答：** 对 `load/store/read-modify-write` 等操作原子性，无数据竞争。不保证复合逻辑（如 check-then-act）原子，需 mutex 或更强同步。

### 44. memory_order 语义？

**答：**
- `relaxed`：仅原子性，无顺序约束
- `acquire`：读侧，后续读写不能重排到此读之前
- `release`：写侧，此前读写不能重排到此写之后
- `seq_cst`：全局顺序一致，最强默认

### 45. 无锁 vs mutex？

**答：** 无锁适合 SPSC 高吞吐、低延迟；实现复杂，ABA 等问题。mutex 简单正确，竞争不激烈时足够；竞争激烈或需复杂不变量时用 lock-free 需谨慎设计。

### 46. SPSC 环形缓冲区设计要点？

**答：** 单生产者单消费者，固定容量，head/tail 索引，通常 capacity+1 区分满/空。生产者写 slot 后 release 更新 write index；消费者 acquire 读 read index。

### 47. `memcpy` vs `memmove`？

**答：** `memcpy` 要求源目标不重叠。`memmove` 支持重叠区域。对非 trivially copyable 类型（含 vptr、自管理资源）不能用 `memcpy` 复制对象。

---

## 四、Qt 框架

### 48. 信号槽机制与优劣？

**答：** 基于元对象系统的观察者模式：emit 信号时调用连接的槽。优点：松耦合、跨线程、类型安全（新语法）。缺点：MOC 开销、调试链路稍复杂、滥用可能导致隐式依赖。

### 49. `Q_OBJECT` 与 MOC？

**答：** `Q_OBJECT` 启用元对象特性。MOC 扫描头文件生成 `moc_*.cpp`，含元信息、信号槽静态连接表、`tr()` 等支持。

### 50. connect 五种连接类型？

**答：**
- **Direct**：同线程同步直接调用
- **Queued**：事件队列异步
- **BlockingQueued**：跨线程阻塞等待槽执行完
- **Auto**：同线程 Direct，跨线程 Queued
- **Unique**：重复 connect 失败

### 51. 跨线程为何用 QueuedConnection？

**答：** GUI 和非 GUI 对象线程亲和性不同，Direct 在错误线程操作 Widget 会崩溃或竞态。Queued 将槽调用投递到目标线程事件循环。

### 52. `QThread` 正确使用方式？

**答：** 推荐 worker 对象 `moveToThread(thread)`，用信号启动/停止工作。避免继承 `QThread` 并重载 `run()` 除非确实需要（如纯循环线程）。不在 `run()` 外随意 `terminate()`。

### 53. QMutex / QReadWriteLock / QWaitCondition？

**答：** `QMutex` 互斥。`QReadWriteLock` 多读单写。`QWaitCondition` 配合 mutex 实现等待/唤醒，用于生产者-消费者。

### 54. 读写锁适用场景？

**答：** 读多写少时并发读性能优于 mutex。写频繁或临界区短时 mutex 可能更简单高效（读写锁本身有开销）。

### 55. `QTimer` 精度？

**答：** 依赖操作系统和事件循环负载，通常毫秒级，非硬实时。`singleShot` 一次性；`start(interval)` 周期性，可能漂移累积。

### 56. `QByteArray` vs `std::string`？

**答：** `QByteArray` 隐式共享（Qt5）、与 Qt API 无缝、支持 `\0` 二进制数据。`std::string` 标准库通用。Qt6 中 QByteArray 仍常用于 IO 和协议。

### 57. QJson 类关系？

**答：** `QJsonObject`/`QJsonArray` 为 DOM 节点。`QJsonDocument` 包装根节点并负责 parse/serialize 与 `QByteArray`/`QString` 互转。

### 58. `QSettings`？

**答：** 支持 INI、注册表（Windows）、macOS plist 等。非线程安全，多线程应加锁或每线程独立实例。

### 59. `QAbstractItemModel` 必实现函数？

**答：** 至少 `rowCount`、`columnCount`、`data`。可编辑模型还需 `setData`、`flags`。树形还需 `index`、`parent`。

### 60. 常用 ItemDataRole？

**答：** `DisplayRole` 显示文本，`EditRole` 编辑值，`BackgroundRole`/`ForegroundRole` 颜色，`CheckStateRole` 勾选，`UserRole` 起自定义数据。

### 61. 何时 emit model 信号？

**答：** 单元格变化 `dataChanged`；结构变化 `beginInsertRows/endInsertRows` 等；大规模重置 `beginResetModel/endResetModel` 或 `layoutChanged`。

### 62. QTcpServer/Socket 流程？

**答：** `listen()` 后 `incomingConnection(socketDescriptor)` 创建 `QTcpSocket`，`readyRead` 读数据，`disconnected` 清理。客户端 `connectToHost()`。

### 63. `QSharedMemory` 流程？

**答：** `create(size)` 或 `attach()` 映射共享段。`lock()/unlock()` 或 `QSystemSemaphore` 同步。键名跨进程一致。

### 64. 事件 filter 与 override 事件？

**答：** `eventFilter` 拦截其他对象事件。`showEvent/closeEvent` 为特定事件 handler。`event()` 为总入口可分发。

### 65. QObject 父子树？

**答：** 父对象销毁时自动 delete 子对象。用于自动管理 Widget 和 QObject 生命周期，避免泄漏。

### 66. `QVector` vs `std::vector`（Qt6）？

**答：** Qt6 中 `QVector` 与 `QList` 统一为 `QList` 别名行为变化。新项目可直接用 `std::vector` 或 Qt 容器视 API 需求。

### 67. `Q_DECLARE_METATYPE` 与 `qRegisterMetaType`？

**答：** 声明类型可存入 `QVariant` 和 QueuedConnection 参数。跨线程 queued 信号需注册（Qt5+ 部分可自动）。

### 68. QueuedConnection 传递自定义类型条件？

**答：** 类型需 `qRegisterMetaType` 或 `Q_DECLARE_METATYPE` + 注册，且可拷贝（事件系统会复制参数）。

---

## 五、并发与多线程

### 69. 进程与线程区别？

**答：** 进程独立地址空间；线程共享进程资源（堆、全局变量、文件描述符），有独立栈和 PC。线程切换开销小于进程。

### 70. 竞态条件？

**答：** 多线程访问共享数据，结果依赖调度顺序。用 mutex、atomic、线程局部存储、不可变数据或消息传递避免。

### 71. 死锁四条件？

**答：** 互斥、占有且等待、不可抢占、循环等待。预防：固定加锁顺序、超时锁、一次性获取所有锁、使用 lock hierarchy。

### 72. 生产者-消费者实现？

**答：** mutex + condition_variable（或 QMutex + QWaitCondition）+ 有界队列；或无锁 SPSC ring buffer；或消息队列/事件驱动。

### 73. 条件变量 wait/wake？

**答：** `wait(lock)` 原子释放锁并阻塞；`wakeOne/wakeAll` 唤醒。必须用 `while(!pred) wait()` 防止虚假唤醒。

### 74. 线程安全含义？

**答：** 多线程并发调用时程序行为正确、无数据竞争。`const` 成员函数不一定线程安全；静态变量、单例初始化需注意。

### 75. atomic 能否替代 mutex？

**答：** 仅简单计数、flag、SPSC 索引等可以。复合操作、多变量不变量、容器修改仍需 mutex。

### 76. False sharing？

**答：** 不同 CPU 核心修改同一 cache line 内不同变量导致缓存行乒乓。用 `alignas(64)` 填充分离热数据。

### 77. `std::thread` vs `QThread`？

**答：** `std::thread` 标准库、轻量、与 STL 集成好。`QThread` 与 Qt 事件循环、信号槽、线程亲和性集成，GUI 应用更自然。

### 78. GUI 线程安全更新 UI？

**答：** 仅在 GUI 线程操作 Widget。工作线程通过信号 QueuedConnection、QMetaObject::invokeMethod、QTimer::singleShot(0, ...) 投递更新。

---

## 六、设计模式

### 79. 单例实现方式？

**答：** Meyers singleton（函数内 static，C++11 线程安全）、双检锁（需 atomic）、`std::call_once`。删除拷贝构造/赋值。

### 80. 单例缺点与测试？

**答：** 全局状态、隐藏依赖、难单元测试。可用依赖注入替代，或测试钩子/接口抽象替换单例。

### 81. 工厂 vs 抽象工厂？

**答：** 工厂方法：创建一种产品的接口。抽象工厂：创建一族相关产品（多个工厂方法组合）。

### 82. 模板方法 vs 策略？

**答：** 模板方法：基类定义算法骨架，子类 override 步骤（继承）。策略：算法可替换对象/composable（组合），运行时切换。

### 83. function + map 实现策略/命令？

**答：** `std::map<Key, std::function<Result(Args...)>>` 注册处理器，根据 key dispatch，避免大量 if-else 或 switch。

### 84. 观察者 vs Qt 信号槽？

**答：** 观察者模式 subject 维护 observer 列表并 notify。Qt 信号槽是编译期/运行时连接的观察者变体，支持跨线程和元类型。

### 85. RAII 与 Scope Guard？

**答：** Scope Guard 在作用域退出时执行 cleanup lambda，是 RAII 的泛化形式（如 `std::lock_guard`）。

### 86. PIMPL？

**答：** 实现细节放在 impl 类，头文件只持 unique_ptr<Impl>。减少编译依赖、稳定 ABI、隐藏私有成员。

---

## 七、模板编程

### 87. 类/函数模板实例化时机？

**答：** 函数模板使用时隐式实例化。类模板在用到成员或显式实例化时实例化（C++11 起 lazy instantiation）。

### 88. 全特化 vs 偏特化？

**答：** 全特化：所有模板参数指定。偏特化：仅部分参数或指针/引用形式（类模板可偏特化，函数模板不可，仅可重载）。

### 89. CRTP？

**答：** `class Derived : public Base<Derived>`。静态多态，编译期绑定，无虚表开销。用于 mixin、静态接口检查。

### 90. `typename` vs `class` 在模板参数？

**答：** 声明类型模板参数时等价。依赖名 `T::type` 必须用 `typename` 告诉编译器是类型。

### 91. 通用环形缓冲区 `FrameBuffer<T>`？

**答：** 模板参数 T，固定 capacity+1，atomic 或 mutex 保护 head/tail，push/pop/peek，满/空判断，可选 memory_order 优化 SPSC。

### 92. 参数包转发给构造函数？

**答：** `template<typename T, typename... Args> void create(Args&&... args) { return T(std::forward<Args>(args)...); }`

### 93. 模板为何放头文件？

**答：** 模板实例化需要完整定义。分离编译需显式实例化声明。一般头文件实现或 `.tpp` include。

---

## 八、二进制协议与底层数据处理

### 94. CRC16 原理与位运算/查表？

**答：** 按位除法求余，反映多项式。位运算逐位慢但省空间；查表法每字节 O(1) 快，占 512 字节（16 位表）。

### 95. Modbus CRC16 vs CRC16-CCITT？

**答：** Modbus 用多项式 0xA001（反射 0x8005），初值 0xFFFF。CCITT 常用 0x1021，初值/异或不同，结果不可混用。

### 96. 大端与小端？

**答：** 大端高字节在低地址；小端低字节在低地址。网络序为大端。可用 `htonl/ntohl` 或手动交换字节。

### 97. 字节流提取固定字段？

**答：** 按偏移 read，注意长度边界、粘包拆包、magic header 对齐。状态机或 ring buffer 累积后再 parse。

### 98. `reinterpret_cast` 读 int 的注意事项？

**答：** 对齐要求、strict aliasing（C++ 中用 `memcpy` 更安全）、32/64 位 int 宽度、符号扩展。

### 99. `#pragma pack` 影响？

**答：** 改变结构体成员对齐，紧凑布局用于协议。默认对齐恢复用 `#pragma pack(pop)`。可移植性需注意。

### 100. `htons/htonl`？

**答：** host to network short/long，将主机字节序转为网络大端字节序。

---

## 九、进程间通信（IPC）

### 101. 共享内存原理？

**答：** 多个进程映射同一物理页到各自虚拟地址空间，直接读写同一块 RAM，速度最快，需额外同步。

### 102. POSIX shm 与 Windows 对应？

**答：** `shm_open`+`mmap` 对应 `CreateFileMapping`+`MapViewOfFile`。Qt `QSharedMemory` 跨平台封装。

### 103. 共享内存为何需同步？

**答：** 读写非原子，可能 torn read/write。需 mutex、semaphore 或 seqlock 保证一致性。

### 104. 先写长度再写数据的协议？

**答：** 常见简单方案。缺点：非原子更新，读者可能读到不一致长度/数据。改进：版本号、双缓冲、seqlock 或消息边界协议。

### 105. 管道/消息队列/共享内存/Socket？

**答：** 管道：父子/simple 流。消息队列：结构化消息。共享内存：大数据低延迟。Socket：跨机器或复杂 IPC，通用但拷贝多。

---

## 十、Python C API 嵌入

### 106. `Py_Initialize` / `Py_Finalize` 顺序？

**答：** 进程内 `Py_Initialize` 一次（或 `Py_IsInitialized` 检查）。`Py_Finalize` 释放解释器，之后不可再 Init（除非新版 embedded 扩展）。顺序：SetHome → Init → 使用 → Finalize。

### 107. `PyObject*` 引用计数？

**答：** 每个对象有 refcount。新引用需 INCREF，不用时 DECREF。 refcount 为 0 时销毁。

### 108. INCREF / DECREF / XDECREF？

**答：** INCREF 增引用。DECREF 减引用（不可对 NULL）。XDECREF 对 NULL 安全跳过。

### 109. Python 对象泄漏场景？

**答：** 忘记 DECREF、异常路径未释放、borrowed ref 误当 new ref、循环引用（C 层较少，Python 层 gc 处理）。

### 110. C++ 调 Python 参数与返回值？

**答：** `PyObject_CallObject`，构造 `PyTuple`/`PyDict` 参数，返回值用 `PyArg_Parse` 或类型检查转换，用完 DECREF。

### 111. GIL 是什么？

**答：** Global Interpreter Lock，同一时刻仅一线程执行 Python 字节码。多线程 CPU 密集 Python 无法并行；C 扩展释放 GIL 可并行。`PyGILState_Ensure/Release` 管理。

### 112. `Py_SetPythonHome` 时机？

**答：** 必须在 `Py_Initialize()` 之前，指定 Python 标准库路径，否则嵌入式环境找不到 `lib/python3.x`。

---

## 十一、数字信号处理（IIR 滤波）

### 113. FIR vs IIR？

**答：** FIR 仅零点，线性相位易实现，阶数高。IIR 有极点零点，阶数低效率高，可能不稳定，相位非线性。

### 114. Biquad 与级联？

**答：** 二阶 IIR 节，传递函数有理分式。高阶滤波分解为多个 Biquad 级联，数值稳定性更好。

### 115. 极点与零点？

**答：** 分母根为极点，分子根为零点。极点决定衰模态和稳定性（单位圆内稳定）；零点影响频率响应零点。

### 116. 预畸变（Pre-warping）？

**答：** 双线性变换将模拟角频率映射到数字域时产生畸变，设计时在模拟域预补偿使数字截止频率准确。

### 117. Butterworth / Chebyshev / RBJ？

**答：** Butterworth 通带最平坦。Chebyshev 通带/阻带 ripple 换更陡过渡。RBJ（Cookbook）参数化 EQ 滤波，直接由中心频率/Q/增益设计。

### 118. 滤波器状态为何要保持？

**答：** IIR 有记忆，输出依赖历史输入输出。流式处理每 sample 更新 state，重置 state 会产生 transient。

### 119. 模板化 `filter(s, state)` 优势？

**答：** State 类型可 float/double 或 SIMD，编译期多态无 virtual 开销，内联优化好，适合实时 DSP。

---

## 十二、DLL / 模块导出

### 120. `dllexport` / `Q_DECL_EXPORT`？

**答：** 标记符号从 DLL 导出，供其他模块链接或 dlsym。Import 侧用 dllimport。Qt 宏跨平台统一 __attribute__((visibility)) 等。

### 121. 导出符号与 `extern "C"`？

**答：** C++ name mangling 使 dlsym 难找符号。C 链接或 `.def` 文件导出 unmangled 名。仅导出必要 API 隐藏实现。

### 122. 动态库 vs 静态库？

**答：** 静态库编译期链接进 exe，无运行时依赖。动态库运行时加载，共享节省内存，需 DLL 在 PATH。失败原因：缺依赖、ABI 不匹配、符号未导出。

---

## 十三、综合与工程实践

### 123. 线程安全消息队列设计？

**答：** mutex + queue + condition_variable；或 lock-free MPMC（复杂）；Qt 可用信号 QueuedConnection 作队列。支持 shutdown 唤醒避免死等。

### 124. 采集线程与 UI 解耦？

**答：** 采集线程只写 buffer/emit 信号；UI 线程订阅数据更新图表。禁止跨线程直接碰 Widget。限频刷新（如 30fps）减负载。

### 125. 异常安全保证？

**答：** Basic：异常后无泄漏不变量可能坏。Strong： commit 或 rollback。Nothrow：绝不抛异常。copy-and-swap 可实现 strong。

### 126. C++/Qt 单元测试？

**答：** Google Test、Qt Test (`QTest`)。Mock 接口、测试纯逻辑不依赖 GUI。CI 用 headless 或 `QApplication` fixture。

### 127. Qt 内存泄漏常见原因？

**答：** 无 parent 的 QObject 未 delete、循环引用（非 QObject）、lambda 捕获 raw pointer、信号槽未 disconnect 延长生命周期。

### 128. Profiling 区分瓶颈？

**答：** CPU profiler 看热点函数。锁分析看 contention。Allocator/heap profiler 看 malloc。Wall time vs CPU time 区分 IO 等待。

### 129. 减少头文件依赖？

**答：** 前置声明、pimpl、减少 include、unity build 慎用。传递依赖用 modules（C++20）或 IWYU。

### 130. 实时流 buffer 满策略？

**答：** 丢弃最旧（低延迟 telemetry）、阻塞（不丢但延迟增）、丢弃最新（保旧数据）、扩容（内存风险）。实时 EEG 常 drop-oldest 或 backpressure 告警。

---

*题目覆盖 NeuroStudio 项目涉及的 C++ 技术栈，答案为通用技术要点，可直接用于面试复习。*
