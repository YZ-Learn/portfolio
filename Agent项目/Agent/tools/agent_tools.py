import os
import random

from langchain_core.tools import tool
from RAG.rag_service import RagSummarizeService
from utils.config_hander import agent_conf
from utils.logger_handler import logger
from utils.path_tool import get_abs_path



rag = RagSummarizeService()

user_ids=['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1010']
month_arr = ['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09',
             '2025-10', '2025-11','2025-12']
external_data ={}

@tool(description="从向量存储中检索参考资料")
def rag_summarize(query:str)->str:
    return rag.rag_summarize(query)

@tool(description="获取指定城市天气，以消息字符串形式返回")
def get_weather(city:str)->str:
    return f"城市{city}天气为晴天，气温26摄氏度，空气湿度30%，南风2级，AQI21，最近12小时降雨概率低"

@tool(description="获取用户所在城市名称，以字符串形式返回")
def get_user_location()->str:
    return random.choice(['杭州','三亚','桂林'])

@tool(description="获取用户的ID，以纯字符串形式返回")
def get_user_id()->str:
    return random.choice(user_ids)


@tool(description="获取当前月份，以纯字符串形式返回")
def get_current_month()->str:
    return random.choice(month_arr)

def generate_external_data():
    """
    {
    "user_id":{"month":{"特征":xxx,"效率":XXX}
    :return:
    """

    if not external_data:
        external_data_path = get_abs_path(agent_conf["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileExistsError(f"{external_data_path}外部数据文件不存在")
        with open(external_data_path,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr:list[str] = line.strip().split(',')
                user_id = arr[0].replace('"','')
                application = arr[1]
                time = arr[2][1:-4]
                battery = arr[3]
                fly_time = arr[4]
                weather = arr[5]
                change = arr[6]

                if user_id not in external_data:
                    external_data[user_id] = {}
                external_data[user_id][time]={
                    "应用场景":application,
                    "电池情况":battery,
                    "飞行时长":fly_time,
                    "天气情况":weather,
                    "对比":change
                }
            # print(external_data)


@tool(description="从外部系统中获取指定用户用户的使用记录，以纯字符串的形式返回，检索不到返回空字符串")
def fetch_external_data(user_id:str,month:str)->str:
    generate_external_data()
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"[fetch_external_data]中，未能检索到{user_id}在{month}中的使用记录")
        return ''


@tool(description="无入参，无返回值，调用后出发中间件，自动为后续后续报告生成提供场景动态和注入上下文动态信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return 'fill_context_for_report()已调用'



# if __name__ == '__main__':
    # print(fetch_external_data('1002', '2025-04'))