# Session 状态与事件总线

## 数据层级

```text
Study
 └── Subject
      └── Session（磁盘目录 + 内存对象）
           ├── 多个 DataSet 文件（如 BDF）
           ├── Attachments
           ├── EegData（Pipeline 工作区）
           └── SessionInfo 元数据
```

`Session` 类型：`History`（离线）/ `RealTime`（实时）；状态 `Idle` / `Running` 表示采集运行态。

## 工作区焦点（两个 Session 指针）

由 **`WorkspaceState`** 持有，**写入只允许 `DataManagerController`**：

| 焦点 | 含义 | 典型写入 API |
|------|------|----------------|
| **processingSession** | 当前离线处理打开的 Session | `openDataSetForProcessing`、`activateProcessingSession` |
| **acquisitionSession** | 当前进入采集工作区的 Session | `enterAcquisition` |

**读侧（新代码）**：`SessionContext::processingSession()` / `acquisitionSession()`。

Legacy：`EEGManager::getCurrentSession()` 等转发到 SessionContext，勿再扩散。

## DataManagerController → AppEventBus

`AppEventBus::wireController` 转发：

| Controller 信号 | AppEventBus 信号 | 典型订阅方 |
|-----------------|------------------|------------|
| `dataSetOpened` | `dataSetOpened` | Config、Content、Coordinator |
| `dataSetClosed` | `dataSetClosed` | Content |
| `dataSetRenamed` | `dataSetRenamed` | Content |
| `acquisitionEntered` | `sessionEnterAcquisition` | MainWindow、Survey、Coordinator |
| `dataProcessEntered` | `sessionEnterDataProcess` | MainWindow、Survey |

### 打开数据集（离线）

```text
Presenter::openDataSet
  → Controller::openDataSetForProcessing
  → 设置 processing Session
  → emit dataSetOpened
  → publishDataProcessEntered → sessionEnterDataProcess
Bus:
  → ConfigWidget::updateConfData（切数据处理 Tab → tabChanged → 历史 stacked）
  → ContentWidget::openDataSet
  → Coordinator::applyMode(DataProcess)
```

### 进入采集工作区（尚未等于硬件开流）

```text
Presenter::enterAcquisition
  → Controller::enterAcquisition
  → 设置 acquisition Session
  → acquisitionEntered → sessionEnterAcquisition
Bus:
  → MainWindow：显示 Dock、切采集 Tab → 实时 stacked
  → Coordinator::applyMode(Acquisition)
  → Survey 插件：音频等
```

硬件 **开始采集**（绑 Session、写 BDF、开流）由 **`EegDeviceCoordinator::startCollectingSession`** 与 Config 采集工具栏触发；若工作区 acquisition Session 不一致，`setAcquireSession` 内会再调 `enterAcquisition` 与 Bus 对齐。

## AppEventBus 信号一览（Core/AppEventBus.h）

- `dataSetOpened(Session*)`
- `dataSetClosed(Session*)`
- `dataSetRenamed(Session*)`
- `sessionEnterAcquisition(Session*)`
- `sessionEnterDataProcess()`

Controller 与 Bus 均为单例；MainWindow 启动时 `wireController` 一次。

## 与 UI 的边界

- `ConfigWidget::updateConfData` / `updateAcquisitionSession`：**只切 Tab、绑控件**，不改 WorkspaceState。
- Content 中间 Tab 切换：`Coordinator` → `activateProcessingSession` → `updateConfData`。
