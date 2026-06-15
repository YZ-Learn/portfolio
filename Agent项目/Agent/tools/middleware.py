from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command
from utils.prompt_loader import load_system_prompts,load_report_prompts
from utils.logger_handler import logger


@wrap_tool_call
def monitor_tool(
        #请求的数据封装
        request:ToolCallRequest,
        #执行的函数本身
        handler:Callable[[ToolCallRequest],ToolMessage|Command],
) -> ToolMessage |Command:#工具执行的监控/日志
    logger.info(f"[monitor_tool]执行工具：{request.tool_call['name']}")
    logger.info(f"[monitor_tool]传入参数：{request.tool_call['args']}")
    try:
        result = handler(request)
        logger.info(f"[monitor_tool]工具{request.tool_call['name']}调用成功")
        #---------------------------------------------------------------------------
        #为函数fill_context_for_report的调用注入标记
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context['report'] = True

        return result
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因{str(e)}")
        raise e

#在模型执行前打印日志
@before_model
def log_before_model(
        state:AgentState,# 整个Agent智能体中的状态记录
        runtime:Runtime,#记录了整个执行过程中的上下文记录
):#在模型执行前输出日志
    logger.info(f"[log_before_model]即调用模型，带有{len(state['messages'])}条消息")
    #取[-1]即取到最新的记录
    logger.debug(f"[log_before_model]{type(state['messages'][-1]).__name__} | {state['messages'][-1].content.strip()}")

    return None

@dynamic_prompt  #每一次在生成提示词之前，调用此函数
def report_prompt_switch(request:ModelRequest):
    is_report = request.runtime.context.get("report",False)#拿不到就返回False
    #当其为true时，即需要切换返回值
    if is_report:
        # print('===='*20,'报告提示词已经切换')
        return load_report_prompts()
    return load_system_prompts()






