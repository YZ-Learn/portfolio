
# 大疆无人机智能客服系统 - 数据流文档

---

## 一、智能问答流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant UI as Streamlit界面
    participant Agent as ReactAgent
    participant Tool as 工具层
    participant RAG as RAG服务
    participant DB as 向量数据库
    participant Model as 大语言模型

    User->>UI: 输入问题（如："无人机电池如何保养？"）
    UI->>Agent: execute_stream(prompt)
    Agent->>Agent: 解析问题意图
    Agent->>Agent: 判断是否需要调用工具
    
    alt 需要调用工具
        Agent->>Tool: 调用rag_summarize(query)
        Tool->>RAG: rag_summarize(query)
        RAG->>DB: 向量检索(query)
        DB-->>RAG: 返回相关文档
        RAG->>Model: 生成总结(context+query)
        Model-->>RAG: 返回总结结果
        RAG-->>Tool: 返回检索结果
        Tool-->>Agent: 返回工具执行结果
        Agent->>Agent: 判断信息是否足够
        
        alt 信息足够
            Agent->>Model: 生成最终回答
            Model-->>Agent: 返回回答
            Agent-->>UI: 流式返回结果
            UI-->>User: 显示回答
        else 信息不足
            Agent->>Tool: 调用其他工具
            Note over Agent,Tool: 最多调用5次
        end
    else 直接回答
        Agent->>Model: 直接生成回答
        Model-->>Agent: 返回回答
        Agent-->>UI: 流式返回结果
        UI-->>User: 显示回答
    end
```

---

## 二、报告生成流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant UI as Streamlit界面
    participant Agent as ReactAgent
    participant Tool as 工具层
    participant RAG as RAG服务
    participant DB as 向量数据库
    participant Model as 大语言模型

    User->>UI: 输入："生成我的使用报告"
    UI->>Agent: execute_stream(prompt)
    Agent->>Agent: 识别报告生成意图
    
    Agent->>Tool: 调用get_user_id()
    Tool-->>Agent: 返回user_id
    
    Agent->>Tool: 调用get_current_month()
    Tool-->>Agent: 返回month
    
    Agent->>Tool: 调用fill_context_for_report()
    Note over Agent,Tool: 触发中间件上下文注入
    Tool-->>Agent: 执行完成
    
    Agent->>Tool: 调用fetch_external_data(user_id, month)
    Tool-->>Agent: 返回用户使用记录
    
    Agent->>Tool: 调用rag_summarize(query)
    Tool->>RAG: rag_summarize(query)
    RAG->>DB: 向量检索(query)
    DB-->>RAG: 返回相关文档
    RAG->>Model: 生成总结
    Model-->>RAG: 返回总结结果
    RAG-->>Tool: 返回检索结果
    Tool-->>Agent: 返回专业建议
    
    Agent->>Model: 生成个性化报告
    Model-->>Agent: 返回报告内容
    Agent-->>UI: 流式返回结果
    UI-->>User: 显示报告
```

---

## 三、天气查询流程

```mermaid
sequenceDiagram
    participant User as 用户
    participant UI as Streamlit界面
    participant Agent as ReactAgent
    participant Tool as 工具层
    participant Model as 大语言模型

    User->>UI: 输入："今天能飞无人机吗？"
    UI->>Agent: execute_stream(prompt)
    Agent->>Agent: 需要获取用户位置
    
    Agent->>Tool: 调用get_user_location()
    Tool-->>Agent: 返回城市名（如：杭州）
    
    Agent->>Tool: 调用get_weather(city)
    Tool-->>Agent: 返回天气信息
    
    Agent->>Tool: 调用rag_summarize(query)
    Tool-->>Agent: 返回天气适配建议
    
    Agent->>Model: 整合信息生成回答
    Model-->>Agent: 返回回答
    Agent-->>UI: 流式返回结果
    UI-->>User: 显示回答
```

---

## 四、工具调用时序图

```mermaid
sequenceDiagram
    participant Agent as ReactAgent
    participant Middleware as 中间件层
    participant Tool as 工具函数
    participant Logger as 日志模块

    Agent->>Middleware: 调用工具
    Middleware->>Logger: 记录工具调用开始
    Logger-->>Middleware: 记录完成
    
    Middleware->>Tool: 执行工具
    Tool-->>Middleware: 返回结果
    
    Middleware->>Logger: 记录工具调用结束
    Logger-->>Middleware: 记录完成
    
    Middleware-->>Agent: 返回结果
```

---

## 五、数据流程图总结

### 5.1 核心数据流

| 阶段 | 数据类型 | 说明 |
|------|----------|------|
| 用户输入 | 文本字符串 | 用户的自然语言问题 |
| 意图识别 | 结构化数据 | 解析后的用户意图 |
| 工具调用 | 字典参数 | 工具名称+入参 |
| 检索结果 | 文档列表 | 向量数据库返回的相关文档 |
| 模型输入 | 提示词+上下文 | 组合后的完整提示词 |
| 模型输出 | 文本字符串 | 大语言模型的回答 |

### 5.2 工具调用链

```mermaid
flowchart LR
    A[用户提问] --> B[意图分析]
    B --> C{需要工具?}
    C -->|是| D[选择工具]
    D --> E[调用工具]
    E --> F{信息足够?}
    F -->|否| D
    F -->|是| G[生成回答]
    C -->|否| G
    G --> H[返回结果]
```

### 5.3 报告生成工具调用顺序

```mermaid
flowchart LR
    A[get_user_id] --> B[get_current_month]
    B --> C[fill_context_for_report]
    C --> D[fetch_external_data]
    D --> E[rag_summarize]
    E --> F[生成报告]
```
