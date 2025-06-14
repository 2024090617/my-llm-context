# VS Code 中使用 CodeGPT API
import codegpt

print(codegpt) 
# list all functions
print(dir(codegpt))
# list all attributes
print(dir(codegpt.__init__))

def build_context(query):
    # 1. 检索 GitHub 知识库
    github_docs = search_github_repo(query, repo="my-llm-context")
    
    # 2. 提取最近修改的本地文件
    local_context = get_recently_edited_files(limit=3)
    
    # 3. MCP 压缩策略
    compressed = compress_context(
        content=github_docs + local_context,
        strategy="key_points",  # 提取关键段落
        target_tokens=6000
    )
    
    return f"""
    [系统上下文]
    {compressed}
    
    [当前任务]
    {query}
    """

# response = codegpt.call(prompt=build_context("如何优化API认证模块？"),model="gpt-4-turbo",context_window="128k")

# def apply_recency_bias(contexts):
#     # 按时间加权：最近内容权重更高
#     weights = [1.0 / (2 ** i) for i in range(len(contexts))]
#     weighted_context = sum(w*c for w,c in zip(weights, contexts))
#     return weighted_context[:TOKEN_LIMIT]
