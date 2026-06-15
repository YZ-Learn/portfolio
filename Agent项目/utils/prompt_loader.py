
from .config_hander import prompt_conf
from .path_tool import get_abs_path
from .logger_handler import logger

def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompt_conf['main_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_system_prompts]在yaml配置中咩有main_prompt_path的配置项")
        raise e

    try:return open(system_prompt_path,"r",encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_system_prompts]解析系统提示词有误，{str(e)}")
        raise e


def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompt_conf['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_rag_prompts]在yaml配置中咩有rag_summarize_prompt_pathh的配置项")
        raise e

    try:
        return open(rag_prompt_path, "r", encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_rag_prompts]解析rag总结提示词有误，{str(e)}")
        raise e


def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompt_conf['report_prompt_path'])
    except KeyError as e:
        logger.error(f"[load_report_prompts]在yaml配置中咩有report_prompt_path的配置项")
        raise e

    try:
        return open(report_prompt_path, "r", encoding='utf-8').read()
    except Exception as e:
        logger.error(f"[load_report_prompts]解析报告生成提示词有误，{str(e)}")
        raise e


if __name__ == '__main__':
    print(load_report_prompts())

