# 插件 Survey 与 Rehab

## 插件模型

- 接口：**`IApplicationPlugin`**（`Platform/IApplicationPlugin.h`）
- 注册：**`PluginManager::instance()`**（编译期静态插件，非运行时 DLL）
- 组合根：**`registerBuiltInApplicationPlugins()`**（`Interactor/AppComposition.cpp`）
  - `NEUROSTUDIO_ENABLE_SURVEY` → `createSurveyPlugin()`
  - `NEUROSTUDIO_ENABLE_REHAB` → `createRehabPlugin()`

## AppContext（注入依赖）

```cpp
struct AppContext {
    AppEventBus* eventBus;
    IWorkspaceMode* workspaceMode;  // EEGWorkspaceCoordinator
    IMainShell* shell;              // MainWindow
    IPlatformHost* platformHost;
    QWidget* hostWidget;
    DataWidget* dataWidget;
    DataManagerWidget* dataManagerWidget;
    ConfigWidget* configWidget;
};
```

插件在 **`initialize(context)`** 中：

- 订阅 `AppEventBus` / `workspaceModeChanged`
- 注册菜单（`IMenuContributor` 等）
- **`registerDataManagerTabs` / `registerConfigTabs`** 增加 Tab

## Survey 模块结构

```text
Survey/
├── Entities/       量表、范式、会话任务仓储
├── Interactor/
│   ├── Audio/      平板音频 WebSocket
│   └── Task/       任务 WebSocket、下发、合并、局域网发现
│       └── TaskIssue/
└── Views/          SurveyDialog、ParadigmDialog、IssueTaskDialog
```

典型行为：

- **`sessionEnterAcquisition`**：启动平板音频服务
- **`workspaceModeChanged`**：离开采集模式停音频
- **`IssueTaskDialog`**：下发前可检查 `hardwareEeg()->isRecording()`
- 任务进度与触发经 **`TaskWebSocketService`** → **`TriggerIngressService`**

## Rehab 模块结构

```text
Rehab/
├── Entities/       RehabProgramManager 等
├── Interactor/Motion/   Python 子进程监管
├── Views/          设备/方案管理对话框
├── Menu/
└── python_apps/rehab_motion/
```

- 菜单扩展：`RehabTreeMenuCommands`（备份等康复树命令）
- 与 EEG 采集交叉：例如删除 Session 时检查 `hardwareEeg()->isCollecting()`

## Platform 其它接口

- **`IMainShell`**：MainWindow 实现，供插件调壳层能力
- **`IPlatformHost` / `PlatformHost`**：平台级服务入口
- **`IDataManagerTabContributor` / `IConfigTabContributor`**：Tab 扩展点

## 扩展新模块建议

1. 新建子目录 + `CMakeLists.txt`，链接 `NeuroStudioHost`
2. 实现 `IApplicationPlugin`，在 `AppComposition.cpp` 注册
3. 只通过 **Bus / SessionContext / hardwareEeg / SettingsFacade** 与主程序交互，避免 include legacy `Device/`
