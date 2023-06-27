import gensim
from gensim.summarization.summarizer import summarize
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def news_summarize(df, num_article):
    # gensim summarize() 사용
    summaries = []
    for n in range(num_article):
        article = df['본문'][n]
        summary = summarize(article, word_count=100)
        summaries.append(summary)
    # openai 사용    
    summary_article = []
    for article in summaries:
        article_length = len(article)
        
        prompt = 'Summarize in Korean: {}\n'.format(article)
        
        max_context_length = 4096
        if len(prompt) > max_context_length:
            prompt = prompt[:max_context_length]
            
        model = "text-davinci-003"

        response = openai.Completion.create(
            model = model,
            prompt = prompt,
            max_tokens = 1024,
            temperature = 0.2,
            top_p = 0.8,
            frequency_penalty=0,
            presence_penalty=0
        )
        summary = response.choices[0].text.strip()
        summary_article.append(summary)
        
    return summary_article

# df = df
# num_article = 3
# summary = news_summarize(df, num_article)
# print(summary)